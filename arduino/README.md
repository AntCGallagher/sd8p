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

## Opcodes

Below are the Opcodes used by Craig Walton's group **(SUBJECT TO CHANGE DEPENDENT ON OUR IMPLEMENTATION)**

| Opcode | Name | Parameters | Description |
|:-------:|:----:|------------|-------------|
| 1 | RESET | None       | Tells arduino to reset the instruction counter to 0 |
| 2 | STOP  | None       | Halts and deletes all instructions |
| 3 | UPDATEWM | uint32_t, int16_t, int16_t, int16_t | Sends a new world model to the arduino |
| 4 | GO | None | Drives robot forward until halted |
| 5 | GOXY | int16_t, int16_t, int16_t, int16_t, int16_t | Drives robot to specified coordinates given its current coordinates |
| 6 | GETBALL | int16_t, int16_t, int16_t, int16_t, int16_t | Drives robot to coordinate, opening grabber and stopping upon detecting the ball |
| 7 | TURN | int16_t, uint8_t | Turns robot by specified degrees, second parameter is number of attempts for correction |
| 8 | GRAB | int8_t | Lifts (and keeps open) grabber or closes grabber |
| 9 | RECEIVE | uint32_t | Opens grabber to receive a pass until ball is detected or timeout reached |
| 10 | PREPKICK | uint8_t | Prepares kick of given strength
| 11 | KICK | uint8_t | Kicks for a given strength |
| 12 | REVERSE | uint16_t | Reverses robot a certain distance |
| 13 | ABORT | None | Same as STOP, but also closes grabber. Responds with `hasBall()` |
| 14 | HASBALL | None | Returns true if ball in robot's possession, false otherwise |
| 15 | RETARG | uint16_t, int16_t, int16_t | Updates target coordinates of GOXY or GETBALL |
| 16 | PENDEF | None | Initiates a penalty defence instruction |
| 17 | PENDEFUPD | int16_t | Updates the penalty defence instruction of where to move to |