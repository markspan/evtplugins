"""A plug-in for using the Tactile Stimulator."""

# authors = ["M.M.Span", "M.Stokroos"]
category = "evt_plugin_collection"
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "_deviceName",
        "label": "Select device: ",
        "options": [
            "DUMMY"
        ],
        "name": "deviceName_widget",
        "tooltip": "Select the Tactile Stimulator or Dummy if not connected: "
    }, {
        "type": "combobox",
        "var": "_mode",
        "label": "Select mode of operation: ",
        "options": [
            "Calibrate",
            "Stimulate"
        ],
        "name": "calibrate_widget",
        "tooltip": "Select the mode of operation: "    
    }, {
        "type": "line_edit",
        "var": "_percOfCalibrationValue",
        "label": "Percentage [%]",
        "name": "value_widget",
        "tooltip": "Give the percentage of the calibrated pulse intensity value to be used."
    }, {
        "type": "line_edit",
        "var": "_pulseDuration",
        "label": "Pulse duration [ms]: ",
        "name": "duration_widget",
        "tooltip": "Pulse duration value in milliseconds"
    }
]