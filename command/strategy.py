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
        ball = curr_world.get_ball()
        print ball.center
