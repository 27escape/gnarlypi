# Hardware Setup

You have the choice of keep in the software on the mini SD card and booting from that and adding other storage which could be removable for simpler copying of files to your computer or setting up something more permanent.

- boot from SD card, store to USB connected device or NVME
- copy 'system' to NVME and boot from that, store to same NVME or USB
- copy 'system' to NVME and boot from that, store to separate NVME
- copy 'system' to USB and boot from that, store to same USB

It al depends what you have available and how much you are willing to spend to create your solution.

For my PI Zero 2, I will investigate using a USB device as the boot/storage device.

If using a different device (or partition) to store your files, then remember that you will need to run the configuration script `./display_config.sh` to ensure that any copied files are placed in the right directory.

## Raspberry PI options

I started developing with a 4GB PI 5, though a 2GB version is now available, which is likely quite suitable for this application.

I am also trialling a PI Zero 2 WH, though will have to see how it copes samba and and web software running, this may be a reduced operating option, having a removable USB drive of some sort may help here with copy files onto computers.

## NVME options

For Pi 5's, there are a number of good devices to choose from that be connected via PCIe

- [NVME Base Duo](https://thepihut.com/products/nvme-base-duo-for-raspberry-pi-5) - boot from one store to the other, useful if you want a 4TB storage drive
- [NVME Base](https://thepihut.com/products/nvme-base-for-raspberry-pi-5-nvme-base)
- [Hat Drive bottom](https://thepihut.com/products/hatdrive-bottom-for-raspberry-pi-5)
- [Hat drive Nano](https://thepihut.com/products/hatdrive-nano-for-raspberry-pi-5) - its tiny and cheap, whats not to like!

Argon make some cases that include NVME expansion options, I think there is one for the PI 4 too, could be worth looking at

For something barebones that you may build into a case, especially if not using a PI 5, then maybe a USB enclosure such as [ELUTENG-M-2-NVME-NGFF-Converter · Amazon US](https://www.amazon.com/ELUTENG-M-2-NVME-NGFF-Converter/dp/B0BJCYR1P7/) or [ELUTENG-M-2-NVME-NGFF-Converter · Amazon UK](https://www.amazon.co.uk/ELUTENG-M-2-USB-Adapter-3-1-Black/dp/B0BGPJMJ43/r)


## Display options

I am a bit wary of buying older display hats and the like, as they are often not very well supported on the newer 64bit OS's and may not receive updates, some of the waveshare devices fall into this category and the ones I have purchased are now essentially unusable :(

Until I have created a web app to display status, I probably will not investigate small HDMI displays, but will focus on small low cost displays (< £25), ideally with buttons such as

- [Adafruit 128x64 OLED Bonnet](https://thepihut.com/products/adafruit-128x64-oled-bonnet-for-raspberry-pi-ada3531)
- [Adafruit PiOLED - 128x32 Monochrome OLED](https://thepihut.com/products/adafruit-pioled-128x32-monochrome-oled-add-on-for-raspberry-pi-ada3527)
- [GFX HAT - 128x64 LCD Display with RGB Backlight and Touch Buttons](https://thepihut.com/products/gfx-hat-128x64-lcd-display-with-rgb-backlight-and-touch-buttons)
- [Adafruit 1.3" Color TFT Bonnet for Raspberry Pi (240x240 TFT + Joystick Add-on)](https://thepihut.com/products/adafruit-1-3-color-tft-bonnet-for-raspberry-pi)
- [Display HAT Mini](https://thepihut.com/products/display-hat-mini)
- [Adafruit Mini PiTFT 1.3" - 240x240 TFT](https://thepihut.com/products/adafruit-mini-pitft-1-3-240x240-tft-add-on-for-raspberry-pi)

I just did a quick trawl of https://thepihut.com/ for these based on price and being either [Pimoroni](https://shop.pimoroni.com/collections/displays?tags=Raspberry%20Pi) or [Adafruit](https://www.adafruit.com/category/63) devices.

I did initially consider ePaper screens but these would not be able to keep up with the copy updates, so could only be used for some of the messages, though you could combine an ePaper device with one of the LED display devices and write your own status program. 


## Configuring your drives



## Partitioning a drive > 2TB

If using a drive > 2TB, then linux generally will not partition it correctly, this is an issue if you are using it as a boot drive! This will go wrong when you try to expand the 'disk' to fit the available space when using `raspi-config`, work arounds would be to continue booting from a SD card and just keep data on the large drive, use one of the dual NVME boards and a small additional NVME drive and use that as the boot device, use a spare USB drive or a USB key type drive.

If you have another computer, windows or mac, then you can use that to initialise the drive, use all of it and format it to be exFAT, this allows it to be read/write on pretty much any computer.

To partition it for ext4 on linux, then ... :TODO:


## Mounting your drive

If you are not booting from a large drive, such as the NVME drive, then attaching a separate USB drive will be the way to go for storing your photos onto.

It is likely that the user you are going to run things as is user 1000, however you can check this by running `id`

Attach the USB drive to your rPi and run `blkid` this will give us info about connected as follows

```
/dev/mmcblk0p1: LABEL_FATBOOT="bootfs" LABEL="bootfs" UUID="91FE-7499" BLOCK_SIZE="512" TYPE="vfat" PARTUUID="123c0f19-01"
/dev/mmcblk0p2: LABEL="rootfs" UUID="22f22fa2-e005-4ccc-86e6-19da1069914d" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="123c0f19-02"
/dev/sda1: LABEL="somedrive UUID="E432-FDBC" BLOCK_SIZE="512" TYPE="exfat" PTTYPE="dos" PARTUUID="89e29715-12324-5678-a33d-88efc3816e59"
```

As we can see, there is a drive connected to `/dev/sda1`, the important part of this output is the "UUID" field with the value `E432-FDBC`. This is for my drive, yours will be different, take a note of it

Now we will create the mount point for this drive and add it to `/etc/fstab` so that it will mount whenever the system is rebooted 

```
sudo mkdir /mnt/fstab
sudo vi /etc/fstab
```

and then, replacing your UUID value, add the following to the end of the fstab file
```
UUID=E432-FDBC /mnt/usb_data   exfat    defaults,noatime,user,rw,exec,auto,rw,nofail,x-systemd.automount,nosuid,nodev,uid=1000,gid=1000,fmask=0022,dmask=0022,iocharset=utf8,errors=remount-ro        1 1
```

To check things are working, we need to reload `/etc/fstab` and we can do that with the following command

```
sudo systemctl daemon-reload
```

Then we can attempt to mount the drive with `sudo mount -a` and we should be able to see, using the `mount` command that the drive has been mounted to `/mnt/usb_data`

Finally, we will link this to the directory we will be saving the data to `$HOME/usb_data`

```
ln -s /mnt/usb_data "$HOME/usb_data"
```
