#-*- coding:utf-8 -*-

"""
Author: Martin Stokroos, 2024

This plug-in is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this plug-in.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas
from libopensesame.oslogging import oslogger
from pyevt import EvtExchanger


class EvtTrigger(Item):

    description = u"A plug-in for generating triggers with EVT devices."

    # Reset plug-in to initial values.
    def reset(self):
        """Resets plug-in to initial values."""
        self.var.device = u'DUMMY'
        self.var.refresh = 'no'
        self.var.outputmode = u'Write output lines'
        self.var.bit0 = 'no'
        self.var.bit1 = 'no'
        self.var.bit2 = 'no'
        self.var.bit3 = 'no'
        self.var.bit4 = 'no'
        self.var.bit5 = 'no'
        self.var.bit6 = 'no'
        self.var.bit7 = 'no'
        self.var.mask = 0
        self.var.duration = 1000

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        super().prepare()
        self.experiment.var._outputValue = 0

        if self.var.device != u'DUMMY':
            # Dynamically load an EVT device
            self.myevt = EvtExchanger()
            try:
                self.myevt.Select(self.var.device)
                self.myevt.SetLines(0)
                oslogger.info("Connecting and resetting EVT device.")
            except:
                self.var.device = u'DUMMY'
                oslogger.warning("Connecting EVT device failed! Switching to dummy-mode.")

    def run(self):
        """The run phase of the plug-in goes here."""
        self.set_item_onset()
        if self.var.device == u'DUMMY':
            if self.var.outputmode == u'Reset output lines':
                self.experiment.var._outputValue = 0
                oslogger.info('dummy: send byte code {}'.format(self.experiment.var._outputValue))
            elif self.var.outputmode == u'Write output lines':
                self.experiment.var._outputValue = self.var.mask
                oslogger.info('dummy: send byte code {}'.format(self.experiment.var._outputValue))
            elif self.var.outputmode == u'Invert output lines':
                self.experiment.var._outputValue ^= self.var.mask
                oslogger.info('dummy: send byte code {}'.format(self.experiment.var._outputValue))
            elif self.var.outputmode == u'Pulse output lines':
                oslogger.info('dummy: send byte code {} for the duration of {} ms'.format(
                self.experiment.var._outputValue ^ self.var.mask, self.var.duration))
        else:
            if self.var.outputmode == u'Reset output lines':
                # Store output state as global. (There is no read-back from the hardware.)
                self.experiment.var._outputValue = 0
                self.myevt.SetLines(self.experiment.var._outputValue)
                oslogger.info('evt: send byte code {}'.format(self.experiment.var._outputValue))
            elif self.var.outputmode == u'Write output lines':
                self.experiment.var._outputValue = self.var.mask
                self.myevt.SetLines(self.experiment.var._outputValue)
                oslogger.info('evt: send byte code {}'.format(self.experiment.var._outputValue))
            elif self.var.outputmode == u'Invert output lines':
                self.experiment.var._outputValue ^= self.var.mask
                self.myevt.SetLines(self.experiment.var._outputValue)
                oslogger.info('evt: send byte code {}'.format(self.experiment.var._outputValue))
            elif self.var.outputmode == u'Pulse output lines':
                self.myevt.PulseLines((self.experiment.var._outputValue ^ self.var.mask), self.var.duration)
                oslogger.info('evt: send byte code {} for the duration of {} ms'.format(
                    self.experiment.var._outputValue ^ self.var.mask, self.var.duration))


class QtEvtTrigger(EvtTrigger, QtAutoPlugin):

    """This class handles the GUI aspect of the plug-in. The name should be the
    same as that of the runtime class with the added prefix Qt.
    
    Important: defining a GUI class is optional, and only necessary if you need
    to implement non-standard interfaces or interactions. In this case, we use
    the GUI class to dynamically enable/ disable some controls (see below).
    """

    def __init__(self, name, experiment, script=None):
        # We don't need to do anything here, except call the parent
        # constructors. Since the parent constructures take different arguments
        # we cannot use super().
        EvtTrigger.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):

        """Constructs the GUI controls. Usually, you can omit this function
        altogether, but if you want to implement more advanced functionality,
        such as controls that are grayed out under certain conditions, you need
        to implement this here.
        """

        super().init_edit_widget()
        self.update_combobox_output_mode()

        self.myevt = EvtExchanger()
        listOfDevices = self.myevt.Attached(u"EventExchanger-EVT")
        if listOfDevices:
            for i in listOfDevices:
                self.device_combobox.addItem(i)
        # Prevents hangup if the same device is not found after reopening the project:
        if not self.var.device in listOfDevices: 
            self.var.device = u'DUMMY'

        # event based calls:
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
            self.device_combobox.clear()
            # create new list:
            self.device_combobox.addItem(u'DUMMY', userData=None)
            listOfDevices = self.myevt.Attached(u"EventExchanger-EVT")
            if listOfDevices:
                for i in listOfDevices:
                    self.device_combobox.addItem(i)

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
            self.var.mask = int(text)
            if 0 <= self.var.mask <= 255:
                binary_string = format(self.var.mask, '08b')
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
            self.byte_value_line_edit.blockSignals(False)
            self.b0_checkbox.setChecked(False)
            self.b1_checkbox.setChecked(False)
            self.b2_checkbox.setChecked(False)
            self.b3_checkbox.setChecked(False)
            self.b4_checkbox.setChecked(False)
            self.b5_checkbox.setChecked(False)
            self.b6_checkbox.setChecked(False)
            self.b7_checkbox.setChecked(False)

