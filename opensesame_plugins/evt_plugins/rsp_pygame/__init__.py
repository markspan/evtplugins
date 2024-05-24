"""Collects input from a RSP-12x responsebox or from a generic keyboard"""

# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "device",
        "label": "Select device :",
        "options": [
            "Keyboard"
        ],
        "name": "device_combobox_widget",
        "tooltip": "Identifies the response box, in case there are multiple response boxes"
    }, {
        "type": "checkbox",
        "var": "refresh_device_list",
        "label": "Refresh device list",
        "name": "refresh_checkbox_widget",
        "tooltip": "Refresch device list checkbox"

    }, {
        "type": "line_edit",
        "var": "correct_response",
        "label": "Correct response :",
        "tooltip": "Expecting a comma-separated list of numbers between 1 and the number of joybuttons"
    }, {
        "type": "line_edit",
        "var": "allowed_responses",
        "label": "Allowed responses :",
        "tooltip": "Expecting a comma-separated list of numbers between 1 and the number of joybuttons"
    }, {
        "type": "line_edit",
        "var": "timeout",
        "label": "Timeout period :",
        "name": "timeout_line_edit_widget",
        "tooltip": "Expecting a value in milliseconds or 'infinite'."
    }, {
        "type": "text",
        "label": "<small>Generic response box plug-in version 0.2.0</small>"
    }
]
