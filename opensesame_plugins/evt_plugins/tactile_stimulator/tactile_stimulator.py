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

"""
from openexp.canvas import Canvas, canvas
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
from openexp.mouse import mouse
"""

class TactileStimulator(Item):
    """"Class for using the Tactile Stimulator."""

    description = u"Plugin for the calibration and the use \
    of the Tactile Stimulator."

    def reset(self):
        self.var._percOfCalibrationValue = 0
        self.var._pulseDuration = 150  # fixed value
        self.var._pulseTimeOut = 1.0  # fixed value
        self.var._interPulseHoldOffTime = 8  # fixed value
        self.var._deviceName = u"DUMMY"
        self.var._mode = u"Calibrate"

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        # Call the parent constructor.
        super().prepare()
        if not 1 <= self.var._pulseDuration <= 2000:
            oslogger.error("Pulse duration out of range!")
            self.var._pulseDuration = 150
        self.experiment.set("tactstim_pulse_duration_ms",
                            self.var._pulseDuration)
        self.EE = EvtExchanger()
        Device = self.EE.Select(self.var._deviceName)

        try:
            if Device is None:
                raise
        except Exception:
            self.var._deviceName = u"DUMMY"
            oslogger.warning(
                "Did not find a Tactile Stimulator: code to debugwindow")

        if self.var._mode == u"Calibrate":
            self.Calibrate_Prepare()
        elif self.var._mode == u"Stimulate":
            self.Do_Pulse_Prepare()

    def run(self):
        self.set_item_onset()
        if self.var._deviceName == u"DUMMY":
            if self.var._mode == u"Stimulate":
                oslogger.info('dummy stimulator: \
                              {}, duration is {} ms'
                              .format(self.var._percOfCalibrationValue,
                                      self.var._pulseDuration))
            else:
                self.Calibrate_Run()
        else:
            if self.var._mode == u"Calibrate":
                self.Calibrate_Run()
            elif self.var._mode == u"Stimulate":
                self.Do_Pulse_Run()
        return True

    def Calibrate_Prepare(self):
        if not (self.var._deviceName == u"DUMMY"):
            self.EE.SetLines(0)
            oslogger.info("In (Hardware) Tactile Stimulator: reset port")

        self.canvas = Canvas(self.experiment)
        self.canvas.set_bgcolor("black")
        self.canvas.clear()
        self.canvas['Title'] = RichText(
            "Tactile Stimulator Calibration",
            center=True,
            x=0,
            y=-int(self.canvas.height/3),
            color="white",
            font_family="mono",
            font_size=28)

        self.canvas['Instruction'] = RichText(
            "Point at the desired value position"
            " on the axis and click ... "
            "Then click TEST",
            center=True,
            x=0,
            y=-int(self.canvas.height / 8),
            color="white")

        self.canvas.set_fgcolor("white")  # Draw the slider axis
        self.canvas['SliderBox'] = Rect(
            -self.canvas.width / 2.2,
            0,
            2 * self.canvas.width / 2.2,
            28,
            fill=False)

        self.canvas.set_fgcolor("white")
        self.canvas['Slider'] = Rect(
            (-self.canvas.width / 2.2) + 6,
            6,
            (2 * self.canvas.width / 2.2) - 12,
            16,
            fill=True)

        self.canvas['TestBox'] = Rect(
            (-self.canvas.width / 3),
            self.canvas.height / 4,
            self.canvas.width / 10,
            self.canvas.height / 10,
            fill=True,
            color="red")

        self.canvas['TestText'] = RichText(
            "TEST",
            x=(-self.canvas.width / 3)+(self.canvas.width / 20),
            y=(self.canvas.height / 4)+(self.canvas.height / 20),
            color="black")

        self.canvas['OKBox'] = Rect(
            (self.canvas.width / 3),
            self.canvas.height / 4,
            -self.canvas.width / 10,
            self.canvas.height / 10,
            fill=True,
            color="green")

        self.canvas['OKText'] = RichText(
            "OK",
            x=(self.canvas.width / 3)-(self.canvas.width / 20),
            y=(self.canvas.height / 4)+(self.canvas.height / 20),
            color="black")

        self.canvas['ValuemA'] = RichText(
            str(round(0, 3)) + "mA",
            x=0,
            y=-(self.canvas.height / 4)+(self.canvas.height / 20),
            color="green")

        self.canvas['ValuePerc'] = RichText(
            "("+str(round(0)) + "%)",
            x=0,
            y=-(self.canvas.height / 4)+(self.canvas.height / 12),
            color="green")

        self.canvas['wait... '] = RichText(
            str(round(0)),
            x=0,
            y=-(self.canvas.height / 10)+(self.canvas.height / 2),
            color="black")

    def Calibrate_Run(self):
        slmouse = mouse(self.experiment, timeout=20, visible=True)
        slmouse.show_cursor(True)
        slmouse.set_pos(pos=(0, 0))
        xperc = 0
        self.canvas['Slider'].w = (xperc / 100) * (
            (2*self.canvas.width / 2.2) - 12)
        self.canvas.show()

        while True:  # Poll the mouse for buttonclicks
            button = None
            while button is None:
                button, position, timestamp = slmouse.get_click()

            button = None
            pos, mtime = slmouse.get_pos()
            x, y = pos

            if (x, y) in self.canvas['SliderBox']:
                xperc = min((x + self.canvas.width / 2.2) / (
                    2 * ((self.canvas.width / 2.2) - 6)) * 100.0, 100)
                self.canvas['Slider'].w = (xperc / 100)*(
                    (2 * self.canvas.width / 2.2) - 12)
                self.canvas['ValuePerc'].text = "(" + \
                    str(round(xperc, 1)) + "%)"
                self.canvas['ValuemA'].text = str(
                    round(5*(xperc / 100.0), 1)) + "mA"
                self.canvas.show()

            if (x, y) in self.canvas['TestBox']:
                if (self.var._deviceName == u"DUMMY"):
                    oslogger.info(
                        "In (Dummy) Tactile Stimulator: pulsing with value: {}"
                        .format(math.floor((xperc / 100.0) * 255)))
                else:
                    self.EE.PulseLines(math.floor((xperc / 100.0) * 255),
                                       self.var._pulseDuration)

                self.canvas['TestBox'].color = "blue"
                self.canvas.show()
                self.canvas['wait... '].color = "green"
                for n in range(1, self.var._interPulseHoldOffTime):
                    self.canvas['wait... '].text = "wait... " + str(
                        self.var._interPulseHoldOffTime - n)
                    self.canvas.show()
                    time.sleep(1)
                self.canvas['wait... '].color = "black"
                self.canvas['wait... '].text = "wait... " + str(0)
                self.canvas['TestBox'].color = "red"
                self.canvas.show()

            if (x, y) in self.canvas['OKBox']:
                self.experiment.set("tactstim_calibration_perc",
                                    round(xperc, 2))
                self.experiment.set("tactstim_calibration_value",
                                    math.floor(xperc * 255.0 / 100))
                self.experiment.set("tactstim_calibration_milliamp",
                                    round(5*(xperc / 100.0), 2))
                oslogger.info("In (Hardware) Tactile Stimulator: \
                              pulse intensity calibration value \
                              (raw, mA): {}, {:.2f}"
                              .format(self.experiment.get(
                                  "tactstim_calibration_value"),
                                  self.experiment.get(
                                      "tactstim_calibration_milliamp")))
                break

    def Do_Pulse_Prepare(self):
        try:
            self.experiment.get("tactstim_calibration_value")
        except Exception:
            oslogger.error("No calibration step taken: First run \
                           the Tactile Stimulator in calibration mode!")

        if not 0 <= self.var._percOfCalibrationValue <= 100:
            oslogger.error("Percentage input out of range!")
            self.var._percOfCalibrationValue = 0

        self.experiment.set(
            "tactstim_pulse_value",
            math.floor(self.var._percOfCalibrationValue *
                       self.experiment.get(
                           "tactstim_calibration_perc") * 255.0 / 10000))
        self.experiment.set(
            "tactstim_pulse_milliamp", round(
                self.var._percOfCalibrationValue *
                self.experiment.get(
                    "tactstim_calibration_perc") * 5.0 / 10000, 2))
        oslogger.info("In (Hardware) Tactile Stimulator: \
                      prepared to pulse with value \
                      (raw, mA): {}, {:.2f}".
                      format(self.experiment.get(
                          "tactstim_pulse_value"),
                          self.experiment.get(
                              "tactstim_pulse_milliamp")))

    def Do_Pulse_Run(self):
        if (self.var._deviceName == u"DUMMY"):
            oslogger.info("In (Dummy) Tactile Stimulator: \
                          pulse with value: " + str(
                              self.var._percOfCalibrationValue))
        else:
            try:
                timeLastPulse = self.experiment.get(
                    "tactstim_time_last_pulse")
            except Exception:
                timeLastPulse = 0
            td = time.time() - timeLastPulse
            """
            oslogger.info("Time duration inbetween pulses: " + str(td))
            """
            if (td > self.var._pulseTimeOut):
                """
                This if statement is to prevent the possibility
                to pulse if the previous stimulus was less then
                the minimum time ago
                """
                self.EE.PulseLines(self.experiment.get(
                    "tactstim_pulse_value"), self.var._pulseDuration)
                oslogger.info("Pulse now!")
            else:
                oslogger.warning("In (Hardware) Tactile Stimulator: \
                                 the next pulse came too early. \
                                 Please don't pulse in rapid succession!")
        self.experiment.set(
            "tactstim_time_last_pulse",
            time.time())  # update the time stamp of the last call


class qttactile_stimulator(TactileStimulator, QtAutoPlugin):
    def __init__(self, name, experiment, script=None):

        TactileStimulator.__init__(self,
                                   name,
                                   experiment,
                                   script)
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
        # QtAutoPlugin.init_edit_widget(self)
        EE = EvtExchanger()
        listOfDevices = EE.Attached(u"SHOCKER")

        """
        If there is no Tactile Stimulator attached,
        the selected name defaults to 'DUMMY' again.
        """
        if listOfDevices:
            for i in listOfDevices:
                self.deviceName_widget.addItem(i)
        else:
            self.var._deviceName = u"DUMMY"

        self.duration_widget.setEnabled(True)
        self.value_widget.returnPressed.connect(self.perc_check)
        self.value_widget.returnPressed.connect(self.duration_check)
        self.calibrate_widget.currentTextChanged.connect(self.type_check)
        self.value_widget.setEnabled(
            self.calibrate_widget.currentText() == u'Stimulate')
