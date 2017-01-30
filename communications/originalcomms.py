import serial
import time
from Queue import Queue
import os
import subprocess as subp
from threading import Thread, Lock
import struct
import copy
from postprocessing.world import World, Ball

"""
See comms-protocol.md for info on how the PC communicates with
the Arduino.
This script is a little messy as we used to send messages to
the Arduino encoded as ASCII strings and later changed to a custom
enumeration and integer parameter encoding, but this script still
uses some of the old ASCII encodings internally. The Arduino-side
of things is tidier.
"""

# turn these on to help with debugging (will print debug info to stdout)
debug_print_sent_msg = False
debug_print_received_msg = False
debug_print_mess_succ = False
debug_print_resending = False
debug_print_ignoring_new_mess = False
debug_print_replacing_wm = False

class Coms(object):
	com = None
	messages_sent = None
	mess_id = None
	outputLock = Lock()
	outputFilename = ""
	errorCounter = 0

	def __init__(self):
		try :
			self.ser = serial.Serial("/dev/ttyACM0" , 115200 , timeout = 0.01)
		except Exception:
			try:
				self.ser = serial.Serial("/dev/ttyACM1" , 115200 , timeout = 0.01)
			except Exception :
				for i in range(0,10):
					print "COMS IS NOT ACTIVE"
		self.messages = Queue()
		self.completed_commands = {}

		self.outputFilename = "communications/logs/output-" + time.strftime("%H-%M-%S-%d-%b-%Y") + ".txt"
		# write blank file
		with self.outputLock:
			with open(self.outputFilename , "w" , False) as f:
				f.write("")

	'''
	This is static method is called once by the callee to handle
	'''
	@staticmethod
	def start_comunications():
		if Coms.com == None :
			Coms.com = Coms()
			Coms.com.messages_sent = dict()
			Coms.com.mess_id = 1
			t = Thread(target = Coms.com.comunications_loop)
			t.daemon = True
			t.start()
			Coms.com.receive_message()
			Coms.com.reset()
		else :
			print "Coms.com allread exists"

	@staticmethod
	def receive_message():
		if Coms.com:
			t = Thread(target = Coms.com.listen_on_serial)
			t.daemon = True
			t.start()
		else:
			print "you must start comunication first"

	@staticmethod
	def sets_time():
		if Coms.com:
			t = Thread(target = Coms.com.update_dict)
			t.daemon = True
			t.start()
		else:
			print "you must start comunication first"

	@staticmethod
	def testASCII(ser):
		ser.reset_input_buffer()
		ser.reset_output_buffer()
		for i in range(0,255) :
			b = bytes(chr(i))
			len = ser.write(b)
			if len != 1:
				print "LEN" + str(i)
			by = ser.read()
			print by, " bysaj"
			if b != by :
				print "FAILED " + str(i)
				print b
				print by
			else:
				print "SUCCESS " + str(i)
				print b

	@staticmethod
	def sf(ser , freq ,loc):
		ser.reset_input_buffer()
		ser.reset_output_buffer()
		f = open(loc , 'r')
		d = f.read()
		dn = "SEND " + str(freq) + " " + str(len(d)) + "\r"
		b = bytes(dn)
		print dn
		Coms.send_message(dn)
		for i in range(0,len(d)):
			ser.write(bytes(d[i]))
			print bytes(d[i])
			time.sleep(1/freq)

	@staticmethod
	def reset():
		return Coms.send_message("RESET")

	@staticmethod
	def reset_dict(self):
		Coms.com.mess_id = 1
		return Coms.com.messages_sent.clear()

	@staticmethod
	def stop():
		return Coms.send_message( "STOP")

	@staticmethod
	def updatewm(ts, rob_x, rob_y, rob_h):
		return Coms.send_message("UPDATEWM " + str(ts) + " " + str(rob_x) + " "+ str(rob_y) + " "+ str(rob_h))

	@staticmethod
	def go():
		return Coms.send_message( "GO ")

	@staticmethod
	def goxy(x_from , y_from, h_from , x_to , y_to):
		return Coms.send_message( "GOXY " + str(int(x_from)) + " " + str(int(y_from)) + " " + str(int(h_from)) + " "+ str(int(x_to)) + " "+ str(int(y_to)))

	@staticmethod
	def getball(x_from , y_from , h_from, x_to , y_to):
		return Coms.send_message( "GETBALL " + str(int(x_from)) + " " + str(int(y_from)) + " " + str(int(h_from)) + " " + str(int(x_to)) + " "+ str(int(y_to)))

	@staticmethod
	def retarg(orig_id, new_x, new_y):
		return Coms.send_message( "RETARG " + str(int(orig_id)) + " " + str(int(new_x)) + " " + str(int(new_y)))

	@staticmethod
	def turn(deg, corrections_allowed = 0):
		return Coms.send_message( "TURN " + str(int(deg)) +" "+ str(int(corrections_allowed)))

	@staticmethod
	def grab(ungrab):
		return Coms.send_message("GRAB " + ("1" if ungrab else "0" ))

	@staticmethod
	def receive(timeout):
		return Coms.send_message("RECEIVE " + str(timeout))

	@staticmethod
	def prepkick(stren):
		return Coms.send_message("PREPKICK "+str(stren))

	@staticmethod
	def kick(stren):
		return Coms.send_message("KICK "+str(stren))

	@staticmethod
	def abort():
		return Coms.send_message("ABORT")

	@staticmethod
	def reverse(dist):
		return Coms.send_message("REVERSE " + str(dist))

	@staticmethod
	def hasball():
		return Coms.send_message("HASBALL")

	@staticmethod
	def pendef():
		return Coms.send_message("PENDEF")

	@staticmethod
	def pendefupd(targ):
		return Coms.send_message("PENDEFUPD " + str(int(targ)))

	@staticmethod
	def hash(s):
		b = bytes(s)
		val = 0
		for by in list(b):
			val = val + ord(by)
		return struct.pack(">H", val)

	# returns message ID assigned
	@staticmethod
	def send_message(mess):
		if Coms.com != None:

			# if WMUPDATE already queued, "replace" it
			if mess.split()[0] == "UPDATEWM":
				for key in Coms.com.messages_sent:
					msg = Coms.com.messages_sent[key]
					if msg.opcode == Message.Messages_Opcode["UPDATEWM"]:
						msg.parameters[0] = mess.split()[1]
						msg.parameters[1] = mess.split()[2]
						msg.parameters[2] = mess.split()[3]
						msg.parameters[3] = mess.split()[4]
						if debug_print_replacing_wm:
							print "Replacing WM with ",msg.parameters
						msg.message = "Replaced WM"
						return -1

			# if no messages been delivered and there are 5 queued, ignore new messages
			if len(Coms.com.messages_sent) == Coms.com.mess_id - 1 and Coms.com.mess_id >= 6:
				if debug_print_ignoring_new_mess:
					print "No messages delivered. Ignoring new message."
			# if 10 messages undelivered, accept Comms has issues and reject new commands
			elif len(Coms.com.messages_sent) >= 10:
				if debug_print_ignoring_new_mess:
					print "Queue getting big. Ignoring new message."
			else:
				id = Coms.com.mess_id
				msg = Message(id,mess)
				Coms.com.messages_sent[str(id)] = msg
				Coms.com.messages.put(msg)
				Coms.com.mess_id += 1
				return id
		else :
			print "No com object exists"
	@staticmethod
	def reset_global_id(max_key):
		Coms.com.mess_id = max_key + 1

	'''
	This method runs in the thread responsible for sending messages to the arduino.
	All messages in the queue are sent. And any message in the dictionary with that has a transmitted time greater than
	1 second, resend that message

	'''
	def comunications_loop(self):

		# open new terminal window with tailf command
		subp.Popen("cd " + os.getcwd() + """  && gnome-terminal --tab -e "tailf """+Coms.com.outputFilename +""" "   """ , shell=True)
		while True :
			try:

				#Try to send any message in the queue
				mess = self.messages.get(False)
				if debug_print_sent_msg:
					print "sending message: ", mess

				# print message to second terminal window
				with Coms.com.outputLock:
					with open(Coms.com.outputFilename , "a" , False) as f:
						f.write(str(mess) + "\n")

				transmit_time = time.time()
				message = mess.pack_message()
				hashed_msg = self.hash(message)
				mess.set_transmit_time(transmit_time)
				self.ser.write(message)
				self.ser.write(hashed_msg)
				time.sleep(0.1)
			except Exception, ex:

				if not type(ex).__name__ == "Empty":
					print str(ex)

				#All messages that we havent heard anything from within 1 second of its transmitted time, are put into the queue  to
				#be resend again
				all_messages_keys = [int(key) for key in Coms.com.messages_sent.keys()]
				if all_messages_keys:
					all_messages_keys.sort()
					for key in all_messages_keys:
						try:
							current_time = time.time()
							msg_obj = Coms.com.messages_sent[str(key)]
							transmit_time = msg_obj.get_transmit_time()
							time_diff = current_time - transmit_time
							if time_diff > 1:
								Coms.com.messages.put(msg_obj)
								if debug_print_resending:
									print "Resending message ",key
						except KeyError:
							print "no message to send!!"
				#'''
				time.sleep(0.01)

	'''
	This method runs in the thread responsible for listening on for received messages from the arduino
	Don't call this method
	'''
	def listen_on_serial(self):
		found = True
		self.ser.flush()
		while found:
			arduino_response = self.ser.readlines()
			if arduino_response:
				joined = "".join(arduino_response)
				if debug_print_received_msg:
					print "@listen_on_serial ", joined
				self.update_message_status(joined)

				# print joined response to second terminal window
				with Coms.com.outputLock:
					with open(Coms.com.outputFilename , "a" , False) as f:
						f.write(str(joined) + "\n")
			self.ser.flush()
			time.sleep(0.01)

	def update_dict(self):
		#while True:
		pass

	def handleArduinoMsg(self, cmdName, cmdParams):

		if cmdName == "SUC":
			Coms.com.errorCounter = 0
			id = cmdParams[0]
			all_messages_keys = [int(key) for key in Coms.com.messages_sent.keys()]
			all_messages_keys.sort()
			self.delete_msg_in_range(int(id)+1, all_messages_keys)
			if debug_print_mess_succ:
				print "Message ", id, " has been successfully received"
		elif cmdName == "ERR":

			# if the errors dont look like they'll resolve themselves, reset
			Coms.com.errorCounter = Coms.com.errorCounter + 1
			if Coms.com.errorCounter > 100:
				Coms.com.reset()

				reset_global_id(0)

			expected_id = int(cmdParams[0])+1
			all_messages_keys = [int(key) for key in Coms.com.messages_sent.keys()]
			all_messages_keys.sort()
			self.delete_msg_in_range(expected_id, all_messages_keys)
			all_messages_keys = [int(key) for key in Coms.com.messages_sent.keys()]
			all_messages_keys.sort()
			Coms.com.messages.queue.clear()
			print "Error: arduino expects command with id ", expected_id
			if expected_id > 1:
				#handle the nonzero case
				self.resend_msg_non_zero(expected_id, all_messages_keys)
			else:
				self.resend_msg_zero(expected_id, all_messages_keys)
		elif cmdName == "ARDRESET":
			Coms.com.errorCounter = 0
			print "Arduino just reset"
			# empty dictionary and reset ID
			Coms.com.messages_sent = dict()
			Coms.com.mess_id = 1
		elif cmdName == "COMP":
			if len(cmdParams) > 1 :
				print "Arduino completed command id ",cmdParams[0]," with success ",cmdParams[1]
				self.completed_commands[cmdParams[0]] = cmdParams[1]
				#set the owner of the ball to us if the command was successfull

				world = World.get_world()

				# world may be None on startup
				while world == None:
					world = World.get_world()

				if cmdParams[1] == 1 or cmdParams[1] == "1" and world.ball and world.ball.owner != 0:
					Ball.last_held_by_us = time.time()
					print "Comms setting last held by us"
					world.ball.owner = 0
				elif cmdParams[1] == 0 or cmdParams[1] == "0" and world.ball and world.ball.owner == 0:
					world.ball.owner = 4
			else :
				print "Arduino completed command id ",cmdParams[0]
				self.completed_commands[cmdParams[0]] = 0

	'''
	Delete every message with id less than or equal to this expected_id
	'''
	def delete_msg_in_range(self, expected_id, all_messages_keys):
		for key in all_messages_keys:
			if key < expected_id:
				key = str(key)
				if key in Coms.com.messages_sent:
					del Coms.com.messages_sent[key]

	'''
	Puts information into the Queue for resending purposes
	This method handles only cases where the reset button was pressed on the arduino or the arduino send a
	reset command to the arduino
	'''
	def resend_msg_zero(self, expected_id, all_messages_keys):
		print "@resending expected_id", expected_id
		if all_messages_keys:
			min_id = min(all_messages_keys)
			max_id = max(all_messages_keys)
			shift_amount = min_id - expected_id
			max_id = max_id - shift_amount
			self.reset_global_id(max_id)

			#Loops through the dictionary and shift the messages to match that of the arduino
			for key in all_messages_keys:
				new_id = key - shift_amount
				i_key = key
				key = str(i_key)
				mess_obj = Coms.com.messages_sent[key]
				del Coms.com.messages_sent[key]
				mess_obj.set_key(new_id)
				new_id = str(new_id)
				Coms.com.messages_sent[new_id] = mess_obj
				Coms.com.messages.put(mess_obj)# comunications_loop running in the background
			#all_messages_keys = [int(key) for key in Coms.com.messages_sent.keys()]
			#min_id = min(all_messages_keys)
			#max_id = max(all_messages_keys)
			#print "finish min: ", min_id, "; max: ", max_id

	'''
	This method resends all the messages up until the expected id received from the arduino.
	The expected_id is the id that the arduino has not received so far
	'''
	def resend_msg_non_zero(self, expected_id, all_messages_keys):
		#dont change the id
		for key in all_messages_keys:
			key = str(key)
			mess_obj = Coms.com.messages_sent[key]
			Coms.com.messages.put(mess_obj)


	'''
	Splits up commands
	Sends them off to handleArduinoMsg()
	'''
	def update_message_status(self, joined):
		for cmd in self.commandsFromJoinedString(joined):
			self.handleArduinoMsg(cmd[0], cmd[1])

	'''
	Given a joined string (not list of tiny little strings)
	Searches for commands (beginning in $ and ending in ;)
	Extracts command name and parameters
	'''
	def commandsFromJoinedString(self, joined):
		commands = []
		# for each region split by $ (except first one)
		for postDS in joined.split("$")[1:]:
			if postDS.find(";") != -1:
				cmd = postDS.split(";")[0]
				if cmd.find("&") != -1:
					splitAmp = cmd.split("&");
					cmdName = splitAmp[0]
					cmdParams = splitAmp[1:]
					commands.append((cmdName, cmdParams))
				else:
					commands.append((cmd, []))
		return commands

