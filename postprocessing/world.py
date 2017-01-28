from __future__ import division
from math import atan2 , pi , sqrt, degrees
from time import time
from threading import Lock
from vision.tools import get_croppings 
from numpy import *
import command.helpers as com
import comunications as coms


"""
This class contains the interface for updating the world model.
The only methods called from outside the class should be set_points
and get_world. It also needs the colour mapping of robots, set_colours
should therefor be called at the begining of each run.
"""


pitch_y_cm = 220
pitch_x_cm = 300

pitch_y_px = 480
pitch_x_px = 640

PLATE_RADIUS = 30

#ONLY USED TO CALCULATE BOX LINES
ROBOT_RADIUS = 15


class World(object):
	points_lock = Lock()
	points = None
	last_world = None
	last_time = 0 

	ball_colour = "red"
	our_team_colour = "blue"
	oposite_team_colour = "yellow"
	our_primary = "pink"
	other_primary = "bright_green"


	pitch = None
	left_goal = None
	right_goal = None
	left_goal_center = None
	right_goal_center = None

	our_side = "Left"
	pitch_no = 0

	def __init__(self , points , c_time , old_world) :
		self.robots = self.get_robots(points=points , last_world=old_world , c_time=c_time)
		self.ball   = self.get_ball(points=points , last_world=old_world , c_time=c_time)

		"""
		if World.ball_colour in points and len(points[World.ball_colour]) > 0 :
			ball = points[World.ball_colour][0]
			x, y = self.px_to_cm(ball[0] , ball[1])
			self.ball = Ball(x, y , old_world.ball if old_world != None else None, c_time)		
		else :
			self.ball = old_world.ball if old_world != None else None
		"""
		self.time = c_time 

	def __str__(self):
		return "World\n" + str(self.__dict__) 

	
	@staticmethod
	def set_globals(no , side):
		"""
		Call before starting the system, no should be the pithc number, 0 or 1 
		and side should be the side our goal is on, "left" or "right"
		"""
		World.pitch_no = no
		World.our_side = "Left" if side == "left" else "Right"

	#Call every time a new frame has been processed
	@staticmethod
	def set_points(new_points):
		World.points_lock.acquire()
		try :
			World.points = new_points
		finally:
			World.points_lock.release()
		World.last_time = time()

	#Fetches the world model, or recaulcualtes it if we received a new set of points
	@staticmethod
	def get_world():
		World.points_lock.acquire()
		try :
			World.last_world = World(World.points , World.last_time , World.last_world) if World.points != None else World.last_world
			World.points = None
		finally:
			World.points_lock.release()
		return World.last_world

	#our_team_colour should be the center dot of our robot
	#our_primary should be the colour of which we have 3 on our top plate 
	@staticmethod
	def set_colours(our_team_colour , our_primary):
		if our_team_colour == "blue" :
			World.our_team_colour = "blue"
			World.oposite_team_colour = "yellow"
		else :
			World.our_team_colour = "yellow"
			World.oposite_team_colour  = "blue"

		if our_primary == "bright_green" or our_primary == "green" :
			World.our_primary = "bright_green"
			World.other_primary = "pink"
		else :
			World.our_primary = "pink"
			World.other_primary = "bright_green"

		print "Our team colour set to " + World.our_team_colour
		print "Our primary colour set to " + World.our_primary



	@staticmethod
	def px_to_cm(x , y):
		x = x * pitch_x_cm / pitch_x_px
		y = y * pitch_y_cm / pitch_y_px
		return (x,y)

	@staticmethod
	def cm_to_px(x ,y):
		x = x * pitch_x_px / pitch_x_cm
		y = y * pitch_y_px / pitch_y_cm
		return (x , y)

	@staticmethod
	def get_goals():
		"""
		Returns an array containing Box objects representing the two goals
		The first ellement will allways be the left goal

		Use calibrate.py to set up where these are.
		"""
		if World.left_goal == None:
			pitch_n0 = World.pitch_no
			crops = get_croppings(pitch = pitch_n0)
			if "Zone_0" in crops :
				zone = crops["Zone_0"]
				if len(zone) == 4 :
					p1 = zone[0]
					p2 = zone[1]
					p3 = zone[2]
					p4 = zone[3]

					p1 = World.px_to_cm(p1[0] , p1[1])
					p2 = World.px_to_cm(p2[0] , p2[1])
					p3 = World.px_to_cm(p3[0] , p3[1])
					p4 = World.px_to_cm(p4[0] , p4[1])
					World.left_goal = Box(p1,p2,p3,p4)
			else :
				print "Please use calibrate to mark the pitch outline"


		if World.right_goal == None:
			pitch_n0 = World.pitch_no
			crops = get_croppings(pitch = pitch_n0)
			if "Zone_1" in crops :
				zone = crops["Zone_1"]
				if len(zone) == 4 :
					p1 = zone[0]
					p2 = zone[1]
					p3 = zone[2]
					p4 = zone[3]

					p1 = World.px_to_cm(p1[0] , p1[1])
					p2 = World.px_to_cm(p2[0] , p2[1])
					p3 = World.px_to_cm(p3[0] , p3[1])
					p4 = World.px_to_cm(p4[0] , p4[1])
					World.right_goal = Box(p1,p2,p3,p4)
			else :
				print "Please use calibrate to mark the pitch outline"


		return [World.left_goal , World.right_goal]

	@staticmethod
	def get_pitch():
		"""
		Returns a Box representing the full pitch

		Use calibrate.py to set this up
		"""
		if World.pitch == None :
			pitch_n0 = World.pitch_no
			crops = get_croppings(pitch = pitch_n0)
			if "outline" in crops :
				zone = crops["outline"]
				if len(zone) == 4 :
					p1 = zone[0]
					p2 = zone[1]
					p3 = zone[2]
					p4 = zone[3]

					p1 = World.px_to_cm(p1[0] , p1[1])
					p2 = World.px_to_cm(p2[0] , p2[1])
					p3 = World.px_to_cm(p3[0] , p3[1])
					p4 = World.px_to_cm(p4[0] , p4[1])
					World.pitch = Box(p1,p2,p3,p4)
			else :
				print "Please use calibrate to mark the pitch outline"
		return World.pitch

	@staticmethod
	def get_goal_center(ours = False):

		if World.left_goal_center == None:
			pitch_n0 = World.pitch_no
			crops = get_croppings(pitch = pitch_n0)
			if "Goal_0" in crops :
				zone = crops["Goal_0"]
				if len(zone) == 1 :
					p = zone[0]

					p = World.px_to_cm(p[0] , p[1])
					World.left_goal_center = array(p)
			else:
				print "Please use calibrate to mark the goals"

		if World.right_goal_center == None:
			pitch_n0 = World.pitch_no
			crops = get_croppings(pitch = pitch_n0)
			if "Goal_1" in crops :
				zone = crops["Goal_1"]
				if len(zone) == 1 :
					p = zone[0]

					p = World.px_to_cm(p[0] , p[1])
					World.right_goal_center = array(p)
			else:
				print "Please use calibrate to mark the goals"

		if ours :
			return World.left_goal_center if World.our_side == "Left" else World.right_goal_center
		else :
			return World.left_goal_center if World.our_side != "Left" else World.right_goal_center





	def get_boxes_to_avoid(self , ignore = 0 ):
		"""
		Returns a set of boxes that the robot with index ignore should avoid. 
		"""

		boxes = [self.get_enemy_goal()]

		for i in range(0,4):
			if self.robots[i] != None and i != ignore:
				boxes.append(self.robots[i].get_bounding_box().get_outer_box())

		return boxes

	def get_enemy_goal(self , outer = True):
		"""
		Returns a an array of points which define the enemy goal.
		"""
		goals = World.get_goals()
		if World.our_side == "Left" :
			return goals[1].get_outer_box() if outer else goals[1].points
		else :
			return goals[0].get_outer_box() if outer else goals[0].points

	def get_robots(self, last_world, points, c_time):
		# {'ball': {'center': (0, 0), 'radius': 0}, 'robots': []}
		# {'center': (cx, cy), 'angle': angle, 'team': team, 'group': group}
		robot_data = points['robots']
		robots     = [None]*4

		for robot in robot_data:
			x_px, y_px = robot['center']
			angle      = robot['angle']
			x, y       = self.px_to_cm(x_px ,y_px)
			identity   = self.identify_robot(team_color=robot['team'] , group_color=robot['group'])

			robots[identity]  = Robot(x, y, angle, x_px, y_px , c_time)

		for i , robot in enumerate(robots):
			if robot == None and last_world != None and last_world.robots != None:
				robots[i] = last_world.robots[i]

		return robots

	def get_ball(self, last_world, points, c_time):
		ball = points['ball']

		if ball and ball['center'] != (-1,-1):
			x, y     = ball['center']
			x, y     = World.px_to_cm(x, y)
			direction= ball['direction']
			ball     = Ball(x, y , direction, last_world.ball if last_world != None else None, t=c_time, robots=self.robots)
		#The ball needs to be reconstructed every time even if we know nothing of it's position.
		#this is used to calculate who owns it.
		elif last_world and last_world.ball:
			ball = Ball(last_world.ball.x , last_world.ball.y , last_world.ball.dir , last_world.ball , last_world.ball.t , self.robots)		
		else :
			ball = last_world.ball if last_world != None else None

		return ball

	def identify_robot(self, team_color, group_color):
		#assign the robot an unique id based on the colour of the points close to the center
		if team_color == World.our_team_colour and World.our_primary == group_color:
			return 0
		elif team_color == World.our_team_colour and World.our_primary != group_color:
			return 1
		elif team_color == World.oposite_team_colour and World.our_primary == group_color:
			return 2
		elif team_color == World.oposite_team_colour and World.our_primary != group_color:
			return 3
		else :
			return -1

