# butchershoplabelprinter
Raspberry PI based label-printer for my butcher shop using the following hardware:
* Raspberry PI >2
* Brother QL-800
* Raspberry Pi Touchscreen Pi Touch Display 7

## OS
This printer uses the [KivyPie](http://kivypie.mitako.eu) distribution.
After installation, the root file system should be expanded to the whole sd-card using the command
`sudo pipaos-config --expand-rootfs` followed by a restart.

## Setup
The tmp partition is to small to install the pip modules as usual. Using this command it will work: 

`TEMPDIR=/home/sysop/tmp/ sudo pip3 install --cache-dir=/home/sysop/tmp/ --build /home/sysop/tmp/ [package]`
### System packages
* Install libfreetype6-dev
### PIP packages
* pipenv
* pillow
* brother-ql

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
This service must be enabled using `sudo systemctl enable rpi-display-backlight`

### Kivy config
Those changes might need to be done in the kivy config file (`/home/sysop/.kivy/config.ini`)
* To use a vitual keyboard complete the line `keyboard_mode = ` with `systemanddock`
* If double keystrokes occur, remove the line `%(name)s = probesysfs,provider=hidinput`.
