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
from libopensesame.oslogging import oslogger
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.py3compat import *
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

import os
import time
import math
import sys

from pyEVT import EvtExchanger

class TactileStimulator(item.item):

	description = u"Allows the calibration *and* the use of the Tactile Stimulator."

	def reset(self):
		self.var._percOfCalibrationValue = 0
		self.var._shockDuration = 150 # fixed value
		self.var._shockTimeOut = 1.0 # fixed value
		self.var._interShockHoldOffTime = 8 # fixed value
		self.var._deviceName = u"DUMMY"
		self.var._mode = u"Calibrate"

				
	def prepare(self):
		self.experiment.set("shocker_shock_duration_ms", self.var._shockDuration)
		item.item.prepare(self)
		self.EE = EvtExchanger()
		Device = self.EE.Select(self.var._deviceName)

		try:
			if Device is None:
				raise
		except:
			self.var._deviceName = u"DUMMY"
			oslogger.warning("Did not find a Tactile Stimulator: code to debugwindow")
			
		if self.var._mode == u"Calibrate":
			self.Calibrate_Prepare()
		elif self.var._mode == u"Shock":
			self.Do_Shock_Prepare()

			
	def run(self):
		self.set_item_onset()
		if 	self.var._deviceName == u"DUMMY":
			if self.var._mode == u"Shock":
				oslogger.info('dummy shock: {} for the duration of {} ms'.format(self.var._percOfCalibrationValue, self.var._shockDuration) )
			else:
				self.Calibrate_Run()			
		else:
			#self.EE.Select(self.PATH)
			if self.var._mode == u"Calibrate":
				self.Calibrate_Run()
			elif self.var._mode == u"Shock":
				self.Do_Shock_Run()
		return True


	def Calibrate_Prepare(self):
		if not (self.var._deviceName == u"DUMMY"):
			self.EE.SetLines(0)
			oslogger.info("In (Hardware) Shock: reset port")
		
		self.canvas = Canvas(self.experiment)
		self.canvas.set_bgcolor("black")
		self.canvas.clear()
        
		self.canvas['Title'] = RichText("Tactile Stimulator Calibration",	
						center = True , 
						x = 0 ,
						y = -int(self.canvas.height/3) , 
						color = "white" , 
						font_family = "mono", 
						font_size = 28)

		self.canvas['Instruction'] = RichText("Point at the desired value position"\
						" on the axis and click ... "\
						"Then click TEST",\
						center = True, 
						x = 0,
						y = -int(self.canvas.height / 8), 
						color = "white")
		# Draw the slider axis

		self.canvas.set_fgcolor("white")
		self.canvas['SliderBox'] = Rect(-self.canvas.width / 2.2,
					 	0,
					 	2 * self.canvas.width / 2.2,
					 	28,
					 	fill=False)

		self.canvas.set_fgcolor("white")
		self.canvas['Slider'] = Rect((-self.canvas.width / 2.2) + 6,
						 6,
						 (2 * self.canvas.width / 2.2) - 12,
						 16,
						 fill=True)
						 
		self.canvas['TestBox'] = Rect((-self.canvas.width / 3),
						 self.canvas.height / 4,
						 self.canvas.width  / 10,
						 self.canvas.height / 10,
						 fill=True,
						 color = "red")
						 
		self.canvas['TestText'] = RichText("TEST", 
						x=(-self.canvas.width / 3)+(self.canvas.width / 20),
						y=(self.canvas.height / 4)+(self.canvas.height / 20),
						color = "black")
		
		self.canvas['OKBox'] = Rect((self.canvas.width / 3),
						 self.canvas.height / 4,
						 -self.canvas.width / 10,
						 self.canvas.height / 10,
						 fill=True,
						 color = "green")
						 
		self.canvas['OKText'] = RichText("OK", 
						x=(self.canvas.width / 3)-(self.canvas.width / 20),
						y=(self.canvas.height / 4)+(self.canvas.height / 20),
						color = "black")
		
		self.canvas['ValuemA'] = RichText(str(round(0,3)) + "mA", 
						x=0,
						y=-(self.canvas.height / 4)+(self.canvas.height / 20),
						color = "green")
						
		self.canvas['ValuePerc'] = RichText("("+str(round(0)) + "%)", 
						x=0,
						y=-(self.canvas.height / 4)+(self.canvas.height / 12),
						color = "green")
		
		self.canvas['wait... '] = RichText(str(round(0)), 
						x=0,
						y=-(self.canvas.height / 10)+(self.canvas.height / 2),
						color = "black")


	def Calibrate_Run(self):
		slmouse = mouse(self.experiment, timeout=20, visible=True)
		slmouse.show_cursor(True)
		slmouse.set_pos(pos=(0,0))
		xperc = 0;
		self.canvas['Slider'].w = (xperc / 100) * ((2 * self.canvas.width / 2.2) - 12)
		self.canvas.show()	
		
		while True:
		# Poll the mouse for buttonclicks
			button = None
			while button == None:
				button, position, timestamp = slmouse.get_click()

			button = None
			pos, mtime = slmouse.get_pos()
			x, y = pos
			
			if (x, y) in self.canvas['SliderBox']:				
				xperc = min((x + self.canvas.width / 2.2) / (2 * ((self.canvas.width / 2.2) - 6)) * 100.0, 100)
				self.canvas['Slider'].w = (xperc / 100) * ((2 * self.canvas.width / 2.2) - 12)
				self.canvas['ValuePerc'].text = "(" + str(round(xperc, 1)) + "%)"
				self.canvas['ValuemA'].text = str( round(5*(xperc/100.0), 1) ) + "mA"
				self.canvas.show()	

			if (x, y) in self.canvas['TestBox']:
				if (self.var._deviceName == u"DUMMY"):
					oslogger.info("In (Dummy) Shock: shocking with value: {}".format(math.floor( (xperc/100.0) * 255) ) )
				else:
					self.EE.PulseLines(math.floor( (xperc/100.0) * 255 ), self.var._shockDuration)
				
				self.canvas['TestBox'].color = "blue"
				self.canvas.show()
				
				self.canvas['wait... '].color = "green"
				for n in range (1, self.var._interShockHoldOffTime):
					self.canvas['wait... '].text = "wait... " + str(self.var._interShockHoldOffTime-n)
					self.canvas.show()
					time.sleep(1)
				self.canvas['wait... '].color = "black"
				self.canvas['wait... '].text = "wait... " + str(0)
				
				self.canvas['TestBox'].color = "red"
				self.canvas.show()	
				
			if (x, y) in self.canvas['OKBox']:
				self.experiment.set( "shocker_calibration_perc", round(xperc, 2) )
				self.experiment.set( "shocker_calibration_value", math.floor( xperc*255.0/100 ) )
				self.experiment.set( "shocker_calibration_milliamp", round(5*(xperc/100.0), 2) )
				oslogger.info("In (Hardware) Shock: shocker calibration value (raw, mA): {}, {:.2f}".format(self.experiment.get("shocker_calibration_value"), self.experiment.get("shocker_calibration_milliamp")))
				break


	def Do_Shock_Prepare(self):
			self.experiment.set( "shocker_shock_value", math.floor(self.var._percOfCalibrationValue * self.experiment.get("shocker_calibration_perc") * 255.0/10000) )
			self.experiment.set( "shocker_shock_milliamp", round( self.var._percOfCalibrationValue * self.experiment.get("shocker_calibration_perc") * 5.0/10000, 2) )
			oslogger.info("In (Hardware) Shock: prepared to shock with value (raw, mA): {}, {:.2f}".format(self.experiment.get("shocker_shock_value"), self.experiment.get("shocker_shock_milliamp")))


	def Do_Shock_Run(self):
		try:
			self.experiment.get("shocker_calibration_value")
		except:
			oslogger.error("No calibration step taken: First run the Tactile Stimulator in calibration mode!")
			return
		
		if (self.var._deviceName == u"DUMMY"):
			oslogger.info("In (Dummy) Shock: shocking with value: " + str(self.var._percOfCalibrationValue))
		else:
			try:
				timeLastShock = self.experiment.get("shocker_time_last_shock")
			except:
				timeLastShock = 0;
				
			td = time.time() - timeLastShock
			#oslogger.info("Time duration inbetween shocks: " + str(td))
			# This line is to prevent the possibility to shock if the previous shock was less then the minimum time ago
			if (td > self.var._shockTimeOut):
				self.EE.PulseLines(self.experiment.get("shocker_shock_value"), self.var._shockDuration)
				oslogger.info("Shock now!")
			else:
				oslogger.warning("In (Hardware) Shock: the shock came too early. Please don't give shocks in rapid succession!")
			
		self.experiment.set("shocker_time_last_shock", time.time()) # update the time stamp of the last call
			
	