"""
Legacy code
	def calculate_positions_of_robots(self , points , last_world , c_time):

		robots = [None]*4
		secondary_points = []
		if World.our_primary in points:
			secondary_points.extend(points[World.our_primary])
		if World.other_primary in points:
			secondary_points.extend(points[World.other_primary])
		for colour in [World.our_team_colour , World.oposite_team_colour] :		
			if colour in points :
				for x , y in points[colour] :
					#find at most 4 points that are closest to the center point of the top plate
					ranking = filter(lambda tup : sqrt(pow(tup[0] - x,2) + pow(tup[1] - y,2)) <= PLATE_RADIUS , secondary_points )
					ranking = sorted(ranking ,key = lambda tup : sqrt(pow(tup[0] - x,2) + pow(tup[1] - y,2)))

					#If there are enough fo them to calculate rotation
					if len(ranking) >= 4:
						closest = ranking[0:4]
						

						identity = self.identify_robot(colour , closest , points)
						rot = self.calculate_robot_rotation((x,y) , closest , identity , points)

						x_px, y_px = (x, y)
						x, y = self.px_to_cm(x ,y)


						robots[identity]  = Robot(x, y, rot, x_px, y_px , c_time)


					else :
						#See if we can identify the robot, and if so at inherit rotation from last time round
						identity = self.identify_robot(colour , ranking[0:len(ranking)] , points)
						if identity >= 0 :
							rot = World.last_world.robots[identity].rot if World.last_world != None and World.last_world.robots[identity] != None else 0
							x_px, y_px = (x, y)
							x, y = self.px_to_cm(x,y)
							robots[identity]  = Robot(x, y, rot, x_px, y_px , c_time)

		for i , robot in enumerate(robots):
			if robot == None and last_world != None:
				robots[i] = last_world.robots[i]


		return robots

	def calculate_robot_rotation(self , pos , sur_p , identity , points):
		#find the colour of each surounding point
		World.our_primarys = []
		World.other_primarys = []
		for tup in sur_p:
			if points[World.our_primary].count(tup) > 0 :
				World.our_primarys.append(tup)
			else :
				World.other_primarys.append(tup)

		x , y = pos

		#check that there are enough close points and that there is a single uniqley coloured one
		if len(sur_p) >= 4 and  (len(World.other_primarys) if (identity % 2) == 0 else len(World.our_primarys)) == 1 :
			rotation_point = World.other_primarys[0] if (identity %2) == 0 else World.our_primarys[0]
			other_points = World.our_primarys if (identity %2) == 0 else World.other_primarys
			closeness = sorted(other_points , key = lambda tup : pow(tup[0] - rotation_point[0],2) +pow(tup[1] - rotation_point[1],2) )


			#calculate the midpoint btween the front two and the back two points respectivley
			start_p = ((closeness[0][0] + rotation_point[0])/2 , (closeness[0][1] + rotation_point[1] )/2)
			end_p   = ((closeness[1][0] + closeness[2][0])/2,(closeness[1][1] + closeness[2][1])/2)

			
			#Trigonometry, (dx,dy) represents direction vector of the robot
			dx = end_p[0] - start_p[0]
			dy = end_p[1] - start_p[1]

			rads = atan2(-dy, dx)
			rads *= -1
			rads %= 2*pi
			degs = degrees(rads)

			return degs
		else :
			# if there isn't a uniqley coloured one inherit rotaion from the old model
			if World.last_world and World.last_world.robots[identity] != None :
				return World.last_world.robots[identity].rot
			else:
				return 0


	def identify_robot(self , colour , sur_p , points):
		World.our_primarys = []
		World.other_primarys = []
		for tup in sur_p:
			if points[World.our_primary].count(tup) > 0 :
				World.our_primarys.append(tup)
			else :
				World.other_primarys.append(tup)

		#assign the robot an unique id based on the colour of the points close to the center
		if colour == World.our_team_colour and len(World.our_primarys) > 1:
			return 0
		elif colour == World.our_team_colour and len(World.other_primarys) > 1:
			return 1
		elif colour == World.oposite_team_colour and len(World.our_primarys) > 1:
			return 2
		elif colour == World.oposite_team_colour and len(World.other_primarys) > 1 :
			return 3
		else :
			return -1
"""



