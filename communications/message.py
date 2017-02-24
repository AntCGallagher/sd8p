from struct import pack

# [ID - 2 bytes][opcode - 1 byte][params - variable length][hash - 2 bytes]
opcodes = {
	"RESET": 1,
	"STOP": 2,
	"UPDATEWM": 3,
	"GO": 4,
	"GOXY": 5,
	"GETBALL": 6,
	"TURN": 7,
	"GRAB": 8,
	"RECEIVE" : 9,
	"PREPKICK": 10,
	"KICK": 11,
	"REVERSE": 12,
	"ABORT": 13,
	"HASBALL": 14,
	"RETARG": 15
}

class Message(object):
	# id : int,
	# cmd_name : string
	# op : int,
	# params: int[] (type of int dependent on operation),
	# hash : int
	# trans: float
	def __init__(self, idx, op_string, params):
		self.id = idx
		self.success = False
		self.attempts = 0
		self.cmd_name = op_string
		self.op = opcodes[op_string]
		self.params = params
		self.trans = None

	# pack() : byte[]
	def pack_message(self):
		# Details of the formatting can be found at https://docs.python.org/2/library/struct.html
		if (self.op in [1,2,4,13,14]):
			packed = pack(">HB", self.id, self.op)
		elif (self.op in [3]):
			packed = pack(">HBIhhh", self.id, self.op, self.params[0], self.params[1], self.params[2], self.params[3])
		elif (self.op in [5,6]):
			packed = pack(">HBhhhhh", self.id, self.op, self.params[0], self.params[1], self.params[2], self.params[3], self.params[4])
		elif (self.op in [7]):
			packed = pack(">HBHhh", self.id, self.op, self.params[0], self.params[1], self.params[2])
		elif (self.op in [8,10,11]):
			packed = pack(">HBB", self.id, self.op, self.params[0])
		elif (self.op in [9]):
			packed = pack(">HBI", self.id, self.op, self.params[0])
		elif (self.op in [12]):
			packed = pack(">HBH", self.id, self.op, self.params[0])
		elif (self.op in [15]):
			packed = pack(">HBHhh", self.id, self.op, self.params[0], self.params[1], self.params[2])

		return packed

	# set_transmit_time(transmit_time : double) : void
	def set_transmit_time(self, transmit_time):
		self.trans = transmit_time
		
	# __str__() : string
	def __str__(self):
		# Convert all params to strings
		params_string = map(str,self.params)
		# Returns in the format "<ID> <OP> <PARAM1> ... <PARAM5>"
		return " ".join([str(self.id), self.cmd_name] + params_string)	