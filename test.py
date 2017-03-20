from communications.communications import Comms
from threading import Thread
from postprocessing.world import World
import time
import serial
import re

global comms

def pos():
	with open(comms.outputFilename) as f:
		log = f.readlines()
		positions = log[len(log)-2]
		positions = [int(pos) for pos in positions.split() if pos[1:].isdigit() or pos.isdigit()]
	return positions

def getCompass():
	with open(comms.outputFilename) as f:
		log = f.readlines()
		floatRegex = re.compile(r'(\-?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')
		line1 = floatRegex.findall(log[len(log)-5])
		line2 = floatRegex.findall(log[len(log)-4])
		line3 = floatRegex.findall(log[len(log)-3])
		line4 = floatRegex.findall(log[len(log)-2])
		Raw = [int(x) for tuple in line1 for x in tuple if x]
		Scaled = [float(x) for tuple in line2 for x in tuple if x and not x.startswith('.')]
		Heading = [float(x) for tuple in line3 for x in tuple if x and not x.startswith('.')]
		ArctanYX = [float(x) for tuple in line4 for x in tuple if x and not x.startswith('.')]
	return Raw, Scaled, Heading, ArctanYX

if __name__ == "__main__" :

	# setup World model
	World.set_colours('yellow' , 'pink')
	pitch_number = int(0)
	World.set_globals(0 , 'left')

	# start Coms
	comms = Comms()
	comms.start()
	time.sleep(2)
	while True:
		cmd = raw_input("Please enter a command: ")
		if cmd == 'go':
			comms.stop()
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
			comms.turn(raw_input('Degrees: '), raw_input('Corrections: '))
		elif cmd == 'kick':
			comms.stop()
			comms.kick(10)
		elif cmd == 'hasball':
			pass
		elif cmd == 'reverse':
			comms.stop()
			dist = raw_input('Distance: ')
			comms.reverse(dist)
		elif cmd == 'abort':
			comms.abort()
		elif cmd == 'grab':
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
		elif cmd == 'crash':
			comms = Comms()
			comms.start()
		elif cmd == 'getpos':
			comms.stop()
			comms.getpos()
			time.sleep(1)
			print("Positions:", pos())
		elif cmd == 'resetpos':
			comms.stop()
			comms.resetpos()
			time.sleep(1)
			print("Positions:", pos())
		elif cmd == 'getcompass':
			comms.stop()
			comms.getcompass()
			time.sleep(1)
			#X: Raw/Scaled[0]; Y: Raw/Scaled[1]; Z: Raw/Scaled[2]
			#Radians: Heading[0]; Degrees: Heading[1]
			"""Raw, Scaled, Heading, ArctanYX = getCompass()
			print("Raw: ", Raw)
			print("Scaled: ", Scaled)
			print("Heading: ", Heading)
			print("ArctanYX: ", ArctanYX)
		elif cmd == 'calibrate':
			comms.port.write(bytes(';'))
			time.sleep(1)
			#X: Raw/Scaled[0]; Y: Raw/Scaled[1]; Z: Raw/Scaled[2]
			#Radians: Heading[0]; Degrees: Heading[1]
			Raw, Scaled, Heading, ArctanYX = getCompass()
			print("Raw: ", Raw)
			print("Scaled: ", Scaled)
			print("Heading: ", Heading)
			print("ArctanYX: ", ArctanYX)"""
