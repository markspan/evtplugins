"""A Plug-in to collect input from a RSP-12x responsebox"""

# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
controls = [
    {
        "type": "combobox",
        "var": "device",
        "label": "Select device :",
        "options": [
            "Keyboard"
        ],
        "name": "device_combobox",
        "tooltip": "Select the desired RSP-device"
    }, {
        "type": "checkbox",
        "var": "refresh_device_list",
        "label": "Refresh device list",
        "name": "refresh_checkbox",
        "tooltip": "Refresch device list checkbox"
    }, {
        "type": "line_edit",
        "var": "correct_response",
        "label": "Correct response :",
        "name": "correct_response_line_edit",
        "tooltip": "Choose the correct response, button (1-8)"
    }, {
        "type": "line_edit",
        "var": "allowed_responses",
        "label": "Allowed responses :",
        "name": "allowed_response_line_edit",
        "tooltip": "Allowed responses (buttons 1-8) seperated by ';'"
    }, {
        "type": "line_edit",
        "var": "timeout",
        "label": "Timeout period :",
        "name": "timeout_line_edit",
        "tooltip": "Expecting a value in milliseconds or 'infinite'"
    }, {
        "type": "text",
        "label": "<small>RSP-12x response box plug-in version 1.0.0</small>"
    }
]
