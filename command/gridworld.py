#My implementation of the grid world idea. Feel free to test/edit it out
class GridWorld(object):
    court_x_cm = 220
    court_y_cm = 300
    court_x_grid = 4
    court_y_grid = 6

    def __init__(self,robots,ball):
        self.robots = self.conv_to_gridRobots(robots)
        self.ball = self.conv_to_gridBall(ball)

    def closest_to_ball(self):
        closest = None
        closest_dist = 100
        ballx = self.ball.x
        bally = self.ball.y
        for robot in self.robots:
            if robot != None:
                if closest_dist >= abs(ballx - robot.x) + abs(bally - robot.y):
                    closest = robot
        return closest


    def get_grid(self,x,y):
        if x < self.court_x_grid and y < self.court_y_grid:
            i = 0
            items = {}
            for robot in self.robots:
                if robot != None:
                    items[i] = robot
                    i += 1

            if self.ball != None:
                items[i] = self.ball

            return items

    def conv_to_gridRobots(self,robots):
        i = 0
        new_robot = {}
        for robot in robots:
            if robot != None:
                new_robot[i] = GridRobot(robot.x,robot.y,robot.rot)
            else:
                new_robot[i] = None
            i += 1

        return new_robot

    def conv_to_gridBall(self,ball):
        if ball != None:
            new_ball = GridBall(ball.x,ball.y)
        else:
            new_ball = None;
        return None

class GridRobot(object):
    def __init__(self,x,y,rotation):
        self.x = int(x/GridWorld.court_x_cm*GridWorld.court_x_grid)
        self.y = int(y/GridWorld.court_y_cm*GridWorld.court_y_grid)
        self.rot = rotation

    def isAt(self,x,y):
        if self.x == x and self.y == y:
            return True
        return False


class GridBall(object):
    def __init__(self,x,y):
        self.x = int(x/GridWorld.court_x_cm*GridWorld.court_x_grid)
        self.y = int(y/GridWorld.court_y_cm*GridWorld.court_y_grid)

    def isAt(self,x,y):
        if self.x == x and self.y == y:
            return True
        return False