class Robot(object):
	def __init__(self, x , y , rot, x_px, y_px , c_time):
		self.t = c_time
		self.o_x = int(x)
		self.o_y = int(y)
		self.rot = int(rot)
		self.x_px = x_px
		self.y_px = y_px
		self.x = self.projectedX()
		self.y = self.projectedY()

	# accounts for height of topplate and distance form camera
	# to give projected down coordinate
	def projectedX(self):
		cameraXLocation = 150
		cameraHeight = 250
		topPlateHeight = 20
		xCentered = self.o_x - cameraXLocation
		return int(self.o_x - ((topPlateHeight * xCentered) / cameraHeight))

	def projectedY(self):
		cameraYLocation = 110
		cameraHeight = 250
		topPlateHeight = 20
		yCentered = self.o_y - cameraYLocation
		return int(self.o_y - ((topPlateHeight * yCentered) / cameraHeight))

	def get_bounding_box(self):
		"""
		Returns a bounding box for the robot in question. 
		"""
		pos = array((self.x, self.y))
		x1 = self.x
		y1 = self.y
		rads = radians(self.rot)
		corners = [(int(x1 + cos(rads + radians(45) + 90*pi/180*i)*15) , (int(y1 + sin(rads + radians(45)+ 90*pi/180*i)*15))) for i in range(4)]

		return Box(corners[0],corners[1],corners[2],corners[3])

	def get_pos(self):
		"""
		Returns a numpy array of the robots position
		"""
		return array((self.x,self.y))

	def is_on_field(self):
		"""
		Checks if the robot has been seen in the last second. 
		"""
		return self.t + 1 > time()


	def __str__(self):
		return "Robot\n" + str(self.__dict__) 



