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

from pyevt import EvtExchanger
from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.oslogging import oslogger


class EvtTrigger(Item):

    description = u"A plug-in for generating triggers with EVT devices."

    """Reset plug-in to initial values."""
    def reset(self):
        self.var.value = 0
        self.var.duration = 1000
        self.var.device = u'DUMMY'
        self.var.outputmode = u'Pulse output lines'

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def prepare(self):
        super().prepare()
        self.var.value = self.clamp(self.var.value, 0, 255)
        self.experiment.var._outputValue = 0

        # Dynamically load an EventExchanger RSP device
        if not hasattr(self, u'EventExchanger'):
            self.myevt = EvtExchanger()
            try:
                self.myevt.Select(self.var.device)
                self.myevt.SetLines(0)
                #oslogger.info("Connecting and resetting EVT device.")
                oslogger.debug("Connecting and resetting EVT device.")
            except:
                self.var.device = u'DUMMY'
                #oslogger.info("Connecting to EVT device failed! Switching to dummy mode.")
                oslogger.debug("Connecting to EVT device failed! Switching to the dummy mode.")
                

    def run(self):
        self.set_item_onset()
        if self.var.device == u'DUMMY':
            if self.var.outputmode == u'Write output lines':
                self.experiment.var._outputValue = self.var.value # Store as global.
                oslogger.info('dummy: send byte code {}'.format(self.var.value))
            elif self.var.outputmode == u'Pulse output lines':
                oslogger.info('dummy: send byte code {} for the duration of {} ms'.format(
                    self.experiment.var._outputValue ^ self.var.value, self.var.duration))
            elif self.var.outputmode == u'Reset output lines':
                oslogger.info('dummy: send byte code {}'.format(0))
            elif self.var.outputmode == u'Invert output lines':
                self.experiment.var._outputValue ^= self.var.value
                oslogger.info('dummy: send byte code {}'.format(self.experiment.var._outputValue))
        else:
            if self.var.outputmode == u'Write output lines':
                self.myevt.SetLines(self.var.value)
                self.experiment.var._outputValue = self.var.value # Store as global. There is no output read-back from the hardware.
                oslogger.info('evt: send byte code {}'.format(self.var.value))
            elif self.var.outputmode == u'Pulse output lines':
                self.myevt.PulseLines((self.experiment.var._outputValue ^ self.var.value), self.var.duration)
                oslogger.info('evt: send byte code {} for the duration of {} ms'.format(
                    self.experiment.var._outputValue ^ self.var.value, self.var.duration))
            elif self.var.outputmode == u'Reset output lines':
                oslogger.info('evt: send byte code {}'.format(0))
                self.myevt.SetLines(0)
                self.experiment.var._outputValue = 0
            elif self.var.outputmode == u'Invert output lines':
                self.experiment.var._outputValue ^= self.var.value
                self.myevt.SetLines(self.experiment.var._outputValue)
                oslogger.info('evt: send byte code {}'.format(self.experiment.var._outputValue))
        return True


class QtEvtTrigger(EvtTrigger, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        # We don't need to do anything here, except call the parent
        # constructors. Since the parent constructures take different arguments
        # we cannot use super().
        EvtTrigger.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()

        myevt = EvtExchanger()
        listOfDevices = myevt.Attached(u"EventExchanger-EVT")
        if listOfDevices:
            for i in listOfDevices:
                self.device_combobox.addItem(i)
        else:
            self.var.device = u'DUMMY'   
        self.output_mode_combobox.currentIndexChanged.connect(self.update_line_edit_state)
    
    def update_line_edit_state(self):
        # Get the current text or index from the combobox
        current_selection = self.output_mode_combobox.currentText()  # or use currentIndex() for the index

        # Enable or disable the line_edit based on the selection
        if current_selection == 'Write output lines':
            self.byte_value_line_edit.setEnabled(True)
            self.duration_line_edit.setEnabled(False)
        elif current_selection == 'Reset output lines':
            self.byte_value_line_edit.setEnabled(False)
            self.duration_line_edit.setEnabled(False)
        elif current_selection == 'Invert output lines':
            self.byte_value_line_edit.setEnabled(True)
            self.duration_line_edit.setEnabled(False)
        elif current_selection == 'Pulse output lines':
            self.byte_value_line_edit.setEnabled(True)
            self.duration_line_edit.setEnabled(True)
        else:
            self.byte_value_line_edit.setEnabled(False)
            self.duration_line_edit.setEnabled(False)
