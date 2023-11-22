"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PAresponse_timeICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
import math
from pyevt import EvtExchanger
from openexp.keyboard import Keyboard
from libopensesame.item import Item
from libopensesame.oslogging import oslogger
from libopensesame.base_response_item import BaseResponseItem
from libqtopensesame.items.qtautoplugin import QtAutoPlugin

class RspPyevt(Item):

    """
        This class (the class with the same name as the module)
        handles the basic functionality of the item. It does
        not deal with GUI stuff.
    """

    description = u"Collects input from a RSP-12x responsebox or from a generic keyboard"

    def reset(self):
        # Set the default values of the plug-in items in the GUI
        self.var.device = u'Keyboard'
        self.var.correct_response = u'1'
        self.var.allowed_responses = u'1;2'
        self.var.timeout = u'infinite'

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        super().prepare()

        if not isinstance(self.var.timeout, int):
            self.var.timeout = None

        self.evt = EvtExchanger()
        try:
            Device = self.evt.Select(self.var.device)
        except:
            self.var.device = u'Keyboard'
            oslogger.info("Cannot find any response box: using the keyboard by default")

        try:
            self._timeout = int(self.var.timeout)
        except Exception:
            self._timeout = -1

        self.var.AllowedEventLines = 0
        try:
            AllowedList = self.var.allowed_responses.split(";")
            for x in AllowedList:
                self.var.AllowedEventLines +=  (1 << (int(x, 10) -1))
        except:
            x = self.var.allowed_responses
            self.var.AllowedEventLines =  (1 << (x-1))

    def run(self):
        # Save the current time ...
        t0 = self.set_item_onset()
        # Call the 'wait for event' function in the EventExchanger C# object.

        if self.var.device != u'Keyboard':
            self.var.response, self.var.response_time = \
                (self.evt.WaitForDigEvents(self.var.AllowedEventLines,
                                           self._timeout))
            if self.var.response > 0:
                self.var.response = math.log2(self.var.response) + 1
            else:
                self.var.response = -1
            
        else:
            # get keyboard response...
            self.var.response, self.var.response_time = self.my_keyboard.get_key(timeout=self._timeout)

        self.CorrectResponse = (
            self.var.response == self.var.correct_response)
        # Add all response related data to the Opensesame responses instance.
        self.experiment.responses.add(response_time=self.var.response_time, \
                                correct=self.CorrectResponse, \
                                response=self.var.response, \
                                item=self.name)
        #Report success        
        return True


class QtRspPyevt(RspPyevt, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        RspPyevt.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()
        evt = EvtExchanger()
        
        listOfDevices = evt.Attached(u"EventExchanger")
        if listOfDevices:
            for i in listOfDevices:
                self.device_widget.addItem(i)
        else:
            self.var.device = u"Keyboard"