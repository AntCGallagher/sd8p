from communications.originalcomms import Coms
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
	Coms.start_comunications()
	time.sleep(2)
	while True:
		cmd = raw_input("Please enter a command: ")
		if cmd == 'go':
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
			deg = raw_input('Degrees: ')
			Coms.turn(deg)
		elif cmd == 'kick':
			Coms.stop()
			stren = raw_input('Strength: ')
			Coms.kick(stren)
		elif cmd == 'hasball':
			pass
		elif cmd == 'reverse':
			pass
		elif cmd == 'abort':
			Coms.abort()
		elif cmd == 'grab':
			grab = raw_input('0 to grab 1 otherwise: ')
			Coms.grab(grab)
		elif cmd == 'prepkick':
			pass
		elif cmd == 'receive':
			pass
		elif cmd == 'getball':
			pass
