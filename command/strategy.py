from postprocessing.world import World
"""
This script will be used to test a simple strategy.
"""

class Strategy(object):

    def __init__(self):
        self.owner = 0

    @staticmethod
    def start():
        curr_world = World.get_world()
        ball = curr_world.ball
        print ball
        our_robot = curr_world.robots[1]
        print our_robot
