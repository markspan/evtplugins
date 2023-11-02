"""A plug-in for using responsebox devices"""

# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "_productName",
        "label": "Select device",
        "options": [
            "Keyboard"
        ],
        "name": "ProductName_widget",
        "tooltip": "Select the desired USB-device or Keyboard"
    }, {
        "type": "line_edit",
        "var": "_correctButton",
        "label": "Correct Button",
        "name": "CorrectButton_widget",
        "tooltip": "Choose the correct button (1-8)"
    }, {
        "type": "line_edit",
        "var": "_allowedButtons",
        "label": "Allowed Buttons",
        "name": "AllowedButtons_widget",
        "tooltip": "Allowed Buttons, (1-8) seperated by ';'= "
    }, {
        "type": "line_edit",
        "var": "_responseTimeout",
        "label": "Response time out",
        "name": "ResponseTimeout_widget",
        "tooltip": "Response timeout in milliseconds"  
    }
]
