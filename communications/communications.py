import serial
import subprocess as sp
import os
import time

from Queue import Queue
from threading import Thread, Lock
from message import Message

# Based on code taken from https://bitbucket.org/craigwalton/sdp-g7
class Comms(object):
	active = False # Whether or not communications is active
	arduino_initialised = False # Messages will only be sent when the arduino is initialised
	messages = Queue() # Queue of unconfirmed messages
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

			# Reset arduino communications. TO BE IMPLEMENTED
			self.reset()
		else:
			print "Cannot start again as Comms already active!"


	def send_messages(self):
		# Open a new terminal
		# sp.Popen("cd " + os.getcwd() + """ && gnome-terminal --tab -e "tailf """ + self.outputFilename + """ "   """ , shell=True)
		# Loop indefinitely
		while True:
			try:
				# Get message at the front of the queue
				msg = self.messages.get(0)
				print "@send_messages", msg

				# Write to file
				with self.outputLock:
					with open(self.outputFilename , "a" , False) as file:
						file.write("@send_messages " + str(msg) + "\n")

				# Pack and send message to arduino
				packed = msg.pack_message()
				msg.set_transmit_time(time.time())

				self.port.write(packed)
				time.sleep(0.01)

			except Exception, ex:
				# In case of error, print exception details
				pass

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
				print "@receive_messages", joined

				# Print response to log
				with self.outputLock:
					with open(self.outputFilename, "a", False) as file:
						file.write("@receive_messages " + str(joined) + "\n")

				# self.update_message_status(joined)

				# Otherwise, check for OK or ERR message

			self.port.flush()

			# Try again every 10ms
			time.sleep(0.01)

	# name : string, params : int[]
	def add_message(self, name, params):
		# Iterate current message_id
		self.message_id = self.message_id + 1
		msg = Message(self.message_id, name, params)
		self.messages.put(msg)

	def reset(self):
		self.messages = Queue()
		self.add_message("RESET", [])
		self.message_id=0

# Create and start a Comms object
comms = Comms()
comms.start()

time.sleep(2)
# Queue a stop message
# comms.add_message("GO", [])
# comms.add_message("STOP", [])
comms.add_message("GO", [])
# time.sleep(2)
# comms.add_message("STOP", [])

while True:
	pass
