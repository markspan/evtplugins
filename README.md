# evt_plugins
OpenSesame plugins for using RUG/BSS Event Exchanger (EVT) devices.
The currently supported OpenSesame version is v4.0

The following plugin collection is available:

Plugin | Description | Status
------ | ----------- | ------
evt_xx | Plugin for Event Exchanger (EVT) 2,3 and 4 variants for event-marking and triggering | not validated
response_box | Button response box variants with 1-4 buttons | not validated
rgb_led_control | multi-color LED control | not validated
tactile_stimulator | Electrotactile Stimulator 0-5mA | validated
vas |  | not validated
vas_2 |  | not validated

## Package dependencies
The plugins are dependent on the Python module pyevt and the underlying HIDAPI package.

[https://pypi.org/project/hidapi/](https://pypi.org/project/hidapi/)

pyevt and hidapi are installed from the Python Console in OpenSesame with the single command:

`!pip install --user pyevt`

## Environmental settings
Default the OpenSesame 4.0 plugins are installed as python site-package and automatically loaded at startup.
When the plugins are located somewhere else, add your path to the python-path of OpenSesame in the `environment.yaml` file in the OpenSesame program directory. See for the instructions here: [https://rapunzel.cogsci.nl/manual/environment/](https://rapunzel.cogsci.nl/manual/environment/) 

## evt_xx

## response_box

## rgb_led_control

## tactile_stimulator
description ...

List of the variables that appear in the OpenSesame variable inspector when using the TactileStimulator plugin:

variable name | description
------------- | -----------
tactstim_calibration_perc | The percentage of the slider setting for the stimulus current of 5mA max.
tactstim_calibration_milliamp | The calibration value of the stimulus current in mA's
tactstim_calibration_value | The byte value representation of the calibrated current
tactstim_pulse_milliamp | The actual current in mA's, applied to the Tactile Stimulator hardware
tactstim_pulse_value | The actual byte value representation that is sent to the Tactile Stimulator
tactstim_pulse_duration_ms | The (fixed) shock duration time in ms
tactstim_time_last_pulse | Unique time stamp in seconds from the moment of the last shock

## vas

## vas_2

