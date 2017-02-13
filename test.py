from communications.communications import Comms
from threading import Thread
from postprocessing.world import World
import time
"""

"""

if __name__ == "__main__" :

	# setup World model
	World.set_colours('yellow' , 'pink')
	pitch_number = int(0)
	World.set_globals(0 , 'left')

	# start comms
	comms = Comms()
	comms.start()
	time.sleep(2)
	while True:
		cmd = raw_input("Please enter a command: ")
		if cmd == 'go':
			comms.go()
		elif cmd == 'stop':
			comms.stop()
		elif cmd == 'goxy':
			comms.stop()
			fX = raw_input('from X: ')
			fY = raw_input('from Y: ')
			h = raw_input('Heading: ')
			tX = raw_input('to X: ')
			tY = raw_input('to Y: ')
			comms.goxy(fX, fY, h, tX, tY)
		elif cmd == 'turn':
	   		comms.stop()
			deg = raw_input('Degrees: ')
			comms.turn(deg)
	   		comms.stop()
			#deg = raw_input('Degrees: ')
			comms.turn(90)
		elif cmd == 'kick':
			comms.stop()
			comms.kick(10)
		elif cmd == 'hasball':
			pass
		elif cmd == 'reverse':
			comms.stop()
			dist = raw_input('Distance???: ')
			comms.reverse(dist)
		elif cmd == 'abort':
			comms.abort()
		elif cmd == 'grab':
			grab = raw_input('0 to grab 1 otherwise: ')
			# Coms.grab(grab)
			if grab == 0:
			    comms.grab(ungrab=False)
			else:
			    comms.grab(ungrab=True)
			comms.stop()
			comms.grab(int(raw_input('1 to ungrab, 0 otherwise: ')))
		elif cmd == 'prepkick':
			pass
		elif cmd == 'receive':
			pass
		elif cmd == 'getball':
			pass
		elif cmd == 'reset':
			comms.reset()
