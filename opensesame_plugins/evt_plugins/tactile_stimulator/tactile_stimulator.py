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
import time
import math
import sys
from pyevt import EvtExchanger
from libopensesame.py3compat import *
from libopensesame.item import Item
from libopensesame.oslogging import oslogger
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas
from openexp.mouse import mouse
from openexp.canvas_elements import (
	Line,
	Rect,
	Polygon,
	Ellipse,
	Image,
	Gabor,
	NoisePatch,
	Circle,
	FixDot,
	ElementFactory,
	RichText,
	Arrow,
	Text
)

class TactileStimulator(Item):
    """Class for handling the Tactile Stimulator."""

    description = u"Plugin for the calibration and the usage of the Tactile Stimulator.\
        \nThe \"calibrate\" instance of the plugin should always precede the \"stimulate\" instance in the same experiment."

    PULSE_VALUE_MAX = 254.0  # some models of the SHK1-1B do accept 255 as max intensity and others 254 (...)

    def reset(self):
        self.var._percOfCalibrationValue = 0
        self.var._pulseDuration = 150  # default value
        self.var._pulseTimeOut = 1.0
        self.var._interPulseHoldOffTime = 8
        self.var._device = u"DUMMY"
        self.var._mode = u"Calibrate"

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        super().prepare()
        if not 1 <= self.var._pulseDuration <= 2000:
            oslogger.error("Pulse duration input out of range!")
            self.var._pulseDuration = 150
        self.experiment.var.tactstim_pulse_duration_ms = self.var._pulseDuration
        self.experiment.var.tactstim_pulse_value = 0
        self.evt = EvtExchanger()
        Device = self.evt.Select(self.var._deviceName)

        try:
            if Device is None:
                raise
        except Exception:
            self.var._deviceName = u"DUMMY"
            oslogger.warning("Did not find "
                             "a Tactile Stimulator device!")

        if self.var._mode == u"Calibrate":
            self.calibrate_prepare()
        elif self.var._mode == u"Stimulate":
            self.stimulate_prepare()

    def calibrate_prepare(self):
        if not (self.var._deviceName == u"DUMMY"):
            self.evt.SetLines(0)
            oslogger.info("Reset Tactile Stimulator Device")

        self.c = Canvas(self.experiment)
        self.c.background_color=u'black'
        # self.c.clear()
        self.c['Title'] = RichText(
            "Tactile Stimulator Calibration",
            center=True,
            x=0,
            y=-int(self.c.height / 3),
            color='white',
            font_family='mono',
            font_size=28
        )
        self.c['Instruction'] = RichText(
            "Point at the desired value position "
            "on the slider and click the mouse button. "
            "Click on TEST to apply the pulse. "
            "Click OK to accept.",
            center=True,
            x=0,
            y=-int(self.c.height / 8),
            color='white'
        )
        self.c.color = u"white"  # Draw the slider axis (was fgcolor ?)
        self.c['Slider_Box'] = Rect(
            -self.c.width / 2.2,
            0,
            2 * self.c.width / 2.2,
            28,
            fill=False
        )
        self.c.color = u"white"
        self.c['Slider'] = Rect(
            (-self.c.width / 2.2) + 6,
            6,
            (2 * self.c.width / 2.2) - 12,
            16,
            fill=True
        )
        self.c['Test_Box'] = Rect(
            -self.c.width / 3,
            self.c.height / 4,
            self.c.width / 10,
            self.c.height / 10,
            fill=True,
            color='red'
        )
        self.c['Test_Text'] = RichText(
            "TEST",
            x=(-self.c.width / 3) + (self.c.width / 20),
            y=(self.c.height / 4) + (self.c.height / 20),
            color='black'
        )
        self.c['OK_Box'] = Rect(
            self.c.width / 3,
            self.c.height / 4,
            -self.c.width / 10,
            self.c.height / 10,
            fill=True,
            color='green'
        )
        self.c['OK_Text'] = RichText(
            "OK",
            x=(self.c.width / 3)-(self.c.width / 20),
            y=(self.c.height / 4)+(self.c.height / 20),
            color='black'
        )
        self.c['Value_mA'] = RichText(
            str(round(0, 3)) + "mA",
            x=0,
            y=-(self.c.height / 4)+(self.c.height / 20),
            color='green'
        )
        self.c['Value_Perc'] = RichText(
            "("+str(round(0)) + "%)",
            x=0,
            y=-(self.c.height / 4)+(self.c.height / 12),
            color='green'
        )
        self.c['wait'] = RichText(
            str(round(0)),
            x=0,
            y=-(self.c.height / 10)+(self.c.height / 2),
            color='black'
        )
        self.c.show()
        self.experiment.var.tactstim_calibration_value = -1 
        # Assign negative number to indicate that the calibration prepare is done

    def stimulate_prepare(self):
        try:
            self.experiment.var.tactstim_calibration_value  # test if exists
        except:
            raise UserWarning("No calibration step has been done. "
                           "First run the Tactile Stimulator "
                           "in calibration mode!")

        if not 0 <= self.var._percOfCalibrationValue <= 100:
            oslogger.error("Given input percentage is out of range!")
            self.var._percOfCalibrationValue = 0

    def run(self):
        self.set_item_onset()
        if self.var._deviceName == u"DUMMY":
            if self.var._mode == u"Stimulate":
                oslogger.info('stimulate with {}% and duration of {}ms'
                              .format(self.var._percOfCalibrationValue,
                                      self.var._pulseDuration))
            else:
                self.calibrate()
        else:
            if self.var._mode == u"Calibrate":
                self.calibrate()
            elif self.var._mode == u"Stimulate":
                self.stimulate()
        return True

    def calibrate(self):
        slmouse = mouse(self.experiment, timeout=20, visible=True)
        slmouse.show_cursor(True)
        slmouse.set_pos(pos=(0, 0))
        xperc = 0
        self.c['Slider'].w = (xperc / 100) * (
            (2*self.c.width / 2.2) - 12)
        self.c.show()

        while True:  # Poll the mouse for buttonclicks
            button = None
            while button is None:
                button, position, timestamp = slmouse.get_click()

            button = None
            pos, mtime = slmouse.get_pos()
            x, y = pos

            if (x, y) in self.c['Slider_Box']:
                xperc = min((x + self.c.width / 2.2) / (
                    2 * ((self.c.width / 2.2) - 6)) * 100.0, 100)
                self.c['Slider'].w = (xperc / 100)*(
                    (2 * self.c.width / 2.2) - 12)
                self.c['Value_Perc'].text = "(" + \
                    str(round(xperc, 1)) + "%)"
                self.c['Value_mA'].text = str(
                    round(5*(xperc / 100.0), 1)) + "mA"
                self.c.show()

            if (x, y) in self.c['Test_Box']:
                if (self.var._deviceName == u"DUMMY"):
                    oslogger.info(
                        "(Dummy) Tactile Stimulator pulsing at: {}%"
                        .format(math.floor((xperc / 100.0) * self.PULSE_VALUE_MAX)))
                else:
                    self.evt.PulseLines(math.floor((xperc / 100.0) * self.PULSE_VALUE_MAX),
                                       self.var._pulseDuration)
                self.c['Test_Box'].color = 'blue'
                self.c.show()
                self.c['wait'].color = 'green'

                for n in range(1, self.var._interPulseHoldOffTime):
                    self.c['wait'].text = "wait... " + str(self.var._interPulseHoldOffTime - n)
                    self.c['wait'].color = 'green'
                    self.c.show()
                    time.sleep(1)
                    self.c['wait'].color = 'black'
                self.c['wait'].text = "wait... " + str(0)
                self.c['Test_Box'].color = 'red'
                self.c.show()

            if (x, y) in self.c['OK_Box']:
                self.experiment.var.tactstim_calibration_perc = round(xperc, 2)
                self.experiment.var.tactstim_calibration_value = math.floor(xperc * self.PULSE_VALUE_MAX / 100)
                self.experiment.var.tactstim_calibration_milliamp = round(5*(xperc / 100.0), 2)
                oslogger.info("The set pulse intensity "
                              "calibration value is "
                              "(raw, mA): {}, {:.2f}".
                              format(self.experiment.var.tactstim_calibration_value,
                                     self.experiment.var.tactstim_calibration_milliamp))
                break

    def stimulate(self):
        if (self.var._deviceName == u"DUMMY"):
            oslogger.info("In (Dummy) Tactile Stimulator: "
                          "pulse with value: " + \
                            str(self.var._percOfCalibrationValue))
        else:
            try:
                timeLastPulse = self.experiment.var.tactstim_time_last_pulse
            except Exception:
                timeLastPulse = 0
            td = time.time() - timeLastPulse
            # oslogger.info("Time duration between pulses: " + str(td))
            
            if (td > self.var._pulseTimeOut):
                """
                This if statement is to prevent the possibility
                to pulse if the previous stimulus was less then
                the minimum time ago
                """
                self.experiment.var.tactstim_pulse_value = math.floor(
                    self.var._percOfCalibrationValue * \
                        self.experiment.var.tactstim_calibration_perc * self.PULSE_VALUE_MAX / 10000)
                self.experiment.var.tactstim_pulse_milliamp = round(
                    self.var._percOfCalibrationValue * \
                        self.experiment.var.tactstim_calibration_perc * 5.0 / 10000, 2)

                self.evt.PulseLines(self.experiment.var.tactstim_pulse_value, self.var._pulseDuration)
                oslogger.info("Tactile-stimulator device "
                              "now pulsing at "
                              "(raw, mA): {}, {:.2f}".
                              format(self.experiment.var.tactstim_pulse_value,
                                     self.experiment.var.tactstim_pulse_milliamp))
            else:
                oslogger.warning("In (Hardware) Tactile Stimulator: "
                                 "the next pulse came too early. "
                                 "Please don't pulse in rapid succession!")
        self.experiment.var.tactstim_time_last_pulse = time.time()  # update the time stamp of the last call


class QtTactileStimulator(TactileStimulator, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        TactileStimulator.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def perc_check(self):
        try:
            val = int(self.value_widget.text())
        except ValueError:
            val = 0
        self.value_widget.setText(str(val))

    def duration_check(self):
        try:
            val = int(self.duration_widget.text())
        except ValueError:
            val = 0
        self.duration_widget.setText(str(val))

    def type_check(self):
        self.value_widget.setEnabled(
            self.calibrate_widget.currentText() == u'Stimulate')

    def init_edit_widget(self):
        super().init_edit_widget()
        evt = EvtExchanger()
        listOfDevices = evt.Attached(u"SHOCKER")

        """
        If there is no Tactile Stimulator attached,
        the selected name defaults to 'DUMMY' again.
        """
        if listOfDevices:
            for i in listOfDevices:
                self.device_widget.addItem(i)
        else:
            self.var._deviceName = u"DUMMY"

        self.duration_widget.setEnabled(True)
        self.value_widget.returnPressed.connect(self.perc_check)
        self.value_widget.returnPressed.connect(self.duration_check)
        self.calibrate_widget.currentTextChanged.connect(self.type_check)
        self.value_widget.setEnabled(
            self.calibrate_widget.currentText() == u'Stimulate')
