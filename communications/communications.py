import serial

from Queue import Queue
from threading import Thread, Lock

# Based on code taken from https://bitbucket.org/craigwalton/sdp-g7
class Comms(object):
	active = False # Whether or not communications is active
	messages = Queue() # Queue of unconfirmed messages
	port = None # The port on which to send/listen for messages
	message_id = 0 # The ID of the last queued command

	def __init__(self):
		# Find the SRF USB stick (should be on ttyACM0 or ttyACM1)
		try :
			self.port = serial.Serial("/dev/ttyACM0", 115200, timeout=0.01)
			print "Serial found at /dev/ttyACM0"
		except Exception:
			try:
				self.port = serial.Serial("/dev/ttyACM1", 115200, timeout=0.01)
				print "Serial found at /dev/ttyACM1"
			except Exception:
					print "Serial not found!!"

# Create a Comms object
comms = Comms()