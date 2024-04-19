"""A plug-in for handling the Tactile Stimulator."""

authors = ["M.M.Span", "M.Stokroos"]
# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "_device",
        "label": "Select device :",
        "options": [
            "DUMMY"
        ],
        "name": "device_combobox",
        "tooltip": "Select the connected Tactile Stimulator or DUMMY for testing purposes: "
    }, {
        "type": "checkbox",
        "var": "_refresh",
        "label": "Refresh device list",
        "name": "refresh_checkbox",
        "tooltip": "Refresch device list checkbox"
    }, {
        "type": "combobox",
        "var": "_mode",
        "label": "Select the mode of operation :",
        "options": [
            "Calibrate",
            "Stimulate"
        ],
        "name": "calibrate_combobox",
        "tooltip": "Select the mode of operation"    
    }, {
        "type": "line_edit",
        "var": "_percOfCalibrationValue",
        "label": "Percentage of the calibrated intensity value applied to the subject 0-100[%] :",
        "name": "value_line_edit",
        "tooltip": "Give the percentage of the calibrated pulse intensity applied to the subject"
    }, {
        "type": "line_edit",
        "var": "_pulseDuration",
        "label": "Pulse duration 1-2000[ms] :",
        "name": "duration_line_edit",
        "tooltip": "Pulse duration value between 1 and 2000 milliseconds"
    }
]