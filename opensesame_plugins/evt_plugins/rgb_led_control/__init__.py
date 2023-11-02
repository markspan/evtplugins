"""Plugin to send LED RGB-data from an\r\nEventExchanger-based digital input/output device."""

# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "_productName",
        "label": "Select device",
        "options": [
            "DUMMY"
        ],
        "name": "PruductName_widget",
        "tooltip": "Select device"
    }, {
        "type": "line_edit",
        "var": "_correctButton",
        "label": "Correct Button",
        "name": "CorrectButton_widget",
        "tooltip": "Correct Button (1 - 8), seperated by ';'"
    }, {
        "type": "line_edit",
        "var": "_allowedButtons",
        "label": "Allowed Buttons",
        "name": "AllowedButtons_widget",
        "tooltip": "Allowed Buttons (1 - 8), seperated by ';'"
    }, {
        "type": "line_edit",
        "var": "_responseTimeout",
        "label": "Response Timeout",
        "name": "ResponseTimeout_widget",
        "tooltip": "Response timeout in ms"
    }, {
        "type": "color_edit",
        "var": "_button1_Led_Color",
        "label": "Color LED button 1",
        "name": "Button1_Led_Color",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "_button2_Led_Color",
        "label": "Color LED button 2",
        "name": "Button2_Led_Color",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "_button3_Led_Color",
        "label": "Color LED button 3",
        "name": "Button3_Led_Color",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "_button4_Led_Color",
        "label": "Color LED button 4",
        "name": "Button4_Led_Color",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "checkbox",
        "var": "_feedback",
        "label": "Color Feedback",
        "name": "Feedbackwidget",
        "tooltip": "When checked, Colors in the buttons give feedback"
    }, {
        "type": "line_edit",
        "var": "_resetAfter",
        "label": "Reset Feedback after",
        "name": "ResetAfter_widget",
        "tooltip": "Reset feedback color after xx ms"
    }, {
        "type": "color_edit",
        "var": "_correctColor",
        "label": "Correct Button Feedback Color",
        "name": "CorrectColor_widget",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }, {
        "type": "color_edit",
        "var": "_inCorrectColor",
        "label": "Incorrect button feedback color",
        "name": "InCorrectColor_widget",
        "tooltip": "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')"
    }
]
