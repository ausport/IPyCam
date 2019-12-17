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

Install the Aravis plugins.

```angular2
cd aravis-0.6.4
./configure
make
make install
```


#### USB Permissions

[From the website] By default, USB devices permissions may not be sufficient to allow 
any user to access the USB3 cameras. This permissions can be changed by using an 
udev rule file. There is a file example in Aravis sources, *src/aravis.rules*. 
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


