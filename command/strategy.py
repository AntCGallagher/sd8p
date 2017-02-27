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
RIGHTGOALX = 286
RIGHTGOALY = 111
CORNER14X = 50
CORNER14Y = 108
CORNER23X = 250
CORNER23Y = 108
MIDX = 160
MIDY = 108
MAX_MOVEMENT_TIME = 1.5


class Strategy(object):
    def __init__(self):
        self.owner = 0
        self.teammate_on = 0
        self.comms = Comms()

    @staticmethod
    def tests():
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
                comms.stop()
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                if robot0 != None:
                    C = namedtuple("C" , "x y")
                    time_to_object = get_time_to_travel(robot0.x,dest_x,robot0.y,dest_y)
                    angle_to_obj = us_to_obj_angle(robot0,C(dest_x,dest_y))
                    print "robot: ", robot0.x, " ", robot0.y
                    print "target: ", dest_x, " ", dest_y
                    print "time: ", time_to_object, " angle: ", angle_to_obj
                    comms.turn(get_angle_to_send(int(angle_to_obj)))
                    time.sleep(1.5)
                    comms.reverse(200)
                    time.sleep(time_to_object)
                    comms.stop()
                else:
                    print "Robot not detected"
            if inp == "grb":
                curr_world = World.get_world()
                ball = curr_world.ball
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                if robot0 != None and ball != None:
                    C = namedtuple("C" , "x y")
                    time_to_object = get_time_to_travel(robot0.x,ball.x,robot0.y,ball.y)
                    angle_to_obj = us_to_obj_angle(robot0,C(ball.x,ball.y))
                    print "robot: ", robot0.x, " ", robot0.y
                    print "ball: ", ball.x, " ", ball.y
                    print "time: ", time_to_object, " angle: ", angle_to_obj
                    comms.turn(angle_to_obj,3)
                    time.sleep(1.5)
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
                comms.turn(value)
                time.sleep(1.5)
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
            if inp == "turntest2":
                curr_world = World.get_world()
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                ball = curr_world.ball
                print robot0.rot, " current rotation"
                angle = us_to_obj_angle(robot0,ball)
                print angle, "angle to ball"
                if angle < 15 and angle > -15:
                    angle = angle + 360
                    print "Angle too small, plus 360"
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

    @staticmethod
    def stop():
        comms = Comms()
        comms.start()
        comms.stop()
        comms.stop()

    @staticmethod
    def start3(start_x,start_y,verbose="n"):
        #TODO: Change default grid depending on side of pitch
        comms = Comms()
        comms.start()
        time.sleep(1)

        #Checking Juno
        missingJunoCounter = 0
        missingEnemy1Counter = 0
        missingEnemy2Counter = 0
        maxMissCounter = 3

        #Last known positions
        last_ball_x = 150
        last_ball_y = 110
        last_me_x = start_x
        last_me_y = start_y
        last_me_rot = 0
        last_juno_x = -1
        last_juno_y = -1
        last_enemy1_x = -1
        last_enemy1_y = -1
        last_enemy2_x = -1
        last_enemy2_y = -1

        # Boolean with which side we are playing
        teamSideLeft = World.our_side == "Left"

        while True:

            #Delays
            time.sleep(0.8)
            #normal strategy
            curr_world = World.get_world()

            ball = curr_world.ball
            robots_array = curr_world.robots
            robot0 = robots_array[0]
            robot1 = robots_array[1]
            robot2 = robots_array[2]
            robot3 = robots_array[3]

            #for easy reference and change. ps: I'm assuming robot1 is Juno
            me = robot0
            juno = robot1

            #Change condition to reflect when to change to solo or duo strategy
            #Currently, if Juno is missing in 3 world models, will convert to solo strat
            if juno != None:
                print "Juno: ", juno.x, " ", juno.y, " Last: ", last_juno_x, " ", last_juno_y, "Counter: ", missingJunoCounter
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

            if ball == None:
                ball = namedtuple("C" , "x y")
                ball.x = last_ball_x
                ball.y = last_ball_y

            if me == None:
                me = namedtuple("C" , "x y rot")
                me.x = last_me_x
                me.y = last_me_y
                me.rot = last_me_rot

            if juno == None:
                solo_strat = True
            else:
                solo_strat = False

            if me.x < 40 or me.x > 260 or me.y < 30 or me.y > 190:
                if verbose == "y": print "Reversing cause it's too close to the wall"
                comms.reverse(100)
                time.sleep(0.8)
                comms.stop()
                time.sleep(0.2)
            else:
                # Currently set to True to test the solo _start TODO: Change for actual match
                solo_strat = True
                if solo_strat:
                    #TODO Strategy if Juno is not found
                    if verbose == "y": print "Strategy: Running SOLO strat"
                    me_grid = get_grid_pos(me.x,me.y)
                    ball_grid = get_grid_pos(ball.x,ball.y)
                    if robot2 != None:
                        robot2_grid = get_grid_pos(robot2.x,robot2.y)
                    if robot3 != None:
                        robot3_grid = get_grid_pos(robot3.x,robot3.y)

                    #Robot distances to ball
                    me_ball_grid_dist = 100
                    robot2_ball_grid_dist = 100
                    robot3_ball_grid_dist = 100
                    if me != None:
                        me_ball_grid_dist = get_grid_distance(me_grid.x,me_grid.y,ball_grid.x,ball_grid.y)
                    if robot2 != None:
                        robot2_ball_grid_dist = get_grid_distance(robot2_grid.x,robot2_grid.y,ball_grid.x,ball_grid.y)
                    if robot3 != None:
                        robot3_ball_grid_dist = get_grid_distance(robot3_grid.x,robot3_grid.y,ball_grid.x,ball_grid.y)

                    if robot2_ball_grid_dist < me_ball_grid_dist or robot3_ball_grid_dist < me_ball_grid_dist:
                        if verbose == "y": print "Strategy: Solo: Going for defense"

                        #Selecting goal coordinates
                        goalx = 0;
                        goaly = 0;
                        goal = namedtuple("C", "x y")
                        if teamSideLeft:
                            goalx = LEFTGOALX
                            goaly = LEFTGOALY
                        else:
                            goalx = RIGHTGOALX
                            goaly = RIGHTGOALY

                        # Change this variable to test blocking.
                        # Apparently calculate_intercept_p is not reliable
                        blocking_enabled = False
                        if blocking_enabled and (robot2_ball_grid_dist < 1 or robot3_ball_grid_dist < 1):
                            # Select shooter
                            shooter = namedtuple("C","x y")
                            if robot2_ball_grid_dist < 1:
                                if verbose == "y": print "Strategy: Solo: Blocking robot2"
                                shooter(robot2.x,robot2.y)
                            elif robot3_ball_grid_dist < 1:
                                if verbose == "y": print "Strategy: Solo: Blocking robot3"
                                shooter(robot3.x,robot3.y)

                            # Calculate intercept location
                            point = calculate_intercept_p({shooter.x,shooter.y},{goalx,goaly},{me.x,me.y})
                            pxy = namedtuple("C","x y")
                            pxy(point[0],point[1])
                            angle_to_obj = us_to_obj_angle(me,pxy)
                            if angle_to_obj < 20:
                                angle_to_obj += 360
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            time_to_object = get_time_to_travel(me.x,me.y,pxy.x,pxy.y)
                            if time_to_object > MAX_MOVEMENT_TIME:
                                time_to_object = MAX_MOVEMENT_TIME
                            comms.turn(angle_to_obj,3)
                            comms.sleep(time_to_turn)
                            comms.go()
                            comms.sleep(time_to_object)
                            comms.stop()
                            time.sleep(0.2)

                        else:
                            if verbose == "y": print "Strategy: Solo: Defending goal"
                            print goalx, " ", me.x, " ", goaly, " ", me .y
                            if (math.pow((me.x - goalx),2) + math.pow((me.y - goaly),2)) < math.pow(10,2):
                                if verbose == "y": print "Strategy: Solo: Near Goal"
                                #Turn towards ball
                                angle_to_obj = us_to_obj_angle(me,ball)
                                if angle_to_obj < 20:
                                    angle_to_obj = angle_to_obj + 360
                                time_to_turn = get_time_to_turn(angle_to_obj)
                                comms.turn(angle_to_obj)
                                time.sleep(time_to_turn)
                            else:
                                if verbose == "y": print "Strategy: Solo: Going to goal"
                                goal = namedtuple("C","x y")
                                angle_to_obj = us_to_obj_angle(me,goal(goalx,goaly))
                                if angle_to_obj < 20:
                                    angle_to_obj = angle_to_obj + 360
                                time_to_turn = get_time_to_turn(angle_to_obj)
                                time_to_object = get_time_to_travel(me.x,goalx,me.y,goaly)
                                if time_to_object > MAX_MOVEMENT_TIME:
                                    time_to_object = MAX_MOVEMENT_TIME
                                comms.turn(angle_to_obj,3)
                                time.sleep(time_to_turn)
                                comms.go()
                                time.sleep(time_to_object)
                                comms.stop()
                    else:
                        if verbose == "y": print "Strategy: Solo: Going for offense"
                        if me_grid.x == ball_grid.x and me_grid.y == ball_grid.y:
                            if verbose == "y": print "Strategy: Solo: Same grid as ball"
                            angle_to_obj = us_to_obj_angle(me,ball)
                            if angle_to_obj < 20:
                                angle_to_obj = angle_to_obj + 360
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            comms.turn(angle_to_obj,5)
                            time.sleep(time_to_turn)
                        else:
                            if verbose == "y": print "Strategy: Solo: Going to ball grid"
                            grid = get_grid_pos(ball.x,ball.y)
                            grid_coordinates = get_pos_grid(grid.x,grid.y)
                            C = namedtuple("C" , "x y")
                            angle_to_obj = us_to_obj_angle(me,C(grid_coordinates.x,grid_coordinates.y))
                            if angle_to_obj < 20:
                                angle_to_obj = angle_to_obj + 360
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            comms.turn(angle_to_obj,3)
                            time.sleep(time_to_turn)
                            comms.stop()
                            time.sleep(0.2)
                            comms.go()
                            time.sleep(MAX_MOVEMENT_TIME)
                            comms.stop()
                            time.sleep(0.2)
                else:
                    #TODO Strategy if Juno is found
                    if verbose == "y": print "Strategy: Running DUO strat"
                    our_grid_pos = get_grid_pos(me.x,me.y)

                    # Check if we are in the right zone
                    if teamSideLeft:
                        if (our_grid_pos.x < 3):
                            if verbose == "y": print "Strategy: Left - In the wrong zone"
                            default_grid  = get_pos_grid(3,1)
                            angle_to_obj = us_to_obj_angle(me,default_grid)
                            if verbose == "y": print default_grid, " coordinates to go to"
                            if verbose == "y": print me.x, " ", me.y, " current robot pos"
                            time_to_object = get_time_to_travel(me.x,default_grid.x,me.y,default_grid.y)
                            if angle_to_obj < 20:
                                angle_to_obj = angle_to_obj + 360
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            comms.turn(angle_to_obj)
                            time.sleep(time_to_turn)
                            comms.stop()
                            time.sleep(0.3)
                            comms.go()
                            if time_to_object > MAX_MOVEMENT_TIME:
                                time.sleep(MAX_MOVEMENT_TIME)
                            else:
                                time.sleep(time_to_object)
                            comms.stop()
                            last_me_x = default_grid.x
                            last_me_y = default_grid.y
                            #last_me_rot = compass
                        else:
                            # Check if Juno has the ball
                            if verbose == "y": print "Strategy: Left - In the valid zone"
                            juno_grid_pos = get_grid_pos(juno.x,juno.y)
                            ball_grid_pos = get_grid_pos(ball.x,ball.y)
                            if ((juno_grid_pos.x == ball_grid_pos.x) and (juno_grid_pos.y == ball_grid_pos.y)):
                                if verbose == "y": print "Strategy: Left - Juno and ball in the same zone"
                                if ((our_grid_pos.x != 3) and (our_grid_pos.x != 1)):
                                    if verbose == "y": print "Strategy: Left - Move to default grid to allow shot"
                                    default_grid  = get_pos_grid(3,1)
                                    angle_to_obj = us_to_obj_angle(me,default_grid)
                                    time_to_object = get_time_to_travel(me.x,default_grid.x,me.y,default_grid.y)
                                    if angle_to_obj < 20:
                                        angle_to_obj = angle_to_obj + 360
                                    time_to_turn = get_time_to_turn(angle_to_obj)
                                    comms.turn(angle_to_obj)
                                    time.sleep(time_to_turn)
                                    comms.go()
                                    if time_to_object > MAX_MOVEMENT_TIME:
                                        time.sleep(MAX_MOVEMENT_TIME)
                                    else:
                                        time.sleep(time_to_object)
                                    comms.stop()
                                    time.sleep(0.2)
                                    last_me_x = default_grid.x
                                    last_me_y = default_grid.y
                                    #last_me_rot = compass
                            else:
                                # Check if the ball is for us
                                if verbose == "y": print "Strategy: Left - Ball is not Juno's"
                                if ((ball_grid_pos.x > 2) and (ball_grid_pos.y > 2)):
                                    if verbose == "y": print "Strategy: Left - Ball in attack area"
                                    # Get the ball
                                    comms.stop()
                                    time.sleep(0.2)
                                else:
                                    # The ball should be left for defense
                                    if verbose == "y": print "Strategy: Left - Ball in defense area"
                                    comms.stop()
                                    time.sleep(0.2)
                    else:
                        # We are on the right side
                        if (our_grid_pos.x >= 3):
                            if verbose == "y": print "Strategy: Right - In the wrong zone"
                            default_grid  = get_pos_grid(2,1)
                            angle_to_obj = us_to_obj_angle(me,default_grid)
                            if verbose == "y": print default_grid, " coordinates to go to"
                            if verbose == "y": print me.x, " ", me.y, " current robot pos"
                            time_to_object = get_time_to_travel(me.x,default_grid.x,me.y,default_grid.y)
                            if angle_to_obj < 20:
                                angle_to_obj = angle_to_obj + 360
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            comms.turn(angle_to_obj)
                            time.sleep(time_to_turn)
                            comms.stop()
                            time.sleep(0.3)
                            comms.go()
                            if time_to_object > MAX_MOVEMENT_TIME:
                                time.sleep(MAX_MOVEMENT_TIME)
                            else:
                                time.sleep(time_to_object)
                            comms.stop()
                            time.sleep(0.2)
                            last_me_x = default_grid.x
                            last_me_y = default_grid.y
                            #last_me_rot = compass
                        else:
                            # Check if Juno has the ball
                            if verbose == "y": print "Strategy: Right - In the valid zone"
                            juno_grid_pos = get_grid_pos(juno.x,juno.y)
                            ball_grid_pos = get_grid_pos(ball.x,ball.y)
                            if ((juno_grid_pos.x == ball_grid_pos.x) and (juno_grid_pos.y == ball_grid_pos.y)):
                                if verbose == "y": print "Strategy: Right - Juno and ball in the same zone"
                                if ((our_grid_pos.x != 2) and (our_grid_pos.x != 1)):
                                    if verbose == "y": print "Strategy: Right - Move to default grid to allow shot"
                                    default_grid  = get_pos_grid(2,1)
                                    angle_to_obj = us_to_obj_angle(me,default_grid)
                                    time_to_object = get_time_to_travel(me.x,default_grid.x,me.y,default_grid.y)
                                    if angle_to_obj < 20:
                                        angle_to_obj = angle_to_obj + 360
                                    time_to_turn = get_time_to_turn(angle_to_obj)
                                    comms.turn(angle_to_obj)
                                    time.sleep(time_to_turn)
                                    comms.go()
                                    if time_to_object > MAX_MOVEMENT_TIME:
                                        time.sleep(MAX_MOVEMENT_TIME)
                                    else:
                                        time.sleep(time_to_object)
                                    comms.stop()
                                    time.sleep(0.2)
                                    last_me_x = default_grid.x
                                    last_me_y = default_grid.y
                                    #last_me_rot = compass
                            else:
                                # Check if the ball is for us
                                if verbose == "y": print "Strategy: Right - Ball is not Juno's"
                                if ((ball_grid_pos.x <= 2) and (ball_grid_pos.y <= 2)):
                                    if verbose == "y": print "Strategy: Right - Ball in attack area"
                                    # Get the ball
                                    comms.stop()
                                    time.sleep(0.2)
                                else:
                                    # The ball should be left for defense
                                    if verbose == "y": print "Strategy: Right - Ball in defense area"
                                    comms.stop()
                                    time.sleep(0.2)
