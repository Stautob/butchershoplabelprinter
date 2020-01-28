# Butcher shop label printer
Raspberry PI based label-printer for my butcher shop using the following hardware:
* Raspberry PI >2
* Brother QL-800
* RasClock RTC Module
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

### Add udev rule for the printer
In order to allow any user to use the USB label printer an according udev rule must be added.
First turn on the printer then connect the USB cable to the Raspberry Pi. When calling `lsusb` a line like `Bus XXX Device YYY: ID ... Brother Industries, Ltd` will appear. To get the VendorId required for the udev rule, the following command is executed: `udevadm info -a -p $(udevadm info -q pat /dev/bus/usb/XXX/YYY)`. In the output one looks for a device that has a line line `ATTR{product}="QL-800"`, or whatever the name of the used printer. From the same block, the value of `ATTR{idVendor}`, in my case `04f9`, is written down.
To add an udev rule just append the line `SUBSYSTEM=="usb", ATTR={idVendor}=="04f9", MODE="0666"` to `/etc/udev/rules.d/99-com.rules`

### Setup RasClock
First the two interfacing methods SPI and I2C must be activated in the raspi-config. Then follow the instructions in [the instructions](https://afterthoughtsoftware.com/products/rasclock).

### Enable auto-login on tty1
To login automatically after boot, the original `/etc/systemd/system/getty.target.wants/getty@tty1.service` must be moved to `/etc/systemd/system/getty.target.wants/getty@tty2.service`. Then the file `/etc/systemd/system/autologin@.service` must be symlinked to `/etc/systemd/system/getty.target.wants/getty@tty1.service`. Next, the username in the `autologin@.service` file must be changed from `pi` to `sysop`. After a reboot the user sysop should be logged in automatically.

### Kivy config
Those changes might need to be done in the kivy config file (`/home/sysop/.kivy/config.ini`)
* To deactivate the vitual keyboard complete the line `keyboard_mode = ` with `system`
* If double keystrokes occur, remove the line `%(name)s = probesysfs,provider=hidinput`.


## 3D Printing
The STL files for the display mount and the mount for the Brother QL-800 can be found in the `3dprint` orphan branch.
