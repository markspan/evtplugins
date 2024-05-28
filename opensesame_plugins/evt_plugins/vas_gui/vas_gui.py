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

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.oslogging import oslogger
from openexp.mouse import Mouse
from openexp.canvas import Canvas
from openexp.canvas_elements import (Line)


class VasGui(Item):

    description = u'A Virtual Analog Slider plugin, controlled by a canvas screen GUI.'

    def reset(self):
        """Resets plug-in to initial values."""
        self.var.vas_canvas_name = u'VASSCREEN'
        self.var.vas_body_name = u'VASBODY'
        self.var.vas_cursor_color = "#ffffff"
        self.var.vas_exitbutton_name = u'VASEXIT'
        self.var.vas_maxlabel_name = u'MAXLABEL'
        self.var.vas_minlabel_name = u'MINLABEL'
        self.var.vas_marker_length = 10
        self.var.vas_marker_width = 4
        self.var.vas_timeout = u'infinite'

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        self.my_mouse = Mouse(self.experiment)
        self.my_mouse.buttonlist = [1]
        
        try:
            self._timeout = int(self.var.vas_timeout)
        except ValueError:
            self._timeout = -1

        # Checking the excistence of the VAS elements is only possible
        # in the runphase as only then the full canvas is available
        self.c = Canvas(self.experiment)
     
        my_canvas = self.experiment.items[self.var.vas_canvas_name].canvas

        try:
            if my_canvas[self.var.vas_body_name] is None or my_canvas[self.var.vas_exitbutton_name] is None:
                oslogger.info("Should not occur")
        except Exception:
            oslogger.error(u"No VAS-elements found on the sketchpad canvas")
        
        self.useLabels = True

        try:
            if my_canvas[self.var.vas_maxlabel_name] is None or my_canvas[self.var.vas_maxlabel_name] is None:
                oslogger.info("Not using min and max labels")
        except Exception:
            self.uselabels = False

        self.c = self.experiment.items[self.var.vas_canvas_name].canvas
        self.ypos = -1
        # is the vasbody a line?
        if all(hasattr(self.c[self.var.vas_body_name], attr) for attr in ["ex", "sx"]):
            self.vas_length = self.c[self.var.vas_body_name].ex - self.c[self.var.vas_body_name].sx
            self.ypos = (self.c[self.var.vas_body_name].sy + self.c[self.var.vas_body_name].ey) / 2
            self.sx = self.c[self.var.vas_body_name].sx
        # is the vasbody a rectangle?
        if all(hasattr(self.c[self.var.vas_body_name], attr) for attr in ["w", "y", "h"]):
            self.vas_length = self.c[self.var.vas_body_name].w
            self.ypos = self.c[self.var.vas_body_name].y + (self.c[self.var.vas_body_name].h / 2)
            self.sx = self.c[self.var.vas_body_name].x
        if self.ypos == -1:
            raise oslogger.error("The VAS-body should be a line or a rectangle")

    def run(self):
        xpos = -1
        self.my_mouse.show_cursor(show=True)
        start_time = self.clock.time()
        while(True):
            # Check if timeout
            if self._timeout >= 0:
                if self.clock.time() - start_time >= self._timeout:
                    self.experiment.var.vas_response_time = self._timeout
                    self.experiment.var.vas_response = -1
                    break

            # Poll the mouse for button clicks
            button, position, timestamp = self.my_mouse.get_click(timeout=None, visible=True)

            if button is not None:
                (x, y), time = self.my_mouse.get_pos()

                if (x, y) in self.c[self.var.vas_body_name]:
                    # clicked on the line: either create the cursor, or move it
                    if xpos == -1:
                        # create the cursor:
                        xpos = 100 * ((x - self.sx) / self.vas_length)
                        self.c['VASCursorLine'] = \
                            Line(x,
                                 self.ypos - self.var.vas_marker_length / 2,
                                 x,
                                 self.ypos + self.var.vas_marker_length / 2,
                                 color=self.var.vas_cursor_color,
                                 penwidth=self.var.vas_marker_width)
                        self.c.show()
                    else:
                        # move it
                        xpos = 100 * ((x - self.sx) / self.vas_length)
                        self.c['VASCursorLine'].sx = x
                        self.c['VASCursorLine'].ex = x
                        self.c.show()

                if self.useLabels:
                    if (x, y) in self.c[self.var.vas_maxlabel_name]:
                        # clicked on the maxlabel: either create the cursor, or move it
                        if xpos == -1:
                            # create the cursor:
                            xpos = 100
                            x = self.sx + self.vas_length
                            self.c['VASCursorLine'] = \
                                Line(x,
                                     self.ypos - self.var.vas_marker_length / 2,
                                     x,
                                     self.ypos + self.var.vas_marker_length / 2,
                                     color=self.var.vas_cursor_color,
                                     penwidth=self.var.vas_marker_width)
                            self.c.show()
                        else:
                            # move it
                            xpos = 100
                            x = self.sx+self.vas_length
                            self.c['VASCursorLine'].sx = x
                            self.c['VASCursorLine'].ex = x
                            self.c.show()

                if (x, y) in self.c[self.var.vas_minlabel_name]:
                    # clicked on the minlabel: either create the
                    # cursor, or move it
                    if xpos == -1:
                        # create the cursor:
                        xpos = 0
                        x = self.sx
                        self.c['VASCursorLine'] = \
                            Line(x,
                                 self.ypos - self.var.vas_marker_length / 2,
                                 x,
                                 self.ypos + self.var.vas_marker_length / 2,
                                 color=self.var.vas_cursor_color,
                                 penwidth=self.var.vas_marker_width)
                        self.c.show()
                    else:
                        # move it
                        xpos = 0
                        x = self.sx
                        self.c['VASCursorLine'].sx = x
                        self.c['VASCursorLine'].ex = x
                        self.c.show()

                if (x, y) in self.c[self.var.vas_exitbutton_name]:
                    if xpos != -1:
                        self.experiment.var.vas_response_time = self.clock.time() - start_time
                        self.experiment.var.vas_response = round(xpos, 2)
                        break


class QtVasGui(VasGui, QtAutoPlugin):

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
        VasGui.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):

        """Constructs the GUI controls. Usually, you can omit this function
        altogether, but if you want to implement more advanced functionality,
        such as controls that are grayed out under certain conditions, you need
        to implement this here.
        """

        # First, call the parent constructor, which constructs the GUI controls
        # based on __init_.py.
        super().init_edit_widget()
        # If you specify a 'name' for a control in __init__.py, this control
        # will be available self.[name]. The type of the object depends on
        # the control. A checkbox will be a QCheckBox, a line_edit will be a
        # QLineEdit. Here we connect the stateChanged signal of the QCheckBox,
        # to the setEnabled() slot of the QLineEdit. This has the effect of
        # disabling the QLineEdit when the QCheckBox is uncheckhed. We also
        # explictly set the starting state.
        # self.line_edit_widget.setEnabled(self.checkbox_widget.isChecked())
        # self.checkbox_widget.stateChanged.connect(
        #    self.line_edit_widget.setEnabled)