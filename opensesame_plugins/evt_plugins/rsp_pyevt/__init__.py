"""Collects input from a RSP-12x responsebox"""

authors = ["M. Stokroos", "M. M. Span"]
# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
help_url = 'www'
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "dummy",
        "label": "Dummy mode (use keyboard instead of joystick)",
        "options": [
            "no",
            "yes"
        ],
        "name": "dummy_widget",
        "tooltip": "Enable dummy mode to test the experiment using a keyboard"
    },
    {
        "type": "combobox",
        "var": "device",
        "label": "Select device",
        "options": [
            "Keyboard"
        ],
        "name": "device_widget",
        "tooltip": "Select the desired RSP-device"
    },
    {
        "type": "line_edit",
        "var": "correct_button",
        "label": "Correct Button",
        "name": "correct_button_widget",
        "tooltip": "Choose the correct button (1-8)"
    },
    {
        "type": "line_edit",
        "var": "allowed_buttons",
        "label": "Allowed Buttons",
        "name": "allowed_buttons_widget",
        "tooltip": "Allowed Buttons, (1-8) seperated by ';'= "
    },
    {
        "type": "line_edit",
        "var": "timeout",
        "label": "Timeout",
        "name": "timeout_widget",
        "tooltip": "Expecting a value in milliseconds or 'infinite'"  
    }
]
