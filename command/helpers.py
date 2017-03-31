import postprocessing as pp
from math import atan2 , pi , sqrt , cos , sin , radians , pow  , isinf , isnan
from time import sleep , time
from numpy import *
from numpy import linalg as la
import numpy as np
from collections import namedtuple



"""
This file defines a number of helper methods that can be used to
calculate all manners of usefull things.
"""

def rotate_vector(v , angle):
	m = array([[numpy.cos(angle), -numpy.sin(theta)],
                         [numpy.sin(theta),  numpy.cos(theta)]])


def us_to_obj_angle(us, obj):
	dir_v= (obj.x - us.x , obj.y - us.y)
	dir_r = (cos(radians(us.rot)) , sin(radians(us.rot)))
	return vector_angle(dir_r, dir_v)


def point_dist(x1 , y1 , x2 , y2 ):
	return sqrt(pow(x1 - x2 ,2 ) + pow(y1 - y2 , 2))


def midpoint(x1, y1, x2, y2):
	return array(((x1+x2)/2, (y1+y2)/2))

def get_zone(x, side):
	if side:
		for i in range(0,4):
			if x < 300/4 *(i+1) :
				return i
	else :
		for i in range(0,4):
			if x > 300/4*(3-i):
				return i
	return 3

def ball_close(robot,ball):
    return math.sqrt(math.pow(robot.x -ball.x,2) + math.pow(robot.y - ball.y,2)) < 10

def get_angle_to_send(angle):
	angle = angle % 360
	if angle <= 180:
		return angle
	else:
		return -(360-angle)

	"""
	if angle > 0:
		if angle < 10:
			return angle + 10
		if angle < 40:
			return angle + 5
		else:
			return angle
	else:
		if angle > -10:
			return angle - 10
		if angle > -40:
			return angle - 5
		else:
			return angle
	"""

def get_angle_corrections(angle):
	if angle > 0:
		if angle < 50:
			return 0
		else:
			return 1
	else:
		if angle > -16:
			return 0
		else:
			return 1


def get_time_to_angle(angle):
	if angle < 40:
		return (((angle+42.6+360)/159.6))
	else:
		return (((angle+42.6)/159.6))

def get_time_to_travel(x_curr, x_dest, y_curr, y_dest):
	distance = math.sqrt(math.pow(x_curr - x_dest,2) + math.pow(y_curr - y_dest,2))
	return (distance*0.027503 +0.14169) #.2

def get_time_to_turn(angle):
	if angle < 240:
		return 2
	else:
		return 3

# Given x y get the grid
def get_grid_pos(x,y):
	C = namedtuple("C" , "x y")
	grid_x_size = 50
	grid_y_size = 55
	return C(math.floor((x/grid_x_size)),math.floor((y/grid_y_size)))

# Given grid, get x y center
def get_pos_grid(x,y):
	C = namedtuple("C" , "x y")
	grid_x_size = 50
	grid_y_size = 55
	grid_corner_x =  x * grid_x_size
	grid_corner_y = y * grid_y_size
	grid_center_x = int(grid_corner_x + (grid_x_size/2))
	grid_center_y = int(grid_corner_y + (grid_y_size/2))
	return C(grid_center_x,grid_center_y)

# Given 2 grid location, return distance between the 2
def get_grid_distance(x1,y1,x2,y2,exact=False):
	if exact:
		return math.pow(math.pow(x1 - x2,2) + math.pow(y1 - y2,2),0.5)
	else:
		return abs(x1-x2) + abs(y1-y2)

# returns which zone a xcoor point is in
def point_zone(xcoor, left):
	if left :
		for i in range(0,4):
			if xcoor < 300/4 *(i+1) :
				return i
	else :
		for i in range(0,4):
			if xcoor > 300/4*(3-i):
				return i

	return 3


def dist(a,b):
	a= array(a)
	b = array(b)
	return sqrt(np.sum((a-b)**2))


# Find the angle betweeen u and v, assumes they are 2d vectors
def vector_angle(u , v):
	dot  = u[0]*v[0] + u[1]*v[1]
	det = u[0]*v[1] - u[1]*v[0]
	angle = atan2(det,dot)
	angle = angle*180/pi
	return angle


