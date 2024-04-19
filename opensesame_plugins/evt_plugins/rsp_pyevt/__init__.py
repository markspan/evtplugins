"""Plugin to collect input from a RSP-12x responsebox"""

authors = ["M. Stokroos"]
category = "RUG/BSS hardware"
help_url = 'https://github.com/MartinStokroos/evt-plugins'

# Defines the GUI controls:
controls = [
    {
        "type": "combobox",
        "var": "_device",
        "label": "Select device :",
        "options": [
            "Keyboard"
        ],
        "name": "device_combobox",
        "tooltip": "Select the desired RSP-device"
    }, {
        "type": "checkbox",
        "var": "refresh",
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
    }
]
