"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from pyevt import EvtExchanger
from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.oslogging import oslogger


class EvtTrigger(Item):

    description = u"A plug-in for generating triggers with EVT devices."

    # Reset plug-in to initial values.
    def reset(self):
        self.var.value = 0
        self.var.duration = 1000
        self.var.device = u'DUMMY'
        self.var.outputmode = u'Pulse output lines'

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def prepare(self):
        super().prepare()
        self.var.value = self.clamp(self.var.value, 0, 255)
        self.experiment.var._outputValue = 0

        # Dynamically load an EventExchanger RSP device
        if not hasattr(self, u'EventExchanger'):
            self.myevt = EvtExchanger()
            try:
                self.myevt.Select(self.var.device)
                self.myevt.SetLines(0)
                #oslogger.info("Connecting and resetting EVT device.")
                oslogger.debug("Connecting and resetting EVT device.")
            except:
                self.var.device = u'DUMMY'
                #oslogger.info("Connecting to EVT device failed! Switching to dummy mode.")
                oslogger.debug("Connecting to EVT device failed! Switching to the dummy mode.")
                

    def run(self):
        self.set_item_onset()
        if self.var.device == u'DUMMY':
            if self.var.outputmode == u'Write output lines':
                self.experiment.var._outputValue = self.var.value # Store as global.
                oslogger.info('dummy: send byte code {}'.format(self.var.value))
            elif self.var.outputmode == u'Pulse output lines':
                oslogger.info('dummy: send byte code {} for the duration of {} ms'.format(
                    self.experiment.var._outputValue ^ self.var.value, self.var.duration))
            elif self.var.outputmode == u'Reset output lines':
                oslogger.info('dummy: send byte code {}'.format(0))
            elif self.var.outputmode == u'Invert output lines':
                self.experiment.var._outputValue ^= self.var.value
                oslogger.info('dummy: send byte code {}'.format(self.experiment.var._outputValue))
        else:
            if self.var.outputmode == u'Write output lines':
                self.myevt.SetLines(self.var.value)
                self.experiment.var._outputValue = self.var.value # Store as global. There is no output read-back from the hardware.
                oslogger.info('evt: send byte code {}'.format(self.var.value))
            elif self.var.outputmode == u'Pulse output lines':
                self.myevt.PulseLines((self.experiment.var._outputValue ^ self.var.value), self.var.duration)
                oslogger.info('evt: send byte code {} for the duration of {} ms'.format(
                    self.experiment.var._outputValue ^ self.var.value, self.var.duration))
            elif self.var.outputmode == u'Reset output lines':
                oslogger.info('evt: send byte code {}'.format(0))
                self.myevt.SetLines(0)
                self.experiment.var._outputValue = 0
            elif self.var.outputmode == u'Invert output lines':
                self.experiment.var._outputValue ^= self.var.value
                self.myevt.SetLines(self.experiment.var._outputValue)
                oslogger.info('evt: send byte code {}'.format(self.experiment.var._outputValue))
        return True


