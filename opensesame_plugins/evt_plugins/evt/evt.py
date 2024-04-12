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
from libopensesame.oslogging import oslogger
from libqtopensesame.items.qtautoplugin import QtAutoPlugin


class Evt(Item):

    description = u"Plugin for setting or pulsing the EVT output lines."

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
        # Dynamically load an EventExchanger RSP device
        if not hasattr(self.experiment, u'EventExchanger'):
            self.experiment.myevt = EvtExchanger()
            try:
                self.experiment.myevt.Select(self.var.device)
                oslogger.info("Connecting to EVT device.")
                #oslogger.debug("Connecting to EVT device.")
            except:
                oslogger.info("Connecting to EVT device failed! Switching to dummy mode.")
                #oslogger.debug("Connecting to EVT device failed!")
                self.var.device = u'DUMMY'

    def run(self):
        self.set_item_onset()
        if self.var.device == u'DUMMY':
            oslogger.info('dummy: send code {} for the duration of {} ms'.format(self.var.value, self.var.duration))
        else:
            if self.var.outputmode == u'Set output lines':
                self.experiment.myevt.SetLines(self.var.value)
            elif self.var.outputmode == u'Pulse output lines':
                self.experiment.myevt.SetLines(0)
                self.experiment.myevt.PulseLines(self.var.value, self.var.duration)
        return True


class QtEvt(Evt, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        # We don't need to do anything here, except call the parent
        # constructors. Since the parent constructures take different arguments
        # we cannot use super().
        Evt.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()

        myevt = EvtExchanger()
        listOfDevices = myevt.Attached(u"EventExchanger-EVT")
        if listOfDevices:
            for i in listOfDevices:
                self.device_widget.addItem(i)
        else:
            self.var.device = u'DUMMY'
