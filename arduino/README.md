# The Arduino

## RF Setup

To setup the RF stick, and Arduino board, we need to run a series of commands. **NOTE: There is no visual feedback in `screen` when you're typing, so be careful.**

Our Group number is 08, and our frequency band is 0x47. (from <http://www.inf.ed.ac.uk/teaching/courses/sdp/equipmentGuide.pdf>)

When you plug in a device via USB, it will create a folder in `/dev` called something along the lines of `/dev/ttyACMX` where X is some number. To figure out which device is which, navigate to /dev/ and run `ls`, then plug in the device to a USB port and run `ls` again, taking note of which new folder shows up. The final digit will be the port number.

Type in the following commands to set up the devices, pressing enter after each one **EXCEPT** `+++` (from <http://www.inf.ed.ac.uk/teaching/courses/sdp/srf_setup.txt>)

To exit press ctrl-a k

###### RF stick (X is the port number of the RF stick)
```
$ screen /dev/ttyACMX 115200 

+++
ATRE
ATAC
ATWR
ATDN

+++
ATID0008
ATAC
ATRP1
ATCN47
ATAC
ATWR
ATDN
```

###### Arduino board (X is the port number of the Arduino connected via USB)
```
$ screen /dev/ttyACMX 115200

+++
ATRE
ATAC
ATWR
ATDN

+++
ATID0008
ATAC
ATRP1
ATAC
ATCN47
ATAC
ATBD 1C200
ATAC
ATWR
ATDN
```