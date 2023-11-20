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

from pyevt import EvtExchanger
from libopensesame.py3compat import *
from libopensesame.base_response_item import BaseResponseItem
from openexp.keyboard import Keyboard
from libopensesame.oslogging import oslogger
from libqtopensesame.items.qtautoplugin import QtAutoPlugin

class RspPyevt(BaseResponseItem):

    """
        This class (the class with the same name as the module)
        handles the basic functionality of the item. It does
        not deal with GUI stuff.
    """

    description = u"Collects input from a RSP-12x response box or from a generic keyboard"
    process_feedback = True

    def reset(self):
        # Set the default values of the plug-in items in the GUI
        self.var.device = u'Keyboard'
        self.var.correct_response = u'1'
        self.var.allowed_responses = u'1;2'
        self.var.timeout = u'infinite'

    def validate_response(self, response):
        try:
            response = int(response)
        except ValueError:
            return False
        return response >= 0 or response <= 255

    def _get_button_press(self):
        r"""Calls libjoystick.get_button_press() with the correct arguments."""
        oslogger.info("Button pressed!")
        return

    def prepare_response_func(self):
        """The preparation phase of the plug-in goes here."""
        self.evt = EvtExchanger()

        try:
            Device = self.evt.Select(self.var.device)
        except:
            self.var.device = u'Keyboard'
            oslogger.info("Cannot find any response box: using the keyboard by default")
        
        if not isinstance(self.var.timeout, int):
            self._timeout = None
        self._keyboard = Keyboard(
            self.experiment,
            keylist=(
                self._allowed_responses if self._allowed_responses
                else list(range(0, 9))  # Only numeric keys
            ),
            timeout=self._timeout
        )
        if self.var.device == u'Keyboard':
            return self._keyboard.get_key

    def response_matches(self, test, ref):
        return safe_decode(test) in ref

    def coroutine(self):
        if self.var.device == u'Keyboard':
            self._keyboard.timeout = 0
        else:
            self._timeout = 0
            self.var.response, self.var.response_time = \
                (self.evt.WaitForDigEvents(self.var.allowed_responses,
                                           self.var.timeout))
            oslogger.info("Response %d =", self.var.response)

        alive = True
        yield
        self._t0 = self.set_item_onset()
        # while alive:
            # button, time = self._collect_response()
            # if button is not None:
            #    break
            # alive = yield
        # self.process_response((button, time))


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