from postprocessing.world import World
from communications.originalcomms import Coms
from helpers import *
import time
"""
This script will be used to test a simple strategy.
At the moment owner represents who has the ball.
"""

class Strategy(object):
    def __init__(self):
        self.owner = 0
        self.teammate_on = 0

    @staticmethod
    def start():

        Coms.start_comunications()

        # Get world model and some values
        curr_world = waitForWorld(False , requireBall = True , no_oponents = 0)
        ball = curr_world.ball
        robots = curr_world.robots
        robot1 = curr_world.robots[0]
        robot2 = curr_world.robots[1] #ours
        robot3 = curr_world.robots[2]
        robot4 = curr_world.robots[3]

        if robot1 != None:
            print "Robot1: ", robot1.x , "  " , robot1.y # ours
            print robot1
        #if robot2 != None:
        #    print "Robot2: ", robot2.x , "  " , robot2.y
        #if robot3 != None:
    #    #    print "Robot3: ", robot3.x , "  " , robot3.y
    #    if robot4 != None:
        #    print "Robot4: ", robot4.x , "  " , robot4.y
    #    print "Ball: " , ball.x , "  " , ball.y

        if robot2 != None and ball != None:
            ball_zone = ball.get_zone()
            print ball.get_zone()
            side = World.our_side
            print "Robot2: " , robot2.x,"  ",robot2.y
            print "Ball: ", ball.x, "  ", ball.y
            angle_to_ball = us_to_obj_angle(robot2,ball)
            print "Angle to ball: " , angle_to_ball
            goal_center = World.get_goal_center(False)
            C = namedtuple("C" , "x y")
            angle_to_goal = us_to_obj_angle(robot2,C(goal_center[0],goal_center[1]))
            #print "Angle to goal: ", angle_to_goal
            #Coms.turn(angle_to_ball)
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
