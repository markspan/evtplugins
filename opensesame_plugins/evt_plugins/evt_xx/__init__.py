"""A plug-in for triggering EVT2/3 USB devices"""

# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "_productName",
        "label": "Select device",
        "options": [
            "DUMMY"
        ],
        "name": "ProductName_widget",
        "tooltip": "Select the desired USB-device or dummy"
    }, {
        "type": "combobox",
        "var": "_outputMode",
        "label": "Select output mode",
        "options": [
            "Pulse output lines",
            "Set output lines"
        ],
        "name": "OutputMode_widget",
        "tooltip": "Select the desired output mode"
    }, {
        "type": "line_edit",
        "var": "_value",
        "label": "Value",
        "name": "value_widget",
        "tooltip": "Value (0-255) to pulse/set port, -1 for no initial output."
    }, {
        "type": "line_edit",
        "var": "_duration",
        "label": "Duration in ms",
        "name": "duration_widget",
        "tooltip": "Expecting a value in milliseconds"  
    }
]
