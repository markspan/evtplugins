"""Collects input from a RSP-12x responsebox or from a generic keyboard"""

authors = ["Edwin Dalmaijer", "Sebastiaan Mathot", "Martin Stokroos"]
category = "RUG/BSS hardware"
help_url = 'https://github.com/MartinStokroos/evt-plugins'

# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "_device",
        "label": "Select device :",
        "options": [
            "Keyboard"
        ],
        "name": "device_widget",
        "tooltip": "Identifies the response box, in case there are multiple response boxes"
    },
    {
        "type": "line_edit",
        "var": "correct_response",
        "label": "Correct response :",
        "tooltip": "Expecting a comma-separated list of numbers between 1 and the number of joybuttons"
    },
    {
        "type": "line_edit",
        "var": "allowed_responses",
        "label": "Allowed responses :",
        "tooltip": "Expecting a comma-separated list of numbers between 1 and the number of joybuttons"
    },
    {
        "type": "line_edit",
        "var": "timeout",
        "label": "Timeout period :",
        "tooltip": "Expecting a value in milliseconds of 'infinite'"
    }
]
