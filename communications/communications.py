import serial
import subprocess as sp
import os
import time
import re

from Queue import Queue
from threading import Thread, Lock
from message import Message
from struct import pack

# Based on code taken from https://bitbucket.org/craigwalton/sdp-g7
class Comms(object):
	active = False # Whether or not communications is active
	ball = False # Whether or not the robot has the ball
	arduino_initialised = False # Messages will only be sent when the arduino is initialised
	messages = [] # List containing all messages
	message_buffer = Queue() # Queue of messages to try sending
	port = None # The port on which to send/listen for messages
	message_id = 0 # The ID of the last queued command
	outputLock = Lock() # Create a thread lock to ensure no interference between threads
	outputFilename = "communications/logs/output-" + time.strftime("%H-%M-%S-%d-%b-%Y") + ".txt" # DO NOT COMMIT LOGS TO GIT REPO

	def __init__(self):
		# Find the SRF USB stick (should be on ttyACM0 or ttyACM1)
		for i in range(0,10):
			self.__findport__(i)
			if (self.port != None):
				break

		if (self.port == None):
			print "Serial not found!!"

		# Create log directory if it doesn't already exist
		if (not os.path.exists("communications/logs")):
			os.mkdir("communications/logs")

		# Create output log (initially blank)
		with self.outputLock:
			with open(self.outputFilename, "w", False) as file:
				file.write("")

	def __findport__(self, idx):
		try:
			self.port = serial.Serial("/dev/ttyACM" + str(idx), 115200, timeout=0.01)
			print "Serial found at /dev/ttyACM" + str(idx)
			return
		except Exception:
			return

	def start(self):
		if (not self.active):
			self.active = True

			# Create thread to handle outgoing messages
			sender = Thread(target=self.send_messages)
			sender.daemon = True
			sender.start()

			# Create thread to listen for incoming messages
			receiver = Thread(target=self.receive_messages)
			receiver.daemon = True
			receiver.start()

			# Reset arduino communications
			self.reset()
		else:
			print "Cannot start again as Comms already active!"


	def send_messages(self):
		# Open a new terminal
		sp.Popen("cd " + os.getcwd() + """ && gnome-terminal --tab -e "tailf """ + self.outputFilename + """ "   """ , shell=True)
		# Loop indefinitely
		while True:
			if self.arduino_initialised:
				try:
					# Get message at the front of the queue
					msg = self.message_buffer.get(0)

					# Write to file
					with self.outputLock:
						with open(self.outputFilename , "a" , False) as file:
							file.write("@send_messages " + str(msg) + "\n")

					# Pack and send message to arduino
					packed = msg.pack_message()
					msg.set_transmit_time(time.time())
					hashed = self.hash(packed)

					self.port.write(packed)
					self.port.write(hashed)
					time.sleep(0.1)

				except Exception, ex:
					if not type(ex).__name__ == "Empty":
						print str(ex)

					for m in self.messages:
						current_time = time.time()
						transmit_time = m.trans
						if transmit_time != None:
							time_diff = current_time - transmit_time
							if time_diff > 1:
								self.message_buffer.put(m)
					time.sleep(0.1)
			else:
				time.sleep(0.1)
		else:
			# Recheck every 100ms
			time.sleep(0.1)

	def receive_messages(self):
		# Flush any leftover data
		self.port.flush()

		while True:
			response = self.port.readlines()

			if response:
				# Convert sequence of bytes to string
				joined = "".join(response)

				if ("$ARDRESET" in joined):
					print "Arduino ready!"
					self.arduino_initialised = True

				if ("$BALL" in joined):
					# print "Got ball command!"
					self.ball = True

				# Print response to log
				with self.outputLock:
					with open(self.outputFilename, "a", False) as file:
						file.write("@receive_messages " + str(joined) + "\n")


				# Otherwise, check for OK or ERR message
				if ("$SUC" in joined):
					ids = re.findall('(?<=\$SUC\&)\d+(?=;)', joined)
					for idx in ids:
						self.delete_up_to_id(idx)

				if ("$ERR" in joined):
					ids = re.findall('(?<=\$ERR\&)\d+(?=;)', joined)
					for idx in ids:
						self.resend_up_to_id(idx)

			self.port.flush()

			# Try again every 10ms
			time.sleep(0.01)

 	# got_ball returns true if the ball has been received since the method was last checked
	def got_ball(self):
		if (self.ball):
			self.ball = False
			return True
		return False

	def delete_up_to_id(self, idx):
		for m in self.messages:
			if (int(m.id) <= int(idx)):
				self.messages.remove(m)

	def resend_up_to_id(self, idx):
		if (int(idx) == 0):
			self.reset()
			return

		self.message_buffer = Queue()
		for m in self.messages:
			if (int(m.id) <= int(idx)):
				self.message_buffer.put(m)

	# name : string, params : int[], params is optional, has default [] (no parameters)
	def add_message(self, name, params=[]):
		# Iterate current message_id
		self.message_id = self.message_id + 1
		msg = Message(self.message_id, name, params)
		self.messages.append(msg)
		self.message_buffer.put(msg)

	def reset(self):
		self.messages = []
		self.message_buffer = Queue()
		# Create a reset message
		msg = Message(1, "RESET", [])
		packed = msg.pack_message()
		msg.set_transmit_time(time.time())
		hashed = self.hash(packed)

		self.arduino_initalised = False

		print "@send_messages", msg

		# Write to file
		with self.outputLock:
			with open(self.outputFilename , "a" , False) as file:
				file.write("@send_messages " + str(msg) + "\n")

		self.port.write(packed)
		self.port.write(hashed)
		self.message_id=1

	def stop(self):
		self.add_message("STOP")

	# timestamp : int, robot_x : int, robot_y : int, robot_h : int
	def updatewm(self, timestamp, robot_x, robot_y, robot_h):
		params = [timestamp, robot_x, robot_y, robot_h]
		self.add_message("UPDATEWM", params)

	def go(self):
		self.add_message("GO")

	# x_from : int, y_from : int, h_from : int, x_to : int, y_to : int
	def goxy(self, x_from , y_from, h_from , x_to , y_to):
		params = [x_from, y_from, h_from, x_to, y_to]
		self.add_message("GOXY", params)

	# x_from : int, y_from : int, h_from : int, x_to : int, y_to : int
	def getball(self, x_from , y_from , h_from, x_to , y_to):
		params = [x_from, y_from, h_from, x_to, y_to]
		self.add_message("GETBALL", params)

	# orig_id : int, new_x : int, new_y : int
	def retarg(self, orig_id, new_x, new_y):
		params = [orig_id, new_x, new_y]
		self.add_message("RETARG", params)

	# deg : int, corrections : int
	def turn(self, deg, corrections = 0):
		params = [deg, corrections]
		self.add_message("TURN", params)

	# ungrab : bool
	def grab(self, ungrab):
		params = [1 if ungrab else 0]
		self.add_message("GRAB", params)

	# timeout : int
	def receive(self, timeout):
		params = [timeout]
		self.add_message("RECEIVE", params)

	# strength : int
	def prepkick(self, strength=1):
		params = [strength]
		self.add_message("PREPKICK", params)

	# strength : int
	def kick(self, strength=1):
		params = [strength]
		self.add_message("KICK", params)

	def abort(self):
		self.add_message("ABORT")

	# dist : int
	def reverse(self, dist):
		params = [dist]
		self.add_message("REVERSE", params)

	def hasball(self):
		self.add_message("HASBALL")

	def getpos(self):
		self.add_message("GETPOS")

	def resetpos(self):
		self.add_message("RESETPOS")

	def getcompass(self):
		self.add_message("GETCOMPASS")

	# hash(packed_msg : string) : byte[]
	def hash(self, packed_msg):
		b = bytes(packed_msg)
		val = 0
		for by in list(b):
			val = val + ord(by)
		return pack(">H", val)
