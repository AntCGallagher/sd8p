from visionwrapper import VisionWrapper
from threading import Thread
from postprocessing.world import World
from command.strategy import Strategy
import time

"""
This script will be used to test some of the robot's functionalities.
"""

if __name__ == "__main__" :

	# parse arguments
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("pitch", help="[0] Main pitch (3.D04), [1] Secondary pitch (3.D03)")
	parser.add_argument("team" , help="yellow or blue" )
	parser.add_argument("our" , help="our 3 dots are: pink or bright_green" )
	parser.add_argument("side" , help="which side of the pitch is ours, left or right?")
	args = parser.parse_args()

	# setup World model
	World.set_colours(args.team , args.our)
	pitch_number = int(args.pitch)
	World.set_globals(pitch_number , args.side)

	# start vision system in background thread
	vis = VisionWrapper(pitch=pitch_number)
	t = Thread(target = vis.run)
	t.daemon = True
	t.start()

	inp = ""
	while inp != "done":
		inp = raw_input("calibrate and type done")
		time.sleep(2)
	while inp != "end":
		time.sleep(1.5)
		Strategy.start()
