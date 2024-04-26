OpenSesame Plug-in Collection for EVT USB-devices
=================================================

*An OpenSesame plug-in collection for sending stimulus synchronization triggers and response collection through EventExchanger-2 USB hardware.*  

Copyright, 2024, Martin Stokroos

Contributions: This code is based on the work of Eise Hoekstra and Mark M. Span. The code is expanded, debugged and polished by Martin Stokroos.


## 1. About
-----------
The OpenSesame plug-in collection for use with Event-Exchanger (EVT-2) USB-devices. EVT-devices and belonging plug-ins are developed by the [Research Support](https://myuniversity.rug.nl/infonet/medewerkers/profiles/departments/11422) Department from the faculty of Behavioural and Social Sciences, University of Groningen

The currently supported OpenSesame version is v4.0

The following plugins are available:

Plugin | Description | OpenSesame back-end | operating system | Status
------ | ----------- | ------------------- | ---------------- | ------
evt_trigger | Plugin for event exchanger EVT-2,3 and 4 variants for generating triggers | PyGame, PsychoPy | Windows | ok
response_box | Plugin for all of the RSP12x button response box variants with 1-8 buttons | PyGame, PsychoPy | Windows |
rsp_pygame | Plugin for RSP12x button response box variants with 1-8 buttons | PyGame | Windows, Linux | ok
tactile_stimulator | Plugin for the Electrotactile Stimulator (SHK-1B) 0-5mA | PyGame | Windows | ok
vas_evt | A Visual Analog Slider plugin controlled via an encoder knob connected to the EVT-2 | PyGame | Windows | not validated
vas_gui | A Visual Analog Slider plugin controlled via the PC-mouse on a predefined canvas (sketchpad) | PyGame | Windows, Linux | Mouse response not ok on Linux.
rgb_led_control | Plugin for multi-color LED control | PyGme | Windows | not validated

### Package dependencies
The plugins are dependent on the Python module pyevt and the underlying hidapi package.

[https://pypi.org/project/hidapi/](https://pypi.org/project/hidapi/)

*pyevt* and *hidapi* are installed from the Python Console in OpenSesame with the single command:

`!pip install --user pyevt`

NOTE: Currently, the plugin package is not released as pip package yet. Instead, clone this repository and copy the plugins manually into your OpenSesame python package folder.

### Environmental settings
By default the OpenSesame 4.0 plugins are installed as python site-package and automatically loaded at startup.
When the plugins are located somewhere else, add your path to the python-path of OpenSesame in the `environment.yaml` file in the OpenSesame program directory (The OPENSESAME_PLUGIN_PATH is old style). See for the instructions here: [https://rapunzel.cogsci.nl/manual/environment/](https://rapunzel.cogsci.nl/manual/environment/) 

### evt_trigger
Possible Modes:

- Write output line
- Reset output lines
- Invert output lines
- Pulse output lines

### response_box

### rsp_pygame

### tactile_stimulator
description ...

List of the variables that appear in the OpenSesame variable inspector when using the tactile_stimulator plugin:

variable name | description
------------- | -----------
*tactstim_calibration_perc* | The percentage of the slider setting for the stimulus current of up to 5mA rms max.
*tactstim_calibration_milliamp* | The calibration value of the stimulus current in mA's. This is the max. current applied to the subject.
*tactstim_calibration_value* | The byte value representation of the calibrated current.
*tactstim_pulse_milliamp* | The actual current in mA's, applied to the subject when pulsing.
*tactstim_pulse_value* | The actual byte value representation that is sent to the tactile stimulator.
*tactstim_pulse_duration_ms* | The pulse duration time in ms.
*tactstim_time_last_pulse* | Unique time stamp in seconds from the moment of the shock.

### vas_evt
The *vas_evt* plugin does not work standalone, but requires a linkage to a custom designed sketchpad screen from the GUI!

### vas_gui
The *vas_gui* plugin does not work standalone, but requires a linkage to a custom designed sketchpad screen from the GUI!

Here below is the list of the variables that will appear in the OpenSesame variable inspector when using the vas_gui plugin:

variable name | description
------------- | -----------
*vas_response* | This value is the reading from the VAS object, ranging from 0 to 100.
*vas_response_time* | this is the repsonse time in ms. The value -1 means that the timeout period was reached.

### rgb_led_control

## 2. LICENSE
-------------

The evt-plugins collection is distributed under the terms of the GNU General Public License 3.
The full license should be included in the file COPYING, or can be obtained from

- <http://www.gnu.org/licenses/gpl.txt>

This plug-in contains works of others.

## 3. Documentation
-------------------

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <http://osdoc.cogsci.nl/>