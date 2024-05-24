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
        "name": "device_combobox_widget",
        "tooltip": "Select the desired RSP-device"
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
        "name": "correct_response_line_edit_widget",
        "tooltip": "Choose the correct response, button (1-8)"
    }, {
        "type": "line_edit",
        "var": "allowed_responses",
        "label": "Allowed responses :",
        "name": "allowed_responses_line_edit_widget",
        "tooltip": "Allowed responses (buttons 1-8) seperated by ';'"
    }, {
        "type": "line_edit",
        "var": "timeout",
        "label": "Timeout [ms]:",
        "name": "timeout_line_edit_widget",
        "tooltip": "Expecting a value in milliseconds or 'infinite'."
    }, {
        "type": "checkbox",
        "var": "close_device",
        "label": "Auto close EVT-device(s). (Use this for the latter instance of the plugin or with a single instance of the plugin.)",
        "name": "close_device_checkbox_widget",
        "tooltip": "Close device list checkbox"
    }, {
        "type": "text",
        "label": "<small>RSP-12x response box plug-in version 0.2.0</small>"
    }
]
