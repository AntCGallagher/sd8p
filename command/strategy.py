from postprocessing.world import World
from communications.originalcomms import Coms
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

    @staticmethod
    def tests():
        inp = ""
        while inp != "done":
            inp = raw_input("ping/goxy/go_robot_ball/turn/median?: (p/gxy/grb/t/m/turntest)")
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
                Coms.start_comunications()
                Coms.stop()
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                if robot0 != None:
                    C = namedtuple("C" , "x y")
                    time_to_object = get_time_to_travel(robot0.x,dest_x,robot0.y,dest_y)
                    angle_to_obj = us_to_obj_angle(robot0,C(dest_x,dest_y))
                    print "robot: ", robot0.x, " ", robot0.y
                    print "target: ", dest_x, " ", dest_y
                    print "time: ", time_to_object, " angle: ", angle_to_obj
                    Coms.turn(get_angle_to_send(int(angle_to_obj)))
                    time.sleep(1.5)
                    Coms.reverse(200)
                    time.sleep(time_to_object)
                    Coms.stop()
                else:
                    print "Robot not detected"
            if inp == "grb":
                Coms.start_comunications()
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
                    Coms.turn(angle_to_obj)
                    time.sleep(1.5)
                    Coms.reverse(200)
                    time.sleep(time_to_object)
                    Coms.stop()
                elif robot0 == None and ball != None:
                    print "Robot and ball not detected"
                elif robot0 == None:
                    print "Robot not detected"
                else:
                    print "Ball not detected"
            if inp == "t":
                value = int(raw_input("angle to turn: "))
                Coms.start_comunications()
                Coms.turn(value)
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
                Coms.start_comunications()
                time.sleep(1)
                inp = int(raw_input("value to turn: "))
                angle_to_turn = get_angle_to_send(inp)
                Coms.turn(inp)
                time.sleep(3)
                Coms.stop()
            if inp == "turntest2":
                Coms.start_comunications()
                time.sleep(1)
                Coms.grab(1)
                time.sleep(1)
                Coms.grab(0)
                time.sleep(1)
                Coms.kick(10)
                time.sleep(1)
                Coms.stop()

    @staticmethod
    def stop():
        Coms.start_comunications()
        Coms.stop()
        Coms.stop()

    @staticmethod
    def taunt():
        Coms.start_comunications()
        time.sleep(1)
        while True:
            Coms.go()
            time.sleep(2)
            Coms.stop()
            time.sleep()
            Coms.turn(90)
            time.sleep(3)
            Coms.stop()
            time.sleep(1)
            Coms.go()
            time.sleep(1)
            Coms.reverse(1000)
            time.sleep(1)
            
    @staticmethod
    def start(corner,start_x,start_y,starting_strategy):
        Coms.start_comunications()
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
                Coms.reverse(1000)
                time.sleep(1)
                Coms.stop()
                time.sleep(0.3)
            if robot0 != None and ball != None:
                print "Main loop"
                if robot0.y > 194 or robot0.x > 265 or robot0.y < 30 or robot0.x < 40:
                    print "Close to wall"
                    Coms.reverse(1000)
                    time.sleep(1)
                    Coms.stop()
                    Coms.turn(180)
                    time.sleep(2)
                    Coms.stop()
                    time.sleep(1)
                    Coms.go()
                    time.sleep(3)
                    Coms.stop()
                else:
                    print "Normal strat"
                    time_to_object = get_time_to_travel(robot0.x,ball.x,robot0.y,ball.y)
                    C = namedtuple("C" , "x y")
                    angle_to_obj = us_to_obj_angle(robot0,C(ball.x,ball.y))
                    time_to_turn = get_time_to_angle(angle_to_obj)
                    print "angle to obj: ", angle_to_obj, "time to turn: ", time_to_turn
                    Coms.grab(0)
                    time.sleep(0.5)
                    Coms.stop()
                    time.sleep(1)
                    Coms.turn(angle_to_obj)
                    time.sleep(3)
                    Coms.stop()
                    time.sleep(0.3)
                    Coms.go()
                    time.sleep(time_to_object-0.05)
                    Coms.stop()
                    time.sleep(1)
                    Coms.grab(1)
                    time.sleep(1)
                    Coms.stop()
                    time.sleep(1)
                    Coms.grab(0)
                    time.sleep(1)
                    Coms.kick(10)
                    time.sleep(1)
                    Coms.stop()
                    time.sleep(1)
                    Coms.grab(1)
                    time.sleep(1)
                    Coms.stop()
                    time.sleep(1)

    @staticmethod
    def start2(corner,start_x,start_y,starting_strategy):
        Coms.start_comunications()
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
                    Coms.turn(angle_to_obj)
                    time.sleep(1.5)
                    Coms.go()
                    time.sleep(time_to_object)
                    Coms.stop()
                    time_to_mid = get_time_to_travel(CORNER14X,MIDX,CORNER14Y,MIDY)
                    if corner == 1:
                        Coms.turn(270)
                        time.sleep(2.5)
                        Coms.go()
                        time.sleep(time_to_mid+0.2)
                        Coms.stop()
                    else:
                        Coms.turn(90)
                        time.sleep(1.5)
                        Coms.go()
                        time.sleep(time_to_mid+0.2)
                        Coms.stop()
                    Coms.grab(1)
                    time.sleep(1)
                    Coms.stop()
                    time.sleep(1)
                    Coms.go()
                    time.sleep(0.4)
                    Coms.stop()
                    time.sleep(1)
                    Coms.grab(0)
                    time.sleep(1)
                    Coms.kick(10)
                    time.sleep(1)
                    Coms.stop()
                else:
                    C = namedtuple("C" , "x y")
                    C2 = namedtuple("C" , "x y rot")
                    robot_temp = C2(start_x,start_y,180)
                    time_to_object = get_time_to_travel(robot_temp.x,CORNER23X,robot_temp.y,CORNER23Y)
                    angle_to_obj = us_to_obj_angle(robot_temp,C(CORNER23X,CORNER23Y))
                    Coms.turn(angle_to_obj)
                    time.sleep(1.5)
                    Coms.go()
                    time.sleep(time_to_object)
                    Coms.stop()
                    time_to_mid = get_time_to_travel(CORNER23X,MIDX,CORNER23Y,MIDY)
                    if corner == 2:
                        Coms.turn(90)
                        time.sleep(1.5)
                        Coms.go()
                        time.sleep(time_to_mid+0.2)
                        Coms.stop()
                    else:
                        Coms.turn(270)
                        time.sleep(2.5)
                        Coms.go()
                        time.sleep(time_to_mid+0.2)
                        Coms.stop()
                    Coms.grab(1)
                    time.sleep(1)
                    Coms.stop()
                    time.sleep(1)
                    Coms.grab(0)
                    time.sleep(1)
                    Coms.kick(10)
                    time.sleep(1)
                    Coms.stop()
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
                        Coms.grab(0)
                        time.sleep(0.5)
                        Coms.turn(angle_to_obj)
                        time.sleep(2.5)
                        Coms.go()
                        time.sleep(time_to_object)
                        Coms.stop()
                        Coms.grab(1)
                        time.sleep(1)
                        Coms.stop()
                        time.sleep(1)
                        Coms.grab(0)
                        time.sleep(1)
                        Coms.kick(10)
                        time.sleep(1)
                        Coms.stop()
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
                            Coms.turn(angle_to_obj)
                            time.sleep(2.5)
                            Coms.go()
                            time.sleep(time_to_object)
                            Coms.stop()
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
                            Coms.turn(angle_to_obj)
                            time.sleep(2.5)
                            Coms.go()
                            time.sleep(time_to_object)
                            Coms.stop()
                            guess_x = CORNER23X
                            guess_y = CORNER23Y
                            guess_rot = robot_temp.rot + angle_to_obj
                    else:
                        print "Stuck"
                        if i % 2 == 0:
                            Coms.reverse(800)
                            time.sleep(1)
                            Coms.turn(180)
                            Coms.stop()
                        else:
                            Coms.go()
                            time.sleep(1.8)
                            Coms.stop()
                        i = i + 1

    #Do we really need static method?
    @staticmethod
    def start3(corner,start_x,start_y,starting_strategy = "n",verbose="n"):
        Coms.start_comunications()
        time.sleep(1)

        #Checking Juno
        missingJunoCounter = 0
        maxJunoCounter = 3

        while True:
            if starting_strategy == "y":
                #TODO kickoff strategy
                if verbose == "y": print "Strategy: Running kickoff strat"
                starting_strategy = "n"

                #Copied from start2()
                if corner == 1 or corner == 4:
                    C = namedtuple("C" , "x y")
                    C2 = namedtuple("C" , "x y rot")
                    robot_temp = C2(start_x,start_y,0)
                    time_to_object = get_time_to_travel(robot_temp.x,CORNER14X,robot_temp.y,CORNER14Y)
                    angle_to_obj = us_to_obj_angle(robot_temp,C(CORNER14X,CORNER14Y))
                    Coms.turn(angle_to_obj)
                    time.sleep(1.5)
                    Coms.go()
                    time.sleep(time_to_object)
                    Coms.stop()
                    time_to_mid = get_time_to_travel(CORNER14X,MIDX,CORNER14Y,MIDY)
                    if corner == 1:
                        Coms.turn(270)
                        time.sleep(2.5)
                        Coms.go()
                        time.sleep(time_to_mid+0.2)
                        Coms.stop()
                    else:
                        Coms.turn(90)
                        time.sleep(1.5)
                        Coms.go()
                        time.sleep(time_to_mid+0.2)
                        Coms.stop()
                    Coms.grab(1)
                    time.sleep(1)
                    Coms.stop()
                    time.sleep(1)
                    Coms.go()
                    time.sleep(0.4)
                    Coms.stop()
                    time.sleep(1)
                    Coms.grab(0)
                    time.sleep(1)
                    Coms.kick(10)
                    time.sleep(1)
                    Coms.stop()
                else:
                    C = namedtuple("C" , "x y")
                    C2 = namedtuple("C" , "x y rot")
                    robot_temp = C2(start_x,start_y,180)
                    time_to_object = get_time_to_travel(robot_temp.x,CORNER23X,robot_temp.y,CORNER23Y)
                    angle_to_obj = us_to_obj_angle(robot_temp,C(CORNER23X,CORNER23Y))
                    Coms.turn(angle_to_obj)
                    time.sleep(1.5)
                    Coms.go()
                    time.sleep(time_to_object)
                    Coms.stop()
                    time_to_mid = get_time_to_travel(CORNER23X,MIDX,CORNER23Y,MIDY)
                    if corner == 2:
                        Coms.turn(90)
                        time.sleep(1.5)
                        Coms.go()
                        time.sleep(time_to_mid+0.2)
                        Coms.stop()
                    else:
                        Coms.turn(270)
                        time.sleep(2.5)
                        Coms.go()
                        time.sleep(time_to_mid+0.2)
                        Coms.stop()
                    Coms.grab(1)
                    time.sleep(1)
                    Coms.stop()
                    time.sleep(1)
                    Coms.grab(0)
                    time.sleep(1)
                    Coms.kick(10)
                    time.sleep(1)
                    Coms.stop()
                guess_x = MIDX
                guess_y = MIDY
                guess_rot = 0

            else:
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

                if ball != None and me != None:
                    if solo_strat:
                        #TODO Strategy if Juno is not found
                        if verbose == "y": print "Strategy: Running SOLO strat"

                    else:
                        #TODO Strategy if Juno is found
                        if verbose == "y": print "Strategy: Running DUO strat"

                elif ball == None:
                    #TODO Strategy if ball not found
                    if verbose == "y": print "Strategy: Ball not found"

                elif me == None:
                    #TODO Strategy is self not found
                    if verbose == "y": print "Strategy: Robot not found"

                else:
                    #You are not supposed to get here
                    print "Strategy: Unknown error"

