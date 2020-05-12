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
from openexp.keyboard import Keyboard

from libopensesame import item
from libopensesame.base_response_item import base_response_item
from libqtopensesame.items.qtautoplugin import qtautoplugin
import os
import sys

from pyEVT import EvtExchanger

class ResponseBox(item.item):

	"""
		This class (the class with the same name as the module)
		handles the basic functionality of the item. It does
		not deal with GUI stuff.
	"""


	description = u"Aquires buttonpress-responses and/or digital events\r\n" \
		" from EventExchanger-based digital input device. "

	def reset(self):

		# Set the default values of the plug-in items in the GUI.
		self.var._ProductName		 = u'DUMMY'
		self.var._CorrectButton		 = u''
		self.var._AllowedButtons	 = u'1;2;3;4'
		self.var._ResponseTimeout	 = u'infinite'


	def prepare(self):

		item.item.prepare(self)

		self.ELister = EvtExchanger()
		Devices = self.ELister.Device().Select(self.var._ProductName)
		if len(Devices) == 0:
			self.var._ProductName		 = u'DUMMY'
			self.ResponseBox = Keyboard(self.experiment);
			print("Cannot find ResponseBox: Using Keyboard")
		else:
			self.ResponseBox = self.ELister.Device()
			self.ResponseBox.Start()

		if not type(self.var._ResponseTimeout) == int:
			self.var._ResponseTimeout = -1

		self.var.AllowedEventLines = 0
		AllowedList = self.var._AllowedButtons.split(";")
		for x in AllowedList:
			self.var.AllowedEventLines +=  (1 << (int(x,10) -1))

	def run(self):
		
		# Save the current time ...
		t0 = self.set_item_onset()
		# Call the 'wait for event' function in the EventExchanger C# object.

		if 	self.var._ProductName != u'DUMMY':
			(self.var.Response,self.var.RT) = \
				(self.ResponseBox.WaitForDigEvents(self.var.AllowedEventLines,
							self.var._ResponseTimeout)) 
			self.ResponseBox.Start()
		else:
			# demo mode: keyboard response.....
			self.var.Response, self.var.RT= self._Keyboard.get_key(timeout=self.var._ResponseTimeout)

		self.CorrectResponse = \
			(self.var.Response == self.var._CorrectButton)
		# Add all response related data to the Opensesame responses instance.
		self.experiment.responses.add(response_time=self.var.RT, \
								correct=self.CorrectResponse, \
								response=self.var.Response, \
								item=self.name)
		#Report success		
		return True


class qtResponseBox(ResponseBox, qtautoplugin):


	def __init__(self, name, experiment, string = None):

		#Pass the word on to the parents
		ResponseBox.__init__(self, name, experiment, string)
		qtautoplugin.__init__(self, __file__)


	def init_edit_widget(self):

	# Pass the word on to the parent
		qtautoplugin.init_edit_widget(self)

		ELister = EvtExchanger()
		listofdevices = ELister.Device().Attached()
		for i in listofdevices:
			self.ProductName_widget.addItem(i)

