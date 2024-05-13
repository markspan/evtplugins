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

import math
from time import sleep
from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas
from libopensesame.oslogging import oslogger
from openexp.keyboard import Keyboard
from pyevt import EventExchanger

# constant
_DEVICE_GROUP = u'RSP'

# global var
open_devices = {} # Store open device handles.


class ResponseBox(Item):

    description = u"A Plug-in to collect input from a RSP-12x responsebox."

    def reset(self):
        """Resets plug-in to initial values."""
        self.var.device = u'Keyboard'
        self.var.correct_response = u'1'
        self.var.allowed_responses = u'1;2'
        self.var.timeout = u'infinite'

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        super().prepare()

        oslogger.info('timeout: {}' .format(self.var.timeout))

        '''
        The next part calculates the bit mask for the allowed responses
        to receive from the RSP-12x.
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

        if self.var.device != u'Keyboard':
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
            except:
                self.var.device = u'Keyboard'
                oslogger.warning("Loading the RSP-12x-box failed! Default is keyboard")
                self.my_keyboard = Keyboard(self.experiment, 
                                    keylist=list_allowed_buttons, timeout=_timeout)
        else:
            self.my_keyboard = Keyboard(self.experiment, 
                                keylist=list_allowed_buttons, timeout=_timeout)

    def run(self):
        """The run phase of the plug-in goes here."""

        if self.var.device != u'Keyboard':
            t0 = self.set_item_onset() # Save the current time.
            
            # Passing self.var._timeout=None does not work(?)
            if isinstance(self.var.timeout, int):
                self.var.timeout = abs(self.var.timeout)
                self.var.response, self.var.end_time = \
                    open_devices[self.current_device].wait_for_event(
                        self.var.combined_allowed_events, self.var.timeout)
            else:
                self.var.response, self.var.end_time = \
                    open_devices[self.current_device].wait_for_event(
                        self.var.combined_allowed_events, None)

            # Decode output to knob number:
            if self.var.response > 0:
                self.var.response = math.log2(self.var.response) + 1
            else:
                self.var.response = -1
        else:
            # Get keyboard response...
            t0 = self.set_item_onset() # Save the current time.
            self.var.response, self.var.end_time = self.my_keyboard.get_key()

        # Pass all response data to the Opensesame response item.
        self.experiment.responses.add(response_time = self.var.end_time, \
                                correct = (self.var.response == \
                                           self.var.correct_response), \
                                response = self.var.response, \
                                item=self.name)


class QtResponseBox(ResponseBox, QtAutoPlugin):
    
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
        ResponseBox.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):

        """Constructs the GUI controls. Usually, you can omit this function
        altogether, but if you want to implement more advanced functionality,
        such as controls that are grayed out under certain conditions, you need
        to implement this here.
        """

        super().init_edit_widget()

        self.combobox_add_devices() # first time fill the combobox
        
        # event-triggered calls:
        self.refresh_checkbox.stateChanged.connect(self.refresh_combobox_device)
        self.device_combobox.currentIndexChanged.connect(self.update_combobox_device)

    def refresh_combobox_device(self):
        if self.refresh_checkbox.isChecked():
            # renew list:
            self.combobox_add_devices()

    def update_combobox_device(self):
        self.refresh_checkbox.setChecked(False)

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
        
        added_items_list = {}
        if device_list:
            d_count = 1
            for d in device_list:
                product_string = d['product_string']
                serial_string = d['serial_number']
                composed_string = str(d_count) + ": " + \
                    product_string[15:] + " s/n: " + serial_string
                # add device string to combobox:
                self.device_combobox.addItem(composed_string)
                added_items_list[d_count] = composed_string
                d_count += 1
                if d_count > 9:
                    # keep number of digits 1
                    break
        # Prevents hangup if the old device is not found after reopening the project.
        # Any change of the hardware configuration can cause this.
        if not self.var.device in added_items_list.values():
            self.var.device = u'0: DUMMY'
            oslogger.warning("The hardware configuration has been changed since the last run! Switching to dummy.")