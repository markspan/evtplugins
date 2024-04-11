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

This file is modified from the Joystick core plugin of 
OpenSesame by: M. Stokroos, 2024
This plugin now accepts EventExchanger-RSP-12 devices, developed by the
Research Support team from the faculty of Behavioural and Social Sciences
from the University of Groningen.


TO DO: Find where to reset the timer in rsp mode.
"""
import math
from pyevt import EvtExchanger
from libopensesame.py3compat import *
from libopensesame.base_response_item import BaseResponseItem
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.keyboard import Keyboard
from libopensesame.oslogging import oslogger

class RspPyevt(BaseResponseItem):

    description = u"Collects input from a RSP-12x responsebox or from a generic keyboard"

    process_feedback = True

    def reset(self):
        # Set the default values of the plug-in items in the GUI
        self.var._device = u'Keyboard'
        self.var.correct_response = u'1'
        self.var.allowed_responses = u'1;2'
        self.var.timeout = u'infinite'
    '''
    def validate_response(self, response):
        try:
            response = int(response)
        except ValueError:
            return False
        return response >= 0 or response <= 255
    '''
    def process_response(self, response_args):
        #oslogger.info('{}'.format(response_args))
        response, t1 = response_args
        '''
        Decode the physical button number here.
        (What is two button are pressed at the same time?
        The hardware doesn't seem to output a double change
        as one single event. To be confirmed...)
        '''
        if self.var._device != u'Keyboard':
            if isinstance(response, list):
                response = response[0]
            if response > 0:
                response = math.log2(response) + 1
            else:
                response = -1
        if self._correct_responses is not None:
            correct = self.response_matches(response, self._correct_responses)
        else:
                correct = None
        self.responses.add(
            response=response, response_time=t1, correct=correct,
            item=self.name, feedback=self.process_feedback)

    def _get_button_press(self):
        r"""Calls EventExcahnger.WaitForDigEvents() with the correct arguments."""
        return self.experiment.evt.WaitForDigEvents(self.var.allowed_events, 
                                                    self.var.timeout)

    def prepare_response_func(self):
        self._keyboard = Keyboard(
            self.experiment,
            keylist=(
                self._allowed_responses if self._allowed_responses
                else list(range(0, 10)) # Only numeric keys
            ),
            timeout = self._timeout
        )
        if self.var._device == u'Keyboard':
            # get keyboard response...
            return self._keyboard.get_key
        
        # Dynamically load an EventExchanger RSP device.
        if not hasattr(self.experiment, u'EventExchanger-RSP-12'):
            self.experiment.evt = EvtExchanger()
            try:
                Device = self.experiment.evt.Select(self.var._device)
                oslogger.debug("Loading the RSP-12x box.")
            except:
                oslogger.debug("Loading the RSP-12x-box failed!")
        '''
        The next part calculates the bit mask for the allowed responses
        to receive from the hardware.
        '''
        self.var.allowed_events = 0
        try:
            AllowedList = self.var.allowed_responses.split(";")
            for x in AllowedList:
                self.var.allowed_events +=  (1 << (int(x, 10) -1))
        except:
            x = self.var.allowed_responses
            self.var.allowed_events =  (1 << (x-1))
        #oslogger.info('{}'.format(self.var.allowed_events))

        if not isinstance(self.var.timeout, int):
            self.var.timeout = -1 # accepted timeout=infinite for EventExchanger.WaitForDigEvents()
        if self._allowed_responses is not None:
            self._allowed_responses = [int(r) for r in self._allowed_responses]
        return self._get_button_press
    
    '''
    def response_matches(self, test, ref):
        return safe_decode(test) in ref

    def coroutine(self):
        if self.var._device == u'Keyboard':
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
    '''

class QtRspPyevt(RspPyevt, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        RspPyevt.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()
        evt = EvtExchanger()
        
        listOfDevices = evt.Attached(u"EventExchanger-RSP-12")
        if listOfDevices:
            for i in listOfDevices:
                self.device_widget.addItem(i)
        else:
            self.var._device = u"Keyboard"