def set_magnitude( u , mag):
	a = array(u)
	if la.norm(a) != 0 :
		a = (a /la.norm(a)) * mag
	return a

def simple_intercept(op1x,op1y,goalx,goaly,usx,usy):
	pxy = namedtuple("pxy","x y")

	if(goalx < 50):
		pxy.x = op1x - 55
	else:
		pxy.x = op1 + 55
		
	if op1y > 190:
		pxy.y = op1y - 45
	elif op1y > 140:
		pxy.y = op1y - 25
	elif op1y > 108:
		pxy.y = op1y
	elif op1y > 60:
		pxy.y = op1y + 25
	else:
		pxy.y = op1y + 45
	return pxy

def calculate_intercept_p(op1p , op2p ,usp) :
	"""
	calculate the closest point on the line op1p to op2p from usp
	Note that this point is not guarnteed to between op1p and op2p
	"""
	op1p = array(op1p)
	op2p = array(op2p)
	usp = array(usp)

	a_to_p = usp - op1p
	a_to_b = op2p - op1p
	atb2 = pow(la.norm(a_to_b), 2)
	atpdatb = dot(a_to_p,a_to_b)
	t = atpdatb / atb2

	point = op1p + a_to_b*t

	limit1 = op1p + set_magnitude(a_to_b , 35 )
	limit2 = op2p + set_magnitude(-1*a_to_b , 35)
	limddist = dist(limit1 , limit2)

	if dist(point, limit1) +dist(point, limit2) > limddist +1 :
		if dist(point , limit1) < dist(point, limit2):
			point = limit1
		else :
			point = limit2



	return point


def calculate_path(start , target, boxes):

	"""
	Calculate a path such that the robot never enters any box in boxes, path might have some redundancy but I don't think that will be a major problem

	This method needs more testing if it is to be used reliably
	"""

	col = []
	for box in boxes:
		if point_in_box(target , box) :
			col.append(box)

	if len(col) > 0 :
		col = sorted(col , key = lambda box : traingle_area(box[0] , box[1] , box[2]) + traingle_area(box[0], box[3] , box[2]))
		box = col[0]
		ret = find_intersecting_edge(start , target , box)
		if ret != None :
			_ , _ , tmp = ret
			target = tmp



	changed = True
	path = [start,target]
	while changed :
		changed = False
		for i in range(0,len(path) -1):
			sub_start = path[i]
			sub_end = path[i+1]
			for i2 , box in enumerate (boxes):
				sub_path = calculate_path_around(sub_start , sub_end , box)
				if len(sub_path) > 1 :
					changed = True
					begin = path[:i+1]
					if i+2 < len(path):
						end = path[i+2:]
					else :
						end = []
					begin.extend(sub_path)
					begin.extend(end)
					path = begin
					boxes.pop(i2)
					break
			if changed :
				break

	return path[1:]


