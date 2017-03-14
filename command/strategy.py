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
                value2 = int(raw_input("corrections: "))
                comms.turn(value,value2)
                time.sleep(1.5)
            if inp == "go":
                value = float(raw_input("Time to go: "))
                comms.go()
                time.sleep(value)
                comms.stop()
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
            if inp == "intercept":
                our_x = int(raw_input("our x: "))
                our_y = int(raw_input("our x: "))
                their_x = int(raw_input("our x: "))
                their_y = int(raw_input("our x: "))
                our_x = int(raw_input("our x: "))
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
    def start3(verbose="n"):
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

            #TODO: Change so that you don't kick everytime after offense strat
            if me.x < 40 or me.x > 260 or me.y < 30 or me.y > 190:
                if verbose == "y": print "Reversing cause it's too close to the wall"
                comms.reverse(100)
                time.sleep(0.8)
                comms.stop()
                time.sleep(0.2)
            else:
                # Currently set to True to test the solo _start TODO: Change for actual match
                #solo_strat = True
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
                            point = simple_intercept({shooter.x,shooter.y},{goalx,goaly},{me.x,me.y})
                            pxy = namedtuple("C","x y")
                            pxy(point[0],point[1])
                            angle_to_obj = us_to_obj_angle(me,pxy)
                            angle_to_obj = get_angle_to_send(angle_to_obj)
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            time_to_object = get_time_to_travel(me.x,me.y,pxy.x,pxy.y)
                            if time_to_object > MAX_MOVEMENT_TIME:
                                time_to_object = MAX_MOVEMENT_TIME
                            comms.turn(angle_to_obj-10,3)
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
                                angle_to_obj = get_angle_to_send(angle_to_obj)
                                time_to_turn = get_time_to_turn(angle_to_obj)
                                comms.turn(angle_to_obj-10)
                                time.sleep(time_to_turn)
                            else:
                                if verbose == "y": print "Strategy: Solo: Going to goal"
                                goal = namedtuple("C","x y")
                                angle_to_obj = us_to_obj_angle(me,goal(goalx,goaly))
                                angle_to_obj = get_angle_to_send(angle_to_obj)
                                time_to_turn = get_time_to_turn(angle_to_obj)
                                time_to_object = get_time_to_travel(me.x,goalx,me.y,goaly)
                                if time_to_object > MAX_MOVEMENT_TIME:
                                    time_to_object = MAX_MOVEMENT_TIME
                                comms.turn(angle_to_obj-10,3)
                                time.sleep(time_to_turn)
                                comms.go()
                                time.sleep(time_to_object)
                                comms.stop()
                    else:
                        if verbose == "y": print "Strategy: Solo: Going for offense"
                        if me != None and ball != None:
                            ball_grid = get_grid_pos(ball.x,ball.y)
                            C = namedtuple("C" , "x y")
                            angle_to_obj = us_to_obj_angle(me,C(ball.x,ball.y))
                            angle_to_obj = get_angle_to_send(angle_to_obj)
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            turn_angle = get_angle_to_send(angle_to_obj)
                            if turn_angle != 0:
                                print "Turnning to ball angle: ", angle_to_obj
                                comms.turn(angle_to_obj-10,3)
                                time.sleep(time_to_turn)
                                comms.stop()
                            time_to_object = get_time_to_travel(me.x,ball.x,me.y,ball.y)
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
                            me = robot0
                            if me != None and ball != None:
                                time.sleep(1)
                                C = namedtuple("C" , "x y")
                                goal = C(SHOOTLEFTX,SHOOTLEFTY)
                                if teamSideLeft:
                                    goal = C(SHOOTRIGHTX,SHOOTRIGHTY)
                                time.sleep(0.2)
                                angle_to_obj = us_to_obj_angle(me,goal)
                                turn_angle = get_angle_to_send(angle_to_obj)
                                time_to_turn = get_time_to_turn(turn_angle)
                                if turn_angle != 0:
                                    print "Turnning to ball angle: ", turn_angle
                                    comms.turn(turn_angle-10,5)
                                    time.sleep(time_to_turn)
                                    comms.stop()
                                time.sleep(1)
                                comms.kick(10)
                                time.sleep(1)
                else:
                    #TODO Strategy if Juno is found
                    if verbose == "y": print "Strategy: Running DUO strat"
                    our_grid_pos = get_grid_pos(me.x,me.y)

                    # Check if we are in the right zone
                    if teamSideLeft:
                        if True:
                            # Check if Juno has the ball
                            if verbose == "y": print "Strategy: Left - In the valid zone"
                            juno_grid_pos = get_grid_pos(juno.x,juno.y)
                            ball_grid_pos = get_grid_pos(ball.x,ball.y)

                            # Check if the ball is for us
                            if verbose == "y": print "Strategy: Left - Ball is not Juno's"
                            if ((ball_grid_pos.x > 2)):
                                if verbose == "y": print "Strategy: Left - Ball in attack area ", ball_grid_pos.x, " ", ball_grid_pos.y
                                if me != None and ball != None:
                                    ball_grid = get_grid_pos(ball.x,ball.y)
                                    C = namedtuple("C" , "x y")
                                    angle_to_obj = us_to_obj_angle(me,C(ball.x,ball.y))
                                    angle_to_obj = get_angle_to_send(angle_to_obj)
                                    time_to_turn = get_time_to_turn(angle_to_obj)
                                    turn_angle = get_angle_to_send(angle_to_obj)
                                    if turn_angle != 0:
                                        print "Turnning to ball angle: ", angle_to_obj
                                        comms.turn(angle_to_obj-10,3)
                                        time.sleep(time_to_turn)
                                        comms.stop()
                                    time_to_object = get_time_to_travel(me.x,ball.x,me.y,ball.y)
                                    print "Time to sleep: ", time_to_object
                                    time.sleep(0.1)
                                    comms.grab(1)
                                    time.sleep(0.4)
                                    comms.go()
                                    time.sleep(time_to_object)
                                    comms.stop()
                                    time.sleep(0.2)
                                    comms.grab(0)
                                    time.sleep(0.5)
                                    curr_world = World.get_world()
                                    ball = curr_world.ball
                                    robots = curr_world.robots
                                    robot0 = curr_world.robots[0]
                                    me = robot0
                                    if me != None and ball != None:
                                        angle_to_obj2 = us_to_obj_angle(me,C(ball.x,ball.y))
                                        if math.fabs(angle_to_obj2) > 7:
                                            angle_to_obj2 = get_angle_to_send(angle_to_obj2)
                                            time_to_turn2 = get_time_to_turn(angle_to_obj2)
                                            comms.turn(angle_to_obj2-10)
                                            time.sleep(time_to_turn2)
                                        time.sleep(1)
                                        C = namedtuple("C" , "x y")
                                        goal = C(SHOOTLEFTX,SHOOTLEFTY)
                                        if teamSideLeft:
                                            goal = C(SHOOTRIGHTX,SHOOTRIGHTY)
                                        time.sleep(0.2)
                                        angle_to_obj = us_to_obj_angle(me,goal)
                                        turn_angle = get_angle_to_send(angle_to_obj)
                                        time_to_turn = get_time_to_turn(turn_angle)
                                        if turn_angle != 0:
                                            print "Turnning to ball angle: ", turn_angle
                                            comms.turn(turn_angle-10,5)
                                            time.sleep(time_to_turn)
                                            comms.stop()
                                        time.sleep(1)
                                        comms.kick(10)
                                        time.sleep(1)
                                comms.stop()
                                time.sleep(0.2)
                            else:
                                # The ball should be left for defense
                                if verbose == "y": print "Strategy: Left - Ball in defense area", ball_grid_pos.x, " ", ball_grid_pos.y
                                if me != None and ball != None:
                                    ball_grid = get_grid_pos(ball.x,ball.y)
                                    C = namedtuple("C" , "x y")
                                    angle_to_obj = us_to_obj_angle(me,C(ball.x,ball.y))
                                    angle_to_obj = get_angle_to_send(angle_to_obj)
                                    time_to_turn = get_time_to_turn(angle_to_obj)
                                    turn_angle = get_angle_to_send(angle_to_obj)
                                    if turn_angle != 0:
                                        print "Turnning to ball angle: ", angle_to_obj
                                        comms.turn(angle_to_obj-10,3)
                                        time.sleep(time_to_turn)
                                        comms.stop()
                                    time_to_object = get_time_to_travel(me.x,ball.x,me.y,ball.y)
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
                                    me = robot0
                                    if me != None and ball != None:
                                        time.sleep(1)
                                        C = namedtuple("C" , "x y")
                                        goal = C(SHOOTLEFTX,SHOOTLEFTY)
                                        if teamSideLeft:
                                            goal = C(SHOOTRIGHTX,SHOOTRIGHTY)
                                        time.sleep(0.2)
                                        angle_to_obj = us_to_obj_angle(me,goal)
                                        turn_angle = get_angle_to_send(angle_to_obj)
                                        time_to_turn = get_time_to_turn(turn_angle)
                                        if turn_angle != 0:
                                            print "Turnning to ball angle: ", turn_angle
                                            comms.turn(turn_angle-10,5)
                                            time.sleep(time_to_turn)
                                            comms.stop()
                                        time.sleep(1)
                                        comms.kick(10)
                                        time.sleep(1)
                                comms.stop()
                                time.sleep(0.2)
                                comms.stop()
                                time.sleep(0.2)
                    else:
                        # We are on the right side
                        if True:
                            # Check if Juno has the ball
                            if verbose == "y": print "Strategy: Right - In the valid zone"
                            juno_grid_pos = get_grid_pos(juno.x,juno.y)
                            ball_grid_pos = get_grid_pos(ball.x,ball.y)

                            # Check if the ball is for us
                            if verbose == "y": print "Strategy: Right - Ball is not Juno's"
                            if ((ball_grid_pos.x <= 2)):
                                if verbose == "y": print "Strategy: Right - Ball in attack area"
                                if me != None and ball != None:
                                    ball_grid = get_grid_pos(ball.x,ball.y)
                                    C = namedtuple("C" , "x y")
                                    angle_to_obj = us_to_obj_angle(me,C(ball.x,ball.y))
                                    angle_to_obj = get_angle_to_send(angle_to_obj)
                                    time_to_turn = get_time_to_turn(angle_to_obj)
                                    turn_angle = get_angle_to_send(angle_to_obj)
                                    if turn_angle != 0:
                                        print "Turnning to ball angle: ", angle_to_obj
                                        comms.turn(angle_to_obj-10,3)
                                        time.sleep(time_to_turn)
                                        comms.stop()
                                    time_to_object = get_time_to_travel(me.x,ball.x,me.y,ball.y)
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
                                    me = robot0
                                    if me != None and ball != None:
                                        time.sleep(1)
                                        C = namedtuple("C" , "x y")
                                        goal = C(SHOOTLEFTX,SHOOTLEFTY)
                                        if teamSideLeft:
                                            goal = C(SHOOTRIGHTX,SHOOTRIGHTY)
                                        time.sleep(0.2)
                                        angle_to_obj = us_to_obj_angle(me,goal)
                                        turn_angle = get_angle_to_send(angle_to_obj)
                                        time_to_turn = get_time_to_turn(turn_angle)
                                        if turn_angle != 0:
                                            print "Turnning to ball angle: ", turn_angle
                                            comms.turn(turn_angle-10,5)
                                            time.sleep(time_to_turn)
                                            comms.stop()
                                        time.sleep(1)
                                        comms.kick(10)
                                        time.sleep(1)
                                comms.stop()
                                time.sleep(0.2)
                            else:
                                # The ball should be left for defense
                                if verbose == "y": print "Strategy: Right - Ball in defense area"
                                if me != None and ball != None:
                                    ball_grid = get_grid_pos(ball.x,ball.y)
                                    C = namedtuple("C" , "x y")
                                    angle_to_obj = us_to_obj_angle(me,C(ball.x,ball.y))
                                    angle_to_obj = get_angle_to_send(angle_to_obj)
                                    time_to_turn = get_time_to_turn(angle_to_obj)
                                    turn_angle = get_angle_to_send(angle_to_obj)
                                    if turn_angle != 0:
                                        print "Turnning to ball angle: ", angle_to_obj
                                        comms.turn(angle_to_obj-10,3)
                                        time.sleep(time_to_turn)
                                        comms.stop()
                                    time_to_object = get_time_to_travel(me.x,ball.x,me.y,ball.y)
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
                                    me = robot0
                                    if me != None and ball != None:
                                        time.sleep(1)
                                        C = namedtuple("C" , "x y")
                                        goal = C(SHOOTLEFTX,SHOOTLEFTY)
                                        if teamSideLeft:
                                            goal = C(SHOOTRIGHTX,SHOOTRIGHTY)
                                        time.sleep(0.2)
                                        angle_to_obj = us_to_obj_angle(me,goal)
                                        turn_angle = get_angle_to_send(angle_to_obj)
                                        time_to_turn = get_time_to_turn(turn_angle)
                                        if turn_angle != 0:
                                            print "Turnning to ball angle: ", turn_angle
                                            comms.turn(turn_angle-10,5)
                                            time.sleep(time_to_turn)
                                            comms.stop()
                                        time.sleep(1)
                                        comms.kick(10)
                                        time.sleep(1)
                                comms.stop()
                                time.sleep(0.2)
                                comms.stop()
                                time.sleep(0.2)

    @staticmethod
    def start4(verbose="n"):
        #TODO: Change default grid depending on side of pitch
        comms = Comms()
        comms.start()
        time.sleep(1)

        #Checking Juno
        missingJunoCounter = 0
        missingEnemy1Counter = 0
        missingEnemy2Counter = 0
        maxMissCounter = 20

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

        # Check if we are in the right zone
        ourgoal = namedtuple("ourgoal","x y")
        oppgoal = namedtuple("oppgoal","x y")
        if teamSideLeft:
            ourgoal(LEFTGOALX,LEFTGOALY)
            oppgoal(RIGHTGOALX,RIGHTGOALY)
        else:
            ourgoal(RIGHTGOALX,RIGHTGOALY)
            oppgoal(LEFTGOALX,LEFTGOALY)

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
            #Currently, if Juno is missing in 20 world models, will convert to solo strat
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

            # Objects grid locations
            our_grid_pos = get_grid_pos(me.x,me.y)
            ball_grid_pos = get_grid_pos(ball.x,ball.y)
            if juno != None:
                juno_grid_pos = get_grid_pos(juno.x,juno.y)
            if robot2 != None:
                robot2_grid_pos = get_grid_pos(robot2.x,robot2.y)
            if robot3 != None:
                robot3_grid_pos = get_grid_pos(robot3.x,robot3.y)

            #TODO: Change so that you don't kick everytime after offense strat
            if me.x < 40 or me.x > 260 or me.y < 30 or me.y > 190:
                if verbose == "y": print "Reversing cause it's too close to the wall"
                comms.reverse(100)
                time.sleep(0.8)
                comms.stop()
                time.sleep(0.2)
            else:
                if solo_strat:
                    if verbose == "y": print "Strategy: Running SOLO strat"

                    #Robot distances to ball
                    me_ball_grid_dist = 100
                    robot2_ball_grid_dist = 100
                    robot3_ball_grid_dist = 100
                    if me != None and ball_grid != None:
                        me_ball_grid_dist = get_grid_distance(our_grid_pos.x,our_grid_pos.y,ball_grid.x,ball_grid.y)
                    if robot2 != None and ball_grid != None:
                        robot2_ball_grid_dist = get_grid_distance(robot2_grid_pos.x,robot2_grid_pos.y,ball_grid.x,ball_grid.y)
                    if robot3 != None and ball_grid != None:
                        robot3_ball_grid_dist = get_grid_distance(robot3_grid_pos.x,robot3_grid_pos.y,ball_grid.x,ball_grid.y)

                    if robot2_ball_grid_dist < me_ball_grid_dist or robot3_ball_grid_dist < me_ball_grid_dist:
                        if verbose == "y": print "Strategy: Solo: Going for defense"

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
                            pxy = simple_intercept({shooter.x,shooter.y},{ourgoal.x,ourgoal.y},{me.x,me.y})
                            angle_to_obj = us_to_obj_angle(me,pxy)
                            angle_to_obj = get_angle_to_send(angle_to_obj)
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            time_to_object = get_time_to_travel(me.x,me.y,pxy.x,pxy.y)
                            comms.turn(angle_to_obj)
                            comms.sleep(time_to_turn)
                            comms.go()
                            comms.sleep(time_to_object)
                            comms.stop()
                            time.sleep(0.2)

                        else:
                            if verbose == "y": print "Strategy: Solo: Defending goal"
                            print ourgoal.x, " ", me.x, " ", ourgoal.y, " ", me.y
                            if (math.pow((me.x - ourgoal.x),2) + math.pow((me.y - ourgoal.y),2)) < math.pow(10,2):
                                if verbose == "y": print "Strategy: Solo: Near Goal"
                                #Turn towards ball
                                angle_to_obj = us_to_obj_angle(me,ball)
                                angle_to_obj = get_angle_to_send(angle_to_obj)
                                time_to_turn = get_time_to_turn(angle_to_obj)
                                comms.turn(angle_to_obj)
                                time.sleep(time_to_turn)
                            else:
                                if verbose == "y": print "Strategy: Solo: Going to goal"
                                goal = namedtuple("C","x y")
                                angle_to_obj = us_to_obj_angle(me,goal(ourgoal.x,ourgoal.y))
                                angle_to_obj = get_angle_to_send(angle_to_obj)
                                time_to_turn = get_time_to_turn(angle_to_obj)
                                time_to_object = get_time_to_travel(me.x,ourgoal.x,me.y,ourgoal.y)
                                comms.turn(angle_to_obj)
                                time.sleep(time_to_turn)
                                comms.go()
                                time.sleep(time_to_object)
                                comms.stop()
                    else:
                        if verbose == "y": print "Strategy: Solo: Going for offense"
                        if me != None and ball != None:
                            ball_grid = get_grid_pos(ball.x,ball.y)
                            C = namedtuple("C" , "x y")
                            angle_to_obj = us_to_obj_angle(me,C(ball.x,ball.y))
                            angle_to_obj = get_angle_to_send(angle_to_obj)
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            turn_angle = get_angle_to_send(angle_to_obj)
                            if turn_angle != 0:
                                print "Turnning to ball angle: ", angle_to_obj
                                comms.turn(angle_to_obj)
                                time.sleep(time_to_turn)
                                comms.stop()
                            time_to_object = get_time_to_travel(me.x,ball.x,me.y,ball.y)
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
                            me = robot0
                            if me != None and ball != None:
                                time.sleep(1)
                                C = namedtuple("C" , "x y")
                                goal = C(SHOOTLEFTX,SHOOTLEFTY)
                                if teamSideLeft:
                                    goal = C(SHOOTRIGHTX,SHOOTRIGHTY)
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
                    if (point_zone(me.x,teamSideLeft) <= 0):

                        if verbose == "y": print "Strategy: Duo: We are in the wrong zone"
                        if me != None and oppgoal != None:
                            """    angle_to_obj = get_angle_to_send(us_to_obj_angle(me,oppgoal))
                            time_to_turn = get_time_to_turn(angle_to_obj)

                            comms.turn(time_to_turn)
                            if verbose == "y": print "Strategy: Duo: Facing opp goal"
                            time.sleep(time_to_turn)
                            comms.stop()

                            comms.go()
                            if verbose == "y": print "Strategy: Duo: Leaving zone"
                            time.sleep(1)
                            """
                        comms.stop()

                    if point_zone(ball.x,teamSideLeft <= 0):
                        if verbose == "y": print "Strategy: Duo: Ball is in zone 0"
                        C = namedtuple("C","x y")
                        weight = 0;
                        """if robot2_grid_pos != None:
                            if (robot2_grid_pos.y >= 2):
                                weight -= 1
                            else:
                                weight += 1
                        if robot3_grid_pos != None:
                            if (robot3_grid_pos.y >= 2):
                                weight -= 1
                            else:
                                weight += 1
                        """

                        if weight >= 0:
                            C(TARGETLOCTOPX,TARGETLOCTOPY)
                        else:
                            C(TARGETLOCBOTX,TARGETLOCBOTY)

                        """
                        if math.fabs(me.x - int(C.x)) + math.fabs(me.y - int(C.y)) < 10:
                            if verbose == "y": print "Strategy: Duo: Facing the ball"
                            angle_to_obj = get_angle_to_send(us_to_obj_angle(me,ball))
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            comms.turn(angle_to_obj)
                            time.sleep(time_to_turn)
                            comms.stop()
                        else:
                            if verbose == "y": print "Strategy: Duo: Going to target location"
                            angle_to_obj = get_angle_to_send(us_to_obj_angle(me,C))
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            time_to_object = get_time_to_travel(me.x,C.x,me.y,C.y)
                            comms.turn(angle_to_obj)
                            time.sleep(time_to_turn)
                            comms.stop()
                            comms.go()
                            time.sleep(time_to_object)
                            comms.stop()
                        """
                    elif (math.fabs(juno_grid_pos.x - ball_grid_pos.x) <= 1 or math.fabs(juno_grid_pos.y - ball_grid_pos.y) <= 1):
                        if verbose == "y": print "Strategy: Duo: Ball is in near Juno."
                        C = namedtuple("C","x y")
                        weight = 0;
                        if juno_grid_pos != None:
                            if (juno_grid_pos.y >= 2):
                                weight -= 1
                            else:
                                weight += 1

                        if weight >= 0:
                            C(TARGETLOCTOPX,TARGETLOCTOPY)
                        else:
                            C(TARGETLOCBOTX,TARGETLOCBOTY)

                        if math.fabs(me.x - TARGETLOCBOTX) + math.fabs(me.y - TARGETLOCBOTY) < 10:
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
                                angle_to_obj = get_angle_to_send(us_to_obj_angle(me,C))
                                time_to_turn = get_time_to_turn(angle_to_obj)
                                time_to_object = get_time_to_travel(me.x,C.x,me.y,C.y)
                                comms.turn(angle_to_obj)
                                time.sleep(time_to_turn)
                                comms.stop()
                                comms.go()
                                time.sleep(time_to_object)
                                comms.stop()
                    else:
                        #Grid distances of robots to ball
                        robot2_ball_grid_dist = 100
                        robot3_ball_grid_dist = 100
                        me_ball_grid_dist = get_grid_distance(me.x,me.y,ball_grid_pos.x,ball_grid_pos.y)
                        if (robot2 != None):
                            robot2_ball_grid_dist = get_grid_distance(robot2_grid_pos.x,robot2_grid_pos.y,ball_grid_pos.x,ball_grid_pos.y)
                        if (robot3 != None):
                            robot3_ball_grid_dist = get_grid_distance(robot3_grid_pos.x,robot3_grid_pos.y,ball_grid_pos.x,ball_grid_pos.y)

                        if (me_ball_grid_dist > robot2_ball_grid_dist or me_ball_grid_dist > robot3_ball_grid_dist):
                            if verbose == "y": print "Strategy: Duo: Ball is closer to the enemy"
                            # TODO
                            # Find in between location x
                            # If x is in zone 0, go to a location
                            # Face the ball
                            if(robot2_ball_grid_dist > robot3_ball_grid_dist):
                                point = simple_intercept({robot3.x,robot3.y},{ourgoal.x,ourgoal.y},{me.x,me.y})
                            else:
                                point = simple_intercept({shooter.x,shooter.y},{ourgoal.x,ourgoal.y},{me.x,me.y})
                            angle_to_obj = get_angle_to_send(us_to_obj_angle(me,ball))
                            time_to_turn = get_time_to_turn(angle_to_obj)
                            time_to_object = get_time_to_travel(me.x,ball.x,me.y,ball.y)
                            if verbose == "y": print "Strategy: Duo: Trying to intercept"
                            time.sleep(time_to_turn)
                            comms.go()
                            time.sleep(time_to_object)
                            comms.stop()
                        else:
                            if verbose == "y": print "Strategy: Duo: We are closest to ball"
                            #Go towards ball
                            #If same grid as ball
                                #Turn to ball
                                #Grab ball
                                #Turn to goal
                                #Shoot

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

                            comms.go()
                            if verbose == "y": print "Strategy: Duo: Heading towards ball"
                            time.sleep(time_to_object)
                            comms.stop()
                            time.sleep(0.2)

                            comms.grab(0)
                            if verbose == "y": print "Strategy: Duo: Grabbing ball"

                            curr_world = World.get_world()
                            ball = curr_world.ball
                            robots = curr_world.robots
                            robot0 = curr_world.robots[0]
                            me = robot0
                            if me != None and ball != None:
                                time.sleep(1)
                                C = namedtuple("C" , "x y")
                                goal = C(SHOOTLEFTX,SHOOTLEFTY)
                                if teamSideLeft:
                                    goal = C(SHOOTRIGHTX,SHOOTRIGHTY)
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