class Message():
	'''
	This class represent the message sent to the arduino itself. Handles each command on its own code and packs it
	to its corresponding function and returns the correct representation in bytes.
	'''
	Messages_Opcode = {
		"RESET":1,
		"STOP":2,
		"UPDATEWM": 3,
		"GO": 4,
		"GOXY":5,
		"GETBALL" : 6,
		"TURN":7,
		"GRAB":8,
		"RECEIVE": 9,
		"PREPKICK":10,
		"KICK": 11,
		"REVERSE": 12,
		"ABORT": 13,
		"HASBALL": 14,
		"RETARG": 15,
		"PENDEF": 16,
		"PENDEFUPD": 17
	}


	def __init__(self,id, message):
		global Messages_Opcode
		self.id = id
		self.isSuccess = False
		self.attempt_number = 0
		command = self.getCommandID(message)
		self.message = message
		self.opcode = self.Messages_Opcode[command]
		self.transmit_time = 0
		#initialises all the command:  a map of commands to its packing fucntion
		self.init_pack()

	def set_transmit_time(self, t):
		self.transmit_time = t

	def get_transmit_time(self):
		return self.transmit_time

	def getCommandID(self, message):
		self.arguments = message.split()
		self.parameters = self.arguments[1:]
		return self.arguments[0]

	def setSuccess(self, status):
		self.isSuccess = status

	def isSuccess(self):
		return self.isSuccess

	def set_key(self, new_id):
		self.id = new_id

	def pack_message(self):

		packed_command = None
		#execute unpack function for command
		command = self.arguments[0]
		#print command
		packed_command = self.function_[command]()
		return packed_command

	def pack_reset(self):
		packed_command = struct.pack(">HB", self.id, self.opcode)
		return packed_command

	def pack_stop(self):
		packed_command = struct.pack(">HB", self.id, self.opcode)
		return packed_command

	def pack_updatewm(self):
		#ts, rob_x, rob_y, rob_h) updatewm
		params = [int(p) for p in self.parameters]
		packed_command = struct.pack(">HBIhhh", self.id,self.opcode,params[0], params[1],params[2], params[3])
		return packed_command

	def pack_go(self):
		#len
		packed_command = struct.pack(">HB", self.id, self.opcode)
		return packed_command

	def pack_goxy(self):
		params = [int(p) for p in self.parameters]
		packed_command = struct.pack(">HBhhhhh", self.id,self.opcode,params[0], params[1],params[2], params[3], params[4])
		return packed_command

	def pack_getBall(self):
		params = [int(p) for p in self.parameters]
		packed_command = struct.pack(">HBhhhhh", self.id,self.opcode,params[0], params[1],params[2], params[3],params[4])
		return packed_command

	def pack_retarg(self):
		params = [int(p) for p in self.parameters]
		packed_command = struct.pack(">HBHhh", self.id,self.opcode,params[0], params[1],params[2])
		return packed_command

	def pack_turn(self):
		#deg
		parameters = [int(param) for param in self.parameters]
		packed_command  = struct.pack(">HBhB", self.id,self.opcode,parameters[0], parameters[1])
		return packed_command

	def pack_grab(self):
		#grab
		param = int(self.parameters[0])
		packed_command  = struct.pack(">HBB", self.id,self.opcode,param)
		return packed_command

	def pack_receive(self):
		param = int(self.parameters[0])
		packed_command  = struct.pack(">HBI", self.id,self.opcode,param)
		return packed_command

	def pack_prekick(self):
		param = int(self.parameters[0])
		packed_command  = struct.pack(">HBB", self.id,self.opcode,param)
		return packed_command

	def pack_kick(self):
		#len
		param = int(self.parameters[0])
		packed_command  = struct.pack(">HBB", self.id,self.opcode,param)
		return packed_command


	def pack_reverse(self):
		param = int(self.parameters[0])
		packed_command  = struct.pack(">HBH", self.id,self.opcode,param)
		return packed_command

	def pack_abort(self):
		packed_command = struct.pack(">HB", self.id, self.opcode)
		return packed_command

	def pack_hasball(self):
		packed_command = struct.pack(">HB", self.id, self.opcode)
		return packed_command

	def pack_pendef(self):
		packed_command = struct.pack(">HB", self.id, self.opcode)
		return packed_command

	def pack_pendefupd(self):
		parameters = [int(param) for param in self.parameters]
		packed_command = struct.pack(">HBh", self.id, self.opcode,parameters[0])
		return packed_command

	def __str__(self):
		msg = str(self.id) + "_" + self.message
		return msg

	def init_pack(self):
		self.function_ = dict()
		self.function_["RESET"] = self.pack_reset
		self.function_["STOP"] = self.pack_stop
		self.function_["UPDATEWM"] = self.pack_updatewm
		self.function_["GO"] = self.pack_go
		self.function_["GOXY"] = self.pack_goxy
		self.function_["GETBALL"] = self.pack_getBall
		self.function_["TURN"] = self.pack_turn
		self.function_["GRAB"] = self.pack_grab
		self.function_["RECEIVE"] = self.pack_receive
		self.function_["PREPKICK"] = self.pack_prekick
		self.function_["KICK"] = self.pack_kick
		self.function_["REVERSE"] = self.pack_reverse
		self.function_["ABORT"] = self.pack_abort
		self.function_["HASBALL"] = self.pack_hasball
		self.function_["PENDEF"] = self.pack_pendef
		self.function_["PENDEFUPD"] = self.pack_pendefupd
