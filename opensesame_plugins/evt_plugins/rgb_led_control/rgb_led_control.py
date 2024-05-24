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

import time
import math
import distutils.util
from time import sleep
from pyevt import EventExchanger
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas
from libopensesame.oslogging import oslogger
from openexp.keyboard import Keyboard

# constant
_DEVICE_GROUP = u'RSP-LT'

# global var
open_devices = {} # Store open device handles.


class RgbLedControl(Item):

    description = u"Plugin to send LED RGB data from \
        \r\nEventExchanger-based digital input/output device."

    # Reset plug-in to initial values.
    def reset(self):
        """Resets plug-in to initial values."""
        self.var.device = u'Keyboard'
        self.var.correct_response = u'1'
        self.var.allowed_responses = u'1;2;3'
        self.var.timeout = u'infinite'
        self.var.button1_color = "#000000"
        self.var.button2_color = "#000000"
        self.var.button3_color = "#000000"
        self.var.button4_color = "#000000"
        self.var.reset_delay = 500
        self.var.feedback = u'yes'
        self.var.correct_color = "#00FF00"
        self.var.incorrect_color = "#FF0000"

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        super().prepare()

        '''
        The next part calculates the bit mask for the allowed responses
        to receive from the RSP-LT.
        '''
        self.var.combined_allowed_events = 0
        try:
            list_allowed_buttons = self.var.allowed_responses.split(";")
            for x in list_allowed_buttons:
                self.var.combined_allowed_events +=  (1 << (int(x, 10) -1))
        except:
            # in case the input is one element
            x = self.var.allowed_responses
            self.var.combined_allowed_events =  (1 << (x-1))
            list_allowed_buttons = []
            list_allowed_buttons.append(x)
        #oslogger.info('{}'.format(list_allowed_buttons))
        #oslogger.info('{}'.format(self.var.combined_allowed_events))

        if self.var.device == u'Keyboard':
            self.my_keyboard = Keyboard(self.experiment, 
                                keylist=list_allowed_buttons,
                                timeout=self.var.timeout if \
                                type(self.var.timeout)==int else None)
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
                    # Get evt device handle:
                    open_devices[composed_string].attach_id(d['path'])
                    oslogger.info('Device successfully attached as: {} s/n: {}'.format(
                        d['product_string'], d['serial_number']))
                    oslogger.info('        ...  and with device ID: {}'.format(
                        open_devices[composed_string]))
            except:
                oslogger.warning("Loading the RSP-12x-box failed! Default is keyboard")
                self.var.device = u'Keyboard'
                self.my_keyboard = Keyboard(self.experiment, 
                                            keylist=list_allowed_buttons,
                                            timeout=self.var.timeout if \
                                            type(self.var.timeout)==int else None)
            # searching for selected device:
            self.current_device = None
            for dkey in open_devices:
                if self.var.device[:15] in dkey:
                    self.current_device = dkey # assign to value that belongs to the key.
            if self.current_device is None:
                oslogger.warning("RSP-12x device not found! Device set to Keyboard.")
                self.var.device = u'Keyboard'
                self.my_keyboard = Keyboard(self.experiment, 
                                            keylist=list_allowed_buttons,
                                            timeout=self.var.timeout if \
                                            type(self.var.timeout)==int else None)
            else:
                oslogger.info('Prepare device: {}'.format(self.current_device))
                # open_devices[self.current_device].write_lines(0) # clear lines

        # pass device var to experiment as global:
        var_name = "self.experiment.var.connected_device_" + self.name
        exec(f'{var_name} = "{self.var.device}"')

    def run(self):
        """The run phase of the plug-in goes here."""
        # Save the current time...
        t0 = self.set_item_onset()

        hexprepend = "0x"
        self.colors = [hexprepend + self.var.button1_color[1:],
                       hexprepend + self.var.button2_color[1:],
                       hexprepend + self.var.button3_color[1:],
                       hexprepend + self.var.button4_color[1:]]
        self.CorrectColor = hexprepend + self.var.correct_color[1:]
        self.InCorrectColor = hexprepend + self.var.incorrect_color[1:]
        CC = int(self.CorrectColor, 16)
        IC = int(self.InCorrectColor, 16)
        BLC = [0, 0, 0, 0]

        for b in range(4):
            BLC[b] = int(self.colors[b], 16)

        if self.var.device != u'Keyboard':
            for b in range(4):
                open_devices[self.current_device].set_led_rgb(
                    ((BLC[b] >> 16) & 0xFF),
                    ((BLC[b] >> 8) & 0xFF),
                    (BLC[b] & 0xFF),
                    b + 1, 1)

            if self.var.feedback == u'yes':
                for b in range(4):
                    open_devices[self.current_device].set_led_rgb(
                        ((IC >> 16) & 0xFF),
                        ((IC >> 8) & 0xFF),
                        (IC & 0xFF),
                        b + 1, b + 11)

                open_devices[self.current_device].set_led_rgb(
                    ((CC >> 16) & 0xFF),
                    ((CC >> 8) & 0xFF),
                    (CC & 0xFF),
                    int(self.var.correct_response),
                    int(self.var.correct_response) + 10)

            # Call the 'wait for event' function in \
            # the EventExchanger C# object.
            self.var.response, self.var.keyboard_response = \
                open_devices[self.current_device].wait_for_event(
                    self.var.combined_allowed_events, self.var.timeout if \
                    type(self.var.timeout)==int else None)

            if (self.var.response != -1):
                self.var.response = math.log2(self.var.response) + 1

            # Feedback:
            if self.var.feedback == u'yes':
                time.sleep(self.var.reset_delay / 1000.0)
                for b in range(4):
                    open_devices[self.current_device].set_led_rgb(0, 0, 0, b + 1, 1)
        else:
            # dummy-mode: keyboard response.....
            self.var.response, self.var.keyboard_response = \
                self.my_keyboard.get_key()

        # HOUSE KEEPING:
        self.var.correct = \
            bool(self.var.response == self.var.correct_response)

        self.var.correct = distutils.util.strtobool(str(self.var.correct))

        print(self.var.correct)
        # Add all response related data to the Opensesame responses instance.
        self.experiment.responses.add(response_time=self.var.keyboard_response,
                                      correct=self.var.correct,
                                      response=self.var.response,
                                      item=self.name)


