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

import os
import sys
import math
from pyevt import EvtExchanger
from libopensesame.py3compat import *
from libopensesame.item import Item
from libopensesame.oslogging import oslogger
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas
from openexp.keyboard import Keyboard


class ResponseBox(Item):

    """
        This class (the class with the same name as the module)
        handles the basic functionality of the item. It does
        not deal with GUI stuff.
    """

    description = u"Acquires buttonpress-responses and/or digital \
        events\r\nfrom Event Exchanger-based digital input device."

    def reset(self):
        # Set the default values of the plug-in items in the GUI
        self.var._productName = u'Keyboard'
        self.var._correctButton = u''
        self.var._allowedButtons = u'1;2;3;4'
        self.var._responseTimeout = u'infinite'

    def prepare(self):
        super().prepare()
        self.EE = EvtExchanger()
        Device = self.EE.Select(self.var._productName)

        try:
            if Device is None:
                raise
            
        except Exception:
            self.var._productName = u'Keyboard'
            self.Keyboard = Keyboard(self.experiment)
            if not type(self.var._responseTimeout) == int:
                self.var._responseTimeout = None
            oslogger.info(
                "Cannot find ResponseBox: Using Keyboard instead")

        if not type(self.var._responseTimeout) == int:
            self.var._responseTimeout = -1
        # Recode Allowed buttons to AllowedEventLines
        self.var.AllowedEventLines = 0
        try:
            AllowedList = self.var._allowedButtons.split(";")
            for x in AllowedList:
                self.var.AllowedEventLines += (1 << (int(x, 10) - 1))
        except Exception:
            x = self.var._allowedButtons
            self.var.AllowedEventLines = (1 << (x - 1))

    def run(self):
        # Save the current time ...
        t0 = self.set_item_onset()
        # Call the 'wait for event' function in the EventExchanger C# object.

        if self.var._productName != u'Keyboard':
            (self.var.Response, self.var.RT) = (
                self.EE.WaitForDigEvents(self.var.AllowedEventLines,
                                         self.var._responseTimeout))
            self.var.Response = math.log2(self.var.Response) + 1

        else:
            # demo mode: keyboard response...
            self.var.Response, self.var.RT = self.Keyboard.get_key(
                timeout=self.var._responseTimeout)

        self.CorrectResponse = \
            (self.var.Response == self.var._correctButton)
        # Add all response related data to the Opensesame responses instance.
        self.experiment.responses.add(
            response_time=self.var.RT,
            correct=self.CorrectResponse,
            response=self.var.Response,
            item=self.name)
        # Report success
        return True


class qtresponse_box(ResponseBox, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        ResponseBox.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()
        EE = EvtExchanger()
        listofdevices = EE.Attached()
        for i in listofdevices:
            self.ProductName_widget.addItem(i)

    self.line_edit_widget.setEnabled(self.checkbox_widget.isChecked())
    self.checkbox_widget.stateChanged.connect(
        self.line_edit_widget.setEnabled)
