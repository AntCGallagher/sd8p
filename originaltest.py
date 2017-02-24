from communications.originalcomms import Coms
from threading import Thread
from postprocessing.world import World
import time
import serial
"""

"""

def getPos():
	Coms.com.ser.write(bytes('Q'))
	time.sleep(1)
	with open(Coms.com.outputFilename) as f:
		log = f.readlines()
		positions = log[len(log)-2]
		positions = [int(pos) for pos in positions.split() if pos[1:].isdigit() or pos.isdigit()]
	#positions[3] = left wheel;
	#positions[5] = right wheel;
	#positions[4] = omni wheel;
	#positions[2] = kicker;
	return positions

def resetPos():
	Coms.com.ser.write(bytes('Z'))
	time.sleep(1)
	with open(Coms.com.outputFilename) as f:
		log = f.readlines()
		positions = log[len(log)-2]
		positions = [int(pos) for pos in positions.split() if pos[1:].isdigit() or pos.isdigit()]
	return positions

if __name__ == "__main__" :

	# setup World model
	World.set_colours('yellow' , 'pink')
	pitch_number = int(0)
	World.set_globals(0 , 'left')

	# start Coms
	#comms = Comms()
	Coms.start_comunications()
	time.sleep(2)
	while True:
		cmd = raw_input("Please enter a command: ")
		if cmd == 'go':
			Coms.stop()
			Coms.go()
		elif cmd == 'stop':
			Coms.stop()
		elif cmd == 'goxy':
			Coms.stop()
			fX = raw_input('from X: ')
			fY = raw_input('from Y: ')
			h = raw_input('Heading: ')
			tX = raw_input('to X: ')
			tY = raw_input('to Y: ')
			Coms.goxy(fX, fY, h, tX, tY)
		elif cmd == 'turn':
	   		Coms.stop()
			Coms.turn(raw_input('Degrees: '), raw_input('Corrections: '))
		elif cmd == 'kick':
			Coms.stop()
			Coms.kick(10)
		elif cmd == 'hasball':
			pass
		elif cmd == 'reverse':
			Coms.stop()
			dist = raw_input('Distance???: ')
			Coms.reverse(dist)
		elif cmd == 'abort':
			Coms.abort()
		elif cmd == 'grab':
			Coms.stop()
			Coms.grab(int(raw_input('1 to ungrab, 0 otherwise: ')))
		elif cmd == 'prepkick':
			pass
		elif cmd == 'receive':
			pass
		elif cmd == 'getball':
			pass
		elif cmd == 'reset':
			Coms.reset()
		elif cmd == 'crash':
			Coms = Comms()
			Coms.start()
		elif cmd == 'getPos':
			print("Positions:", getPos())
		elif cmd == 'resetPos':
			print("Positions:", resetPos())
