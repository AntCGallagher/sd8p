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
	parser.add_argument("onevsone", help="For use in 1v1, true or false")
	args = parser.parse_args()


	# If 1v1:
	if (args.onevsone == 1):
		object_count_pink = 0
		object_count_green = 0
		enemy_colour = raw_input("opponents primary colour : ")
		if (enemy_colour == "pink"):
			object_count_pink = object_count_pink + 3
			object_count_green = object_count_green + 1
		elif (enemy_colour == "green"):
			object_count_pink = object_count_pink + 1
			object_count_green = object_count_green + 3

		if (args.our == "pink"):
			object_count_pink = object_count_pink + 3
			object_count_green = object_count_green + 1
		elif (args.our == "green"):
			object_count_green = object_count_green + 3
			object_count_pink = object_count_pink + 1

		print object_count_pink
		print object_count_green

		# Alter config data:
		json_content = tools.get_json(PATH+'/vision/calibrations/calibrations.json')
		json_content["default"]["PITCH0"]["blue"]["object_count"] = 1
		json_content["default"]["PITCH0"]["plate"]["object_count"] = 2
		json_content["default"]["PITCH0"]["bright_green"]["object_count"] = object_count_green
		json_content["default"]["PITCH0"]["yellow"]["object_count"] = 1
		json_content["default"]["PITCH0"]["pink"]["object_count"] = object_count_pink
		json_content["default"]["PITCH0"]["green"]["object_count"] = object_count_green
		####
		json_content["default"]["PITCH1"]["blue"]["object_count"] = 1
		json_content["default"]["PITCH1"]["plate"]["object_count"] = 2
		json_content["default"]["PITCH1"]["bright_green"]["object_count"] = object_count_green
		json_content["default"]["PITCH1"]["yellow"]["object_count"] = 1
		json_content["default"]["PITCH1"]["pink"]["object_count"] = object_count_pink
		json_content["default"]["PITCH1"]["green"]["object_count"] = object_count_green
		tools.write_json(PATH+'/vision/calibrations/calibrations.json', json_content)
	else:
		json_content = tools.get_json(PATH+'/vision/calibrations/calibrations.json')
		json_content["default"]["PITCH0"]["blue"]["object_count"] = 2
		json_content["default"]["PITCH0"]["plate"]["object_count"] = 4
		json_content["default"]["PITCH0"]["bright_green"]["object_count"] = 8
		json_content["default"]["PITCH0"]["yellow"]["object_count"] = 2
		json_content["default"]["PITCH0"]["pink"]["object_count"] = 8
		json_content["default"]["PITCH0"]["green"]["object_count"] = 8
		####
		json_content["default"]["PITCH1"]["blue"]["object_count"] = 2
		json_content["default"]["PITCH1"]["plate"]["object_count"] = 3
		json_content["default"]["PITCH1"]["bright_green"]["object_count"] = 8
		json_content["default"]["PITCH1"]["yellow"]["object_count"] = 2
		json_content["default"]["PITCH1"]["pink"]["object_count"] = 8
		json_content["default"]["PITCH1"]["green"]["object_count"] = 8
		tools.write_json(PATH+'/vision/calibrations/calibrations.json', json_content)

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
	while inp != "s" or inp != "c":
		inp = raw_input("stop or calibrate (s/c)? : ")
		if inp == "s":
			Strategy.stop()
		if inp == "c":
			while inp != "done":
				inp = raw_input("calibrate and type done: ")
			while inp != "s" or inp != "t":
				inp = raw_input("tests/start? (t/s): ")
				if inp == "s":
					corner = int(raw_input("Corner to start ((0,0) = 1 clockwise): "))
					curr_x = int(raw_input("Current x: "))
					curr_y = int(raw_input("Current y: "))
					while inp != "y":
				 		inp = raw_input("start? (y/n)")
						if inp == "y":
							Strategy.start(corner,curr_x,curr_y)					
				if inp == "t":
					Strategy.tests()
