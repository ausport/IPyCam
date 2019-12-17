# IPyCam
IP camera codebase for connecting Prosilica GigE devices.

### Requirements

IPyCam depends on the Aravis + GStreamer frameworks.

The Aravis Project is an open source plugin, which detects genicam devices.

GStreamer should be pre-installed on Jetson devices.  Aravis will need to be 
additionally installed.

The GitHub repository is maintained at: https://github.com/AravisProject

I currently use the latest stable version (0.6.x).
 
Download and extract the tar:

```
wget http://ftp.acc.umu.se/pub/GNOME/sources/aravis/0.6/aravis-0.6.4.tar.xz
tar -xf aravis-0.6.4.tar.xz
```

The current version of `intltool` may need to be installed:

```angular2html
sudo apt-get install intltool
```

Install the Aravis plugins.

```angular2
cd aravis-0.6.4
./configure
make
sudo make install
```


#### USB Permissions

[From the website] By default, USB devices permissions may not be sufficient to allow 
any user to access the USB3 cameras. This permissions can be changed by using an 
udev rule file. 
This file must be placed in `/etc/udev/rules.d` directory 
(The exact location may depend on the distribution you are using). 
This file only contains declarations for a couple of vendors. 
If you want to add an entry with the vendor of your camera, the output of 
`lsusb` command will give you the vendor id, which is the first 4 digits of the ID field.

The aravis.rules file is configured for the Jai USB3 camera and available in this repository.

```angular2
# JAI Corporation GO-2400C-USB
SUBSYSTEM=="usb", ATTRS{idVendor}=="14fb", MODE:="0666", TAG+="uaccess", TAG+="udev-acl"
```

It should be copied to the `/etc/udev/rules.d` directory.

**Reboot.**


```angular2
export GST_PLUGIN_PATH="/usr/local/lib/gstreamer-1.0"
```

Test the device with:

```angular2html
cd /Tests
./arv-camera-test 
```

If everything works...

```angular2html
Looking for the first available camera
vendor name           = JAI Corporation
model name            = GO-2400C-USB
device id             = (null)
image width           = 1936
image height          = 1216
horizontal binning    = 1
vertical binning      = 1
payload               = 2354176 bytes
exposure              = 6210 µs
gain                  = 1 dB
uv bandwidth limit     = 0 [1..-1]
Frame rate = 62 Hz
Frame rate = 52 Hz
Frame rate = 52 Hz
Frame rate = 52 Hz
```