class Ball(object):
	last_held_by_us = 0
	last_ask = 0

	def __init__(self , x , y , direction, last_ball ,t, robots):	
		self.x = int(x) 
		self.y = int(y)
		self.t = t

		self.dir = direction
		
		#Check that time has actually passed, this should not happen often but who knows
		"""
		if (last_ball != None) and t-last_ball.t > 0:
			self.dir = ((x - last_ball.x)/(t-last_ball.t),(y - last_ball.y)/(t-last_ball.t))
		elif last_ball != None:
			self.dir = last_ball.dir
		else :
			self.dir = (0,0)
		"""

		#Try to figgure our who currently has the ball. if anyone
		holder  = com.isBallHeld(ball = self , robots = robots)

		if last_ball and last_ball.owner == 0 and holder != 0 :
			if Ball.last_ask + 1 < time() : 
				Ball.last_ask = time()
				coms.comunications.Coms.hasball()
				print "HAsball sent"
			self.owner = 0
		elif holder == 0 and last_ball and last_ball.owner != 0:
			if Ball.last_ask + 1 < time() : 
				Ball.last_ask = time()
				coms.comunications.Coms.hasball()
				print "HAsball sent"
			self.owner = -1
		elif Ball.last_held_by_us + 0.5 > self.t :
			self.owner = 0
		elif  last_ball != None and (holder == 4 or (last_ball.owner != -1 and holder != -1)):
			self.owner = last_ball.owner
		else:
			self.owner = holder
		

	def get_pos(self):
		"""
		Returns a numpy array of the robots position
		"""
		return array((self.x,self.y))


	def __str__(self):
		return "Ball\n" + str(self.__dict__) 

	def get_zone(self):
		"""
		Checks which zone the ball is in, ranges from 0 to 3 where 0 is the zone our goal is in and
		3 is the zone the enemy goal is in
		"""
		if World.our_side == "Left" :
			for i in range(0,4):
				if self.x < pitch_x_cm/4 *(i+1) :
					return i 
		else :
			for i in range(0,4):
				if self.x > pitch_x_cm/4*(3-i):
					return i

		return 3




class Box(object):
	"""
	Class used to represent a box defined by 4 ordered points
	"""
	def __init__(self , p1 , p2 , p3 , p4):
		self.points = [p1,p2,p3,p4]
		self.inner = None
		self.outer = None

	def get_center(self):
		acc = array((0,0))
		for point in self.points:
			point = array(point)
			acc = acc+point
		return acc/len(self.points)

	def get_inner_box(self):
		if self.inner == None:
			self.inner = []
			center = self.get_center()
			for x,y in self.points:
				x = x - ROBOT_RADIUS if x > center[0] else x + ROBOT_RADIUS
				y = y - ROBOT_RADIUS if y > center[1] else y + ROBOT_RADIUS
				self.inner.append((x,y))
			self.inner = array(self.inner).astype(int)

		return self.inner



	def get_outer_box(self):
		if self.outer == None:
			self.outer = []
			center = self.get_center()
			for x,y in self.points:
				x = x + ROBOT_RADIUS if x > center[0] else x - ROBOT_RADIUS
				y = y + ROBOT_RADIUS if y > center[1] else y - ROBOT_RADIUS
				self.outer.append((x,y))
			self.outer=array(self.outer).astype(int)

		return self.outer