# NOTE: this is not adequately tested so is currently not in use
def calculate_path_around(start , target , box):
	"""
	Calculate a path from start to target around a box
	a box is defined as four points where if two are next to each other in the collection
	there is a bounding line between them. Note that the first and the last are considdered linked

	Returns a list of points to travel by, the final point is allways target, does not include start
	"""

	box = array(box)
	start = array(start)
	target = array(target)

	if len(box) != 4 or point_in_box(start , box) or point_in_box(target,box) :
		return [target]

	crossed_segments = []

	#find which lines we intersect
	for i in range(0,4):
		p1 = box[i]
		p2 = box[(i + 1)%4]
		intersect = seg_intersect(start , target , p1 , p2)
		if not isnan(intersect[0])  and not isinf(intersect[0]) and (point_between(intersect , start , target) ):
			crossed_segments.append((p1,p2))


	if len(crossed_segments) < 2 :
		return [target]


	#Filter out extra connections that appear in some edge cases
	if len(crossed_segments) > 2 :
		temp = []
		points = sorted(box , key = lambda x :  dist(x,start))
		far = points[-1]
		close = points[0]
		far_p = False
		close_p = False
		for p1 , p2 in crossed_segments:
			if ((p1.tolist() ==  close.tolist()) or (p2.tolist() ==  close.tolist())) and not close_p :
				temp.append((p1 , p2))
				close_p = True
			if (p1.tolist() == far.tolist() or p2.tolist() == far.tolist()) and not far_p :
				temp.append((p1 , p2))
				far_p = True
		crossed_segments = temp


	line1 = crossed_segments[0]
	line2 = crossed_segments[1]

	#If the two lines we are intercepting are next to each other we just travel by their shared point.
	if (line1[1].tolist() ==line2[0].tolist() ) :
		return [line1[1] , target]
	elif( line1[0].tolist() == line2[1].tolist()) :
		return [line1[0] , target]
	else :
		#If they are not next to each other there are two possible paths
		path1 = [line1[0] , line2[1]]
		path2 = [line1[1] , line2[0]]
		if (dist(start , path1[0]) > dist(start, path1[1])):
			path1.reverse()
		if (dist(start , path2[0]) > dist(start, path2[1])):
			path2.reverse()

		#find the shortest path
		length1 = dist(start , path1[0]) + dist(path1[0],path1[1])  + dist(path1[1] , target)
		length2	= dist(start , path2[0]) + dist(path2[0],path2[1])  + dist(path2[1] , target)

		#if one of the paths contain points which are outside the pitch it pick the other
		if len([p for p in path1 if not  point_in_box(p , pp.world.World.get_pitch().get_inner_box())]) != 0 :
			path2.append(target)
			final = path2
		elif (length1 < length2):
			path1.append(target)
			final =  path1
		else :
			path2.append(target)
			final = path2

		#I might be the case that we don't have to travel by both of the points in the path. Check for this
		point = seg_intersect(start , final[1] , path1[0] , path2[0])
		if not isnan(point[0])  and not isinf(point[0]) and not point_between(point , path1[0] , path2[0]) :
			return [final[1] , target]
		else :
			return final

		return final


def point_between(point , end1 , end2, error_margin = 0.001):
	"""
	Checks if point is between end1 and end2 and on the line defined by them
	"""
	return dist(point , end1) + dist(point , end2) < dist(end1 , end2) + error_margin


def seg_intersect(a1,a2, b1,b2) :
    """
    Taken from http://stackoverflow.com/questions/3252194/numpy-and-line-intersections
    Returns an array of infs if the lines are paralell
    Returns an array of Nans if the lines are equal
    """
    a1 = array(a1)
    a2 = array(a2)
    b1 = array(b1)
    b2 = array(b2)


    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = dot( dap, db)
    num = dot( dap, dp )
    return (num / denom.astype(float))*db + b1


def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def point_in_boxes(point, boxes):
	for box in boxes :
		if point_in_box(point , box) :
			return True
	return False


def point_in_box(point , box ):
	"""
	As the title says, check if a point is inside a box
	by calculating the area of the box and the area of some triangles
	"""
	area = traingle_area(box[0] , box[1] , box[2]) + traingle_area(box[0], box[3] , box[2])
	acc = 0
	for i in range(0,len(box)):
		p1 = box[i]
		p2 = box[(i+1)%len(box)]
		acc = acc + traingle_area(p1,p2,point)

	return abs(acc - area) < 2 # Chnage the two here if your scale is smaller. it's there to deal with integer scale rounding errors


