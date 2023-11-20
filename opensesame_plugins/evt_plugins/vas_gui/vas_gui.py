# -*- coding:utf-8 -*-

"""
No rights reserved. All files in this repository are released into the public
domain.
"""
import sys
# import numpy as np
from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.oslogging import oslogger
from openexp.mouse import Mouse
from openexp.canvas import Canvas
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

class VasGui(Item):

    """
    This class (the class with the same name as the module) handles the basic
    functionality of the item. It does not deal with GUI stuff.
    """

    description = u'A Revised VAS modifier for a canvas'

    def reset(self):

        """
        desc:
            Resets plug-in to initial values.
        """

        self.var.vas_canvas_name = u'VASSCREEN'
        self.var.vas_body_name = u'VASBODY'
        self.var.vas_cursor_color = "#ffffff"
        self.var.vas_exitbutton_name = u'VASEXIT'
        self.var.vas_maxlabel_name = u'MAXLABEL'
        self.var.vas_minlabel_name = u'MINLABEL'
        self.var.vas_linesize = 10

    def prepare(self):

        """The preparation phase of the plug-in goes here."""
        super().prepare()

        # Checking the excistence of the VAS elements is only possible
        # in the runphase as only then the full canvas is available
        self.c = Canvas(self.experiment)
        self.my_mouse = Mouse(self.experiment, timeout=20)
        self.my_mouse.show_cursor(True)
        self.my_mouse.set_pos(pos=(0, 0))
     
        # my_canvas = self.experiment.items[self.var.vas_canvas_name].canvas
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
        # is the vasbody a line or a rect?
        if hasattr(self.c[self.var.vas_body_name], 'ex') and hasattr(self.c[self.var.vas_body_name], 'sx'):
            self.vas_length = self.c[self.var.vas_body_name].ex - self.c[self.var.vas_body_name].sx
            self.ypos = (self.c[self.var.vas_body_name].sy + self.c[self.var.vas_body_name].ey) / 2
            self.sx = self.c[self.var.vas_body_name].sx

        if hasattr(self.c[self.var.vas_body_name], 'w') and hasattr(self.c[self.var.vas_body_name], 'y') and hasattr(self.c[self.var.vas_body_name], 'h'):
            self.vas_length = self.c[self.var.vas_body_name].w
            self.ypos = self.c[self.var.vas_body_name].y + (self.c[self.var.vas_body_name].h / 2)
            self.sx = self.c[self.var.vas_body_name].x

        if self.ypos == -1:
            raise oslogger.error("The VAS Body should be a line or a rectangle")

    def run(self):
        # self.set_item_onset(self.c.show())
        # st = self.experiment.time()
        xpos = -1

        while(True):

            # Poll the mouse for buttonclicks
            button = None
            while button is None:
                button, position, timestamp = self.my_mouse.get_click()

            button = None
            (x, y), mtime = self.my_mouse.get_pos()

            if (x, y) in self.c[self.var.vas_body_name]:
                # clicked on the line: either create the cursor, or move it
                if xpos == -1:
                    # create the cursor:
                    xpos = 100 * ((x - self.sx) / self.vas_length)
                    self.c['VASCursorLine'] = \
                        Line(x,
                             self.ypos - (self.var.vas_linesize / 2),
                             x,
                             self.ypos + (self.var.vas_linesize / 2),
                             color=self.var.vas_cursor_color)
                else:
                    # move it
                    xpos = 100 * ((x - self.sx) / self.vas_length)
                    self.c['VASCursorLine'].sx = x
                    self.c['VASCursorLine'].ex = x

            if self.useLabels:
                if (x, y) in self.c[self.var.vas_maxlabel_name]:
                    # clicked on the maxlabel: either create
                    # the cursor, or move it
                    if xpos == -1:
                        # create the cursor:
                        xpos = 100
                        x = self.sx+self.vas_length
                        self.c['VASCursorLine'] = \
                            Line(x,
                                 self.ypos - (self.var.vas_linesize / 2),
                                 x,
                                 self.ypos + (self.var.vas_linesize / 2),
                                 color=self.var.vas_cursor_color)
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
                                 self.ypos - (self.var.vas_linesize / 2),
                                 x,
                                 self.ypos+(self.var.vas_linesize / 2),
                                 color=self.var.vas_cursor_color)
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

        # Add all response related data to the Opensesame responses instance.
        self.experiment.responses.add(response_time=self.experiment.time()-st,
                                      correct=None,
                                      response=str(round(xpos, 2)),
                                      item=self.name)


class QtVasGui(VasGui, QtAutoPlugin):

    """
    This class handles the GUI aspect of the plug-in. By using
    qtautoplugin, we usually need to do hardly anything,
    because the GUI is defined in info.json.
    """

    def __init__(self, name, experiment, script=None):
        VasGui.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):

        """
        Constructs the GUI controls. Usually, you can omit this function
        altogether, but if you want to implement more advanced functionality,
        such as controls that are grayed out under certain conditions, you need
        to implement this here.
        """
        super().init_edit_widget()
