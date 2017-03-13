# sd8p
SDP 2017 - Group 8

Strategy code is a mess, message me if you have any issues.

To start the robot, use the command python start.py 0 yellow pink left on the home directory. Change the 0 for 1 depending on the room, the left to right depending on the side you are defending. Calibrate the image and once you're satisfied type done and press ENTER. It will wait for the world model before starting, so if there is only one robot on the pitch good luck.

The strategy at the moment is as follows:

If the ball is in your zone 0 (the zone of the box) and you are farther than it from the goal, your job is to defend it. Move to the corner to get a good angle and go back at attacking the ball once you can push it away. (This is pretty buggy at the moment because the vision sees ghost of sd8p).

Otherwise attack the ball. Calculate the angle to the ball and turn a bit and move forward. Calculate the angle again, if it's within a threshold try to cover a lot of distance, otherwise correct it and move a bit. There are a lot of sleeps on the code, change at your own caution.

As a last resort, if the robot is in the same position as the beginning it tries to reverse (buggy again for multiple reasons).

13 March 17
If any robot stays in the same place for 20 world model will be assumed that it is not working thus ignored by strategy system.

If Juno is ignored {
    Run solo strategy
    If sd8p closer to the ball {
        Go to ball and shoot
    } else {
        Go to center of goal
        Always face the ball
    }
} else {
    Run duo strategy
    If sd8p in zone 0 {
        Leave zone 0
    }
    If ball in zone 0 {
        Go to a location
        Always face the ball
    } else if Juno is near ball {
        Go to a location
        Always face the ball
    } else {
        If sd8p is closest to ball {
            Go to ball and shoot
        } else {
            Calculate intercept location x
            If x in zone 0 {
                Go to a location
                Always face the ball
            } else {
                Go to x
                Always face the enemy
            }
        }
    }
}

