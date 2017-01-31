from postprocessing.world import World
from communications.originalcomms import Coms
import helpers
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
        # Start communications
        #Coms.start_comunications()

        # Get world model and some values
        curr_world = World.get_world()
        ball = curr_world.ball
        robots = curr_world.robots
        robot1 = curr_world.robots[0]
        robot2 = curr_world.robots[1]
        robot3 = curr_world.robots[2]
        robot4 = curr_world.robots[3]
        if robot1 != None:
            angle = helpers.us_to_obj_angle(robot1,ball)
        #Coms.stop()
        time.sleep(2)
        #Coms.goxy(our_robot.x, our_robot.y, angle, ball.x, ball.y)
        #Coms.turn(angle2)
        if robot1 != None:
            print robot1.x," robot 1",robot1.y
        if robot2 != None:
            print robot2.x," robot 2",robot2.y
        if robot3 != None:
            print robot3.x," robot 3",robot3.y
        if robot4 != None:
            print robot4.x," robot 4",robot4.y
        print ball.x," ",ball.y
        #print angle
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
