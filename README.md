OpenSesame Plugin Collection for EVT USB-devices
=================================================

*An OpenSesame plugin collection for sending stimulus synchronization triggers and for response collection through EventExchanger v2 USB hardware.*  

Copyright 2010-2024 Mark Span (<m.m.span@rug.nl>), M. Stokroos (<m.stokroos@rug.nl>)

Contributions: This code is based on the work of Eise Hoekstra and Mark M. Span. The code is debugged and largely rewritten for OpenSesame 4 by Martin Stokroos.

## 1. About
The OpenSesame plugin collection for use with Event-Exchanger (EVT-2) USB-devices.

EVT-devices and the associated plugins are developed by the [Research Support](https://myuniversity.rug.nl/infonet/medewerkers/profiles/departments/11422) department from the faculty of Behavioural and Social Sciences from the University of Groningen.

The currently supported OpenSesame version is from v4.0

The following plugins are available:

icon | plugin | Description | OpenSesame back-end | operating system | Status
---- | ------- | ----------- | ------------------- | ---------------- | ------
![](opensesame_plugins/evt_plugins/evt_trigger/evt_trigger_large.png) | evt_trigger | plugin for event exchanger EVT-2,3 and 4 variants for generating triggers | PyGame, PsychoPy | Windows | ok
![](opensesame_plugins/evt_plugins/response_box/response_box_large.png) | response_box | plugin for all of the RSP12x button response box variants with 1-8 buttons | PyGame, PsychoPy | Windows | ok
![](opensesame_plugins/evt_plugins/rsp_pygame/rsp_pygame_large.png) | rsp_pygame | plugin for RSP12x button response box variants with 1-8 buttons | PyGame | Windows, Linux | ok
![](opensesame_plugins/evt_plugins/tactile_stimulator/tactile_stimulator_large.png) | tactile_stimulator | plugin for the Electrotactile Stimulator (SHK-1B) 0-5mA | PyGame | Windows | ok
![](opensesame_plugins/evt_plugins/vas_evt/vas_evt_large.png) | vas_evt | A Visual Analog Slider plugin controlled via an encoder knob connected to the EVT-2 | PyGame | Windows | planned
![](opensesame_plugins/evt_plugins/vas_gui/vas_gui_large.png) | vas_gui | A Visual Analog Slider plugin controlled via the PC-mouse on a predefined canvas (sketchpad) | PyGame | Windows, Linux | Mouse response not ok in Linux.
![](opensesame_plugins/evt_plugins/rgb_led_control/rgb_led_control_large.png) | rgb_led_control | plugin for multi-color LED response boxes | PyGme | Windows | not validated

### Package dependencies
The plugins are dependent on the Python module pyevt and the underlying hidapi package.

[https://pypi.org/project/hidapi/](https://pypi.org/project/hidapi/)

*pyevt* and *hidapi* are installed from the Python Console in OpenSesame with the single command:

`!pip install --user pyevt`

NOTE: Currently, the plugin package is not released as pip package yet. Instead, clone this repository and copy the plugins manually into your OpenSesame python package folder.

### Environmental settings
By default, the OpenSesame 4.0 plugins are installed as python site-package and automatically loaded at the startup.
When the plugins are located somewhere else, add your path to the python-path of OpenSesame in the `environment.yaml` file in the OpenSesame program directory (The OPENSESAME_plugin_PATH is old style). See for the instructions here: [https://rapunzel.cogsci.nl/manual/environment/](https://rapunzel.cogsci.nl/manual/environment/) 

- Linux
In Linux (Ubuntu) permission for using EVT (HID) devices should be given by adding the next lines in a file named, for example: `99-evt-devices.rules` in `/etc/udev/rules.d`:

```
# /etc/udev/rules.d/99-evt-devices.rules

# All EVT devices
SUBSYSTEM=="usb", ATTR{idVendor}=="0004", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0008", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0009", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0114", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0208", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0308", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0408", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0508", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0604", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0808", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0909", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="1803", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="1807", MODE="0660", GROUP="plugdev"
```

The user should be member of the `plugdev` -group.

## 2. Plugin Descriptions

### evt_trigger
Possible Modes:

- Clear output lines
- Write output line
- Invert output lines
- Pulse output lines

### response_box
Collects responses from a 1 to 8 button RSP-12x response box.

After the prepare phase of the plugin, a workspace variable `connected_device_plugin_instance_name` is created to check if the actual tactile-stimulator device is really detected and connected to the plugin.

### rsp_pygame
This response-box plugin works for EVT devices as well for joystick devices. It makes use of the pygame joystick API and is platform independent. 

### tactile_stimulator
The tactile_stimulator plugin operates in two modes. Usually two instances of this plugin are used in the OpenSesame experiment. Mode-I, the `Calibration`-mode should always precede the `Stimulate`-mode. In `Calibration`-mode the upper limit of stimulus-current threshold is set between 0 and 5mA rms. In the `Stimulate`-mode, a percentage of the stimulus-current upper limit is set to be applied to the subject. The `Calibration`-mode can be used standalone for instance to precondition the subject. The pulse duration can be extended up to 2000ms.

After the prepare phase of the plugin, a workspace variable `connected_device_plugin_instance_name` is created to check if the actual tactile-stimulator device is really detected and connected to the plugin.

Here below follows a list of variables that appear in the OpenSesame variable inspector when using the tactile_stimulator plugin:

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
A Visual Analog Slider plugin controlled by an EVT rotary or linear encoder.
The *vas_evt* plugin does not work standalone, but requires a linkage to a custom designed sketchpad screen.

### vas_gui
A Visual Analog Slider plugin. The *vas_gui* plugin does not work standalone, but requires a linkage to a custom designed sketchpad screen with an analog slider design!

Here below is the list of the variables that will appear in the OpenSesame variable inspector when using the vas_gui plugin:

variable name | description
------------- | -----------
*vas_response* | This value is the reading from the VAS object, ranging from 0 to 100.
*vas_response_time* | this is the repsonse time in ms. The value -1 means that the timeout period was reached.

### rgb_led_control
This plugin works for the RSP-LT device, a response-box with RGB-controlled LED buttons.

## 3. LICENSE
The evt-plugins collection is distributed under the terms of the GNU General Public License 3.
The full license should be included in the file COPYING, or can be obtained from

[http://www.gnu.org/licenses/gpl.txt](http://www.gnu.org/licenses/gpl.txt)

This plugin collection contains the work of others.

## 4. Documentation
Installation instructions and documentation on OpenSesame are available on the documentation website:

[http://osdoc.cogsci.nl/](http://osdoc.cogsci.nl/)

Evt-plugin information:

[https://markspan.github.io/evtplugins/](https://markspan.github.io/evtplugins/)