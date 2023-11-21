# evt_plugins
OpenSesame plugins for using RUG/BSS Event Exchanger (EVT) devices.
The currently supported OpenSesame version is v4.0

The following plugin collection is available:

Plugin | Description | Desktop | OS compatibility | Status
------ | ----------- | ------- | ---------------- | ------
evt_xx | Plugin for Event Exchanger EVT-2,3 and 4 variants for event-marking and triggering | pygame(legacy) | Win | not validated
rsp_pyevt | Plugin for RSP12x button response box variants with 1-8 buttons | pygame(legacy) | Windows | not validated
rsp_pygame | Plugin for RSP12x button response box variants with 1-8 buttons | pygame(legacy) | Windows/Linux | validated
rgb_led_control | Plugin for multi-color LED control | pygame(legacy) | Windows | not validated
tactile_stimulator | Plugin for the Electrotactile Stimulator (SHK-1B) 0-5mA | pygame(legacy) | Windows | not validated
vas_evt | A Visual Analog Slider plugin controlled via an encoder knob connected to the EVT-2 | pygame(legacy) | Windows | not validated
vas_gui | A Visual Analog Slider plugin controlled via the PC-mouse on a predefined canvas (sketchpad) | pygame(legacy) | Windows | not validated

## Package dependencies
The plugins are dependent on the Python module pyevt and the underlying hidapi package.

[https://pypi.org/project/hidapi/](https://pypi.org/project/hidapi/)

pyevt and hidapi are installed from the Python Console in OpenSesame with the single command:

`!pip install --user pyevt`

## Environmental settings
Default the OpenSesame 4.0 plugins are installed as python site-package and automatically loaded at startup.
When the plugins are located somewhere else, add your path to the python-path of OpenSesame in the `environment.yaml` file in the OpenSesame program directory. See for the instructions here: [https://rapunzel.cogsci.nl/manual/environment/](https://rapunzel.cogsci.nl/manual/environment/) 

## evt_xx

## rsp_pyevt

## rsp_pygame

## rgb_led_control

## tactile_stimulator
description ...

List of the variables that appear in the OpenSesame variable inspector when using the TactileStimulator plugin:

variable name | description
------------- | -----------
tactstim_calibration_perc | The percentage of the slider setting for the stimulus current of 5mA rms  max.
tactstim_calibration_milliamp | The calibration value of the stimulus current in mA's. This is the max. current applied to the subject.
tactstim_calibration_value | The byte value representation of the calibrated current
tactstim_pulse_milliamp | The actual current in mA's, applied to the subject when pulsing.
tactstim_pulse_value | The actual byte value representation that is sent to the Tactile Stimulator
tactstim_pulse_duration_ms | The pulse duration time in ms
tactstim_time_last_pulse | Unique time stamp in seconds from the moment of the shock

## vas_evt
The *vas_evt* plugin does not work standalone, but requires a link with a custom designed sketchpad screen to build the GUI!

## vas_gui
The *vas_gui* plugin does not work standalone, but requires a link with a custom designed sketchpad screen to build the GUI!
