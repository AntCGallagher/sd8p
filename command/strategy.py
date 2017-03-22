from postprocessing.world import World
from communications.communications import Comms
from helpers import *
import math
import time
import numpy as np
from gridworld import GridWorld
"""
This script will be used to test a simple strategy.
"""
BOTLEFX = 30
BOTLEFY = 195
BOTRIGX = 250
BOTRIGY = 190
TOPLEFX = 38
TOPLEFY = 20
TOPRIGX = 255
TOPRIGY = 36
LEFTGOALX = 21
LEFTGOALY = 109
SHOOTLEFTX = 15
SHOOTLEFTY = 98
SHOOTRIGHTX = 286
SHOOTRIGHTY = 125
RIGHTGOALX = 286
RIGHTGOALY = 111
CORNER14X = 50
CORNER14Y = 108
CORNER23X = 250
CORNER23Y = 108
MIDX = 160
MIDY = 108
MAX_MOVEMENT_TIME = 1.5
TARGETLOCTOPX = 160
TARGETLOCTOPY = 36
TARGETLOCBOTX = 160
TARGETLOCBOTY = 195


class Strategy(object):
    def __init__(self):
        self.owner = 0
        self.teammate_on = 0
        self.comms = Comms()


    def tests(self):
        inp = ""
        comms = Comms()
        comms.start()
        while inp != "done":
            inp = raw_input("(p/gxy/grb/t/m/turntest/turntest2/g/pos/rpos/gridxy/xygrid/rgrid)")
            if inp == "p":
                curr_world = World.get_world()
                ball = curr_world.ball
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                robot1 = curr_world.robots[1]
                robot2 = curr_world.robots[2]
                robot3 = curr_world.robots[3]
                if robot0 != None:
                    print "Robot0: ", robot0.x , "  " , robot0.y, " ", robot0.rot
                if robot1 != None:
                    print "Robot1: ", robot1.x , "  " , robot1.y
                if robot2 != None:
                    print "Robot2: ", robot2.x , "  " , robot2.y
                if robot3 != None:
                    print "Robot3: ", robot3.x , "  " , robot3.y
                if ball != None:
                    print "Ball: " , ball.x , "  " , ball.y
                print "\n"
            if inp == "gxy":
                dest_x = float(raw_input("dest_x: "))
                dest_y = float(raw_input("dest_y: "))
                time_action = int(raw_input("time to go: "))
                comms.stop()
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                if robot0 != None:
                    currTime = time.time()
                    comms.goxy(robot0.x,robot0.x,robot0.rot,dest_x,dest_y)
                    while(time.time() - currTime < time_action):
                        diff = time.time() - currTime
                        print "Time difference: ",diff
                        curr_world = World.get_world()
                        robots = curr_world.robots
                        robot0 = curr_world.robots[0]
                        if robot0 != None:
                            print "Robot: ",robot0.x, " ", robot0.y, " ", robot0.rot
                            comms.updatewm(time.time(),robot0.x,robot0.y,robot0.rot)
                        else:
                            print "Lost robot!"
                        time.sleep(0.4)
                    comms.stop()
                else:
                    print "Robot not detected"
                comms.stop()
            if inp == "trb":
                curr_world = World.get_world()
                ball = curr_world.ball
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                if robot0 != None and ball != None:
                    C = namedtuple("C" , "x y")
                    angle_to_obj = us_to_obj_angle(robot0,C(ball.x,ball.y))
                    angle_to_obj = get_angle_to_send(angle_to_obj)
                    time_to_turn = get_time_to_turn(angle_to_obj)
                    print "robot: ", robot0.x, " ", robot0.y
                    print "ball: ", ball.x, " ", ball.y
                    print "angle: ", angle_to_obj
                    comms.turn(angle_to_obj)
                    time.sleep(time_to_turn)
                    comms.stop()
                elif robot0 == None and ball != None:
                    print "Robot and ball not detected"
                elif robot0 == None:
                    print "Robot not detected"
                else:
                    print "Ball not detected"
            if inp == "grb":
                curr_world = World.get_world()
                ball = curr_world.ball
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                if robot0 != None and ball != None:
                    C = namedtuple("C" , "x y")
                    time_to_object = get_time_to_travel(robot0.x,ball.x,robot0.y,ball.y)
                    angle_to_obj = us_to_obj_angle(robot0,C(ball.x,ball.y))
                    time_to_turn = get_time_to_turn(angle_to_obj)
                    print "robot: ", robot0.x, " ", robot0.y
                    print "ball: ", ball.x, " ", ball.y
                    print "time: ", time_to_object, " angle: ", angle_to_obj
                    comms.turn(angle_to_obj,3)
                    time.sleep(time_to_turn)
                    comms.go()
                    time.sleep(time_to_object)
                    comms.stop()
                elif robot0 == None and ball != None:
                    print "Robot and ball not detected"
                elif robot0 == None:
                    print "Robot not detected"
                else:
                    print "Ball not detected"
            if inp == "t":
                value = int(raw_input("angle to turn: "))
                ang = get_angle_to_send(value)
                comms.turn(ang,0)
                time.sleep(1.5)
            if inp == "go":
                value = float(raw_input("Time to go: "))
                self.basicGoSensor(comms,value)
            if inp == "s":
                comms.stop()
                time.sleep(1)
            if inp == "comp":
    			comms.stop()
    			comms.getcompass()
    			time.sleep(1)
            if inp == "gox":
                curr_world = World.get_world()
                ball = curr_world.ball
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                if robot0 != None and ball != None:
                    C = namedtuple("C" , "x y")
                    value = float(raw_input("X to go: "))
                    time_to_travel = get_time_to_travel(robot0.x,robot0.x+value, robot0.y, robot0.y)
                    comms.go()
                    time.sleep(time_to_travel)
                    comms.stop()
                elif robot0 == None and ball != None:
                    print "Robot and ball not detected"
                elif robot0 == None:
                    print "Robot not detected"
                else:
                    print "Ball not detected"
            if inp == "m":
                curr_world = World.get_world()
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                list = []
                calculated_time = time.time() + 1
                while(calculated_time > time.time()):
                    temp_world = World.get_world()
                    list.append(temp_world.robots[0].rot)
                list.sort()
                print "Curr rot: robot0.rot"
                print np.median(list)
                print len(list)
                print robot0.rot
            if inp == "turntest":
                inp = int(raw_input("value to turn: "))
                if angle < 15 and angle > -15:
                    angle = angle + 360
                    print "Angle too small, plus 360"
                comms.turn(inp,3)
                time.sleep(2)
                comms.stop()
            if inp == "goxytest":
    			comms.stop()
    			fX = raw_input('from X: ')
    			fY = raw_input('from Y: ')
    			h = raw_input('Heading: ')
    			tX = raw_input('to X: ')
    			tY = raw_input('to Y: ')
    			comms.goxy(fX, fY, h, tX, tY)
            if inp == "ballgrid":
                teamSideLeft = World.our_side == "Left"
                curr_world = World.get_world()
                ball = curr_world.ball
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                if robot0 != None and ball != None:
                    ball_grid = get_grid_pos(ball.x,ball.y)
                    C = namedtuple("C" , "x y")
                    angle_to_obj = us_to_obj_angle(robot0,C(ball.x,ball.y))
                    angle_to_obj = get_angle_to_send(angle_to_obj)
                    time_to_turn = get_time_to_turn(angle_to_obj)
                    turn_angle = get_angle_to_send(angle_to_obj)
                    if turn_angle != 0:
                        print "Turnning to ball angle: ", angle_to_obj
                        comms.turn(angle_to_obj,3)
                        time.sleep(time_to_turn)
                        comms.stop()
                    time_to_object = get_time_to_travel(robot0.x,ball.x,robot0.y,ball.y)
                    print "Time to sleep: ", time_to_object
                    time.sleep(0.1)
                    comms.grab(1)
                    time.sleep(0.4)
                    comms.go()
                    time.sleep(time_to_object)
                    comms.stop()
                    time.sleep(0.2)
                    comms.grab(0)
                    curr_world = World.get_world()
                    ball = curr_world.ball
                    robots = curr_world.robots
                    robot0 = curr_world.robots[0]
                    if robot0 != None and ball != None:
                        time.sleep(1)
                        C = namedtuple("C" , "x y")
                        goal = C(SHOOTLEFTX,SHOOTLEFTY)
                        if teamSideLeft:
                            goal = C(SHOOTRIGHTX,SHOOTRIGHTY)
                        time.sleep(0.2)
                        angle_to_obj = us_to_obj_angle(robot0,goal)
                        turn_angle = get_angle_to_send(angle_to_obj)
                        time_to_turn = get_time_to_turn(turn_angle)
                        if turn_angle != 0:
                            print "Turnning to ball angle: ", turn_angle
                            comms.turn(turn_angle,5)
                            time.sleep(time_to_turn)
                            comms.stop()
                        time.sleep(1)
                        comms.kick(10)
                        time.sleep(1)
                elif robot0 == None and ball != None:
                    print "Robot and ball not detected"
                elif robot0 == None:
                    print "Robot not detected"
                else:
                    print "Ball not detected"
            if inp == "turnball":
                curr_world = World.get_world()
                ball = curr_world.ball
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                if robot0 != None and ball != None:
                    C = namedtuple("C" , "x y")
                    angle_to_obj = us_to_obj_angle(robot0,C(ball.x,ball.y))
                    turn_angle = get_angle_to_send(angle_to_obj)
                    corrections = get_angle_corrections(turn_angle)
                    time_to_turn = get_time_to_turn(turn_angle)
                    print turn_angle, " turning this"
                    if turn_angle != 0:
                        print "Turnning to ball angle: ", angle_to_obj, " turn angle: ", turn_angle, " and correcting: ", corrections
                        comms.turn(turn_angle,corrections)
                        time.sleep(time_to_turn)
                        comms.stop()
                elif robot0 == None and ball != None:
                    print "Robot and ball not detected"
                elif robot0 == None:
                    print "Robot not detected"
                else:
                    print "Ball not detected"
            if inp == "grabgridball":
                curr_world = World.get_world()
                ball = curr_world.ball
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                if robot0 != None and ball != None:
                    C = namedtuple("C" , "x y")
                    comms.grab(1)
                    time.sleep(1.8)
                    comms.go()
                    time.sleep(0.4)
                    comms.stop()
                    time.sleep(0.8)
                    comms.grab(0)
                    time.sleep(0.2)
            if inp == "turngoal":
                curr_world = World.get_world()
                ball = curr_world.ball
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                teamSideLeft = World.our_side == "Left"
                if robot0 != None:
                    comms.grab(0)
                    time.sleep(0.5)
                    C = namedtuple("C" , "x y")
                    goal = C(SHOOTLEFTX,SHOOTLEFTY)
                    if teamSideLeft:
                        goal = C(SHOOTRIGHTX,SHOOTRIGHTY)
                    time.sleep(0.2)
                    angle_to_obj = us_to_obj_angle(robot0,goal)
                    turn_angle = get_angle_to_send(angle_to_obj)
                    time_to_turn = get_time_to_turn(turn_angle)
                    if turn_angle != 0:
                        print "Turnning to ball angle: ", turn_angle
                        comms.turn(turn_angle,3)
                        time.sleep(time_to_turn)
                        comms.stop()
                    time.sleep(1)
                    comms.kick(10)
                    time.sleep(1)
            if inp == "turntest2":
                curr_world = World.get_world()
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                ball = curr_world.ball
                print robot0.rot, " current rotation"
                angle = us_to_obj_angle(robot0,ball)
                print angle, "angle to ball"
                angle = get_angle_to_send(angle)
                comms.turn(angle,3)
            if inp == "gridxy":
                inpx = int(raw_input("x value: "))
                inpy = int(raw_input("y value: "))
                print(get_grid_pos(inpx,inpy))
            if inp == "g":
                comms.grab(0)
            if inp == "pos":
            	print("Positions:", getPos())
            if inp == "rpos":
                resetPos()
            if inp == "xygrid":
                inpx = int(raw_input("x grid value: "))
                inpy = int(raw_input("y grid value: "))
                print(get_pos_grid(inpx,inpy))
            if inp == "rgrid":
                robot_num = int(raw_input("robot num: "))
                curr_world = World.get_world()
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                robot1 = curr_world.robots[1]
                robot2 = curr_world.robots[2]
                robot3 = curr_world.robots[3]
                ball = curr_world.ball
                if robot_num == 0:
                    if robot0 != None:
                        print get_grid_pos(robot0.x,robot0.y)
                if robot_num == 1:
                    if robot1 != None:
                        print get_grid_pos(robot1.x,robot1.y)
                if robot_num == 2:
                    if robot2 != None:
                        print get_grid_pos(robot2.x,robot2.y)
                if robot_num == 3:
                    if robot3 != None:
                        print get_grid_pos(robot3.x,robot3.y)
                if robot_num == 4:
                    if ball != None:
                        print get_grid_pos(ball.x,ball.y)
            if inp == "ug":
                comms.grab(1)
            if inp == "kick":
                comms.kick(10)
            if inp == "ballnearby":
                curr_world = World.get_world()
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                ball = curr_world.ball
                if robot0 != None and ball != None:
                    if (math.pow((robot0.x - robot1.x),2) + math.pow((robot0.y - robot1.y),2)) < math.pow(10,2):
                        print "Ball is close"
                    else:
                        print "Ball is far"
            if inp == "collision":
                value = float(raw_input("Time to go: "))
                curr_world = World.get_world()
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                robot1 = curr_world.robots[1]
                robot2 = curr_world.robots[2]
                robot3 = curr_world.robots[3]
                # Need to account for rotation
                comms.go()
                curr_time = time.time()
                while(time.time()-curr_time < value):
                    print "Time difference: ", time.time() - curr_time, " Value: ", value
                    time.sleep(0.1)
                    curr_world = World.get_world()
                    robots = curr_world.robots
                    robot0 = curr_world.robots[0]
                    robot1 = curr_world.robots[1]
                    robot2 = curr_world.robots[2]
                    robot3 = curr_world.robots[3]
                    colliding = False
                    if robot0 != None:
                        if robot1 != None and robot1.x != robot0.x and robot1.y != robot0.y:
                            print "Distance 1: ", (math.pow((robot0.x - robot1.x),2) + math.pow((robot0.y - robot1.y),2))
                            if (math.pow((robot0.x - robot1.x),2) + math.pow((robot0.y - robot1.y),2)) < math.pow(52,2) and math.pow((robot0.y - robot1.y),2) < math.pow(20,2):
                                colliding = True
                        if robot2 != None:
                            print "Distance 2: ", (math.pow((robot0.x - robot2.x),2) + math.pow((robot0.y - robot2.y),2))
                            if (math.pow((robot0.x - robot2.x),2) + math.pow((robot0.y - robot2.y),2)) < math.pow(52,2) and math.pow((robot0.y - robot1.y),2) < math.pow(20,2):
                                colliding = True
                        if robot3 != None:
                            print "Distance 3: ", (math.pow((robot0.x - robot3.x),2) + math.pow((robot0.y - robot3.y),2))
                            if (math.pow((robot0.x - robot3.x),2) + math.pow((robot0.y - robot3.y),2)) < math.pow(52,2) and math.pow((robot0.y - robot1.y),2) < math.pow(20,2):
                                colliding = True
                    if colliding:
                        comms.stop()
                        break
            if inp == "intercept":
                our_x = int(raw_input("our x: "))
                our_y = int(raw_input("our x: "))
                their_x = int(raw_input("our x: "))
                their_y = int(raw_input("our x: "))
                our_x = int(raw_input("our x: "))
            if inp == "hasball":
                comms.stop()
                time.sleep(0.2)
                comms.hasball()
                time.sleep(0.2)
                print(comms.got_ball())
            if inp == "reverse":
                curr_world = World.get_world()
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                robot1 = curr_world.robots[1]
                robot2 = curr_world.robots[2]
                robot3 = curr_world.robots[3]
                me = robot0
                print "Positon: ", me.x, " ", me.y, " ", me.rot
                reverse = False

                if me.x < 45:
                    if me.y > 187:
                        if not(me.rot >= 270 or (me.rot >= -90 and me.rot <= 90)):
                            reverse = True
                    elif me.y < 36:
                        if ((me.rot <= -270 or not(me.rot >= -90 and me.rot <= 90))):
                            reverse = True
                    else:
                        if not(me.rot >= -90 and me.rot <= 90):
                            reverse = True
                elif me.x > 260:
                    if me.y > 187:
                        if not((me.rot <= 270 and me.rot >= 180) or (me.rot >= -180 and me.rot <= -90)):
                            reverse = True
                    elif me.y < 36:
                        if ((me.rot <= 270 and me.rot >= 180) or (me.rot >= -180 and me.rot <= -90)):
                            reverse = True
                    else:
                        if not((me.rot >= 90 and me.rot <= 270) or (me.rot <= -90 and me.rot >= -270)):
                            reverse = True
                elif me.y > 187:
                    if me.x > 260:
                        if not((me.rot <= 270 and me.rot >= 180) or (me.rot >= -180 and me.rot <= -90)):
                            reverse = True
                    elif me.x < 45:
                        if not(me.rot >= 270 or not(me.rot >= -90 and me.rot <= 0)):
                            reverse = True
                    else:
                        if not((me.rot >= 180 and me.rot <= 360) or (me.rot <= 0 and me.rot >= -180)):
                            reverse = True
                elif me.y < 36:
                    if me.x > 260:
                        if ((me.rot <= 270 and me.rot >= 180) or (me.rot >= -180 and me.rot <= -90)):
                            reverse = True
                    elif me.x < 45:
                        if ((me.rot <= -270 and me.rot >= -360) or (me.rot >= 0 and me.rot <= 90)):
                            reverse = True
                    else:
                        if not((me.rot >= 0 and me.rot <= 180) or (me.rot <= -180 and me.rot >= -360)):
                            reverse = True

                if (reverse):
                    print "Strategy: Too close to the wall reversing"
                    comms.reverse(100)
                    time.sleep(1)
                    comms.stop()
                else:
                    comms.go()
                    time.sleep(1)
                    comms.stop()
            if inp == "zone":
                robot_num = int(raw_input("robot num: "))
                teamSideLeft = World.our_side == "Left"
                curr_world = World.get_world()
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                robot1 = curr_world.robots[1]
                robot2 = curr_world.robots[2]
                robot3 = curr_world.robots[3]
                ball = curr_world.ball
                if robot_num == 0:
                    if robot0 != None:
                        print get_zone(robot0.x,teamSideLeft)
                if robot_num == 1:
                    if robot1 != None:
                        print get_zone(robot1.x,teamSideLeft)
                if robot_num == 2:
                    if robot2 != None:
                        print get_zone(robot2.x,teamSideLeft)
                if robot_num == 3:
                    if robot3 != None:
                        print get_zone(robot3.x,teamSideLeft)
                if robot_num == 4:
                    if ball != None:
                        print get_zone(ball.x,teamSideLeft)
            if inp == "pf":
                curr_world = World.get_world()
                robots = curr_world.robots
                me = curr_world.robots[0]
                juno = curr_world.robots[1]
                robot2 = curr_world.robots[2]
                robot3 = curr_world.robots[3]
                ball = curr_world.ball

                our_grid_pos = None
                ball_grid_pos = None
                juno_grid_pos = None
                robot2_grid_pos = None
                robot3_grid_pos = None
                if ball != None:
                    ball_grid_pos = get_grid_pos(ball.x,ball.y)
                if me != None:
                    our_grid_pos = get_grid_pos(me.x,me.y)
                if juno != None:
                    juno_grid_pos = get_grid_pos(juno.x,juno.y)
                if robot2 != None:
                    robot2_grid_pos = get_grid_pos(robot2.x,robot2.y)
                if robot3 != None:
                    robot3_grid_pos = get_grid_pos(robot3.x,robot3.y)

                pfobs = namedtuple("pfobs","x y")
                box = []
                if juno != None:
                    box.append(pfobs(int(juno_grid_pos.x),int(juno_grid_pos.y)))
                if robot2 != None:
                    box.append(pfobs(int(robot2_grid_pos.x),int(robot2_grid_pos.y)))
                if robot3 != None:
                    box.append(pfobs(int(robot3_grid_pos.x),int(robot3_grid_pos.y)))

                if me != None and ball != None:
                    me = namedtuple("me","x y")
                    test = self.gridGoXY(me(int(our_grid_pos.x),int(our_grid_pos.y)),int(ball_grid_pos.x),int(ball_grid_pos.y),box)
                    print test
                else:
                    print "Me or Ball not found"


    def getPos():
        comms = Comms()
    	comms.com.ser.write(bytes('Y'))
    	time.sleep(1)
    	with open(comms.outputFilename) as f:
    		log = f.readlines()
    		positions = log[len(log)-2]
    		positions = [int(pos) for pos in positions.split() if pos[1:].isdigit() or pos.isdigit()]
    	#positions[3] = left wheel;
    	#positions[5] = right wheel;
    	#positions[4] = omni wheel;
    	#positions[2] = kicker;
    	return positions

    def resetPos():
        comms = Comms()
    	comms.ser.write(bytes('Z'))
    	time.sleep(1)
    	with open(comms.outputFilename) as f:
    		log = f.readlines()
    		positions = log[len(log)-2]
    		positions = [int(pos) for pos in positions.split() if pos[1:].isdigit() or pos.isdigit()]
    	return positions

    def gridGoXY(self,me,destx,desty,obstacles):
        grid = [["Empty" for x in xrange(4)] for y in xrange(6)]
        grid[me.x][me.y] = "Start"
        grid[destx][desty] = "Goal"
        """
        for i in obstacles:
            grid[i.x][i.y] = "Obstacle"
        """
        gridtuple = namedtuple("gridtuple","x y path stat")
        location = gridtuple(me.x,me.y,[],"Start")
        queue = [location]

        self.printgrd(grid)

        while (len(queue) > 0):
            currentlocation = queue.pop()

            # Checking up
            newlocationn = self.exploreInDirection(currentlocation,"North",grid)
            if newlocationn.stat =="Goal":
                return newlocationn.path
            elif newlocationn.stat == "Valid":
                grid[newlocationn.x][newlocationn.y] = "Visited"
                queue.append(newlocationn)

            # Checking right
            newlocatione = self.exploreInDirection(currentlocation,"East",grid)
            if newlocatione.stat =="Goal":
                return newlocatione.path
            elif newlocatione.stat == "Valid":
                grid[newlocatione.x][newlocatione.y] = "Visited"
                queue.append(newlocatione)

            # Checking down
            newlocations = self.exploreInDirection(currentlocation,"South",grid)
            if newlocations.stat =="Goal":
                return newlocations.path
            elif newlocations.stat == "Valid":
                grid[newlocations.x][newlocations.y] = "Visited"
                queue.append(newlocations)

            # Checking left
            newlocationw = self.exploreInDirection(currentlocation,"West",grid)
            if newlocationw.stat =="Goal":
                return newlocationw.path
            elif newlocationw.stat == "Valid":
                grid[newlocationw.x][newlocationw.y] = "Visited"
                queue.append(newlocationw)


        print "PATHFINDING: No path to objective found"
        return False

    def exploreInDirection(self,location,direction,grid):
        gridtuple = namedtuple("gridtuple","x y path stat")

        newPath = location.path
        newPath.append(direction)

        x = location.x
        y = location.y

        if direction == "North":
            y -= 1
        elif direction == "South":
            y += 1
        elif direction == "East":
            x += 1
        elif direction == "West":
            x -= 1

        nextstatus = self.getLocationStatus(x,y,grid)
        nextlocation = gridtuple(x,y,newPath,nextstatus)

        return nextlocation

    def getLocationStatus(self,x,y,grid):
        if x < 0 or x > 5 or y < 0 or y > 3:
            return "Invalid"
        elif grid[x][y] == "Goal":
            return "Goal"
        elif grid[x][y] != "Empty":
            return "Blocked"
        else:
            return "Valid"

    def printgrd(self,grid):
        for x in xrange(4):
            row = []
            for y in xrange(6):
                row.append(grid[y][x])
            print row

    """
    Methods to make strategy readable
    """

    def basicGo(self,comms,sleeptime):
        comms.go()
        time.sleep(sleeptime)
        comms.stop()
        time.sleep(0.1)

    def basicGoSensor(self,comms,sleeptime):
        comms.grab(1)
        time.sleep(0.2)
        comms.go()
        time.sleep(sleeptime)
        comms.stop()
        time.sleep(0.2)
        if comms.got_ball():
            print "Currently have the ball"
        else:
            print "No ball"

    def basicGoSensorCollision(self,comms,sleeptime):
        grabbed = False
        colliding = False
        comms.grab(1)
        time.sleep(0.2)
        comms.go()
        curr_time = time.time()
        while(time.time()-curr_time < sleeptime):
            curr_world = World.get_world()
            robots = curr_world.robots
            robot0 = curr_world.robots[0]
            robot1 = curr_world.robots[1]
            robot2 = curr_world.robots[2]
            robot3 = curr_world.robots[3]
            time.sleep(0.1)
            comms.hasball()
            time.sleep(0.3)
            if comms.got_ball():
                print "Saw ball"
                grabbed = True
                comms.stop()
                comms.grab(0)
                break
            if robot0 != None:
                if robot1 != None and robot1.x != robot0.x and robot1.y != robot0.y:
                    #print "Distance 1: ", (math.pow((robot0.x - robot1.x),2) + math.pow((robot0.y - robot1.y),2))
                    if (math.pow((robot0.x - robot1.x),2) + math.pow((robot0.y - robot1.y),2)) < math.pow(52,2) and math.pow((robot0.y - robot1.y),2) < math.pow(20,2):
                        colliding = True
                if robot2 != None:
                    #print "Distance 2: ", (math.pow((robot0.x - robot2.x),2) + math.pow((robot0.y - robot2.y),2))
                    if (math.pow((robot0.x - robot2.x),2) + math.pow((robot0.y - robot2.y),2)) < math.pow(52,2) and math.pow((robot0.y - robot1.y),2) < math.pow(20,2):
                        colliding = True
                if robot3 != None:
                    #print "Distance 3: ", (math.pow((robot0.x - robot3.x),2) + math.pow((robot0.y - robot3.y),2))
                    if (math.pow((robot0.x - robot3.x),2) + math.pow((robot0.y - robot3.y),2)) < math.pow(52,2) and math.pow((robot0.y - robot1.y),2) < math.pow(20,2):
                        colliding = True
            if colliding:
                comms.stop()
                break
        comms.stop()
        time.sleep(0.2)
        comms.grab(0)
        if grabbed:
            print "Grabbed"
        else:
            print "No ball"
        if colliding:
            print "Collided"
        else:
            print "No collision"

    def basicRotate(self,comms,angle):
        comms.turn(angle,get_angle_corrections)
        time.sleep(get_time_to_turn)
        comms.stop()

    @staticmethod
    def stop():
        comms = Comms()
        comms.start()
        comms.stop()
        comms.stop()

    def start4(self,verbose="n"):
        comms = Comms()
        comms.start()
        time.sleep(1)

        #Checking Juno
        missingJunoCounter = 0
        missingEnemy1Counter = 0
        missingEnemy2Counter = 0
        maxMissCounter = 5

        #Last known positions
        last_ball_x = 150
        last_ball_y = 110
        last_me_x = -1
        last_me_y = -1
        last_me_rot = 0
        last_juno_x = -1
        last_juno_y = -1
        last_enemy1_x = -1
        last_enemy1_y = -1
        last_enemy2_x = -1
        last_enemy2_y = -1

        # Boolean with which side we are playing
        teamSideLeft = World.our_side == "Left"

        # Named tuples (mini classes with no function)
        # named tuple cannot be assigned values
        loctuple = namedtuple("goal","x y")
        metuple = namedtuple("me","x y rot")
        robottuple = namedtuple("robot","x y")
        balltuple = namedtuple("ball","x y")

        # Check if we are in the right zone
        ourgoal = None;
        oppgoal = None;
        if teamSideLeft:
            ourgoal = loctuple(LEFTGOALX,LEFTGOALY)
            oppgoal = loctuple(RIGHTGOALX,RIGHTGOALY)
        else:
            ourgoal = loctuple(RIGHTGOALX,RIGHTGOALY)
            oppgoal = loctuple(LEFTGOALX,LEFTGOALY)

        while True:
            #Delays
            time.sleep(0.8)

            # Extract world model
            curr_world = World.get_world()
            ball = curr_world.ball
            robots_array = curr_world.robots
            robot0 = robots_array[0]
            robot1 = robots_array[1]
            robot2 = robots_array[2]
            robot3 = robots_array[3]
            # for easy reference and change. ps: I'm assuming robot1 is Juno
            me = robot0
            juno = robot1

            #Change condition to reflect when to change to solo or duo strategy
            #Currently, if Juno is missing in 5 world models, will convert to solo strat
            ball_grid = None
            if juno != None:
                print "Juno: ", juno.x, " ", juno.y, " Last: ", last_juno_x, " ", last_juno_y, "Counter: ", missingJunoCounter
                if ball != None:
                    ball_grid = get_grid_pos(ball.x,ball.y)
                    juno_grid = get_grid_pos(juno.x,juno.y)
                    if(ball_grid.x == juno_grid.x and ball_grid.y == juno_grid.y):
                        missingJunoCounter = 0
                if (juno.x == last_juno_x and juno.y == last_juno_y):
                    missingJunoCounter += 1
                else:
                    missingJunoCounter = 0
                    solo_strat = False
                last_juno_x = juno.x
                last_juno_y = juno.y
                if missingJunoCounter >= maxMissCounter:
                    if verbose == "y": print "Strategy: Juno in the same position/missing"
                    solo_strat = True
                    juno = None
            else:
                missingJunoCounter += 1
                if missingJunoCounter == maxMissCounter:
                    if verbose == "y": print "Strategy: Juno not found"
                    solo_strat = True
                    juno = None

            # Check if robot2 is working--------------------------------------------------------------------------------
            if robot2 != None:
                if (robot2.x == last_enemy1_x and robot2.y == last_enemy1_y):
                    missingEnemy1Counter += 1
                    if missingEnemy1Counter == maxMissCounter:
                        if verbose == "y": print "Strategy: Enemy 1 not found"
                        last_enemy1_x = robot2.x
                        last_enemy1_y = robot2.y
                        robot2 = None
                else:
                    missingEnemy1Counter = 0
            else:
                missingEnemy1Counter += 1
                if missingEnemy1Counter == maxMissCounter:
                    if verbose == "y": print "Strategy: Enemy 1 not found"
                    robot2 = None

            # Check if robot3 is working--------------------------------------------------------------------------------
            if robot3 != None:
                if (robot3.x == last_enemy2_x and robot3.y == last_enemy2_y):
                    missingEnemy1Counter += 1
                    if missingEnemy2Counter == maxMissCounter:
                        if verbose == "y": print "Strategy: Enemy 2 not found"
                        last_enemy2_x = robot3.x
                        last_enemy2_y = robot3.y
                        robot3 = None
                    else:
                        missingEnemy2Counter = 0
            else:
                missingEnemy2Counter += 1
                if missingEnemy2Counter == maxMissCounter:
                    if verbose == "y": print "Strategy: Enemy 2 not found"
                    robot3 = None

            # Set last known location to ball and me--------------------------------------------------------------------
            if ball == None:
                ball = balltuple(last_ball_x,last_ball_y)

            if me == None:
                me = metuple(last_me_x,last_me_y,last_me_rot)

            if juno == None:
                solo_strat = True
            else:
                solo_strat = False

            # Objects grid locations
            our_grid_pos = get_grid_pos(me.x,me.y)
            ball_grid_pos = get_grid_pos(ball.x,ball.y)
            juno_grid_pos = None
            robot2_grid_pos = None
            robot3_grid_pos = None
            if juno != None:
                juno_grid_pos = get_grid_pos(juno.x,juno.y)
            if robot2 != None:
                robot2_grid_pos = get_grid_pos(robot2.x,robot2.y)
            if robot3 != None:
                robot3_grid_pos = get_grid_pos(robot3.x,robot3.y)

            # Reverse if too close to wall and facing the wall. Else, continue normally
            reverse = False

            if me.x < 45:
                if me.y > 187:
                    if not(me.rot >= 270 or (me.rot >= -90 and me.rot <= 90)):
                        reverse = True
                elif me.y < 36:
                    if ((me.rot <= -270 or not(me.rot >= -90 and me.rot <= 90))):
                        reverse = True
                else:
                    if not(me.rot >= -90 and me.rot <= 90):
                        reverse = True
            elif me.x > 260:
                if me.y > 187:
                    if not((me.rot <= 270 and me.rot >= 180) or (me.rot >= -180 and me.rot <= -90)):
                        reverse = True
                elif me.y < 36:
                    if ((me.rot <= 270 and me.rot >= 180) or (me.rot >= -180 and me.rot <= -90)):
                        reverse = True
                else:
                    if not((me.rot >= 90 and me.rot <= 270) or (me.rot <= -90 and me.rot >= -270)):
                        reverse = True
            elif me.y > 187:
                if me.x > 260:
                    if not((me.rot <= 270 and me.rot >= 180) or (me.rot >= -180 and me.rot <= -90)):
                        reverse = True
                elif me.x < 45:
                    if not(me.rot >= 270 or not(me.rot >= -90 and me.rot <= 0)):
                        reverse = True
                else:
                    if not((me.rot >= 180 and me.rot <= 360) or (me.rot <= 0 and me.rot >= -180)):
                        reverse = True
            elif me.y < 36:
                if me.x > 260:
                    if ((me.rot <= 270 and me.rot >= 180) or (me.rot >= -180 and me.rot <= -90)):
                        reverse = True
                elif me.x < 45:
                    if ((me.rot <= -270 and me.rot >= -360) or (me.rot >= 0 and me.rot <= 90)):
                        reverse = True
                else:
                    if not((me.rot >= 0 and me.rot <= 180) or (me.rot <= -180 and me.rot >= -360)):
                        reverse = True

            if (reverse):
                if verbose == "y": print "Strategy: Too close to the wall reversing"
                comms.reverse(100)
                time.sleep(0.8)
                comms.stop()
                time.sleep(0.2)
            else :
                #TODO: Delete for match
                #solo_strat = True
                if solo_strat:
                    if verbose == "y": print "Strategy: Running SOLO strat"
                    """
                    Solo strategy starts here
                    """

                    #Robot distances to ball
                    me_ball_grid_dist = 100
                    robot2_ball_grid_dist = 100
                    robot3_ball_grid_dist = 100
                    if me != None and ball_grid_pos != None:
                        me_ball_grid_dist = get_grid_distance(int(our_grid_pos.x),int(our_grid_pos.y),int(ball_grid_pos.x),int(ball_grid_pos.y))
                    if robot2 != None and ball_grid_pos != None:
                        robot2_ball_grid_dist = get_grid_distance(int(robot2_grid_pos.x),int(robot2_grid_pos.y),int(ball_grid_pos.x),int(ball_grid_pos.y))
                    if robot3 != None and ball_grid_pos != None:
                        robot3_ball_grid_dist = get_grid_distance(int(robot3_grid_pos.x),int(robot3_grid_pos.y),int(ball_grid_pos.x),int(ball_grid_pos.y))

                    if robot2_ball_grid_dist < me_ball_grid_dist or robot3_ball_grid_dist < me_ball_grid_dist:
                        if verbose == "y": print "Strategy: Solo: Going for defense"

                        # Apparently calculate_intercept_p is not reliable
                        blocking_enabled = False
                        if blocking_enabled and (robot2_ball_grid_dist < 1 or robot3_ball_grid_dist < 1):
                            # Select shooter
                            shooter = None;
                            if robot2_ball_grid_dist < 1:
                                if verbose == "y": print "Strategy: Solo: Blocking robot2"
                                shooter = robottuple(robot2.x,robot2.y)
                            elif robot3_ball_grid_dist < 1:
                                if verbose == "y": print "Strategy: Solo: Blocking robot3"
                                shooter(robot3.x,robot3.y)

                            # Calculate intercept location
                            pxy = simple_intercept({shooter.x,shooter.y},{ourgoal.x,ourgoal.y},{me.x,me.y})
                            angle_to_obj = us_to_obj_angle(me,pxy)
                            angle_to_obj = get_angle_to_send(angle_to_obj)
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            time_to_object = get_time_to_travel(me.x,me.y,pxy.x,pxy.y)
                            comms.turn(angle_to_obj)
                            comms.sleep(time_to_turn)
                            self.basicGo(comms,time_to_turn)

                        else:
                            if verbose == "y": print "Strategy: Solo: Defending goal"
                            if teamSideLeft:
                                defendloc = loctuple(51,112)
                            else:
                                defendloc = loctuple(243,112)
                            if (math.sqrt(math.pow(me.x-defendloc.x,2) + math.pow(me.y - defendloc.y,2)) < 30):
                                if verbose == "y": print "Strategy: Solo: Near Goal"
                                if math.fabs(-90 - me.rot) < 15:
                                    # Move up and down
                                    if verbose == "y": print "Strategy: Solo: Defending"
                                    comms.go()
                                    time.sleep(1)
                                    comms.stop()
                                    comms.reverse(10)
                                    time.sleep(1)
                                    comms.stop()
                                else:
                                    #Turn towards ball
                                    if verbose == "y": print "Strategy: Solo: Rotating to 0"
                                    angle_to_obj = -90 - me.rot
                                    comms.turn(angle_to_obj,get_angle_corrections(angle_to_obj))
                                    time.sleep(get_time_to_turn(angle_to_obj))
                            else:
                                if verbose == "y": print "Strategy: Solo: Going to goal"
                                angle_to_obj = us_to_obj_angle(me,defendloc)
                                angle_to_obj = get_angle_to_send(angle_to_obj)
                                time_to_turn = get_time_to_turn(angle_to_obj)
                                time_to_object = get_time_to_travel(me.x,defendloc.x,me.y,defendloc.y)
                                comms.turn(angle_to_obj)
                                time.sleep(time_to_turn)
                                self.basicGo(comms,time_to_object)
                    else:
                        if verbose == "y": print "Strategy: Solo: Going for offense"
                        if me != None and ball != None:
                            ball_grid = get_grid_pos(ball.x,ball.y)
                            angle_to_obj = us_to_obj_angle(me,ball)
                            angle_to_obj = get_angle_to_send(angle_to_obj)
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            turn_angle = get_angle_to_send(angle_to_obj)
                            if turn_angle != 0:
                                print "Turning to ball angle: ", angle_to_obj
                                comms.turn(angle_to_obj)
                                time.sleep(time_to_turn)
                                comms.stop()
                            time_to_object = get_time_to_travel(me.x,ball.x,me.y,ball.y)
                            print "Time to sleep: ", time_to_object
                            time.sleep(0.3)
                            comms.grab(1)
                            time.sleep(0.4)
                            self.basicGo(comms,time_to_object)
                            time.sleep(0.2)
                            comms.grab(0)
                            time.sleep(0.1)
                            comms.hasball()
                            time.sleep(0.2)
                            hasBall = comms.got_ball()
                            if hasBall:
                                curr_world = World.get_world()
                                ball = curr_world.ball
                                robots = curr_world.robots
                                robot0 = curr_world.robots[0]
                                me = robot0
                                if me != None and ball != None:
                                    time.sleep(1)
                                    goal = loctuple(SHOOTLEFTX,SHOOTLEFTY)
                                    if teamSideLeft:
                                        goal = loctuple(SHOOTRIGHTX,SHOOTRIGHTY)
                                    time.sleep(0.2)
                                    angle_to_obj = us_to_obj_angle(me,goal)
                                    turn_angle = get_angle_to_send(angle_to_obj)
                                    time_to_turn = get_time_to_turn(turn_angle)
                                    if turn_angle != 0:
                                        print "Turnning to ball angle: ", turn_angle
                                        comms.turn(turn_angle)
                                        time.sleep(time_to_turn)
                                        comms.stop()
                                    time.sleep(1)
                                    comms.kick(10)
                                    time.sleep(1)
                else:
                    if verbose == "y": print "Strategy: Running DUO strat"
                    """
                    Duo strategy starts here
                    """
                    if get_zone(me.x,teamSideLeft) <= 0:

                        if verbose == "y": print "Strategy: Duo: We are in the wrong zone"
                        if me != None and oppgoal != None:
                            angle_to_obj = get_angle_to_send(us_to_obj_angle(me,oppgoal))
                            time_to_turn = get_time_to_turn(angle_to_obj)

                            comms.turn(time_to_turn)
                            if verbose == "y": print "Strategy: Duo: Facing opp goal"
                            time.sleep(time_to_turn)
                            comms.stop()

                            if verbose == "y": print "Strategy: Duo: Leaving zone"
                            self.basicGo(comms,1)

                    if get_zone(ball.x,teamSideLeft) <= 0:
                        if verbose == "y": print "Strategy: Duo: Ball is in zone 0"
                        weight = 0;
                        if robot2_grid_pos != None:
                            if (robot2_grid_pos.y >= 2):
                                weight += 1
                            else:
                                weight -= 1
                        if robot3_grid_pos != None:
                            if (robot3_grid_pos.y >= 2):
                                weight += 1
                            else:
                                weight -= 1

                        targetloc = None
                        if weight >= 0:
                            targetloc = loctuple(TARGETLOCTOPX,TARGETLOCTOPY)
                        else:
                            targetloc = loctuple(TARGETLOCBOTX,TARGETLOCBOTY)

                        if math.fabs(me.x - int(targetloc.x)) + math.fabs(me.y - int(targetloc.y)) < 30:
                            if verbose == "y": print "Strategy: Duo: Facing the ball"
                            angle_to_obj = get_angle_to_send(us_to_obj_angle(me,ball))
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            comms.turn(angle_to_obj)
                            time.sleep(time_to_turn)
                            comms.stop()
                        else:
                            if verbose == "y": print "Strategy: Duo: Going to target location"
                            angle_to_obj = get_angle_to_send(us_to_obj_angle(me,targetloc))
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            time_to_object = get_time_to_travel(me.x,targetloc.x,me.y,targetloc.y)
                            comms.turn(angle_to_obj)
                            time.sleep(time_to_turn)
                            comms.stop()
                            self.basicGo(comms,time_to_object)

                    elif (math.fabs(juno_grid_pos.x - ball_grid_pos.x) <= 1 and math.fabs(juno_grid_pos.y - ball_grid_pos.y) <= 1):
                        if verbose == "y": print "Strategy: Duo: Ball is in near Juno."

                        weight = 0;
                        if juno_grid_pos != None:
                            if (juno_grid_pos.y >= 2):
                                weight += 1
                            else:
                                weight -= 1

                        targetloc = None
                        if weight >= 0:
                            targetloc = loctuple(TARGETLOCTOPX,TARGETLOCTOPY)
                        else:
                            targetloc = loctuple(TARGETLOCBOTX,TARGETLOCBOTY)

                        if math.fabs(me.x - int(targetloc.x)) + math.fabs(me.y - int(targetloc.y)) < 30:
                            if me != None and ball != None:
                                if verbose == "y": print "Strategy: Duo: Facing the ball"
                                angle_to_obj = get_angle_to_send(us_to_obj_angle(me,ball))
                                time_to_turn = get_time_to_turn(angle_to_obj)
                                comms.turn(angle_to_obj)
                                time.sleep(time_to_turn)
                                comms.stop()
                        else:
                            if me != None:
                                if verbose == "y": print "Strategy: Duo: Going to target location"
                                angle_to_obj = get_angle_to_send(us_to_obj_angle(me,targetloc))
                                time_to_turn = get_time_to_turn(angle_to_obj)
                                time_to_object = get_time_to_travel(me.x,targetloc.x,me.y,targetloc.y)
                                comms.turn(angle_to_obj)
                                time.sleep(time_to_turn)
                                comms.stop()
                                self.basicGo(comms,time_to_object)
                    else:
                        #Grid distances of robots to ball
                        robot2_ball_grid_dist = 100
                        robot3_ball_grid_dist = 100
                        me_ball_grid_dist = get_grid_distance(our_grid_pos.x,our_grid_pos.y,ball_grid_pos.x,ball_grid_pos.y)
                        if (robot2 != None):
                            robot2_ball_grid_dist = get_grid_distance(robot2_grid_pos.x,robot2_grid_pos.y,ball_grid_pos.x,ball_grid_pos.y)
                        if (robot3 != None):
                            robot3_ball_grid_dist = get_grid_distance(robot3_grid_pos.x,robot3_grid_pos.y,ball_grid_pos.x,ball_grid_pos.y)

                        if (me_ball_grid_dist > robot2_ball_grid_dist or me_ball_grid_dist > robot3_ball_grid_dist):
                            if verbose == "y": print "Strategy: Duo: Ball is closer to the enemy"

                            # Point is not used yet because of unreliability?
                            """
                            if(robot2_ball_grid_dist > robot3_ball_grid_dist):
                                point = simple_intercept({robot3.x,robot3.y},{ourgoal.x,ourgoal.y},{me.x,me.y})
                            else:
                                point = simple_intercept({shooter.x,shooter.y},{ourgoal.x,ourgoal.y},{me.x,me.y})
                            """
                            angle_to_obj = get_angle_to_send(us_to_obj_angle(me,ball))
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            time_to_object = get_time_to_travel(me.x,ball.x,me.y,ball.y)
                            if verbose == "y": print "Strategy: Duo: Trying to intercept"
                            time.sleep(time_to_turn)
                            self.basicGo(comms,time_to_object)
                        else:
                            if verbose == "y": print "Strategy: Duo: We are closest to ball"

                            if verbose == "y": print "Strategy: Duo: Going towards the ball"
                            angle_to_obj = get_angle_to_send(us_to_obj_angle(me,ball))
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            time_to_object = get_time_to_travel(me.x,ball.x,me.y,ball.y)

                            comms.turn(angle_to_obj)
                            if verbose == "y": print "Strategy: Duo: Facing ball"
                            time.sleep(time_to_turn)
                            comms.stop()
                            comms.grab(1)
                            time.sleep(0.4)

                            if verbose == "y": print "Strategy: Duo: Heading towards ball"
                            self.basicGo(comms,time_to_object)
                            time.sleep(0.2)

                            comms.grab(0)
                            if verbose == "y": print "Strategy: Duo: Grabbing ball"

                            time.sleep(0.1)
                            comms.hasball()
                            time.sleep(0.2)
                            hasBall = comms.got_ball()

                            if hasBall:
                                curr_world = World.get_world()
                                ball = curr_world.ball
                                robots = curr_world.robots
                                robot0 = curr_world.robots[0]
                                me = robot0
                                if me != None and ball != None:
                                    time.sleep(1)
                                    goal = loctuple(SHOOTLEFTX,SHOOTLEFTY)
                                    if teamSideLeft:
                                        goal = loctuple(SHOOTRIGHTX,SHOOTRIGHTY)
                                    time.sleep(0.2)
                                    angle_to_obj = us_to_obj_angle(me,goal)
                                    turn_angle = get_angle_to_send(angle_to_obj)
                                    time_to_turn = get_time_to_turn(turn_angle)
                                    if turn_angle != 0:
                                        print "Turnning to ball angle: ", turn_angle
                                        comms.turn(turn_angle)
                                        if verbose == "y": print "Strategy: Duo: Aiming"
                                        time.sleep(time_to_turn)
                                        comms.stop()
                                    time.sleep(1)
                                    comms.kick(10)
                                    if verbose == "y": print "Strategy: Duo: Shooting"
                                    time.sleep(1)
