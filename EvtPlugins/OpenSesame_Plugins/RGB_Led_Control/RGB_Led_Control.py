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
from libqtopensesame.items.qtautoplugin import qtautoplugin
import os
import sys
import time

from pyEVT import EvtExchanger


class RGB_Led_Control(item.item):

	"""
		This class (the class with the same name as the module)
		handles the basic functionality of the item. It does
		not deal with GUI stuff.
	"""


	description = u"Sets and/or sends RGB led data from\r\n" \
			"EventExchanger-based digital input/output device."

	def reset(self):

		# Set the default values of the plug-in items in the GUI.
		self.var._ProductName		 = u'DUMMY'
		self.var._CorrectButton		 = u'1'
		self.var._AllowedButtons	 = u'1;2;3'
		self.var._ResponseTimeout	 = u'infinite'

		self.var._Button1_Led_Color    = "#000000"
		self.var._Button2_Led_Color    = "#000000"
		self.var._Button3_Led_Color    = "#000000"
		self.var._Button4_Led_Color    = "#000000"

		self.var.ResetAfter 				  = 500;
		self.var.Feedback 					  = u'yes'
		self.var.CorrectColor  			  = "#00FF00"
		self.var.InCorrectColor  			  = "#FF0000"
		
	def prepare(self):

		item.item.prepare(self)

		self.ELister = EvtExchanger()
		Devices = self.ELister.Device().Select(self.var._ProductName)
		if len(Devices) == 0:
			self.var._ProductName = u'DUMMY'
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

		hexprepend = "0x"
		self.colors = [hexprepend + self.var._Button1_Led_Color[1:], \
							hexprepend + self.var._Button2_Led_Color[1:], \
							hexprepend + self.var._Button3_Led_Color[1:], \
							hexprepend + self.var._Button4_Led_Color[1:]]
		
		self.CorrectColor = hexprepend + self.var.CorrectColor[1:]
		self.InCorrectColor = hexprepend + self.var.InCorrectColor[1:]
		CC=int(self.CorrectColor,16)
		IC=int(self.InCorrectColor,16)
		
		BLC = [0,0,0,0]
		for b in range(4):
			BLC[b] = int(self.colors[b] , 16)			
		
		if self.var._ProductName != u'DUMMY':
			for b in range(4):
				self.ResponseBox.SetLedColor( \
					((BLC[b] >> 16) & 0xFF), \
					((BLC[b] >> 8) & 0xFF), \
					(BLC[b] & 0xFF), \
					b+1, 1)
		
			if self.var.Feedback == u'yes':
				for b in range(4):
					self.ResponseBox.SetLedColor( \
						((IC >> 16) & 0xFF), \
						((IC >> 8) & 0xFF), \
						(IC & 0xFF), \
						b+1, b+11)
		
				self.ResponseBox.SetLedColor( \
					((CC >> 16) & 0xFF), \
					((CC >> 8) & 0xFF), \
					(CC & 0xFF), \
					int(self.var._CorrectButton), int(self.var._CorrectButton)+10)
		
			# Call the 'wait for event' function in the EventExchanger C# object.

			(self.var.Response,self.var.RT) = \
				(self.ResponseBox.WaitForDigEvents(self.var.AllowedEventLines,
							self.var._ResponseTimeout)) 

			#FEEDBACK:
			if self.var.Feedback == u'yes':
				time.sleep(self.var.ResetAfter/1000.0)
				for b in range(4):
					self.ResponseBox.SetLedColor(0,0,0,b+1,1)
		else:
			# demo mode: keyboard response.....
			if self.var._ResponseTimeout==-1:
				self.var._ResponseTimeout = None
			self.var.Response, self.var.RT= self.ResponseBox.get_key(timeout=self.var._ResponseTimeout)

		#HOUSEHOLD:
		self.CorrectResponse = \
			(self.var.Response == self.var._CorrectButton)
		# Add all response related data to the Opensesame responses instance.
		self.experiment.responses.add(response_time=self.var.RT, \
								correct=self.CorrectResponse, \
								response=self.var.Response, \
								item=self.name)
		#Report success		
		return True

class qtRGB_Led_Control(RGB_Led_Control, qtautoplugin):
	def __init__(self, name, experiment, string = None):

		#Pass the word on to the parents
		RGB_Led_Control.__init__(self, name, experiment, string)
		qtautoplugin.__init__(self, __file__)


	def init_edit_widget(self):

	# Pass the word on to the parent
		qtautoplugin.init_edit_widget(self)
		ELister = EvtExchanger()
		listofdevices = ELister.Device().Attached()
		for i in listofdevices:
			self.ProductName_widget.addItem(i)

