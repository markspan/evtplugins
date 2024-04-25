"""Plugin for the RSP-LT response box for sending RGB-data."""

authors = ["M. Stokroos", "M.M. Span"]
category = "RUG/BSS hardware"
help_url = 'https://markspan.github.io/evtplugins/'
# Defines the GUI controls:
controls = [
    {
        "type": "combobox",
        "var": "device",
        "label": "Select device :",
        "options": [
            "DUMMY"
        ],
        "name": "device_combobox",
        "tooltip": "Select device"
    }, {
        "type": "checkbox",
        "var": "refresh",
        "label": "Refresh device list",
        "name": "refresh_checkbox",
        "tooltip": "Refresch device list checkbox"
    }, {
        "type": "line_edit",
        "var": "correct_button",
        "label": "Correct Button :",
        "name": "correct_button_line_edit",
        "tooltip": "Correct Button (1 - 8), seperated by ';'"
    }, {
        "type": "line_edit",
        "var": "allowed_buttons",
        "label": "Allowed Buttons :",
        "name": "allowed_buttons_line_edit",
        "tooltip": "Allowed Buttons (1 - 8), seperated by ';'"
    }, {
        "type": "line_edit",
        "var": "timeout",
        "label": "Response Timeout :",
        "name": "response_timeout_line_edit",
        "tooltip": "Response timeout in ms"
    }, {
        "type": "color_edit",
        "var": "button1_color",
        "label": "Color button 1 :",
        "name": "button1_color_edit",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "button2_color",
        "label": "Color button 2 :",
        "name": "button2_color_edit",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "button3_color",
        "label": "Color button 3 :",
        "name": "button3_color_edit",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "button4_color",
        "label": "Color button 4 :",
        "name": "button4_color_edit",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "checkbox",
        "var": "feedback",
        "label": "Color Feedback",
        "name": "feedback_checkbox",
        "tooltip": "When checked, Colors in the buttons give feedback"
    }, {
        "type": "line_edit",
        "var": "reset_delay",
        "label": "Reset Feedback after [ms] :",
        "name": "reset_delay_line_edit",
        "tooltip": "Reset feedback color after xx ms"
    }, {
        "type": "color_edit",
        "var": "correct_color",
        "label": "Correct button feedback color :",
        "name": "correct_color_edit",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "incorrect_color",
        "label": "Incorrect button feedback color :",
        "name": "incorrect_color_edit",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }
]