def traingle_area(p1,p2,p3):
	area = abs((p1[0]*(p2[1]-p3[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p1[1]-p2[1])))/2.0
	return area


def find_intersecting_edge(start , finish , box):
	"""
	Finds the edge of box which the line start finish crosses
	returns a trupel containing the the points defining the edge and the intersection point
	"""
	for i in range(0,4):
		p1 = box[i]
		p2 = box[(i+1)%4]
		intersect = seg_intersect(start , finish , p1 , p2 )
		if not isnan(intersect[0])  and not isinf(intersect[0]) and (point_between(intersect , start , finish) ):
			return (p1,p2 , intersect)

	return None


def find_closest_edge(point ,  box ):
	"""
	Finds the closest edge from a point to a box
	"""
	distances = [(traingle_area(box[i] , box[(i+1)%4] , point)/dist(box[i] , box[(i+1)%4]),box[i] , box[(i+1)%4]) for i in range(0,4)]
	distances = sorted(distances , key = lambda p : p[0])
	return distances[0][1] , distances[0][2]


def isBallHeld(ball = None , robots = None):
	"""
	If we can't see the ball, return 4
	If a robot holds the ball return the index of that robot
	Otherwise return -1
	"""
	if robots == None :
		world = waitForWorld(False)
		robots = world.robots

	if ball == None :
		world = waitForWorld(False)
		ball = world.ball

	# cant see ball
	if ball.x == 0 and ball.y == 0:
		return 4

	t = time()

	if t - ball.t > 0.2 and t - ball.t < 1:
		#If we can't see the ball try to determine if someone might have grabbed it recently.
		for i , robot  in enumerate(robots):
			if robot != None and point_dist(robot.x , robot.y , ball.x , ball.y) < 20:
				return i
		return 4
	#if the ball has been gone for longer than 1.5 seconds, assume that we cannot use the current positions of robots to determine who has it
	elif  t - ball.t > 1 :
		return 4

	for i , robot  in enumerate(robots):
		if robot == None:
			continue
		dist = point_dist(robot.x , robot.y , ball.x , ball.y)
		angle = us_to_obj_angle(robot , ball)
		if  robot != None  and ((dist < 20 and abs(angle) < 45) or dist < 10):
			return i

	return -1


def isBallStill():
	"""
	Checks if the ball is still by getting the ball position, waiting, ad getting it again
	"""
	b1 = waitForWorld(False).ball
	#Todo, experiment with timeout to find lowest possible value
	sleep(0.2)
	b2 = waitForWorld(False).ball
	d = point_dist(b1.x, b1.y , b2.x , b2.y)

	return d < 5


def waitForWorld(requireTeammate = False , requireBall = True , no_oponents = 0):
	"""
	Waits for a world model that fullfills the required conditions and returns that
	"""
	world = pp.world.World.get_world()
	no_oponents = no_oponents if no_oponents <= 2 else 2
	while world == None or world.robots[0] == None or (requireBall and world.ball == None) or (requireTeammate and world.robots[1] == None) or (no_oponents > len([world.robots[i] for i in range(2,4) if world.robots[i] != None])) : #Congratulations on making it to the end of the conditional
		world = pp.world.World.get_world()
	return world


def robotIsGoalie(robot, left):
	"""
	Given a robot object and side of pitch,
	checks if they're in suitable position for goalkeeping in penalty situation
	"""
	if robot == None or (time() - robot.t) > 5:
		return False
	y_okay = robot.get_pos()[1] > 70 and robot.get_pos()[1] < 150
	if left:
		x_okay = robot.get_pos()[0] < 50
	else:
		x_okay = robot.get_pos()[0] > 250
	return y_okay and x_okay


def getPenaltyGoaliePos(us, op1, op2):
	left = us.get_pos()[0] < 150
	if robotIsGoalie(op1, left):
		return op1.get_pos()
	elif robotIsGoalie(op2, left):
		return op2.get_pos()
	else:	# if we can't see any robot
		print "Can't see a goalie"
		if left:
			return array((0,110))
		else:
			return array((300,110))


def robotIsPenaltyTaker(robot, left):
	"""
	Given a robot object and side of pitch,
	checks if they're in suitable position for taking a penalty against us
	"""
	if robot == None or robot.is_on_field() == False:
		return False
	y_okay = robot.get_pos()[1] > 50 and robot.get_pos()[1] < 170
	if left:
		x_okay = robot.get_pos()[0] < 130
	else:
		x_okay = robot.get_pos()[0] > 150
	return y_okay and x_okay


def getPenaltyTakerPos(left, op1, op2):
	if robotIsPenaltyTaker(op1, left):
		return op1
	elif robotIsPenaltyTaker(op2, left):
		return op2
	else:
		return None

"""
# TODO May need some callibration and change of algorithm
def noSensorHasBall(me,ball):
	# Acceptable distance and angle for hasBall assumption
	dist = 10
	angle = 30

	dist_a = math.sqrt(math.pow(me.x-ball.x,2)+math.pow(me.y-ball.y,2));
	dist_b = ball.y-me.y;
	angle_a = me.rot - math.acos(dist_a/dist_b)

	return angle_a < angle and dist_a < dist

	return True
"""
