#-*- coding:utf-8 -*-

"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import Canvas, canvas
from libopensesame.oslogging import oslogger
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
from openexp.mouse import Mouse
from libopensesame.exceptions import osexception
import os
import sys
import numpy as np


from pyEVT import EvtExchanger


class VAS2(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'A Revised VAS modifier for a canvas'

	def reset(self):

		"""
		desc:
			Resets plug-in to initial values.
		"""

		# Here we provide default values for the variables that are specified
		# in info.json. If you do not provide default values, the plug-in will
		# work, but the variables will be undefined when they are not explicitly
		# set in the GUI.
		self.var.VAS_CANVAS_NAME			 	= u'VASSCREEN'
		self.var.VAS_BODY_NAME				 	= u'VASBODY'
		self.var.VAS_CURSOR_COLOR				= "#ffffff"
		self.var.VAS_EXITBUTTON_NAME			= u'VASEXIT'
		self.var.VAS_MAXLABEL_NAME			    = u'MAXLABEL'
		self.var.VAS_MINLABEL_NAME			    = u'MINLABEL'
		self.var.VAS_LINESIZE					= 10

		
	def prepare(self):

		"""The preparation phase of the plug-in goes here."""
		item.prepare(self)
		
		# Checking the excistence of the VAS elements is only possible in the runphase
		# as only then the full canvas is availeable
		
		self.c = Canvas(self.experiment)
		
		self.slmouse = Mouse(self.experiment, timeout=20, visible=True)
		self.slmouse.show_cursor(True)
		self.slmouse.set_pos(pos=(0,0))

		my_canvas = self.experiment.items[self.var.VAS_CANVAS_NAME].canvas
		
		try:
			if my_canvas[self.var.VAS_BODY_NAME] == None or my_canvas[self.var.VAS_EXITBUTTON_NAME] == None:
				oslogger.info("Should not occur")
		except Exception as e:
			raise osexception(u"Prepare: READ the VAS manual:\n\rNo VAS elements found on the named canvas")
		
		self.useLabels = True
		
		try:
			if my_canvas[self.var.VAS_MAXLABEL_NAME] == None or my_canvas[self.var.VAS_MAXLABEL_NAME] == None:
				oslogger.info("Should not occur")
		except Exception as e:
			self.uselabels = False
		
		self.c = self.experiment.items[self.var.VAS_CANVAS_NAME].canvas		
		self.ypos = -1
		# is the vasbody a line or a rect?
		if hasattr(self.c[self.var.VAS_BODY_NAME], 'ex') and hasattr(self.c[self.var.VAS_BODY_NAME], 'sx'):
			self.VASLENGTH = self.c[self.var.VAS_BODY_NAME].ex - self.c[self.var.VAS_BODY_NAME].sx
			self.ypos = (self.c[self.var.VAS_BODY_NAME].sy + self.c[self.var.VAS_BODY_NAME].ey) / 2
			self.sx = self.c[self.var.VAS_BODY_NAME].sx
		
		if hasattr(self.c[self.var.VAS_BODY_NAME], 'w') and hasattr(self.c[self.var.VAS_BODY_NAME], 'y') and hasattr(self.c[self.var.VAS_BODY_NAME], 'h'):
			self.VASLENGTH = self.c[self.var.VAS_BODY_NAME].w
			self.ypos = self.c[self.var.VAS_BODY_NAME].y+(self.c[self.var.VAS_BODY_NAME].h/2)
			self.sx = self.c[self.var.VAS_BODY_NAME].x
		
		if self.ypos == -1:
			raise TypeError("VasBody should be a line or a Rect")
		
		
	def run(self):
		self.set_item_onset(self.c.show())
		st = self.experiment.time()
		xpos = -1
		
		while(True):
		# Poll the mouse for buttonclicks
			button = None
			while button == None:
				button, position, timestamp = self.slmouse.get_click()

			button = None
			(x,y), mtime = self.slmouse.get_pos()
			
			if (x,y) in self.c[self.var.VAS_BODY_NAME]:
				# clicked on the line: either create the cursor, or move it
				if xpos == -1:
					# create the cursor:
					xpos = 100 * ((x - self.sx) / self.VASLENGTH)
					self.c['VASCursorLine'] = Line(x, self.ypos-(self.var.VAS_LINESIZE/2), x, self.ypos+(self.var.VAS_LINESIZE/2), color = self.var.VAS_CURSOR_COLOR)
				else:
					# move it
					xpos = 100 * ((x - self.sx) / self.VASLENGTH)
					self.c['VASCursorLine'].sx = x
					self.c['VASCursorLine'].ex = x
					
			if self.useLabels:
				if (x,y) in self.c[self.var.VAS_MAXLABEL_NAME]:
					# clicked on the maxlabel: either create the cursor, or move it
					if xpos == -1:
						# create the cursor:
						xpos = 100
						x = self.sx+self.VASLENGTH
						self.c['VASCursorLine'] = Line(x, self.ypos-(self.var.VAS_LINESIZE/2), x, self.ypos+(self.var.VAS_LINESIZE/2), color = self.var.VAS_CURSOR_COLOR)
					else:
						# move it
						xpos = 100
						x = self.sx+self.VASLENGTH
						self.c['VASCursorLine'].sx = x
						self.c['VASCursorLine'].ex = x

				if (x,y) in self.c[self.var.VAS_MINLABEL_NAME]:
					# clicked on the minlabel: either create the cursor, or move it
					if xpos == -1:
						# create the cursor:
						xpos = 0
						x = self.sx
						self.c['VASCursorLine'] = Line(x, self.ypos-(self.var.VAS_LINESIZE/2), x, self.ypos+(self.var.VAS_LINESIZE/2), color = self.var.VAS_CURSOR_COLOR)
					else:
						# move it
						xpos = 0
						x = self.sx
						self.c['VASCursorLine'].sx = x
						self.c['VASCursorLine'].ex = x
				
				
			if (x,y) in self.c[self.var.VAS_EXITBUTTON_NAME]:
				if xpos != -1:
					break
			
			self.c.show()
			
		# Add all response related data to the Opensesame responses instance.
		self.experiment.responses.add(response_time=self.experiment.time()-st, \
								correct=None, \
								response=str(round(xpos,2)), \
								item=self.name)


class qtVAS2(VAS2, qtautoplugin):

	"""
	This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
	usually need to do hardly anything, because the GUI is defined in info.json.
	"""

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.

		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.

		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		# We don't need to do anything here, except call the parent
		# constructors.
		VAS2.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

			
	def init_edit_widget(self):

		"""
		Constructs the GUI controls. Usually, you can omit this function
		altogether, but if you want to implement more advanced functionality,
		such as controls that are grayed out under certain conditions, you need
		to implement this here.
		"""

		# First, call the parent constructor, which constructs the GUI controls
		# based on info.json.
		qtautoplugin.init_edit_widget(self)
		# If you specify a 'name' for a control in info.json, this control will
		# be available self.[name]. The type of the object depends on the
		# control. A checkbox will be a QCheckBox, a line_edit will be a
		# QLineEdit. Here we connect the stateChanged signal of the QCheckBox,
		# to the setEnabled() slot of the QLineEdit. This has the effect of
		# disabling the QLineEdit when the QCheckBox is uncheckhed. We also
		# explictly set the starting state.
		#self.line_edit_widget.setEnabled(self.checkbox_widget.isChecked())
		#self.checkbox_widget.stateChanged.connect(
		#	self.line_edit_widget.setEnabled)
	 
	
