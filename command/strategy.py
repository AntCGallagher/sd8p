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


class Strategy(object):
    def __init__(self):
        self.owner = 0
        self.teammate_on = 0
        self.comms = Comms()

    @staticmethod
    def tests():
        inp = ""
        comms = Comms()
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
                comms.start()
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
                comms.start()
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
                comms.start_comunications()
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
                comms.start_comunications()
                time.sleep(1)
                inp = int(raw_input("value to turn: "))
                angle_to_turn = get_angle_to_send(inp)
                comms.turn(inp)
                time.sleep(3)
                comms.stop()
            if inp == "turntest2":
                comms.start_comunications()
                time.sleep(1)
                comms.grab(1)
                time.sleep(1)
                comms.grab(0)
                time.sleep(1)
                comms.kick(10)
                time.sleep(1)
                comms.stop()
            if inp == "gridxy":
                inpx = int(raw_input("x value: "))
                inpy = int(raw_input("y value: "))
                print(get_grid_pos(inpx,inpy))
            if inp == "g":
                comms.start()
                time.sleep(1)
                inp = float(raw_input("Time to sleep: "))
                comms.go()
                time.sleep(inp)
                comms.stop()
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

    def getPos():
    	self.comms.com.ser.write(bytes('Y'))
    	time.sleep(1)
    	with open(self.comms.outputFilename) as f:
    		log = f.readlines()
    		positions = log[len(log)-2]
    		positions = [int(pos) for pos in positions.split() if pos[1:].isdigit() or pos.isdigit()]
    	#positions[3] = left wheel;
    	#positions[5] = right wheel;
    	#positions[4] = omni wheel;
    	#positions[2] = kicker;
    	return positions

    def resetPos():
    	self.comms.ser.write(bytes('Z'))
    	time.sleep(1)
    	with open(self.comms.outputFilename) as f:
    		log = f.readlines()
    		positions = log[len(log)-2]
    		positions = [int(pos) for pos in positions.split() if pos[1:].isdigit() or pos.isdigit()]
    	return positions

    @staticmethod
    def stop():
        self.comms.start()
        self.comms.stop()
        self.comms.stop()

    @staticmethod
    def taunt():
        self.comms.start()
        time.sleep(1)
        while True:
            self.comms.go()
            time.sleep(2)
            self.comms.stop()
            time.sleep()
            self.comms.turn(90)
            time.sleep(3)
            self.comms.stop()
            time.sleep(1)
            self.comms.go()
            time.sleep(1)
            self.comms.reverse(1000)
            time.sleep(1)

    @staticmethod
    def start(corner,start_x,start_y,starting_strategy):
        self.comms.start_comunications()
        time.sleep(1)
        while True:
            time.sleep(0.4)
            curr_world = World.get_world()

            ball = curr_world.ball
            robots_array = curr_world.robots
            robot0 = robots_array[0]
            robot1 = robots_array[1]
            robot2 = robots_array[2]
            robot3 = robots_array[3]

            if robot0 == None:
                print "Going back"
                self.comms.reverse(1000)
                time.sleep(1)
                self.comms.stop()
                time.sleep(0.3)
            if robot0 != None and ball != None:
                print "Main loop"
                if robot0.y > 194 or robot0.x > 265 or robot0.y < 30 or robot0.x < 40:
                    print "Close to wall"
                    self.comms.reverse(1000)
                    time.sleep(1)
                    self.comms.stop()
                    self.comms.turn(180)
                    time.sleep(2)
                    self.comms.stop()
                    time.sleep(1)
                    self.comms.go()
                    time.sleep(3)
                    self.comms.stop()
                else:
                    print "Normal strat"
                    time_to_object = get_time_to_travel(robot0.x,ball.x,robot0.y,ball.y)
                    C = namedtuple("C" , "x y")
                    angle_to_obj = us_to_obj_angle(robot0,C(ball.x,ball.y))
                    time_to_turn = get_time_to_angle(angle_to_obj)
                    print "angle to obj: ", angle_to_obj, "time to turn: ", time_to_turn
                    self.comms.grab(0)
                    time.sleep(0.5)
                    self.comms.stop()
                    time.sleep(1)
                    self.comms.turn(angle_to_obj)
                    time.sleep(3)
                    self.comms.stop()
                    time.sleep(0.3)
                    self.comms.go()
                    time.sleep(time_to_object-0.05)
                    self.comms.stop()
                    time.sleep(1)
                    self.comms.grab(1)
                    time.sleep(1)
                    self.comms.stop()
                    time.sleep(1)
                    self.comms.grab(0)
                    time.sleep(1)
                    self.comms.kick(10)
                    time.sleep(1)
                    self.comms.stop()
                    time.sleep(1)
                    self.comms.grab(1)
                    time.sleep(1)
                    self.comms.stop()
                    time.sleep(1)

    @staticmethod
    def start2(corner,start_x,start_y,starting_strategy):
        self.comms.start()
        time.sleep(1)
        guess_x = start_x
        guess_y = start_y
        guess_rot = 0
        i = 0
        while True:
            if starting_strategy == "y":
                starting_strategy = "n"
                if corner == 1 or corner == 4:
                    C = namedtuple("C" , "x y")
                    C2 = namedtuple("C" , "x y rot")
                    robot_temp = C2(start_x,start_y,0)
                    time_to_object = get_time_to_travel(robot_temp.x,CORNER14X,robot_temp.y,CORNER14Y)
                    angle_to_obj = us_to_obj_angle(robot_temp,C(CORNER14X,CORNER14Y))
                    self.comms.turn(angle_to_obj)
                    time.sleep(1.5)
                    self.comms.go()
                    time.sleep(time_to_object)
                    self.comms.stop()
                    time_to_mid = get_time_to_travel(CORNER14X,MIDX,CORNER14Y,MIDY)
                    if corner == 1:
                        self.comms.turn(270)
                        time.sleep(2.5)
                        self.comms.go()
                        time.sleep(time_to_mid+0.2)
                        self.comms.stop()
                    else:
                        self.comms.turn(90)
                        time.sleep(1.5)
                        self.comms.go()
                        time.sleep(time_to_mid+0.2)
                        self.comms.stop()
                    self.comms.grab(1)
                    time.sleep(1)
                    self.comms.stop()
                    time.sleep(1)
                    self.comms.go()
                    time.sleep(0.4)
                    self.comms.stop()
                    time.sleep(1)
                    self.comms.grab(0)
                    time.sleep(1)
                    self.comms.kick(10)
                    time.sleep(1)
                    self.comms.stop()
                else:
                    C = namedtuple("C" , "x y")
                    C2 = namedtuple("C" , "x y rot")
                    robot_temp = C2(start_x,start_y,180)
                    time_to_object = get_time_to_travel(robot_temp.x,CORNER23X,robot_temp.y,CORNER23Y)
                    angle_to_obj = us_to_obj_angle(robot_temp,C(CORNER23X,CORNER23Y))
                    self.comms.turn(angle_to_obj)
                    time.sleep(1.5)
                    self.comms.go()
                    time.sleep(time_to_object)
                    self.comms.stop()
                    time_to_mid = get_time_to_travel(CORNER23X,MIDX,CORNER23Y,MIDY)
                    if corner == 2:
                        self.comms.turn(90)
                        time.sleep(1.5)
                        self.comms.go()
                        time.sleep(time_to_mid+0.2)
                        self.comms.stop()
                    else:
                        self.comms.turn(270)
                        time.sleep(2.5)
                        self.comms.go()
                        time.sleep(time_to_mid+0.2)
                        self.comms.stop()
                    self.comms.grab(1)
                    time.sleep(1)
                    self.comms.stop()
                    time.sleep(1)
                    self.comms.grab(0)
                    time.sleep(1)
                    self.comms.kick(10)
                    time.sleep(1)
                    self.comms.stop()
                guess_x = MIDX
                guess_y = MIDY
                guess_rot = 0
            else:
                # Normal strategy here
                curr_world = World.get_world()

                ball = curr_world.ball
                robots_array = curr_world.robots
                robot0 = robots_array[0]
                robot1 = robots_array[1]
                robot2 = robots_array[2]
                robot3 = robots_array[3]

                defense_mode = False
                # Add conditions to change defense here
                if defense_mode:
                    defense_mode = False
                    """
                    me = robot0
                    ally = robot1
                    teamSideLeft = World.our_side == "Left"
                    if me != None and ball != None:
                        if ally != 0:
                            #Ally dependent defense
                            if point_zone(ally.x,teamSideLeft) != 1:
                                if teamSideLeft:
                                    destX = LEFTGOALX
                                    destY = LEFTGOALY
                                else:
                                    destX = RIGHTGOALX
                                    destY = RIGHTGOALY

                                #Go to goal
                                C = namedtuple("C","x y")
                                time_to_dest = get_time_to_travel(me.x,destX,me.y,destY)
                                angle_to_dest = us_to_obj_angle(me,C(destX,destY))
                                Coms.turn(angle_to_dest,1)
                                Coms.sleep(2.5)
                                Coms.go()
                                Coms.sleep(time_to_dest)
                                Coms.stop()

                                #Point up
                                C2 = namedtuple("C","x y")
                                angle_to_dest = us_to_obj_angle(me,C2(me.x,me.y - 10))
                                Coms.turn(angle_to_dest,1)
                                Coms.sleep(2.5)
                            else:
                                if teamSideLeft:
                                    goalX = LEFTGOALX
                                    goalY = LEFTGOALY
                                else:
                                    goalX = RIGHTGOALX
                                    goalY = RIGHTGOALY
                                ball_array = {ball.x,ball.y}
                                goal_array = {goalX,goalY}
                                self_array = {me.x,me.y}
                                point = calculate_intercept_p(ball_array,goal_array,self_array)

                                C = namedtuple("C","x y")
                                time_to_dest = get_time_to_travel(me.x,point[0],me.y,point[1])
                                angle_to_dest = us_to_obj_angle(me,C(point[0],point[1]))
                                Coms.turn(angle_to_dest,1)
                                Coms.sleep(2.5)
                                Coms.go()
                                Coms.sleep(time_to_dest)
                                Coms.stop()

                        else:
                            print "Defense Strategy: Ally not found\n"
                            #Solo defense
                            if teamSideLeft:
                                destX = LEFTGOALX
                                destY = LEFTGOALY
                            else:
                                destX = RIGHTGOALX
                                destY = RIGHTGOALY

                            #Go to goal
                            C = namedtuple("C","x y")
                            time_to_dest = get_time_to_travel(me.x,destX,me.y,destY)
                            angle_to_dest = us_to_obj_angle(me,C(destX,destY))
                            Coms.turn(angle_to_dest,1)
                            Coms.sleep(2.5)
                            Coms.go()
                            Coms.sleep(time_to_dest)
                            Coms.stop()

                            #Point up
                            C2 = namedtuple("C","x y")
                            angle_to_dest = us_to_obj_angle(me,C2(me.x,me.y - 10))
                            Coms.turn(angle_to_dest,1)
                            Coms.sleep(2.5)
                    """
                else:
                    if robot0 != None and ball != None:
                        guess_x = robot0.x
                        guess_y = robot0.y
                        guess_rot = robot0.rot
                        C = namedtuple("C" , "x y")
                        time_to_object = get_time_to_travel(robot0.x,ball.x,robot0.y,ball.y)
                        angle_to_obj = us_to_obj_angle(robot0,C(ball.x,ball.y))
                        print "robot: ", robot0.x, " ", robot0.y
                        print "ball: ", ball.x, " ", ball.y
                        print "time: ", time_to_object, " angle: ", angle_to_obj
                        print "\n"
                        self.comms.grab(0)
                        time.sleep(0.5)
                        self.comms.turn(angle_to_obj)
                        time.sleep(2.5)
                        self.comms.go()
                        time.sleep(time_to_object)
                        self.comms.stop()
                        self.comms.grab(1)
                        time.sleep(1)
                        self.comms.stop()
                        time.sleep(1)
                        self.comms.grab(0)
                        time.sleep(1)
                        self.comms.kick(10)
                        time.sleep(1)
                        self.comms.stop()
                        guess_x = ball.x
                        guess_y = ball.y
                        guess_rot = robot0.rot + angle_to_obj
                    elif robot0 == None:
                        if World.our_side == "Left":
                            C = namedtuple("C" , "x y")
                            C2 = namedtuple("C" , "x y rot")
                            robot_temp = C2(guess_x,guess_y,guess_rot)
                            time_to_object = get_time_to_travel(guess_x,CORNER14X,guess_y,CORNER14Y)
                            angle_to_obj = us_to_obj_angle(robot_temp,C(CORNER14X,CORNER14Y))
                            print "robot: ", guess_x, " ", guess_y
                            print "time: ", time_to_object, " angle: ", angle_to_obj
                            print "\n"
                            self.comms.turn(angle_to_obj)
                            time.sleep(2.5)
                            self.comms.go()
                            time.sleep(time_to_object)
                            self.comms.stop()
                            guess_x = CORNER14X
                            guess_y = CORNER14Y
                            guess_rot = robot_temp.rot + angle_to_obj
                        else:
                            C = namedtuple("C" , "x y")
                            C2 = namedtuple("C" , "x y rot")
                            robot_temp = C2(guess_x,guess_y,guess_rot)
                            time_to_object = get_time_to_travel(guess_x,CORNER23X,guess_y,CORNER23Y)
                            angle_to_obj = us_to_obj_angle(robot_temp,C(CORNER23X,CORNER23Y))
                            print "robot: ", guess_x, " ", guess_y
                            print "time: ", time_to_object, " angle: ", angle_to_obj
                            print "\n"
                            self.comms.turn(angle_to_obj)
                            time.sleep(2.5)
                            self.comms.go()
                            time.sleep(time_to_object)
                            self.comms.stop()
                            guess_x = CORNER23X
                            guess_y = CORNER23Y
                            guess_rot = robot_temp.rot + angle_to_obj
                    else:
                        print "Stuck"
                        if i % 2 == 0:
                            self.comms.reverse(800)
                            time.sleep(1)
                            self.comms.turn(180)
                            self.comms.stop()
                        else:
                            self.comms.go()
                            time.sleep(1.8)
                            self.comms.stop()
                        i = i + 1

    #Do we really need static method?
    @staticmethod
    def start3(start_x,start_y,verbose="n"):
        self.comms.start()
        time.sleep(1)

        #Checking Juno
        missingJunoCounter = 0
        maxJunoCounter = 3

        #Last known positions
        last_ball_x = 150
        last_ball_y = 110
        last_me_x = start_x
        last_me_y = start_y
        last_me_rot = 0

        while True:
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
                missingJunoCounter = 0
                solo_strat = False
            else:
                missingJunoCounter += 1
                if missingJunoCounter == maxJunoCounter:
                    if verbose == "y": print "Strategy: Juno not found"
                    solo_strat = True

            if ball == None:
                ball.x = last_ball_x
                ball.y = last_ball_y

            if me == None:
                me.x = last_me_x
                me.y = last_me_y
                me.rot = last_me_rot

            if solo_strat:
                #TODO Strategy if Juno is not found
                if verbose == "y": print "Strategy: Running SOLO strat"
            else:
                #TODO Strategy if Juno is found
                if verbose == "y": print "Strategy: Running DUO strat"
                our_grid_pos = get_grid_pos(me.x,me.y)

                # Check if we are in the right zone
                if ((our_grid_pos.grid_x < 3) or (our_grid_pos.grid_y < 3)):
                    if verbose == "y": print "Strategy: In the wrong zone"
                    default_grid  = get_pos_grid(3,0)
                    angle_to_obj = us_to_obj_angle(me,default_grid)
                    time_to_object = get_time_to_travel(me.x,default_grid.x,me.y,default_grid.y)
                    self.comms.turn(angle_to_obj)
                    time.sleep(1.5)
                    self.comms.go()
                    time.sleep(time_to_object)
                    self.comms.stop()
                    last_me_x = default_grid.x
                    last_me_y = default_grid.y
                    #last_me_rot = compass
                else:
                    # Check if Juno has the ball
                    if verbose == "y": print "Strategy: In the valid zone"
                    juno_grid_pos = get_grid_pos(juno.x,juno.y)
                    ball_grid_pos = get_grid_pos(ball.x,ball.y)
                    if ((juno_grid_pos.x == ball_grid_pos.x) and (juno_grid_pos.y == ball_grid_pos.y)):
                        if verbose == "y": print "Strategy: Juno and ball in the same zone"
                        if ((our_grid_pos.grid_x != 3) and (our_grid_pos.grid_y != 0)):
                            if verbose == "y": print "Strategy: Move to default grid to allow shot"
                            default_grid  = get_pos_grid(3,0)
                            angle_to_obj = us_to_obj_angle(me,default_grid)
                            time_to_object = get_time_to_travel(me.x,default_grid.x,me.y,default_grid.y)
                            self.comms.turn(angle_to_obj)
                            time.sleep(1.5)
                            self.comms.go()
                            time.sleep(time_to_object)
                            self.comms.stop()
                            last_me_x = default_grid.x
                            last_me_y = default_grid.y
                            #last_me_rot = compass
                    else:
                        # Check if the ball is for us
                        if verbose == "y": print "Strategy: Ball is not Juno's"
                        if ((ball_grid_pos.x > 2) and (ball_grid_pos.y > 2)):
                            if verbose == "y": print "Strategy: Ball in attack area"
                            # Get the ball
                            Coms.stop()
                        else:
                            # The ball should be left for defense
                            if verbose == "y": print "Strategy: Ball in defense area"
                            Coms.stop()
