"""A plug-in for EVT devices"""

authors = ["M. Stokroos", "M.M. Span"]
category = "RUG/BSS hardware"
help_url = 'https://github.com/MartinStokroos/evt-plugins'
controls = [
    {
        "type": "combobox",
        "var": "device",
        "label": "Select device :",
        "options": [
            "DUMMY"
        ],
        "name": "device_widget",
        "tooltip": "Select the desired USB-device or dummy"
    }, {
        "type": "combobox",
        "var": "outputmode",
        "label": "Select output mode :",
        "options": [
            "Pulse output lines",
            "Set output lines"
        ],
        "name": "output_mode_widget",
        "tooltip": "Select the desired output mode"
    }, {
        "type": "line_edit",
        "var": "value",
        "label": "Value :",
        "name": "value_widget",
        "tooltip": "Value [0-255] to pulse/set port, -1 for no initial output."
    }, {
        "type": "line_edit",
        "var": "duration",
        "label": "Duration in ms :",
        "name": "duration_widget",
        "tooltip": "Expecting a value in milliseconds"  
    }
]
