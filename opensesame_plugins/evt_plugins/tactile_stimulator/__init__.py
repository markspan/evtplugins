"""A plug-in for handling the Tactile Stimulator."""

authors = ["M.M.Span", "M.Stokroos"]
# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "_deviceName",
        "label": "Select device :",
        "options": [
            "DUMMY"
        ],
        "name": "device_widget",
        "tooltip": "Select the connected Tactile Stimulator or DUMMY for testing purposes: "
    },
    {
        "type": "combobox",
        "var": "_mode",
        "label": "Select the mode of operation :",
        "options": [
            "Calibrate",
            "Stimulate"
        ],
        "name": "calibrate_widget",
        "tooltip": "Select the mode of operation"    
    },
    {
        "type": "line_edit",
        "var": "_percOfCalibrationValue",
        "label": "Percentage of the calibrated intensity value applied to the subject [%] :",
        "name": "value_widget",
        "tooltip": "Give the percentage of the calibrated pulse intensity applied to the subject"
    },
    {
        "type": "line_edit",
        "var": "_pulseDuration",
        "label": "Pulse duration [ms] :",
        "name": "duration_widget",
        "tooltip": "Pulse duration value between 1 and 2000 milliseconds"
    }
]