"""Collects input from a RSP-12x responsebox"""

authors = ["Edwin Dalmaijer", "Sebastiaan Mathot", "Martin Stokroos"]
category = "RUG/BSS hardware"
controls = [
    {
        "type": "combobox",
        "var": "_dummy",
        "label": "Dummy mode (use keyboard instead of RSP-12x)",
        "options": [
            "no",
            "yes"
        ],
        "tooltip": "Enable dummy mode to test the experiment using a keyboard"
    },
    {
        "type": "combobox",
        "var": "_device",
        "label": "Device nr.",
        "options": [
            "Keyboard"
        ],
        "name": "device_widget",
        "tooltip": "Identifies the response box, in case there are multiple response boxes"
    },
    {
        "type": "line_edit",
        "var": "correct_response",
        "label": "Correct response",
        "tooltip": "Expecting a comma-separated list of numbers between 1 and the number of joybuttons"
    },
    {
        "type": "line_edit",
        "var": "allowed_responses",
        "label": "Allowed responses",
        "tooltip": "Expecting a comma-separated list of numbers between 1 and the number of joybuttons"
    },
    {
        "type": "line_edit",
        "var": "timeout",
        "label": "Timeout",
        "tooltip": "Expecting a value in milliseconds of 'infinite'"
    }
]
