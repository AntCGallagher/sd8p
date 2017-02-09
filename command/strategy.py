from postprocessing.world import World
from communications.originalcomms import Coms
from helpers import *
import math
import time
import numpy
"""
This script will be used to test a simple strategy.
At the moment owner represents who has the ball.
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
        time.sleep(4)

    @staticmethod
    def start():

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

    @staticmethod
    def ping_location():
        curr_world = waitForWorld(False , requireBall = True , no_oponents = 0)
        robot1 = curr_world.robots[0]
        time.sleep(2)
        print "Robot position: ", robot1.x , "  " , robot1.y

    @staticmethod
    def test_corner():
        Coms.start_comunications()
        curr_world = World.get_world()
        robot1 = curr_world.robots[0]
        C = namedtuple("C" , "x y")
        angle_to_corner = us_to_obj_angle(robot1,C(TOPRIGX,TOPRIGY))
        print "Angle: ", angle_to_corner
        Coms.stop()
        time.sleep(1)
        Coms.stop()
        time.sleep(1)
        Coms.stop()
        time.sleep(1)
        Coms.turn(-angle_to_corner)
        time.sleep(1)
        Coms.stop()
        time.sleep(1)
        Coms.go()
        time.sleep(3.3)
        Coms.stop()
        time.sleep(0.5)
        Coms.reverse(1)
        time.sleep(0.7)
        Coms.stop()
        time.sleep(1)


    #Gets the right goal centers, tested
    @staticmethod
    def test_goal_center():
        curr_world = World.get_world()
        print curr_world.get_goal_center()

    """
            #Change strategy depending on the zone
            if side == "left":
                if ball_zone == 0 or ball_zone == 1:
                    #Coms.turn(95)
                    print "left zone 0 1"
                else:
                    #Coms.turn(190)
                    print "left zone 2 3"
            else:
                if ball_zone == 0 or ball_zone == 1:
                    #Coms.go()
                    #time.sleep(1)
                    #Coms.stop()
                    print "right zone 0 1"
                else:
                    #Coms.kick(10)
                    #Coms.stop()
                    print "right zone 2 3"

        #print angle
    """



"""
        # Set up fields
        owner = ball.owner
        print ball
        our_robot = curr_world.robots[1]
        print our_robot
        print owner
        print "Angle"
        print helpers.us_to_obj_angle(our_robot,ball)
"""
"""
        # Pick your strategy depending on who has the ball
        if self.owner == 0:
            #implement get ball
        elif self.owner == 1:
            #implement shoot or pass
        else:
            #implement intercept
"""
