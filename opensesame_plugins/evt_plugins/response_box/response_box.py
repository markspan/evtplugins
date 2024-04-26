#-*- coding:utf-8 -*-

"""
Author: Martin Stokroos
2024

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
from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas
from libopensesame.oslogging import oslogger
from openexp.keyboard import Keyboard
from pyevt import EvtExchanger


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

        if isinstance(self.var.timeout, int):
            if self.var.timeout > 0:
                _timeout = self.var.timeout
            else:
                _timeout = 0
        else:
            _timeout = None
        self.var._timeout = _timeout
        #oslogger.info('timeout: {}' .format(self.var._timeout))

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
            # Dynamically load an EVT device
            self.myevt = EvtExchanger()
            try:
                self.myevt.Select(self.var.device)
                oslogger.info("Connecting the RSP-12x box.")
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
        # Trick to pass self.var._timeout to WaitForDigEvents(). Passing directly does not work(?)
        if self.var._timeout is None:
            _timeout is None
        else:
            _timeout = self.var._timeout

        if self.var.device != u'Keyboard':
            t0 = self.set_item_onset() # Save the current time.
            self.var.response, self.var.end_time = \
                self.myevt.WaitForDigEvents(
                    self.var.combined_allowed_events, _timeout)
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
    
    def __init__(self, name, experiment, script=None):
        ResponseBox.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()
        
        myevt = EvtExchanger()
        listOfDevices = myevt.Attached(u"EventExchanger-RSP-12")
        if listOfDevices:
            for i in listOfDevices:
                self.device_combobox.addItem(i)
        # Prevents hangup if device is not found after reopening the project:
        if not self.var.device in listOfDevices: 
            self.var.device = u'Keyboard'
        self.refresh_checkbox.stateChanged.connect(self.refresh_combobox_device)
        self.device_combobox.currentIndexChanged.connect(self.update_combobox_device)

    def refresh_combobox_device(self):
        if self.refresh_checkbox.isChecked():
            self.device_combobox.clear()
            # create new list:
            self.device_combobox.addItem(u'Keyboard', userData=None)
            myevt = EvtExchanger()
            listOfDevices = myevt.Attached(u"EventExchanger-RSP-12")
            if listOfDevices:
                for i in listOfDevices:
                    self.device_combobox.addItem(i)

    def update_combobox_device(self):
        self.refresh_checkbox.setChecked(False)