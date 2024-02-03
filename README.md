# Butcher shop label printer
Raspberry PI based label-printer for my butcher shop using the following hardware:
* Raspberry PI >2
* Brother QL-800
* RasClock RTC Module
* Raspberry Pi Touchscreen Pi Touch Display 7
* Optionally a buzzer module operatable from GPIO
* Optionally a double relais board operatable from GPIO
* Optionally a kern scale with RS232 interface (Or any other compatible scale but only a scale module for the kern scale is provided)

## Label Example (With current template)
![LosTresCazadores_example](https://user-images.githubusercontent.com/1346821/128201470-6f1ff850-afa4-4e39-b2d0-9e2977cb308b.png)

## Raspberry PI


### Pinout
By default the following GPIO are used:
* GPIO 26 - Buzzer 5V
* GPIO 16 - Relay 5V (On/Off for scale and printer)


## OS
This printer uses the Raspian OS Lite. The minimal recommended SD card size is 8Gb.

## Setup
Create a user named bslp (the group bslp is used in some locations)

### System packages
* Install python-dev: `$sudo apt install python-dev`
* Install opengl: `$sudo apt install freeglut3-dev`
* Install libmtdev: `$sudo apt install libmtdev-dev`
* Install libfreetype6-dev ???

### Poetry
* First install the required packages using `$poetry install`
* Then run the app using `$poetry run bslp`

## Config


### Turning off the display
This solution does the same as Raspbian does.
The following service file should be added to `/lib/systemd/system/rpi-display-backlight.service`
```service
[Unit]
Description=Turns off Raspberry Pi display backlight on shutdown/reboot
ConditionPathIsDirectory=/proc/device-tree/rpi_backlight
DefaultDependencies=no
Before=umount.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c ‘/bin/echo 1 > /sys/class/backlight/rpi_backlight/bl_power’

[Install]
WantedBy=reboot.target halt.target poweroff.target
```
This service must be enabled using `$sudo systemctl enable rpi-display-backlight`

### Add udev rule for the printer
In order to allow any user to use the USB label printer an according udev rule must be added.
First turn on the printer then connect the USB cable to the Raspberry Pi. When calling `lsusb` a line like `Bus XXX Device YYY: ID AAAA:BBBB Brother Industries, Ltd` will appear. To add an udev rule just append the line `SUBSYSTEM=="usb", ATTRS{idVendor}=="AAAA", ATTRS{idProduct}=="BBBB", GROUP="bslp", MODE="0666"` to `/etc/udev/rules.d/99-com.rules`. For Brother devices this vendor ID should be `04f9`.

`$echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="04f9", ATTRS{idProduct}=="209b", GROUP="bslp", MODE="0666"' | sudo tee -a /etc/udev/rules.d/99.com.rules`

### Setup RasClock
First the two interfacing methods SPI and I2C must be activated in the raspi-config. Then follow the instructions in [the instructions](https://afterthoughtsoftware.com/products/rasclock).

### Enable auto-login on tty1
Open the raspi config `$ sudo raspi-config` -> System -> S5 Boot / Auto Login -> B2 Console Autologin.

### Kivy config
Those changes might need to be done in the kivy config file (`/home/sysop/.kivy/config.ini`)
* To deactivate the vitual keyboard complete the line `keyboard_mode = ` with `system`
* If double keystrokes occur, remove the line `%(name)s = probesysfs,provider=hidinput`.

### Hardware Modifications
The label printer and the scale controller can be modified so the ON/OFF buttons can be activated with the relais. 
Both are quite easy to open, solder, and to lead the wires out of the case. The wires may not be put on a single relais!


## 3D Printing
The STL files for the display mount and the mount for the Brother QL-800 can be found in the `3dprint` orphan branch.
