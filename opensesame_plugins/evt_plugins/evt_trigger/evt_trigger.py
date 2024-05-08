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
from time import sleep
from pyevt import EventExchanger # pyevt 2.0

# constant
_DEVICE_GROUP = u'EVT'

# global var
open_devices = {} # Store open device handles.

class EvtTrigger(Item):

    description = u"A plug-in for generating triggers with EVT devices."

    # Reset plug-in to initial values.
    def reset(self):
        """Resets plug-in to initial values."""
        self.var.device = u'0: DUMMY'
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
        self.experiment.var.output_value = 0

        if int(self.var.device[:1]) == 0:
            oslogger.warning("Dummy prepare")
        else:
            # Create a shadow device list to find 'path' from the current selected device.
            # 'path' is an unique device ID.
            myevt = EventExchanger()
            sleep(0.1) # without a delay, the list will not always be complete.
            try:
                device_list = myevt.scan(_DEVICE_GROUP) # filter on allowed EVT types
                del myevt
                # oslogger.info("device list: {}".format(device_list))
            except:
                oslogger.warning("Connecting EVT device failed!")

            try:
                d_count = 1            
                for d in device_list:
                    if not d_count in open_devices: # skip if already open
                        # Dynamically load all EVT devices from the list
                        open_devices[d_count] = EventExchanger()
                        open_devices[d_count].attach_id(d['path']) # Get evt device handle
                        oslogger.info('Device successfully attached as:{} s/n:{}'.format(
                            d['product_string'], d['serial_number']))
                    d_count += 1
                oslogger.info('open devices: {}'.format(open_devices))
                self.current_device = int(self.var.device[:1])
                oslogger.info('Prepare - current device: {}'.format(self.current_device))
                open_devices[self.current_device].write_lines(0) # clear lines
            except:
                self.var.device = u'0: DUMMY'
                oslogger.warning("Device missing! Switching to dummy.")

    def run(self):
        """The run phase of the plug-in goes here."""
        self.set_item_onset()
        if self.var.device == u'0: DUMMY':
            if self.var.outputmode == u'Reset output lines':
                self.experiment.var.output_value = 0
                oslogger.info('dummy: send byte code {}'.format(self.experiment.var.output_value))
            elif self.var.outputmode == u'Write output lines':
                self.experiment.var.output_value = self.var.mask
                oslogger.info('dummy: send byte code {}'.format(self.experiment.var.output_value))
            elif self.var.outputmode == u'Invert output lines':
                self.experiment.var.output_value ^= self.var.mask
                oslogger.info('dummy: send byte code {}'.format(self.experiment.var.output_value))
            elif self.var.outputmode == u'Pulse output lines':
                oslogger.info('dummy: send byte code {} for the duration of {} ms'.format(
                self.experiment.var.output_value ^ self.var.mask, self.var.duration))
        else:
            if self.var.outputmode == u'Reset output lines':
                # Store output state as global. (There is no read-back from the hardware.)
                self.experiment.var.output_value = 0
                open_devices[self.current_device].write_lines(self.experiment.var.output_value)
                oslogger.info('{}: send byte code {}'.format(
                    open_devices[self.current_device], self.experiment.var.output_value))
            elif self.var.outputmode == u'Write output lines':
                self.experiment.var.output_value = self.var.mask
                open_devices[self.current_device].write_lines(self.experiment.var.output_value)
                oslogger.info('{}: send byte code {}'.format(
                    open_devices[self.current_device], self.experiment.var.output_value))
            elif self.var.outputmode == u'Invert output lines':
                self.experiment.var.output_value ^= self.var.mask
                open_devices[self.current_device].write_lines(self.experiment.var.output_value)
                oslogger.info('{}: send byte code {}'.format(
                    open_devices[self.current_device], self.experiment.var.output_value))
            elif self.var.outputmode == u'Pulse output lines':
                open_devices[self.current_device].pulse_lines(
                    (self.experiment.var.output_value ^ self.var.mask), self.var.duration)
                oslogger.info('{}: send byte code {} for the duration of {} ms'.format(
                    open_devices[self.current_device],
                    self.experiment.var.output_value ^ self.var.mask, self.var.duration))
            # open_devices[self.current_device].close()

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
        # First, call the parent constructor, which constructs the GUI controls
        # based on __init_.py.
        super().init_edit_widget()

        self.update_combobox_output_mode() # enable/disable actual line_edit widgets.
        self.combobox_add_devices()
        
        # Event triggered calls:
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
            # renew list:
            self.combobox_add_devices()

    def update_combobox_device(self):
        self.refresh_checkbox.setChecked(False)

    def update_combobox_output_mode(self):
        # Get the current text or index from the combobox
        current_selection = self.output_mode_combobox.currentText()  # or use currentIndex() for the index
        # Enable or disable the line_edit based on the selection
        if current_selection == 'Reset output lines':
            self.byte_value_line_edit.setEnabled(False)
            self.duration_line_edit.setEnabled(False)
            self.byte_value_line_edit.setText(str(0)) # bit mask=0
        elif current_selection == 'Write output lines':
            self.byte_value_line_edit.setEnabled(True)
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

    def combobox_add_devices(self):
        self.device_combobox.clear()
        self.device_combobox.addItem(u'0: DUMMY', userData=None)
        
        # Create the EVT device list
        myevt = EventExchanger()
        sleep(0.5) # without a delay, the list will not always be complete.
        try:
            device_list = myevt.scan(_DEVICE_GROUP) # filter on allowed EVT types
            del myevt
        except:
            device_list = None
        
        added_item_list = {}
        if device_list:
            d_count = 1
            for d in device_list:
                product_string = d['product_string']
                serial_string = d['serial_number']
                composed_string = str(d_count) + ": " + \
                    product_string[15:] + " s/n: " + serial_string
                # add device string to combobox:
                self.device_combobox.addItem(composed_string)
                added_item_list[d_count] = composed_string
                d_count += 1
                if d_count > 9:
                    # keep number of digits 1
                    break
            # Prevents hangup if the old device is not found after reopening the project.
            # Any change of the hardware configuration can cause this.
            if not self.var.device in added_item_list.values():
                self.var.device = u'0: DUMMY'
