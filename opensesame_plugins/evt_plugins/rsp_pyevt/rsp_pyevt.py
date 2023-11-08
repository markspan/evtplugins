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
# from libopensesame.base_response_item import BaseResponseItem
# from libopensesame.oslogging import oslogger
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
# from openexp.canvas import Canvas
from openexp.keyboard import Keyboard


class RspPyevt(Item):
    """
        This class (the class with the same name as the module)
        handles the basic functionality of the item. It does
        not deal with GUI stuff.
    """

    description = u"Acquires buttonpress events from RSP-1x input devices."

    def reset(self):
        """Resets plug-in to initial values"""
        self.var.dummy = u'no'
        self.var.device = u'Keyboard'
        self.var.correct_button = u''
        self.var.allowed_buttons = u'1;2;3;4'
        self.var.timeout = u'infinite'

    def prepare(self):
        super().prepare()
        
        self._keyboard = Keyboard(
            self.experiment,
            keylist=(
                self._allowed_responses if self._allowed_responses
                else list(range(0, 10))  # Only numeric keys
            ),
            timeout=self._timeout
        )
        if self.var.dummy == u'yes':
            return self._keyboard.get_key
        # Dynamically load a rsp instance
        Device = self.EE.Select(self.var.device)
        
        if not type(self.var.timeout) == int:
            self.var.timeout = -1
        # Recode Allowed buttons to AllowedEventLines
        self.var.allowedEventLines = 0
        try:
            allowedList = self.var.allowed_buttons.split(";")
            for x in allowedList:
                self.var.allowedEventLines += (1 << (int(x, 10) - 1))
        except Exception:
            x = self.var.allowed_buttons
            self.var.allowedEventLines = (1 << (x - 1))

    def run(self):
        if self.var._dummy == u'yes':
            self._keyboard.timeout = 0
        else:
            self._timeout = 0
        alive = True
        yield
        self._t0 = self.set_item_onset()
        while alive:
            button, time = self._collect_response()
            if button is not None:
                break
            alive = yield
        self.process_response((button, time))


class QtResponseBox(RspPyevt, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        RspPyevt.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()
        evt = EvtExchanger()
        listofdevices = evt.Attached()
        for i in listofdevices:
            self.device_widget.addItem(i)

    # self.correct_button_widget.setEnabled(self.checkbox_widget.isChecked())
    # self.allowed_buttons_widget.setEnabled(self.checkbox_widget.isChecked())
    # self.timeout_widget.setEnabled(self.checkbox_widget.isChecked())
