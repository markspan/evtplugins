"""A plug-in for handling the Tactile Stimulator."""

# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "device",
        "label": "Select device :",
        "options": [
            "0: DUMMY"
        ],
        "name": "device_combobox",
        "tooltip": "Select the connected Tactile Stimulator or DUMMY."
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
        "name": "mode_combobox",
        "tooltip": "Select the mode of operation"    
    }, {
        "type": "line_edit",
        "var": "perc_calibr_value",
        "label": "Percentage of the calibrated intensity value applied to the subject 0-100% :",
        "name": "perc_line_edit",
        "tooltip": "Give the percentage of the calibrated pulse intensity applied to the subject"
    }, {
        "type": "line_edit",
        "var": "pulse_duration_value",
        "label": "Pulse duration 1-2000[ms] :",
        "name": "duration_line_edit",
        "tooltip": "Pulse duration value between 1 and 2000 milliseconds"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> The calibrate instance of the plugin should always precede the stimulate instance within the experiment.</small>"
    }, {
        "type": "text",
        "label": "<small>Tactile Stimulator plug-in version 0.2.0</small>"
    }
]