class qtTactileStimulator(TactileStimulator, qtautoplugin):
	def __init__(self, name, experiment, string = None):

		#Pass the word on to the parents
		TactileStimulator.__init__(self, name, experiment, string)
		qtautoplugin.__init__(self, __file__)

	def perc_check(self):
		try:
			val = int(self.value_widget.text())
			val = min(max(val,0),100)
		except:
			val = 0
			
		self.value_widget.setText(str(val))
		 
	def type_check(self):
		self.value_widget.setEnabled(self.calibrate_widget.currentText() == u'Shock')
	
	def init_edit_widget(self):
	# Pass the word on to the parent
		qtautoplugin.init_edit_widget(self)

		EE = EvtExchanger()
		listOfDevices = EE.Attached(u"SHOCKER")
		# if there is no shocker attached, the selected name defaults to 'Dummy' again.
		if listOfDevices:
			for i in listOfDevices:
				self.deviceName_widget.addItem(i)
		else:
			self.var._deviceName = u"DUMMY"
		
		self.duration_widget.setEnabled(False) # fixed value for shock duration, indicator only
		self.value_widget.returnPressed.connect(self.perc_check)
		self.calibrate_widget.currentTextChanged.connect(self.type_check)
		self.value_widget.setEnabled(self.calibrate_widget.currentText() == u'Shock')
