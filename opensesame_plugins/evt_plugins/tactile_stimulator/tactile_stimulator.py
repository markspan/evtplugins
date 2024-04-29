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

EVT_UMU = False # Set True to emulate SHOCKER with EVT-x

class TactileStimulator(Item):
    """Python module for handling the Tactile Stimulator."""

    description = u"Plugin for the calibration and the usage of the Tactile Stimulator."

    PULSE_VALUE_MAX = 254.0  # some models of the SHK1-1B do accept 255 as the max intensity and others 254 (...)

    def reset(self):
        """Resets plug-in to initial values."""
        self.var.perc_calibr_value = 0
        self.var.pulse_duration_value = 150  # default value
        self.var.device = u"DUMMY"
        self.var.mode = u"Calibrate"
        self.var._pulse_timeout = 1.0
        self.var._inter_pulse_holdoff = 8

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        super().prepare()
        self.experiment.var.tactstim_pulse_duration_value_ms = self.var.pulse_duration_value
        self.experiment.var.tactstim_pulse_value = 0
        if self.var.device != u'DUMMY':
            # Dynamically load an EVT device
            self.myevt = EvtExchanger()
            try:
                self.myevt.Select(self.var.device)
                self.myevt.SetLines(0)
                oslogger.info("Connecting and resetting the Tactile Stimulator.")
            except:
                self.var.device = u'DUMMY'
                oslogger.warning("Connecting the Tactile Stimulator device failed! Switching to dummy-mode.")
        if self.var.mode == u"Calibrate":
            self.calibrate_prepare()
        elif self.var.mode == u"Stimulate":
            self.stimulate_prepare()

    def calibrate_prepare(self):
        if not (self.var.device == u"DUMMY"):
            self.myevt.SetLines(0)
            oslogger.info("Reset Tactile Stimulator")

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
            "Point at the desired value "
            "on the bar and click the mouse button. "
            "Click TEST to apply a pulse to the subject. "
            "Click OK to accept the set intensity.",
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
            raise UserWarning("Not calibrated!")

    def run(self):
        """The run phase of the plug-in goes here."""
        self.set_item_onset()
        if self.var.device == u"DUMMY":
            if self.var.mode == u"Stimulate":
                oslogger.info('(Dummy) stimulate at {}% and duration of {}ms'
                              .format(self.var.perc_calibr_value,
                                      self.var.pulse_duration_value))
            else:
                self.calibrate()
        else:
            if self.var.mode == u"Calibrate":
                self.calibrate()
            elif self.var.mode == u"Stimulate":
                self.stimulate()
        return True

    def calibrate(self):
        slmouse = mouse(self.experiment, timeout=None, visible=True)
        slmouse.set_pos(pos=(0, 0))
        slmouse.show_cursor(True)
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
                if (self.var.device == u"DUMMY"):
                    oslogger.info(
                        "(Dummy) Tactile Stimulator pulsing intensity value: {}"
                        .format(math.floor((xperc / 100.0) * self.PULSE_VALUE_MAX)))
                else:
                    self.myevt.PulseLines(math.floor((xperc / 100.0) * self.PULSE_VALUE_MAX),
                                       self.var.pulse_duration_value)
                self.c['Test_Box'].color = 'blue'
                self.c.show()
                self.c['wait'].color = 'green'

                for n in range(1, self.var._inter_pulse_holdoff):
                    self.c['wait'].text = "wait... " + str(self.var._inter_pulse_holdoff - n)
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
                oslogger.info("(Dummy) The set pulse "
                              "intensity value is "
                              "(raw, mA): {}, {:.2f}".
                              format(self.experiment.var.tactstim_calibration_value,
                                     self.experiment.var.tactstim_calibration_milliamp))
                break

    def stimulate(self):
        if (self.var.device == u"DUMMY"):
            oslogger.info("(Dummy) Tactile Stimulator "
                          "pulsing at: " + \
                            str(self.var.perc_calibr_value) + \
                            "%")
        else:
            try:
                timeLastPulse = self.experiment.var.tactstim_time_last_pulse
            except Exception:
                timeLastPulse = 0
            td = time.time() - timeLastPulse
            # oslogger.info("Time duration between pulses: " + str(td))
            
            if (td > self.var._pulse_timeout):
                """
                This if statement is to prevent the possibility
                to pulse if the previous stimulus was less then
                the minimum time ago
                """
                self.experiment.var.tactstim_pulse_value = math.floor(
                    self.var.perc_calibr_value * \
                        self.experiment.var.tactstim_calibration_perc * self.PULSE_VALUE_MAX / 10000)
                self.experiment.var.tactstim_pulse_milliamp = round(
                    self.var.perc_calibr_value * \
                        self.experiment.var.tactstim_calibration_perc * 5.0 / 10000, 2)

                self.myevt.PulseLines(self.experiment.var.tactstim_pulse_value, self.var.pulse_duration_value)
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

    def init_edit_widget(self):
        super().init_edit_widget()
        self.update_combobox_mode()

        self.myevt = EvtExchanger()
        if EVT_UMU:
            listOfDevices = self.myevt.Attached(u"EventExchanger-EVT")
        else:
            listOfDevices = self.myevt.Attached(u"SHOCKER")
        if listOfDevices:
            for i in listOfDevices:
                self.device_combobox.addItem(i)
        # Prevents hangup if device is not found after reopening the project:
        if not self.var.device in listOfDevices: 
            self.var.device = u'DUMMY'

        # event based calls:
        self.mode_combobox.currentIndexChanged.connect(self.update_combobox_mode)
        self.refresh_checkbox.stateChanged.connect(self.refresh_comboboxdevice)
        self.device_combobox.currentIndexChanged.connect(self.update_comboboxdevice)
        self.perc_line_edit.textChanged.connect(self.check_input_perc)
        self.duration_line_edit.textChanged.connect(self.check_input_duration)

    def update_combobox_mode(self):
        # Get the current text or index from the combobox
        current_selection = self.mode_combobox.currentText()  # or use currentIndex() for the index
        # Enable or disable the line_edit based on the combobox selection
        if current_selection == 'Calibrate':
            self.perc_line_edit.setEnabled(False)
            self.duration_line_edit.setEnabled(True)
        elif current_selection == 'Stimulate':
            self.perc_line_edit.setEnabled(True)
            self.duration_line_edit.setEnabled(True)
        else:
            self.perc_line_edit.setEnabled(False)
            self.duration_line_edit.setEnabled(False)

    def refresh_comboboxdevice(self):
        if self.refresh_checkbox.isChecked():
            self.device_combobox.clear()
            # create new list:
            self.device_combobox.addItem(u'DUMMY', userData=None)
            if EVT_UMU:
                listOfDevices = self.myevt.Attached(u"EventExchanger-EVT")
            else:
                listOfDevices = self.myevt.Attached(u"SHOCKER")
            if listOfDevices:
                for i in listOfDevices:
                    self.device_combobox.addItem(i)

    def update_comboboxdevice(self):
        self.refresh_checkbox.setChecked(False)

    def check_input_perc(self, text):
        try:
            self.var.perc_calibr_value = int(text)
            if not 0 <= self.var.perc_calibr_value <= 100:
                raise ValueError
        except ValueError:
            # Handle invalid input or out of range value
            self.perc_line_edit.blockSignals(True)
            self.perc_line_edit.setText('')
            self.perc_line_edit.blockSignals(False)

    def check_input_duration(self, text):
        try:
            self.var.pulse_duration_value = int(text)
            if not 1 <= self.var.pulse_duration_value <= 2000:
                raise ValueError
        except ValueError:
            # Handle invalid input or out of range value
            self.duration_line_edit.blockSignals(True)
            self.duration_line_edit.setText('')
            self.duration_line_edit.blockSignals(False)