class QtEvtTrigger(EvtTrigger, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        # We don't need to do anything here, except call the parent
        # constructors. Since the parent constructures take different arguments
        # we cannot use super().
        EvtTrigger.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()
        myevt = EvtExchanger()
        listOfDevices = myevt.Attached(u"EventExchanger-EVT")
        if listOfDevices:
            for i in listOfDevices:
                self.device_combobox.addItem(i)
        del myevt # cleanup handle

        self.refresh_checkbox.stateChanged.connect(self.refresh_combobox_device)
        self.device_combobox.currentIndexChanged.connect(self.update_combobox_device)
        self.output_mode_combobox.currentIndexChanged.connect(self.update_combobox_output_mode)
        # Connect checkbox inputs with line input and vice verse.
        self.b0_checkbox.stateChanged.connect(self.update_line_edit_value)
        self.b1_checkbox.stateChanged.connect(self.update_line_edit_value)
        self.b2_checkbox.stateChanged.connect(self.update_line_edit_value)
        self.b3_checkbox.stateChanged.connect(self.update_line_edit_value)
        self.b4_checkbox.stateChanged.connect(self.update_line_edit_value)
        self.b5_checkbox.stateChanged.connect(self.update_line_edit_value)
        self.b6_checkbox.stateChanged.connect(self.update_line_edit_value)
        self.b7_checkbox.stateChanged.connect(self.update_line_edit_value)
        self.byte_value_line_edit.textChanged.connect(self.update_checkboxes)

    def refresh_combobox_device(self):
        if self.refresh_checkbox.isChecked():
            number_of_items = self.device_combobox.count()
            for i in range(number_of_items):
                if i > 0:
                    self.device_combobox.removeItem(i)
            # create new list:
            myevt = EvtExchanger()
            listOfDevices = myevt.Attached(u"EventExchanger-EVT")
            if listOfDevices:
                for i in listOfDevices:
                    self.device_combobox.addItem(i)
            del myevt

    def update_combobox_device(self):
        self.refresh_checkbox.setChecked(False)

    def update_combobox_output_mode(self):
        # Get the current text or index from the combobox
        current_selection = self.output_mode_combobox.currentText()  # or use currentIndex() for the index

        # Enable or disable the line_edit based on the selection
        if current_selection == 'Write output lines':
            self.byte_value_line_edit.setEnabled(True)
            self.duration_line_edit.setEnabled(False)
        elif current_selection == 'Reset output lines':
            self.byte_value_line_edit.setEnabled(False)
            self.duration_line_edit.setEnabled(False)
        elif current_selection == 'Invert output lines':
            self.byte_value_line_edit.setEnabled(True)
            self.duration_line_edit.setEnabled(False)
        elif current_selection == 'Pulse output lines':
            self.byte_value_line_edit.setEnabled(True)
            self.duration_line_edit.setEnabled(True)
        else:
            self.byte_value_line_edit.setEnabled(False)
            self.duration_line_edit.setEnabled(False)

    def update_line_edit_value(self):
        # Calculate the decimal value from checkboxes. (How can we enumerate and loop this?)
        tempVar = self.b0_checkbox.isChecked()
        tempVar |= self.b1_checkbox.isChecked() << 1
        tempVar |= self.b2_checkbox.isChecked() << 2
        tempVar |= self.b3_checkbox.isChecked() << 3
        tempVar |= self.b4_checkbox.isChecked() << 4
        tempVar |= self.b5_checkbox.isChecked() << 5
        tempVar |= self.b6_checkbox.isChecked() << 6
        tempVar |= self.b7_checkbox.isChecked() << 7
        # Update line edit without triggering the textChanged signal
        self.byte_value_line_edit.blockSignals(True)
        self.byte_value_line_edit.setText(str(tempVar))
        self.byte_value_line_edit.blockSignals(False)

    def update_checkboxes(self, text):
        # Convert line edit text to binary and update checkboxes
        try:
            self.var.value = int(text)
            if 0 <= self.var.value <= 255:
                binary_string = format(self.var.value, '08b')
                self.b0_checkbox.setChecked(binary_string[7] == '1')
                self.b1_checkbox.setChecked(binary_string[6] == '1')
                self.b2_checkbox.setChecked(binary_string[5] == '1')
                self.b3_checkbox.setChecked(binary_string[4] == '1')
                self.b4_checkbox.setChecked(binary_string[3] == '1')
                self.b5_checkbox.setChecked(binary_string[2] == '1')
                self.b6_checkbox.setChecked(binary_string[1] == '1')
                self.b7_checkbox.setChecked(binary_string[0] == '1')
            else:
                raise ValueError
        except ValueError:
            # Handle invalid input or out of range value
            self.byte_value_line_edit.blockSignals(True)
            self.byte_value_line_edit.setText('')
            self.b0_checkbox.setChecked(False)
            self.b1_checkbox.setChecked(False)
            self.b2_checkbox.setChecked(False)
            self.b3_checkbox.setChecked(False)
            self.b4_checkbox.setChecked(False)
            self.b5_checkbox.setChecked(False)
            self.b6_checkbox.setChecked(False)
            self.b7_checkbox.setChecked(False)
            self.byte_value_line_edit.blockSignals(False)