class QtRgbLedControl(RgbLedControl, QtAutoPlugin):

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
        RgbLedControl.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):

        """Constructs the GUI controls. Usually, you can omit this function
        altogether, but if you want to implement more advanced functionality,
        such as controls that are grayed out under certain conditions, you need
        to implement this here.
        """

        super().init_edit_widget()

        self.combobox_add_devices() # first time fill the combobox

        # Event-triggered calls:
        self.refresh_checkbox_widget.stateChanged.connect(self.refresh_combobox_device)
        self.device_combobox_widget.currentIndexChanged.connect(self.update_combobox_device)
        self.timeout_line_edit_widget.textChanged.connect(self.check_timeout_duration)

    def refresh_combobox_device(self):
        if self.refresh_checkbox_widget.isChecked():
            # renew list:
            self.combobox_add_devices()

    def update_combobox_device(self):
        self.refresh_checkbox_widget.setChecked(False)

    def check_timeout_duration(self, text):
        try:
            if text in u'infinite':
                self.var.timeout = None
            else:
                self.var.timeout = int(text)
                if not 0 <= self.var.timeout <= 3600000:
                    raise ValueError
        except ValueError:
            # Handle invalid input or out of range value
            self.timeout_line_edit_widget.blockSignals(True)
            self.timeout_line_edit_widget.setText('')
            self.timeout_line_edit_widget.blockSignals(False)

    def combobox_add_devices(self):
        self.device_combobox_widget.clear()
        self.device_combobox_widget.addItem(u'Keyboard', userData=None)
        
        # Create the EVT device list
        sleep(1) # delay after possible init of a previous instance of this plugin. 
        myevt = EventExchanger()
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
                self.device_combobox_widget_widget.addItem(composed_string)
                # previous used device present?
                if self.var.device[:15] in product_string:
                    self.var.device = composed_string
                    previous_device_found = True       
        except:
            self.var.device = u'Keyboard'
            oslogger.warning("No devices found! Switching to Keyboard.")

        if previous_device_found is False:
            self.var.device = u'Keyboard'
            oslogger.warning(
                "The hardware configuration has been changed since the last run! Switching to Keyboard.")