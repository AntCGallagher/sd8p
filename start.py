from visionwrapper import VisionWrapper
from threading import Thread
from postprocessing.world import World
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
	parser.add_argument("record" , help="add if you would like to record", nargs='?')
	parser.add_argument("extras" , help="add if you would like to show vision features for debugging", nargs='?')
	args = parser.parse_args()

	# setup World model
	World.set_colours(args.team , args.our)
	pitch_number = int(args.pitch)
	World.set_globals(pitch_number , args.side)


	if (args.record == 'record'):
		record = True
	else:
		record = False
	if (args.extras == 'extras'):
		extras = True
	else:
		extras = False
	# start vision system in background thread
	vis = VisionWrapper(pitch=pitch_number, record=record, extras=extras)
	t = Thread(target = vis.run)
	t.daemon = True
	t.start()

	inp = ""
	strategy = Strategy()
	while inp != "s" or inp != "c":
		inp = raw_input("stop or calibrate (s/c)? : ")
		if inp == "s":
			strategy.stop()
		if inp == "c":
			while inp != "done":
				inp = raw_input("calibrate and type done: ")
			while inp != "s" or inp != "t":
				inp = raw_input("tests/start? (t/s): ")
				if inp == "s":
					verbose = raw_input("Verbose debug? (y/n)")
					while inp != "y":
				 		inp = raw_input("start? (y/n))")
						if inp == "y":
							strategy.start4(verbose)
				if inp == "t":
					strategy.tests()
