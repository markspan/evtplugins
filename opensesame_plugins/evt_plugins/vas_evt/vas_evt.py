# -*- coding:utf-8 -*-

"""
No rights reserved. All files in this repository are released into the public
domain.
"""
import os
import sys
import numpy as np
from pyevt import EvtExchanger
from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas
from libopensesame.oslogging import oslogger
from openexp.keyboard import Keyboard
from openexp.mouse import Mouse
from libopensesame.exceptions import osexception


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
        self.var.vas_encoder_id = u"MOUSE"
        self.var.vas_exit_method = u'MOUSE'
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
        self.evt = EvtExchanger()
        Devices = self.evt.Select(self.var.vas_encoder_id)

        try:
            self.evt.RENC_SetUp(1024,
                               0,
                               int(1024 *
                                   (self.var.vas_cursor_startposition /
                                    100.0)),
                               1,
                               1)
            if Devices[0] is None:
                raise

        except Exception:
            self.var.vas_encoder_id = u"MOUSE"
            oslogger.info("Cannot find encoder input device: Using mouse")

        # Checking the excistence of the VAS elements is only
        # possible in the runphase as only then the full
        # canvas is availeable.

        self.c = Canvas(self.experiment)
        self._Keyboard = Keyboard(self.experiment, timeout=0)
        self._Mouse = Mouse(self.experiment)
        my_canvas = self.experiment.items[self.var.vas_canvas_name].canvas

        try:
            if my_canvas[self.var.vas_cursor_nameE] is not None or
            if my_canvas[self.var.vas_body_nameE] is not None:
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

    def run(self):
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
            if self.var.vas_exit_method == 'MOUSE':
                button, position, timestamp = self._Mouse.get_click(timeout=2)
                if button is not None:
                    break
            if self.var.vas_exit_method == 'KEY':
                key, time = self._Keyboard.get_key(timeout=5)
                if key is not None:
                    if key == self.var.VAS_EXITKEY:
                        break

            self._Keyboard.flush()

            if self.var.vas_encoder_id != u"MOUSE":
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


class QtVasEvt(VasEvt, QtAutoPlugin):

    """
    This class handles the GUI aspect of the plug-in.
    By using qtautoplugin, we usually need to do hardly
    anything, because the GUI is defined in info.json.
    """

    def __init__(self, name, experiment, script=None):

        """
        Constructor.

        Arguments:
        name        --    The name of the plug-in.
        experiment    --    The experiment object.

        Keyword arguments:
        script        --    A definition script. (default=None)
        """

        # We don't need to do anything here, except call the parent
        # constructors.
        VasEvt.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def c(self):
        self.VAS_TIMERNAME_widget.setEnabled(
            self.vas_exit_method_widget.currentText() == u'TIME')
        self.vas_duration_widget.setEnabled(
            self.vas_exit_method_widget.currentText() == u'TIME')
        self.VAS_EXITKEY_widget.setEnabled(
            self.vas_exit_method_widget.currentText() == u'KEY')

    def init_edit_widget(self):

        """
        Constructs the GUI controls. Usually, you can omit this function
        altogether, but if you want to implement more advanced functionality,
        such as controls that are grayed out under certain conditions, you need
        to implement this here.
        """

        super().init_edit_widget()

        ELister = EvtExchanger()
        listofdevices = ELister.Attached()
        for i in listofdevices:
            self.VAS_ENCODERID_widget.addItem(i)
        self.VAS_TIMERNAME_widget.setEnabled(
            self.vas_exit_method_widget.currentText() == u'TIME')
        self.vas_duration_widget.setEnabled(
            self.vas_exit_method_widget.currentText() == u'TIME')
        self.VAS_EXITKEY_widget.setEnabled(
            self.vas_exit_method_widget.currentText() == u'KEY')
        self.vas_exit_method_widget.currentTextChanged.connect(self.c)
