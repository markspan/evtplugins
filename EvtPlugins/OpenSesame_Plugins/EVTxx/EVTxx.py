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

from libopensesame import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.py3compat import *
import os
import sys

from pyEVT import EvtExchanger

class EVTxx(item.item):

	"""
		This class (the class with the same name as the module)
		handles the basic functionality of the item. It does
		not deal with GUI stuff.
	"""


	description = u"Allows setting or pulsing values of pins on the "  \
					"output port of various EventExchanger devices"

	def reset(self):
		self.var._value = 0
		self.var._duration = 500
		self.var._ProductName = u'DUMMY'
		self.var._OutputMode = u'Pulse Output Lines'


	def prepare(self):

		item.item.prepare(self)
		if not hasattr(self, u'EventExchanger'):
			self.ELister = EvtExchanger()
			Devices = self.ELister.Device().Select(self.var._ProductName)
			if len(Devices) == 0:
				self.EventExchanger = None
				self.var._ProductName = u'DUMMY'
				print("Cannot find eventexchanger: code to debugwindow")
			else:
				self.EventExchanger = self.ELister.Device()

			self.python_workspace[u'EventExchanger'] = self.EventExchanger
		#else:
			#self.EventExchanger = self.python_workspace[u'EventExchanger']
			
	def run(self):
		self.set_item_onset()
		if 	self.var._ProductName == u'DUMMY':
			print("code: %i for %i ms" % (self.var._value, self.var._duration) )
		else:
			if self.var._OutputMode == u'Set Output Lines':
				self.EventExchanger.SetLines(self.var._value)
			elif self.var._OutputMode == u'Pulse Output Lines':
				self.EventExchanger.SetLines(0)
				self.EventExchanger.PulseLines(self.var._value, self.var._duration)
	
		t0 = self.set_item_onset()
	
		return True

class qtEVTxx(EVTxx, qtautoplugin):
	def __init__(self, name, experiment, string = None):

		#Pass the word on to the parents
		EVTxx.__init__(self, name, experiment, string)
		qtautoplugin.__init__(self, __file__)

	def init_edit_widget(self):
	# Pass the word on to the parent
		qtautoplugin.init_edit_widget(self)

		ELister = EvtExchanger()
		listofdevices = ELister.Device().Attached()
		for i in listofdevices:
			self.ProductName_widget.addItem(i)




