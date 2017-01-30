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
        Coms.start_comunications()

        # Get world model and some values
        curr_world = World.get_world()
        ball = curr_world.ball
        robots = curr_world.robots
        our_robot = curr_world.robots[1]
        angle = helpers.us_to_obj_angle(our_robot,ball)
        Coms.stop()
        Coms.goxy(our_robot.x, our_robot.y, angle, ball.x, ball.y)
        time.sleep(5)
        angle2 = helpers.us_to_obj_angle(our_robot,ball)
        Coms.turn(angle2)
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
