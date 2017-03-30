from visionwrapper import VisionWrapper
from threading import Thread
from postprocessing.world import World
from communications.communications import Comms
from command.strategy import Strategy
import time
from vision import tools
import numpy as np
import cv2
import json
import socket
import os
import cPickle

"""
This script will be used to test some of the robot's functionalities.
"""

if __name__ == "__main__" :
	PATH = os.path.dirname(os.path.realpath(__file__))

	# parse arguments
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("pitch", help="[0] Main pitch (3.D04), [1] Secondary pitch (3.D03)")
	parser.add_argument("team" , help="yellow or blue" )
	parser.add_argument("our" , help="our 3 dots are: pink or bright_green" )
	parser.add_argument("side" , help="which side of the pitch is ours, left or right?")
	parser.add_argument("opt1" , help="add 'record' if you would like to record or add 'extras' to show vision features for debugging", nargs='?')
	parser.add_argument("opt2" , help="add 'record' if you would like to record or add 'extras' to show vision features for debugging", nargs='?')
	parser.add_argument("opt3" , help="add 'verbose' if you would like to record or add 'extras' to show vision features for debugging", nargs='?')
	args = parser.parse_args()

	# setup World model
	World.set_colours(args.team , args.our)
	pitch_number = int(args.pitch)
	World.set_globals(pitch_number , args.side)


	if (args.opt1 == 'record' or args.opt2 == 'record' or args.opt3 == 'record'):
		record = True
	else:
		record = False
	if (args.opt1 == 'extras' or args.opt2 == 'extras' or args.opt3 == 'extras'):
		extras = True
	else:
		extras = False
	if (args.opt1 == 'verbose' or args.opt2 == 'verbose' or args.opt3 == 'verbose'):
		verbose = "y"
	else:
		verbose = "n"

	# start vision system in background thread
	vis = VisionWrapper(pitch=pitch_number, record=record, extras=extras)
	t = Thread(target = vis.run)
	t.daemon = True
	t.start()

	inp = ""
	strategy = Strategy()
	comms = Comms()
	while True:
		try:
			comms_active = comms.start()
			if comms_active:
				while inp != "t" or inp != "s" or inp != "r":
					inp = raw_input("Tests, start or reset? (t/s/r) : ")
					if inp == "s":
						strategy.start4(comms,verbose)
					if inp == "t":
						strategy.tests(comms)
					if inp == "r":
						comms.reset()
			else:
				print "Check RF!"
		except:
			os._exit(1)
