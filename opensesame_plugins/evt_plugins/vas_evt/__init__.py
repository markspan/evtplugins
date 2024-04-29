"""VAS plugin"""

# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "vas_encoder_id",
        "label": "Type of Encoder",
        "options": [
            "MOUSE"
        ],
        "name": "vas_encoderid_widget",
        "tooltip": "What encoder are you using?"
    }, {
        "type": "line_edit",
        "var": "vas_canvas_name",
        "label": "Name of the VAS canvas",
        "name": "vas_canvasname_widget",
        "tooltip": "Enter the name of the VAS canvas element"
    }, {
        "type": "line_edit",
        "var": "vas_body_name",
        "label": "Name of the line-element",
        "name": "vas_bodyname_widget",
        "tooltip": "Name of the line element of the VAS on the canvas"
    }, {
        "type": "line_edit",
        "var": "vas_=cursor_name",
        "label": "Name of the cursor",
        "name": "vas_cursorname_widget",
        "tooltip": "Name of the cursor element of the VAS on the canvas"
    }, {
        "type": "line_edit",
        "var": "vas_timer_name",
        "label": "Name of the timer line",
        "name": "vas_timername_widget",
        "tooltip": "Name of the (optional) timer line, only availeable if 'VAS exit method' = TIME"
    }, {
        "type": "combobox",
        "var": "vas_exit_method",
        "label": "VAS exit method",
        "options": [
            "MOUSE",
            "TIME",
            "KEY"
        ],
        "name": "vas_exit_method_widget",
        "tooltip": "Exit by mouseclick, key or after a set time."
    }, {
        "type": "line_edit",
        "var": "vas_exitkey",
        "label": "Exit key of VAS when\r\n KEY is selected as VAS exit method.",
        "name": "vas_exitkey_widget",
        "tooltip": "Enter key to end VAS"
    }, {
        "type": "spinbox",
        "var": "vas_cursor_startposition",
        "label": "Start value",
        "min_val": 0,
        "max_val": 100,
        "name": "vas_startpos_widget",
        "prefix": "0%",
        "suffix": "100%",
        "tooltip": "Slider start position"
    }, {
        "type": "text",
        "label": "<small>VAS-EVT plug-in version 2.0.0</small>"
    }
]
