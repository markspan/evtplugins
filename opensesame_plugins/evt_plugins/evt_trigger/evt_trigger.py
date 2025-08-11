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
from libopensesame.oslogging import oslogger
from time import sleep
from pyevt import EventExchanger # pyevt 2.0

# constant
_DEVICE_GROUP = u'EVT'

# global var
open_devices = {} # store open device handles.
device_output_value = {} # store output state of connected devices.

class EvtTrigger(Item):

    description = u"A plug-in for generating triggers with EVT devices."

    global open_devices
    global device_output_value

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
        self.var.close_device = 'no'

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        super().prepare()

        self.output_value = 0 # create output state storage for dummy mode.

        if self.var.device == u'DUMMY':
            oslogger.warning("Hardware configuration could have changed! Dummy prepare...")
        elif len(open_devices) == 0:
            # Create a shadow device list to find 'path' from the current selected device.
            # 'path' is an unique device ID.
            temp_evt = EventExchanger()
            sleep(1) # without a delay, the list will not always be complete.
            try:
                device_list = temp_evt.scan(_DEVICE_GROUP) # filter on allowed EVT types
                del temp_evt
                # oslogger.info("device list: {}".format(device_list))
                for d in device_list:
                    sleep(1) # without a delays, the device will not always be there.
                    composed_string = d['product_string'] + " s/n: " + d['serial_number']
                    open_devices[composed_string] = EventExchanger()
                    device_output_value[composed_string] = 0 # create device output state storage
                    # Get evt device handle:
                    open_devices[composed_string].attach_id(d['path'])
                    oslogger.info('Device successfully attached as: {} s/n: {}'.format(
                        d['product_string'], d['serial_number']))
                    oslogger.info('        ...  and with device ID: {}'.format(
                        open_devices[composed_string]))
            except:
                oslogger.warning("Connecting EVT-device failed! Device set to dummy.")
                self.var.device = u'DUMMY'

        # searching for selected device:
        self.current_device = None
        for dkey in open_devices:
            if self.var.device[:15] in dkey:
                self.current_device = dkey # assign to value that belongs to the key.
        if self.current_device is None:
            oslogger.warning("EVT-device not found! Device set to dummy.")
            self.var.device = u'DUMMY'
        else:
            oslogger.info('Preparing device: {}'.format(open_devices[self.current_device]))
            open_devices[self.current_device].write_lines(0) # clear lines

        # pass device var to experiment as global:
        var_name = "self.experiment.var.connected_device_" + self.name
        exec(f'{var_name} = "{self.var.device}"')

    def run(self):
        """The run phase of the plug-in goes here."""
        self.set_item_onset()
        if self.var.device == u'DUMMY':
            if self.var.outputmode == u'Clear output lines':
                self.output_value = 0
                oslogger.info('dummy: send byte code {}'.format(self.output_value))
            elif self.var.outputmode == u'Write output lines':
                self.output_value = self.var.mask
                oslogger.info('dummy: send byte code {}'.format(self.output_value))
            elif self.var.outputmode == u'Invert output lines':
                self.output_value ^= self.var.mask
                oslogger.info('dummy: send byte code {}'.format(self.output_value))
            elif self.var.outputmode == u'Pulse output lines':
                oslogger.info('dummy: send byte code {} for the duration of {} ms'.format(
                self.output_value ^ self.var.mask, self.var.duration))
        else:
            if self.var.outputmode == u'Clear output lines':
                # Store output state as global. (There is no read-back from the hardware.)
                device_output_value[self.current_device] = 0
                open_devices[self.current_device].write_lines(device_output_value[self.current_device])
                oslogger.info('{}: send byte code {}'.format(
                    open_devices[self.current_device], device_output_value[self.current_device]))
            elif self.var.outputmode == u'Write output lines':
                device_output_value[self.current_device] = self.var.mask
                open_devices[self.current_device].write_lines(device_output_value[self.current_device])
                oslogger.info('{}: send byte code {}'.format(
                    open_devices[self.current_device], device_output_value[self.current_device]))
            elif self.var.outputmode == u'Invert output lines':
                device_output_value[self.current_device] ^= self.var.mask
                open_devices[self.current_device].write_lines(device_output_value[self.current_device])
                oslogger.info('{}: send byte code {}'.format(
                    open_devices[self.current_device], device_output_value[self.current_device]))
            elif self.var.outputmode == u'Pulse output lines':
                open_devices[self.current_device].pulse_lines(
                    (device_output_value[self.current_device] ^ self.var.mask), self.var.duration)
                oslogger.info('{}: send byte code {} for the duration of {} ms'.format(
                    open_devices[self.current_device],
                    device_output_value[self.current_device] ^ self.var.mask, self.var.duration))
        # close the device?
        if self.var.close_device == 'yes':
            for dkey in open_devices:
                try:
                    open_devices[dkey].close()
                    oslogger.info('Device: {} successfully closed!'.format(open_devices[dkey]))
                except:
                    oslogger.warning('Device {} for closing not found!'.format(open_devices[dkey]))


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
        self.refresh_checkbox_widget.stateChanged.connect(self.refresh_combobox_device)
        self.device_combobox_widget.currentIndexChanged.connect(self.update_combobox_device)
        self.output_mode_combobox_widget.currentIndexChanged.connect(self.update_combobox_output_mode)
        self.close_device_checkbox_widget.stateChanged.connect(self.close_device)
        # Connect checkbox inputs with line input and vice verse.
        self.b0_checkbox_widget.stateChanged.connect(self.update_line_edit_value)
        self.b1_checkbox_widget.stateChanged.connect(self.update_line_edit_value)
        self.b2_checkbox_widget.stateChanged.connect(self.update_line_edit_value)
        self.b3_checkbox_widget.stateChanged.connect(self.update_line_edit_value)
        self.b4_checkbox_widget.stateChanged.connect(self.update_line_edit_value)
        self.b5_checkbox_widget.stateChanged.connect(self.update_line_edit_value)
        self.b6_checkbox_widget.stateChanged.connect(self.update_line_edit_value)
        self.b7_checkbox_widget.stateChanged.connect(self.update_line_edit_value)
        self.byte_value_line_edit_widget.textChanged.connect(self.update_checkboxes)

    def refresh_combobox_device(self):
        if self.refresh_checkbox_widget.isChecked():
            # renew list:
            self.combobox_add_devices()

    def update_combobox_device(self):
        self.refresh_checkbox_widget.setChecked(False)

    def update_combobox_output_mode(self):
        # Get the current text or index from the combobox
        current_selection = self.output_mode_combobox_widget.currentText()  # or use currentIndex() for the index
        # Enable or disable the line_edit based on the selection
        if current_selection == 'Clear output lines':
            self.byte_value_line_edit_widget.setEnabled(False)
            self.duration_line_edit_widget.setEnabled(False)
            self.byte_value_line_edit_widget.setText(str(0)) # bit mask=0
        elif current_selection == 'Write output lines':
            self.byte_value_line_edit_widget.setEnabled(True)
            self.duration_line_edit_widget.setEnabled(False)
        elif current_selection == 'Invert output lines':
            self.byte_value_line_edit_widget.setEnabled(True)
            self.duration_line_edit_widget.setEnabled(False)
        elif current_selection == 'Pulse output lines':
            self.byte_value_line_edit_widget.setEnabled(True)
            self.duration_line_edit_widget.setEnabled(True)
        else:
            self.byte_value_line_edit_widget.setEnabled(False)
            self.duration_line_edit_widget.setEnabled(False)

    def update_line_edit_value(self):
        # Calculate the decimal value from checkboxes. (How can we enumerate and loop this?)
        tempVar = self.b0_checkbox_widget.isChecked()
        tempVar |= self.b1_checkbox_widget.isChecked() << 1
        tempVar |= self.b2_checkbox_widget.isChecked() << 2
        tempVar |= self.b3_checkbox_widget.isChecked() << 3
        tempVar |= self.b4_checkbox_widget.isChecked() << 4
        tempVar |= self.b5_checkbox_widget.isChecked() << 5
        tempVar |= self.b6_checkbox_widget.isChecked() << 6
        tempVar |= self.b7_checkbox_widget.isChecked() << 7
        # Update line edit without triggering the textChanged signal
        self.byte_value_line_edit_widget.blockSignals(True)
        self.byte_value_line_edit_widget.setText(str(tempVar))
        self.byte_value_line_edit_widget.blockSignals(False)

    def update_checkboxes(self, text):
        # Convert line edit text to binary and update checkboxes
        try:
            self.var.mask = int(text)
            if 0 <= self.var.mask <= 255:
                binary_string = format(self.var.mask, '08b')
                self.b0_checkbox_widget.setChecked(binary_string[7] == '1')
                self.b1_checkbox_widget.setChecked(binary_string[6] == '1')
                self.b2_checkbox_widget.setChecked(binary_string[5] == '1')
                self.b3_checkbox_widget.setChecked(binary_string[4] == '1')
                self.b4_checkbox_widget.setChecked(binary_string[3] == '1')
                self.b5_checkbox_widget.setChecked(binary_string[2] == '1')
                self.b6_checkbox_widget.setChecked(binary_string[1] == '1')
                self.b7_checkbox_widget.setChecked(binary_string[0] == '1')
            else:
                raise ValueError
        except ValueError:
            # Handle invalid input or out of range value
            self.byte_value_line_edit_widget.blockSignals(True)
            self.byte_value_line_edit_widget.setText('')
            self.byte_value_line_edit_widget.blockSignals(False)
            self.b0_checkbox_widget.setChecked(False)
            self.b1_checkbox_widget.setChecked(False)
            self.b2_checkbox_widget.setChecked(False)
            self.b3_checkbox_widget.setChecked(False)
            self.b4_checkbox_widget.setChecked(False)
            self.b5_checkbox_widget.setChecked(False)
            self.b6_checkbox_widget.setChecked(False)
            self.b7_checkbox_widget.setChecked(False)

    def combobox_add_devices(self):
        self.device_combobox_widget.clear()
        self.device_combobox_widget.addItem(u'DUMMY', userData=None)
        
        # Create the EVT device list
        sleep(.5) # delay after possible init of a previous instance of this plugin. 
        myevt = EventExchanger()
        sleep(.2)
        try:
            device_list = myevt.scan(_DEVICE_GROUP) # filter on allowed EVT types
            del myevt
        except:
            device_list = {}
        
        try:
            previous_device_found = False
            for d in device_list:
                product_string = d['product_string']
                serial_string = d['serial_number']
                composed_string = product_string[15:] + " s/n: " + serial_string
                # add device id to combobox:
                self.device_combobox_widget.addItem(composed_string)
                # previous used device present?
                if self.var.device[:15] in product_string:
                    self.var.device = composed_string
                    previous_device_found = True       
        except:
            self.var.device = u'DUMMY'
            oslogger.warning("No devices found! Switching to dummy.")

        if previous_device_found is False:
            self.var.device = u'DUMMY'
            oslogger.warning("The hardware configuration has been changed since the last run! Switching to dummy.")

    def close_device(self):
        if self.close_device_checkbox_widget.isChecked():
            self.var.close_device = 'yes'
        else:
            self.var.close_device = 'no'
