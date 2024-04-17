"""A plug-in for generating triggers with EVT devices."""

authors = ["M. Stokroos", "M.M. Span"]
category = "RUG/BSS hardware"
help_url = 'https://github.com/MartinStokroos/evt-plugins'

# Defines the GUI controls:
controls = [
    {
        "type": "combobox",
        "var": "device",
        "label": "Select device :",
        "options": [
            "DUMMY"
        ],
        "name": "device_combobox",
        "tooltip": "Select the desired USB-device or dummy"
    },
    {
        "type": "combobox",
        "var": "outputmode",
        "label": "Select output mode :",
        "options": [
            "Write output lines",
            "Reset output lines",
            "Invert output lines",
            "Pulse output lines"
        ],
        "name": "output_mode_combobox",
        "tooltip": "Select the desired output mode"
    },
    {
        "type": "line_edit",
        "var": "value",
        "label": "Bit mask value :",
        "name": "byte_value_line_edit",
        "tooltip": "Bit mask value [0-255]"
    },
    {
        "type": "line_edit",
        "var": "duration",
        "label": "Duration in ms :",
        "name": "duration_line_edit",
        "tooltip": "Expecting a value in milliseconds"
    }
]
