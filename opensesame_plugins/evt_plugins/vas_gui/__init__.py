"""VAS-GUI plugin"""

authors = ["M. M. Span", "M. Stokroos"]
category = "RUG/BSS hardware"
help_url = 'https://markspan.github.io/evtplugins/'
# Defines the GUI controls
controls = [
    {   
        "type": "line_edit",
        "var": "vas_canvas_name",
        "label": "Name of the VAS canvas :",
        "name": "vas_canvasname_widget",
        "tooltip": "Enter the name of the VAS canvas element"
    }, {
        "type": "line_edit",
        "var": "vas_body_name",
        "label": "Name of the line-element :",
        "name": "vas_bodyname_widget",
        "tooltip": "Name of the Line Element of the VAS on the Canvas"
    }, {
        "type": "color_edit",
        "var": "vas_cursor_color",
        "label": "Color of the cursor :",
        "name": "vas_cursorcolor_widget",
        "tooltip": "Color of the Cursor Element of the VAS on the Canvas"
    }, {
        "type": "line_edit",
        "var": "vas_exitbutton_name",
        "label": "Name of the Exit Button :",
        "name": "vas_exitbutton_widget",
        "tooltip": "Name of the exitbutton"
    }, {
        "type": "line_edit",
        "var": "vas_minlabel_name",
        "label": "Name of the textelement to the left of the VAS :",
        "name": "vas_minlabel_widget",
        "tooltip": "Enter the name of the textelement to the left of the VAS"
    }, {
        "type": "line_edit",
        "var": "vas_maxlabel_name",
        "label": "Name of the textelement to the right of the VAS :",
        "name": "vas_maxlabel_widget",
        "tooltip": "Enter the name of the textelement to the right of the VAS"
    }, {
        "type": "spinbox",
        "var": "vas_marker_length",
        "label": "Marker length in pixels :",
        "min_val": 1,
        "max_val": 100,
        "name": "vas_markerlength_widget",
        "tooltip": "Enter the length of the marker in pixels."
    }, {
        "type": "spinbox",
        "var": "vas_marker_width",
        "label": "Marker width in pixels :",
        "min_val": 1,
        "max_val": 100,
        "name": "vas_markerwidth_widget",
        "tooltip": "Enter the width of the marker in pixels."
    }, {
        "type": "line_edit",
        "var": "vas_timeout",
        "label": "Timeout period [ms] :",
        "name": "timeout_widget",
        "tooltip": "Expecting a value in milliseconds. '-1' is infinite"  
    }
]
