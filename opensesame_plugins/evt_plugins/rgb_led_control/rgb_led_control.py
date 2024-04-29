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

import time
import math
import distutils.util
from pyevt import EvtExchanger
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas
from libopensesame.oslogging import oslogger
from openexp.keyboard import Keyboard

class RgbLedControl(Item):

    description = u"Plugin to send LED RGB data from \
        \r\nEventExchanger-based digital input/output device."

    # Reset plug-in to initial values.
    def reset(self):
        """Resets plug-in to initial values."""
        self.var.device = u'DUMMY'
        self.var.correct_button = u'1'
        self.var.allowed_buttons = u'1;2;3'
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
        # Dynamically load an EVT device
        self.myevt = EvtExchanger()
        try:
            self.myevt.Select(self.var.device)
            self.myevt.SetLines(0)
            oslogger.info("Connecting and resetting EVT device.")
        except:
            self.var.device = u'DUMMY'
            oslogger.warning("Connecting to EVT device failed! Switching to dummy-mode.")

        if not type(self.var.timeout) == int \
        and not type(self.var.timeout) == float:
            self.var.timeout = -1
        # Recode Allowed buttons to AllowedEventLines
        self.var.AllowedEventLines = 0
        try:
            AllowedList = self.var.allowed_buttons.split(";")
            for x in AllowedList:
                self.var.AllowedEventLines += (1 << (int(x, 10) - 1))
        except Exception:
            x = self.var.allowed_buttons
            self.var.AllowedEventLines = (1 << (x - 1))

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

        if self.var.device != u'DUMMY':
            for b in range(4):
                self.myevt.SetLedColor(
                    ((BLC[b] >> 16) & 0xFF),
                    ((BLC[b] >> 8) & 0xFF),
                    (BLC[b] & 0xFF),
                    b + 1, 1)

            if self.var.feedback == u'yes':
                for b in range(4):
                    self.myevt.SetLedColor(
                        ((IC >> 16) & 0xFF),
                        ((IC >> 8) & 0xFF),
                        (IC & 0xFF),
                        b + 1, b + 11)

                self.myevt.SetLedColor(
                    ((CC >> 16) & 0xFF),
                    ((CC >> 8) & 0xFF),
                    (CC & 0xFF),
                    int(self.var.correct_button),
                    int(self.var.correct_button) + 10)

            # Call the 'wait for event' function in \
            # the EventExchanger C# object.
            (self.var.Response, self.var.RT) = (
                self.myevt.WaitForDigEvents(
                    self.var.AllowedEventLines, self.var.timeout))

            if (self.var.Response != -1):
                self.var.Response = math.log2(self.var.Response) + 1

            # FEEDBACK:
            if self.var.feedback == u'yes':
                time.sleep(self.var.reset_delay / 1000.0)
                for b in range(4):
                    self.myevt.SetLedColor(0, 0, 0, b + 1, 1)

        else:
            # demo mode: keyboard response.....
            if self.var.timeout == -1:
                self.var.timeout = None
            self.var.Response,
            self.var.RT = self.Keyboard.get_key(
                timeout=self.var.timeout)

        # HOUSE KEEPING:
        self.var.correct = \
            bool(self.var.Response == self.var.correct_button)

        self.var.correct = distutils.util.strtobool(str(self.var.correct))

        print(self.var.correct)
        # Add all response related data to the Opensesame responses instance.
        self.experiment.responses.add(response_time=self.var.RT,
                                      correct=self.var.correct,
                                      response=self.var.Response,
                                      item=self.name)
        # Report success
        return True


class QtRgbLedControl(RgbLedControl, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        RgbLedControl.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()

        self.myevt = EvtExchanger()
        listOfDevices = self.myevt.Attached(u"EventExchanger-RSP-LT")
        if listOfDevices:
            for i in listOfDevices:
                self.device_combobox.addItem(i)
        # Prevents hangup if device is not found after reopening the project:
        if not self.var.device in listOfDevices: 
            self.var.device = u'DUMMY'
            
        # event based calls:
        self.refresh_checkbox.stateChanged.connect(self.refresh_combobox_device)
        self.device_combobox.currentIndexChanged.connect(self.update_combobox_device)

    def refresh_combobox_device(self):
        if self.refresh_checkbox.isChecked():
            self.device_combobox.clear()
            # create new list:
            self.device_combobox.addItem(u'DUMMY', userData=None)
            listOfDevices = self.myevt.Attached(u"EventExchanger-RSP-LT")
            if listOfDevices:
                for i in listOfDevices:
                    self.device_combobox.addItem(i)

    def update_combobox_device(self):
        self.refresh_checkbox.setChecked(False)
