"""VAS plugin"""

# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "VAS_ENCODER_ID",
        "label": "Type of Encoder",
        "options": [
            "MOUSE"
        ],
        "name": "VAS_ENCODERID_widget",
        "tooltip": "What encoder are you using?"
    }, {
        "type": "line_edit",
        "var": "VAS_CANVAS_NAME",
        "label": "Name of the VAS canvas",
        "name": "VAS_canvasname_widget",
        "tooltip": "Enter the name of the VAS canvas element"
    }, {
        "type": "line_edit",
        "var": "VAS_BODY_NAME",
        "label": "Name of the line-element",
        "name": "VAS_bodyname_widget",
        "tooltip": "Name of the Line Element of the VAS on the Canvas"
    }, {
        "type": "line_edit",
        "var": "VAS_CURSOR_NAME",
        "label": "Name of the cursor",
        "name": "VAS_cursorname_widget",
        "tooltip": "Name of the Cursor Element of the VAS on the Canvas"
    }, {
        "type": "line_edit",
        "var": "VAS_TIMER_NAME",
        "label": "Name of the timer line",
        "name": "VAS_TIMERNAME_widget",
        "tooltip": "Name of the (optional) timer line, only availeable if 'VAS exit method' = TIME"
    }, {
        "type": "combobox",
        "var": "VAS_EXIT_METHOD",
        "label": "VAS exit method",
        "options": [
            "MOUSE",
            "TIME",
            "KEY"
        ],
        "name": "VAS_EXIT_METHOD_widget",
        "tooltip": "Exit by mouseclick, key or after a set time."
    }, {
        "type": "line_edit",
        "var": "VAS_EXITKEY",
        "label": "Exit key of VAS when\r\n KEY is selected as VAS exit method.",
        "name": "VAS_EXITKEY_widget",
        "tooltip": "Enter key to end VAS"
    }, {
        "type": "spinbox",
        "var": "VAS_CURSOR_STARTPOSITION",
        "label": "Start value",
        "min_val": 0,
        "max_val": 100,
        "name": "VAS_STARTPOS_widget",
        "prefix": "0%",
        "suffix": "100%",
        "tooltip": "Slider Start Position"
    }
]
