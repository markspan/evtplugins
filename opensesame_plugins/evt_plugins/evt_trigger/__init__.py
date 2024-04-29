"""A plug-in for generating triggers with EVT devices."""

# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
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
        "tooltip": "Select the desired EVT-device or DUMMY."
    }, {
        "type": "checkbox",
        "var": "refresh",
        "label": "Refresh device list",
        "name": "refresh_checkbox",
        "tooltip": "Refresch device list checkbox"
    }, {
        "type": "combobox",
        "var": "outputmode",
        "label": "Select output mode :",
        "options": [
            "Reset output lines",
            "Write output lines",
            "Invert output lines",
            "Pulse output lines"
        ],
        "name": "output_mode_combobox",
        "tooltip": "Select the desired output mode"
    }, {
        "type": "checkbox",
        "var": "bit0",
        "label": "output 0",
        "name": "b0_checkbox",
        "tooltip": "bit 0 checkbox"
    }, {
        "type": "checkbox",
        "var": "bit1",
        "label": "output 1",
        "name": "b1_checkbox",
        "tooltip": "bit 1 checkbox"
    }, {
        "type": "checkbox",
        "var": "bit2",
        "label": "output 2",
        "name": "b2_checkbox",
        "tooltip": "bit 2 checkbox"
    }, {
        "type": "checkbox",
        "var": "bit3",
        "label": "output 3",
        "name": "b3_checkbox",
        "tooltip": "bit 3 checkbox"
    }, {
        "type": "checkbox",
        "var": "bit4",
        "label": "output 4",
        "name": "b4_checkbox",
        "tooltip": "bit 4 checkbox"
    }, {
        "type": "checkbox",
        "var": "bit5",
        "label": "output 5",
        "name": "b5_checkbox",
        "tooltip": "bit 5 checkbox"
    }, {
        "type": "checkbox",
        "var": "bit6",
        "label": "output 6",
        "name": "b6_checkbox",
        "tooltip": "bit 6 checkbox"
    }, {
        "type": "checkbox",
        "var": "bit7",
        "label": "output 7",
        "name": "b7_checkbox",
        "tooltip": "bit 7 checkbox"
    }, {
        "type": "line_edit",
        "var": "mask",
        "label": "Byte or bit-mask value :",
        "name": "byte_value_line_edit",
        "tooltip": "Bit mask value [0-255]"
    }, {
        "type": "line_edit",
        "var": "duration",
        "label": "Duration [ms] :",
        "name": "duration_line_edit",
        "tooltip": "Expecting a value in milliseconds"
    }, {
        "type": "text",
        "label": "<small>EVT-trigger plug-in version 2.0.0</small>"
    }
]
