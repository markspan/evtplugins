# -*- coding:utf-8 -*-

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

import os
import sys
import numpy as np
from pyevt import EventExchanger
from time import sleep
from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas
from libopensesame.oslogging import oslogger
from openexp.keyboard import Keyboard
from openexp.mouse import Mouse
from libopensesame.exceptions import osexception

# constant
_DEVICE_GROUP = u'RDC1'

# global var
open_devices = {} # Store open device handles.


class VasEvt(Item):

    """
    This class (the class with the same name as the module) handles the basic
    functionality of the item. It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'A VAS modifier for a canvas'

    def reset(self):

        """
        desc:
            Resets plug-in to initial values.
        """

        # Here we provide default values for the variables that are specified
        # in info.json. If you do not provide default values, the plug-in will
        # work, but the variables will be undefined when they are not
        # explicitly set in the GUI.
        self.var.device = u"0: Mouse"
        self.var.vas_exit_method = u'Mouse'
        self.var.vas_exit_key = u' '
        self.var.vas_duration = 10000
        self.var.vas_canvas_name = u'VASSCREEN'
        self.var.vas_body_nameE = u'VASBODY'
        self.var.vas_cursor_nameE = u'VASCURSOR'
        self.var.vas_timer_nameE = u'VASTIMER'
        self.var.vas_cursor_startposition = 0

    def prepare(self):

        """The preparation phase of the plug-in goes here."""
        super().prepare()

        if int(self.var.device[:1]) == 0:
            oslogger.warning("Dummy prepare")
        else:
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
                open_devices[self.current_device].renc_init(
                    1024, 0, int(1024 * (self.var.vas_cursor_startposition / 100.0)), 1, 1)
            except:
                self.var.device = u'0: Mouse'
                oslogger.warning("Device missing! Switching to dummy.")
        '''
        # Checking the excistence of the VAS elements is only
        # possible in the runphase as only then the full
        # canvas is availeable.
        self.c = Canvas(self.experiment)
        self._Keyboard = Keyboard(self.experiment, timeout=0)
        self._Mouse = Mouse(self.experiment)
        my_canvas = self.experiment.items[self.var.vas_canvas_name].canvas

        try:
            if my_canvas[self.var.vas_cursor_nameE] is not None or \
                my_canvas[self.var.vas_body_nameE] is not None:
                    oslogger.info("Should not occur")
        except Exception as e:
            raise osexception(u"Please read the VAS manual:\n\r\
                              No VAS elements found on the named canvas")

        self.c = self.experiment.items[self.var.vas_canvas_name].canvas
        self.c[self.var.vas_cursor_nameE].sx = \
            (self.c[self.var.vas_body_nameE].sx +
             self.c[self.var.vas_body_nameE].ex) / 2.0
        self.c[self.var.vas_cursor_nameE].ex = \
            self.c[self.var.vas_cursor_nameE].sx

        self.VASLENGTH = self.c[self.var.vas_body_nameE].ex - \
            self.c[self.var.vas_body_nameE].sx
        self.SHOWTIMER = False
        if self.var.vas_exit_method == 'TIME':
            if my_canvas[self.var.vas_cursor_nameE] is not None:
                self.SHOWTIMER = True
                self.w = self.c[self.var.vas_timer_nameE].ex - \
                    self.c[self.var.vas_timer_nameE].sx
                self.h = self.c[self.var.vas_timer_nameE].ey - \
                    self.c[self.var.vas_timer_nameE].sy
                self.TIMER_DIR = 'vert'
                self.TIMERSIZE = self.h
                if (abs(self.w) > abs(self.h)):
                    self.TIMER_DIR = 'horiz'
                    self.TIMERSIZE = self.w
    '''
    def run(self):
        '''
        self.set_item_onset(self.c.show())
        st = self.experiment.time()
        val = int(1024*(self.var.vas_cursor_startposition/100.0))

        while(True):
            if self.var.vas_exit_method == 'TIME':
                if self.SHOWTIMER:
                    tperc = (self.experiment.time()-st)/self.var.vas_duration
                    if self.TIMER_DIR == 'horiz':
                        self.c[self.var.vas_timer_nameE].ex = \
                            self.c[self.var.vas_timer_nameE].sx + (
                                (1 - tperc) * self.w)
                    else:
                        self.c[self.var.vas_timer_nameE].ey = \
                            self.c[self.var.vas_timer_nameE].sy + (
                                (1 - tperc) * self.h)

                if ((self.experiment.time()-st) > self.var.vas_duration):
                    break
            if self.var.vas_exit_method == 'Mouse':
                button, position, timestamp = self._Mouse.get_click(timeout=2)
                if button is not None:
                    break
            if self.var.vas_exit_method == 'KEY':
                key, time = self._Keyboard.get_key(timeout=5)
                if key is not None:
                    if key == self.var.VAS_EXITKEY:
                        break

            self._Keyboard.flush()

            if self.var.vas_encoder_id != u"0: Mouse":
                val = self.evt.GetAxis()
            else:
                (val, y), time = self._Mouse.get_pos()
                val = (val + 512)

            if val is not None:
                val = (val)/1024.0
                val = np.clip(val, 0, 1)
                try:
                    self.c["VASVALUE"].text = str(round(val, 2))
                except Exception as e:
                    e.Message = ""

                for i in self.c[self.var.vas_cursor_nameE]:
                    i.sx = self.c[self.var.vas_body_nameE].sx + \
                        (val*self.VASLENGTH)
                    i.ex = i.sx

            self.c.show()

        # Add all response related data to the Opensesame responses instance.
        self.experiment.responses.add(response_time=self.experiment.time()-st,
                                      correct=None,
                                      response=str(round(val, 2)),
                                      item=self.name)
        '''

class QtVasEvt(VasEvt, QtAutoPlugin):

    """
    This class handles the GUI aspect of the plug-in.
    By using qtautoplugin, we usually need to do hardly
    anything, because the GUI is defined in info.json.
    """

    def __init__(self, name, experiment, script=None):
        # We don't need to do anything here, except call the parent
        # constructors. Since the parent constructures take different arguments
        # we cannot use super().
        VasEvt.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
    '''
    def c(self):
        self.VAS_TIMERNAME_widget.setEnabled(
            self.vas_exit_method_widget.currentText() == u'TIME')
        self.vas_duration_widget.setEnabled(
            self.vas_exit_method_widget.currentText() == u'TIME')
        self.VAS_EXITKEY_widget.setEnabled(
            self.vas_exit_method_widget.currentText() == u'KEY')
    '''
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
        '''
        self.vas_timername_widget.setEnabled(
            self.vas_exit_method_widget.currentText() == u'TIME')
        self.vas_duration_widget.setEnabled(
            self.vas_exit_method_widget.currentText() == u'TIME')
        self.vas_exit_method_widget.setEnabled(
            self.vas_exit_method_widget.currentText() == u'KEY')
        self.vas_exit_method_widget.currentTextChanged.connect(self.c)
        '''
    def refresh_combobox_device(self):
        if self.refresh_checkbox.isChecked():
            # renew list:
            self.combobox_add_devices()

    def update_combobox_device(self):
        self.refresh_checkbox.setChecked(False)

    def combobox_add_devices(self):
        self.device_combobox.clear()
        self.device_combobox.addItem(u'0: Keyboard', userData=None)
        
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
            self.var.device = u'0: Keyboard'
            oslogger.warning("The hardware configuration has been changed since the last run! Switching to dummy.")