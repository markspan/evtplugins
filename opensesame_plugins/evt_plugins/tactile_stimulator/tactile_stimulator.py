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

from time import (time, sleep)
import math
from pyevt import EventExchanger
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

# constants
# Set u'EventExchanger-EVT' to emulate SHOCKER with EVT-x
_DEVICE_GROUP = u'SHOCKER'
#_DEVICE_GROUP = u'EventExchanger-EVT'

# global var
open_devices = {} # Store open device handles.

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
        self.var.close_device = 'no'

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        super().prepare()

        self.experiment.var.tactstim_pulse_duration_value_ms = self.var.pulse_duration_value
        self.experiment.var.tactstim_pulse_value = 0

        if self.var.device == u'DUMMY':
            oslogger.warning("Hardware configuration could have changed! Dummy prepare...")
        elif len(open_devices) == 0:
            # Create a shadow device list to find 'path' from the current selected device.
            # 'path' is an unique device ID.
            temp_evt = EventExchanger()
            sleep(1) # without a delay, the list will not always be complete.
            try:
                device_list = temp_evt.scan(_DEVICE_GROUP) # filter on allowed EVT types
                del temp_evt
                # oslogger.info("device list: {}".format(device_list))
                for d in device_list:
                    sleep(1) # without a delays, the device will not always be there.
                    composed_string = d['product_string'] + " s/n: " + d['serial_number']
                    open_devices[composed_string] = EventExchanger()
                    # Get evt device handle:
                    open_devices[composed_string].attach_id(d['path'])
                    oslogger.info('Device successfully attached as: {} s/n: {}'.format(
                        d['product_string'], d['serial_number']))
                    oslogger.info('        ...  and with device ID: {}'.format(
                        open_devices[composed_string]))
            except:
                oslogger.warning("Connecting the Tactile-stimulator failed! Device set to dummy.")
                self.var.device = u'DUMMY'

        # searching for selected device:
        self.current_device = None
        for dkey in open_devices:
            if self.var.device[:15] in dkey:
                self.current_device = dkey # assign to value that belongs to the key.
        if self.current_device is None:
            oslogger.warning("Tactile-stimulator not found! Device set to dummy.")
            self.var.device = u'DUMMY'
        else:
            oslogger.info('Preparing device: {}'.format(self.current_device))
            open_devices[self.current_device].write_lines(0) # clear lines

        # pass device var to experiment as global:
        var_name = "self.experiment.var.connected_device_" + self.name
        exec(f'{var_name} = "{self.var.device}"')

        if self.var.mode == u"Calibrate":
            self.calibrate_prepare()
        elif self.var.mode == u"Stimulate":
            self.stimulate_prepare()

    def calibrate_prepare(self):
        if not (self.var.device == u"DUMMY"):
            open_devices[self.current_device].write_lines(0) # clear lines
            oslogger.info("Reset Tactile-stimulator.")

        self.c = Canvas(self.experiment)
        self.c.background_color=u'black'
        # self.c.clear()
        self.c['Title'] = RichText(
            "Tactile Stimulator Calibration",
            center=True,
            x=0,
            y=-int(self.c.height / 3) + (self.c.height / 20),
            color='white',
            font_family='mono',
            font_size=28
        )
        self.c['Instruction'] = RichText(
            "Point at the desired value on the"
            "\nscale and click the mouse button."
            "\nClick TEST to apply a pulse to the subject or"
            "\nclick OK to accept the set intensity.",
            center=True,
            x=0,
            y=-int(self.c.height / 8) + (self.c.height / 20),
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

        # close the device?
        if self.var.close_device == 'yes':
            for dkey in open_devices:
                try:
                    open_devices[dkey].close()
                    oslogger.info('Device: {} successfully closed!'.format(open_devices[dkey]))
                except:
                    oslogger.warning('Device {} for closing not found!'.format(open_devices[dkey]))

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
                    open_devices[self.current_device].pulse_lines(math.floor((xperc / 100.0) * self.PULSE_VALUE_MAX),
                                       self.var.pulse_duration_value)
                self.c['Test_Box'].color = 'blue'
                self.c.show()
                self.c['wait'].color = 'green'

                for n in range(1, self.var._inter_pulse_holdoff):
                    self.c['wait'].text = "wait... " + str(self.var._inter_pulse_holdoff - n)
                    self.c['wait'].color = 'green'
                    self.c.show()
                    sleep(1)
                    self.c['wait'].color = 'black'
                self.c['wait'].text = "wait... " + str(0)
                self.c['Test_Box'].color = 'red'
                self.c.show()

            if (x, y) in self.c['OK_Box']:
                self.experiment.var.tactstim_calibration_perc = round(xperc, 2)
                self.experiment.var.tactstim_calibration_value = math.floor(xperc * self.PULSE_VALUE_MAX / 100)
                self.experiment.var.tactstim_calibration_milliamp = round(5*(xperc / 100.0), 2)
                oslogger.info("The set pulse intensity value is "
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
            td = time() - timeLastPulse
            # oslogger.info("Time duration between pulses: " + str(td))
            
            if (td > self.var._pulse_timeout):
                """
                This if statement is to prevent the possibility
                to pulse if the previous stimulus was less then
                the minimum interval time ago
                """
                self.experiment.var.tactstim_pulse_value = math.floor(
                    self.var.perc_calibr_value * \
                        self.experiment.var.tactstim_calibration_perc * self.PULSE_VALUE_MAX / 10000)
                self.experiment.var.tactstim_pulse_milliamp = round(
                    self.var.perc_calibr_value * \
                        self.experiment.var.tactstim_calibration_perc * 5.0 / 10000, 2)

                open_devices[self.current_device].pulse_lines(self.experiment.var.tactstim_pulse_value, self.var.pulse_duration_value)
                oslogger.info("Device {} now pulsing at "
                              "(raw, mA): {}, {:.2f}".
                              format(open_devices[self.current_device],
                                  self.experiment.var.tactstim_pulse_value,
                                  self.experiment.var.tactstim_pulse_milliamp))
            else:
                oslogger.warning("In (Hardware) Tactile Stimulator: "
                                 "the next pulse came too early. "
                                 "Please don't pulse in rapid succession!")
        self.experiment.var.tactstim_time_last_pulse = time()  # update the time stamp of the last call


class QtTactileStimulator(TactileStimulator, QtAutoPlugin):

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
        TactileStimulator.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):

        """Constructs the GUI controls. Usually, you can omit this function
        altogether, but if you want to implement more advanced functionality,
        such as controls that are grayed out under certain conditions, you need
        to implement this here.
        """

        super().init_edit_widget()

        self.refresh_checkbox_widget.setChecked(False)
        self.update_combobox_mode()
        self.combobox_add_devices() # first time fill the combobox

        # event based calls:
        self.mode_combobox_widget.currentIndexChanged.connect(self.update_combobox_mode)
        self.refresh_checkbox_widget.stateChanged.connect(self.refresh_combobox_device)
        self.device_combobox_widget.currentIndexChanged.connect(self.update_combobox_device)
        self.perc_line_edit_widget.textChanged.connect(self.check_input_perc)
        self.duration_line_edit_widget.textChanged.connect(self.check_input_duration)
        self.close_device_checkbox_widget.stateChanged.connect(self.close_device)

    def update_combobox_mode(self):
        # Get the current text or index from the combobox
        current_selection = self.mode_combobox_widget.currentText()  # or use currentIndex() for the index
        # Enable or disable the line_edit based on the combobox selection
        if current_selection == 'Calibrate':
            self.perc_line_edit_widget.setEnabled(False)
            self.duration_line_edit_widget.setEnabled(True)
        elif current_selection == 'Stimulate':
            self.perc_line_edit_widget.setEnabled(True)
            self.duration_line_edit_widget.setEnabled(True)
        else:
            self.perc_line_edit_widget.setEnabled(False)
            self.duration_line_edit_widget.setEnabled(False)

    def refresh_combobox_device(self):
        if self.refresh_checkbox_widget.isChecked():
            # renew list:
            self.combobox_add_devices()

    def update_combobox_device(self):
        self.refresh_checkbox_widget.setChecked(False)

    def check_input_perc(self, text):
        try:
            self.var.perc_calibr_value = int(text)
            if not 0 <= self.var.perc_calibr_value <= 100:
                raise ValueError
        except ValueError:
            # Handle invalid input or out of range value
            self.perc_line_edit_widget.blockSignals(True)
            self.perc_line_edit_widget.setText('')
            self.perc_line_edit_widget.blockSignals(False)

    def check_input_duration(self, text):
        try:
            self.var.pulse_duration_value = int(text)
            if not 1 <= self.var.pulse_duration_value <= 2000:
                raise ValueError
        except ValueError:
            # Handle invalid input or out of range value
            self.duration_line_edit_widget.blockSignals(True)
            self.duration_line_edit_widget.setText('')
            self.duration_line_edit_widget.blockSignals(False)

    def combobox_add_devices(self):
        self.device_combobox_widget.clear()
        self.device_combobox_widget.addItem(u'DUMMY', userData=None)
        
        # Create the EVT device list
        sleep(1) # delay after possible init of a previous instance of this plugin. 
        myevt = EventExchanger()
        try:
            device_list = myevt.scan(_DEVICE_GROUP) # filter on allowed EVT types
            del myevt
        except:
            device_list = {}
        
        try:
            previous_device_found = False
            for d in device_list:
                product_string = d['product_string']
                serial_string = d['serial_number']
                composed_string = product_string[15:] + " s/n: " + serial_string
                # add device id to combobox:
                self.device_combobox_widget.addItem(composed_string)
                # previous used device present?
                if self.var.device[:15] in product_string:
                    self.var.device = composed_string
                    previous_device_found = True       
        except:
            self.var.device = u'DUMMY'
            oslogger.warning("No devices found! Switching to dummy.")

        if previous_device_found is False:
            self.var.device = u'DUMMY'
            oslogger.warning("The hardware configuration has been changed since the last run! Switching to dummy.")

    def close_device(self):
        if self.close_device_checkbox_widget.isChecked():
            self.var.close_device = 'yes'
        else:
            self.var.close_device = 'no'