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

import pygame
from libopensesame.py3compat import *
from libopensesame.base_response_item import BaseResponseItem
from openexp.keyboard import Keyboard
from libopensesame.oslogging import oslogger
from libqtopensesame.items.qtautoplugin import QtAutoPlugin


class RspPygame(BaseResponseItem):

    description = u"Collects input from a RSP-12x responsebox or from a generic keyboard"
    process_feedback = True

    def reset(self):
        self.var.device = u'Keyboard'
        self.var.timeout = u'infinite'
        self.var.allowed_responses = u'1;2'
        self.var.correct_response = u'1'
        self.var.device = u'Keyboard'

    def validate_response(self, response):
        try:
            response = int(response)
        except ValueError:
            return False
        return response >= 0 or response <= 255

    def _get_button_press(self):
        r"""Calls libjoystick.get_button_press() with the correct arguments."""
        # oslogger.info("Button pressed!")
        return self.experiment.joystick.get_joybutton(
            joybuttonlist=self._allowed_responses,
            timeout=self.var.timeout if type(self.var.timeout) == int else None
        )

    def prepare_response_func(self):
        self._keyboard = Keyboard(
            self.experiment,
            keylist=(
                self._allowed_responses if self._allowed_responses
                else list(range(0, 10))  # Only numeric keys
            ),
            timeout=self._timeout
        )
        if self.var.device == u'Keyboard':
            return self._keyboard.get_key
        # Dynamically load a joystick instance
        if not hasattr(self.experiment, u'joystick'):
            from .libjoystick import LibJoystick
            device_id = ord(self.var.device[-1]) - ord('0') # get the last char as int for joystick ID
            oslogger.info("RSP-12x ID: " + str(device_id))
            self.experiment.joystick = LibJoystick(self.experiment, device=device_id)
            self.python_workspace[u'joystick'] = self.experiment.joystick
        if self._allowed_responses is not None:
            self._allowed_responses = [int(r) for r in self._allowed_responses]
        return self._get_button_press

    def coroutine(self):
        if self.var.device == u'Keyboard':
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


class QtRspPygame(RspPygame, QtAutoPlugin):

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
        RspPygame.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):

        """Constructs the GUI controls. Usually, you can omit this function
        altogether, but if you want to implement more advanced functionality,
        such as controls that are grayed out under certain conditions, you need
        to implement this here.
        """

        super().init_edit_widget()

        self.combobox_add_devices()

        # event-triggered calls:
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
                self.var.timeout = u'infinite'
            else:
                self.var.timeout = int(text)
                if (not 0 <= self.var.timeout <= 3600000):
                    raise ValueError
        except ValueError:
            # Handle invalid input or out of range value
            self.timeout_line_edit_widget.blockSignals(True)
            self.timeout_line_edit_widget.setText('')
            self.timeout_line_edit_widget.blockSignals(False)

    def combobox_add_devices(self):
        self.device_combobox_widget.clear()
        self.device_combobox_widget.addItem(u'Keyboard', userData=None)

        previous_device_found = False
        pygame.joystick.init()
        joycount = pygame.joystick.get_count()
        for i in range(joycount):
            # add device(s) to combobox list
            self.device_combobox_widget.addItem("joystick-device_" + str(i))
            # Previous used device present?
            if ord(self.var.device[-1]) - ord('0') == i:
                previous_device_found = True
            if i > 8:
                break
        pygame.joystick.quit()

        if previous_device_found is False:
            self.var.device = u'Keyboard'
            oslogger.warning("The hardware configuration has been changed since the last run! Switching to Keyboard.")



