from postprocessing.world import World
from communications.originalcomms import Coms
from helpers import *
import math
import time
import numpy
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

class Strategy(object):
    def __init__(self):
        self.owner = 0
        self.teammate_on = 0

    @staticmethod
    def tests():
        inp = ""
        while inp != "done":
            inp = raw_input("ping/goxy/go_robot_ball/turn ? (p/gxy/grb/t)")
            if inp == "p"
                curr_world = World.get_world()
                ball = curr_world.ball
                robots = curr_world.robots
                robot0 = curr_world.robots[0]
                robot1 = curr_world.robots[1]
                robot2 = curr_world.robots[2]
                robot3 = curr_world.robots[3]
                if robot0 != None:
                    print "Robot0: ", robot0.x , "  " , robot0.y
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
                    Coms.turn(get_angle_to_send(int(angle_to_obj)))
                    time.sleep(1.5)
                    Coms.reverse(200)
                    time.sleep(time_to_object)
                    Coms.stop()
                elif robot0 == None && ball != None:
                    print "Robot and ball not detected"
                elif robot0 == None:
                    print "Robot not detected"
                else:
                    print "Ball not detected"
            if inp == "t":
                value = int(raw_input("angle to turn: "))
                Coms.start_comunications()
                Coms.turn(get_angle_to_send(value))
                time.sleep(1.5)


    @staticmethod
    def stop():
        Coms.start_comunications()
        Coms.stop()
        curr_world = World.get_world()
        ball = curr_world.ball
        robots = curr_world.robots
        robot0 = curr_world.robots[0]
        inp = ""
        while inp != "done":
            inp = raw_input("action please: ")
            if inp == "go":
                C = namedtuple("C" , "x y")
                time_to_object = get_time_to_travel(robot0.x,ball.x,robot0.y,ball.y)
                angle_to_obj = us_to_obj_angle(robot0,C(ball.x,ball.y))
                print "robot: ", robot0.x, " ", robot0.y
                print "ball: ", ball.x, " ", ball.y
                print "time: ", time_to_object, " angle: ", angle_to_obj
                Coms.turn(get_angle_to_send(int(angle_to_obj)))
                time.sleep(1.5)
                Coms.reverse(200)
                time.sleep(time_to_object)
                Coms.stop()
            if inp == "stop":
                Coms.stop()

    @staticmethod
    def start():
        #Coms.turn(get_angle_to_send(int(value))) TODO: Turn like this
        Coms.start_comunications()

        # Get world model and some values
        curr_world = waitForWorld(False , requireBall = True , no_oponents = 0)
        ball = curr_world.ball
        robots = curr_world.robots
        robot1 = curr_world.robots[0]
        robot2 = curr_world.robots[1]
        robot3 = curr_world.robots[2]
        robot4 = curr_world.robots[3]


        if robot1 != None and ball != None:
            list = []
            calculated_time = time.time() + 1
            while(calculated_time > time.time()):
                temp_world = World.get_world()
                list.append(temp_world.robots[0].rot)
            ball_zone = ball.get_zone()
            side = World.our_side
            print "Ball: ", ball.x, "  ", ball.y
            robot1.rot = np.median(list)
            angle_to_ball = us_to_obj_angle(robot1,ball)
            print "Angle to ball: " , angle_to_ball
            #print "Math god angle: " , mathgod(robot1.x,robot1.y,robot1.rot,ball.x,ball.y)
            goal_center = World.get_goal_center(False)
            C = namedtuple("C" , "x y")
            #print "Angle to goal: ", angle_to_goal

            oldx = robot1.x
            oldy = robot1.y
            print "Side currently on: ", side, " Zone: ", ball_zone, " Robot x: ", robot1.x
            if side == "Left":
                if (ball_zone == 0 and (robot1.x > ball.x)):
                    print "LEFT DEFENSE"
                    C = namedtuple("C" , "x y")
                    angle_to_corner = us_to_obj_angle(robot1,C(TOPLEFX,TOPLEFY))
                    Coms.stop()
                    time.sleep(0.3)
                    Coms.stop()
                    time.sleep(0.3)
                    Coms.stop()
                    time.sleep(0.3)
                    Coms.turn(-angle_to_corner)
                    time.sleep(1)
                    Coms.go()
                    time.sleep(3.3)
                    Coms.stop()
                    time.sleep(0.5)
                    Coms.reverse(1)
                    time.sleep(0.7)
                    Coms.stop()
                else:
                    if math.fabs(angle_to_ball) < 10:
                        Coms.go()
                        time.sleep(1.5)
                        Coms.stop()
                    else:
                        Coms.stop()
                        Coms.turn(-angle_to_ball)
                        time.sleep(1)
                        Coms.go()
                        time.sleep(0.6)
                        Coms.stop()
            else:
                if (ball_zone == 0 and (robot1.x < ball.x)):
                    print side
                    print "RIGHT DEFENSE"
                    C = namedtuple("C" , "x y")
                    angle_to_corner = us_to_obj_angle(robot1,C(TOPRIGX,TOPRIGY))
                    Coms.stop()
                    time.sleep(0.3)
                    Coms.stop()
                    time.sleep(0.3)
                    Coms.stop()
                    time.sleep(0.3)
                    Coms.turn(-angle_to_corner)
                    time.sleep(1)
                    Coms.go()
                    time.sleep(3.3)
                    Coms.stop()
                    time.sleep(0.5)
                    Coms.reverse(1)
                    time.sleep(0.7)
                    Coms.stop()
                else:
                    if math.fabs(angle_to_ball) < 10:
                        Coms.go()
                        time.sleep(1.5)
                        Coms.stop()
                    else:
                        Coms.stop()
                        Coms.turn(-angle_to_ball)
                        time.sleep(1)
                        Coms.go()
                        time.sleep(0.6)
                        Coms.stop()
        if ball_close(robot1,ball):
            Coms.turn(360)
            time.sleep(0.6)
            Coms.stop()
        final_world = World.get_world()
        future_robot = final_world.robots[1]
        if (math.fabs(oldx-future_robot.x) + math.fabs(oldy - future_robot.y)) < 7:
            Coms.reverse(1)
            time.sleep(1)
            Coms.stop()
