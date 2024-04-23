"""Plugin to send LED RGB-data from an\r\nEventExchanger-based digital input/output device."""

authors = ["M. Stokroos", "M.M. Span"]
category = "RUG/BSS hardware"
help_url = 'https://github.com/MartinStokroos/evt-plugins'
# Defines the GUI controls:
controls = [
    {
        "type": "combobox",
        "var": "_device",
        "label": "Select device :",
        "options": [
            "DUMMY"
        ],
        "name": "device_combobox",
        "tooltip": "Select device"
    }, {
        "type": "checkbox",
        "var": "_refreshButton",
        "label": "Refresh device list",
        "name": "refresh_checkbox",
        "tooltip": "Refresch device list checkbox"
    }, {
        "type": "line_edit",
        "var": "_correctButton",
        "label": "Correct Button :",
        "name": "correct_button_line_edit",
        "tooltip": "Correct Button (1 - 8), seperated by ';'"
    }, {
        "type": "line_edit",
        "var": "_allowedButtons",
        "label": "Allowed Buttons :",
        "name": "allowed_buttons_line_edit",
        "tooltip": "Allowed Buttons (1 - 8), seperated by ';'"
    }, {
        "type": "line_edit",
        "var": "_responseTimeout",
        "label": "Response Timeout :",
        "name": "response_timeout_line_edit",
        "tooltip": "Response timeout in ms"
    }, {
        "type": "color_edit",
        "var": "_button1_Led_Color",
        "label": "LED-color button 1 :",
        "name": "button_1_color_edit",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "_button2_Led_Color",
        "label": "LED-color button 2 :",
        "name": "button_2_color_edit",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "_button3_Led_Color",
        "label": "LED-color button 3 :",
        "name": "button_3_color_edit",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "_button4_Led_Color",
        "label": "LED-color button 4 :",
        "name": "button_4_color_edit",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "checkbox",
        "var": "_feedback",
        "label": "Color Feedback",
        "name": "feedback_checkbox",
        "tooltip": "When checked, Colors in the buttons give feedback"
    }, {
        "type": "line_edit",
        "var": "_resetAfter",
        "label": "Reset Feedback after [ms] :",
        "name": "reset_delay_line_edit",
        "tooltip": "Reset feedback color after xx ms"
    }, {
        "type": "color_edit",
        "var": "_correctColor",
        "label": "Correct button feedback color :",
        "name": "correct_color_edit",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "_incorrectColor",
        "label": "Incorrect button feedback color :",
        "name": "incorrect_color_edit",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }
]
