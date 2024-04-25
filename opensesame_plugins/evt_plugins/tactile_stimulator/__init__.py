"""A plug-in for handling the Tactile Stimulator."""

authors = ["M. Stokroos", "M.M. Span"]
category = "RUG/BSS hardware"
help_url = 'https://markspan.github.io/evtplugins/'
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "device",
        "label": "Select device :",
        "options": [
            "DUMMY"
        ],
        "name": "device_combobox",
        "tooltip": "Select the connected Tactile Stimulator or DUMMY for testing purposes: "
    }, {
        "type": "checkbox",
        "var": "refresh",
        "label": "Refresh device list",
        "name": "refresh_checkbox",
        "tooltip": "Refresch device list checkbox"
    }, {
        "type": "combobox",
        "var": "mode",
        "label": "Select the mode of operation :",
        "options": [
            "Calibrate",
            "Stimulate"
        ],
        "name": "calibrate_combobox",
        "tooltip": "Select the mode of operation"    
    }, {
        "type": "line_edit",
        "var": "perc_calibr_value",
        "label": "Percentage of the calibrated intensity value applied to the subject 0-100[%] :",
        "name": "value_line_edit",
        "tooltip": "Give the percentage of the calibrated pulse intensity applied to the subject"
    }, {
        "type": "line_edit",
        "var": "pulse_duration",
        "label": "Pulse duration 1-2000[ms] :",
        "name": "duration_line_edit",
        "tooltip": "Pulse duration value between 1 and 2000 milliseconds"
    }
]