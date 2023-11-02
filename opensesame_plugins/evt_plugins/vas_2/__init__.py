"""VAS2 plugin"""

# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
# Defines the GUI controls
controls = [
    {   
        "type": "line_edit",
        "var": "VAS_CANVAS_NAME",
        "label": "Name of the VAS canvas",
        "name": "VAS_canvasname_widget",
        "tooltip": "Enter the name of the VAS canvas element"
    }, {
        "type": "line_edit",
        "var": "VAS_BODY_NAME",
        "label": "Name of the line-element",
        "name": "VAS_bodyname_widget",
        "tooltip": "Name of the Line Element of the VAS on the Canvas"
    }, {
        "type": "color_edit",
        "var": "VAS_CURSOR_COLOR",
        "label": "Color of the cursor",
        "name": "VAS_cursorcolor_widget",
        "tooltip": "Color of the Cursor Element of the VAS on the Canvas"
    }, {
        "type": "line_edit",
        "var": "VAS_EXITBUTTON_NAME",
        "label": "Name of the Exit Button",
        "name": "VAS_EXITBUTTON_widget",
        "tooltip": "Name of the exitbutton"
    }, {
        "type": "line_edit",
        "var": "VAS_MINLABEL_NAME",
        "label": "Name of the textelement to the left of the VAS",
        "name": "VAS_MINLABEL_widget",
        "tooltip": "Enter the name of the textelement to the left of the VAS"
    }, {
        "type": "line_edit",
        "var": "VAS_MAXLABEL_NAME",
        "label": "Name of the textelement to the right of the VAS",
        "name": "VAS_MAXLABEL_widget",
        "tooltip": "Enter the name of the textelement to the right of the VAS"
    }, {
        "type": "spinbox",
        "var": "VAS_LINESIZE",
        "label": "Start value",
        "min_val": 1,
        "max_val": 1000,
        "name": "VAS_LINESIZE_widget",
        "tooltip": "Enter the length you want to have for the marker in pixels."
    }
]
