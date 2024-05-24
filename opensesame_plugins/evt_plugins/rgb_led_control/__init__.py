"""Plug-in for sending RGB-data to the RSP-LT response box."""

# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
# Defines the GUI controls:
controls = [
    {
        "type": "combobox",
        "var": "device",
        "label": "Select device :",
        "options": [
            "Keyboard"
        ],
        "name": "device_combobox_widget",
        "tooltip": "Select device"
    }, {
        "type": "checkbox",
        "var": "refresh",
        "label": "Refresh device list",
        "name": "refresh_checkbox_widget",
        "tooltip": "Refresch device list checkbox"
    }, {
        "type": "line_edit",
        "var": "correct_response",
        "label": "Correct response :",
        "name": "correct_response_line_edit_widget",
        "tooltip": "Correct Button (1 - 8), seperated by ';'"
    }, {
        "type": "line_edit",
        "var": "allowed_responses",
        "label": "Allowed responses :",
        "name": "allowed_responses_line_edit_widget",
        "tooltip": "Allowed Buttons (1 - 8), seperated by ';'"
    }, {
        "type": "line_edit",
        "var": "timeout",
        "label": "Response timeout [ms] :",
        "name": "timeout_line_edit_widget",
        "tooltip": "Response timeout in ms"
    }, {
        "type": "color_edit",
        "var": "button1_color",
        "label": "Color button 1 :",
        "name": "button1_color_edit_widget",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "button2_color",
        "label": "Color button 2 :",
        "name": "button2_color_edit_widget",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "button3_color",
        "label": "Color button 3 :",
        "name": "button3_color_edit_widget",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "button4_color",
        "label": "Color button 4 :",
        "name": "button4_color_edit_widget",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "checkbox",
        "var": "feedback",
        "label": "Color Feedback",
        "name": "feedback_checkbox_widget",
        "tooltip": "When checked, Colors in the buttons give feedback"
    }, {
        "type": "line_edit",
        "var": "reset_delay",
        "label": "Reset Feedback after [ms] :",
        "name": "reset_delay_line_edit_widget",
        "tooltip": "Reset feedback color after xx ms"
    }, {
        "type": "color_edit",
        "var": "correct_color",
        "label": "Correct button feedback color :",
        "name": "correct_color_edit_widget",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "incorrect_color",
        "label": "Incorrect button feedback color :",
        "name": "incorrect_color_edit_widget",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "checkbox",
        "var": "close_device",
        "label": "Auto close EVT-device(s). (Use this for the latter instance of the plugin or with a single instance of the plugin.)",
        "name": "close_device_checkbox_widget",
        "tooltip": "Close device list checkbox"
    }, {
        "type": "text",
        "label": "<small>RGB-LED control plug-in version 0.2.0</small>"
    }
]
