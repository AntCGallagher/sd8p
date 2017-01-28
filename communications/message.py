import struct

# [ID - 2 bytes][opcode - 1 byte][params - variable length][hash - 2 bytes]
opcodes = {
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

		# Calculate hash (VERY SIMPLE, CONSIDER CHANGING)
		self.hash = self.id + self.op + sum(self.params)

	# pack() : byte[]
	def pack_message(self):
		# Details of the formatting can be found at https://docs.python.org/2/library/struct.html
		if (self.op in [1,2,4]):
			# Op codes 1,2,4 take None as args
			packed = struct.pack(">HB", self.id, self.op)

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