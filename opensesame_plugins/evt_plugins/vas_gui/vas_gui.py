# -*- coding:utf-8 -*-

"""
No rights reserved. All files in this repository are released into the public
domain.
"""
from libopensesame.py3compat import *
from libopensesame.item import Item
from libopensesame.oslogging import oslogger
from openexp.mouse import Mouse
from openexp.canvas import Canvas
from openexp.canvas_elements import (
	Line
)

class VasGui(Item):

    """
    This class (the class with the same name as the module) handles the basic
    functionality of the item. It does not deal with GUI stuff.
    """

    description = u'A Revised VAS modifier for a canvas'

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

    def prepare(self):

        """The preparation phase of the plug-in goes here."""

        self.my_mouse = Mouse(self.experiment)
        self.my_mouse.buttonlist = [1]

        # Checking the excistence of the VAS elements is only possible
        # in the runphase as only then the full canvas is available
        self.c = Canvas(self.experiment)
     
        my_canvas = self.experiment.items[self.var.vas_canvas_name].canvas

        try:
            if my_canvas[self.var.vas_body_name] is None or my_canvas[self.var.vas_exitbutton_name] is None:
                oslogger.info("Should not occur")
        except Exception:
            oslogger.error(u"READ the VAS manual: no VAS-elements found on the given canvas")
        self.useLabels = True

        try:
            if my_canvas[self.var.vas_maxlabel_name] is None or my_canvas[self.var.vas_maxlabel_name] is None:
                oslogger.info("Should not occur")
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
            raise oslogger.error("The VAS Body should be a line or a rectangle")

    def run(self):
        start_time = self.clock.time()
        xpos = -1

        self.my_mouse.set_pos(pos=(0, 0))
        self.my_mouse.show_cursor(show=True)

        while(True):
            # Poll the mouse for button clicks
            button, position, timestamp = self.my_mouse.get_click(timeout=20)

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
                    else:
                        # move it
                        xpos = 100 * ((x - self.sx) / self.vas_length)
                        self.c['VASCursorLine'].sx = x
                        self.c['VASCursorLine'].ex = x

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
                        else:
                            # move it
                            xpos = 100
                            x = self.sx+self.vas_length
                            self.c['VASCursorLine'].sx = x
                            self.c['VASCursorLine'].ex = x

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
                    else:
                        # move it
                        xpos = 0
                        x = self.sx
                        self.c['VASCursorLine'].sx = x
                        self.c['VASCursorLine'].ex = x

                if (x, y) in self.c[self.var.vas_exitbutton_name]:
                    if xpos != -1:
                        break

                self.c.show()

        self.experiment.var.vas_response_time = self.clock.time() - start_time
        self.experiment.var.vas_response = round(xpos, 2)
