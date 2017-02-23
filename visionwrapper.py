from vision.vision import Camera
import vision.tools as tools
#from vision.my_tracker import MyTracker
from vision.test_tracker import MyTracker
from postprocessing.world import World
import cv2
from math import radians,cos,sin , pi
from numpy import array
from vision.colors import BGR_COMMON
from vision.findCameraSettings import CameraCalibrationGUI

class VisionWrapper(object):

    def __init__(self, pitch, ourTeamColor='yellow', otherTeamColor='blue', ballColor='red'):
        self.pitch         = pitch
        self.camera        = Camera(pitch=pitch)
        self.calibration   = tools.get_colors(pitch)
        self.tracker       = MyTracker(self.calibration)
        #self.tracker       = MyTracker([ourTeamColor, otherTeamColor, ballColor, 'pink', 'bright_green'], self.calibration)
        self.points        = {} # point dictionary for tracked colors
        self.GUI_name           = "Killer Robot App"
        self.calibration_gui    = CameraCalibrationGUI(calibration=self.calibration , name=self.GUI_name)

    def run(self):

        images = []

        while(True):

            time = tools.current_milli_time()

            # Update trackbars
            self.calibration_gui.update()

            # get updated camera settings
            settings = self.calibration_gui.getSettings()

            # Update camera settings
            self.camera.reset_camera_settings(settings=settings)


            # capture frame by frame
            frame = self.camera.get_frame()

            #images.append(frame)

            #if len(images) > 2:
            #    images = images[1:]

            image = frame;
            #if len(images) == 2:
            #    image = cv2.addWeighted(images[0], 0.5 ,images[1], 0.5, 0)
            #    temp2 = cv2.addWeighted(images[2], 0.5 ,images[3], 0.5, 0)
            #    image = cv2.addWeighted(temp1, 0.5 ,temp2, 0.5, 0)


            # Get tracked object points
            self.points, modified_frame = self.tracker.get_world_state(image)



            # TODO: think about tracked points sometimes jerking arround
            # maybe get a threshold of how far of a distance change should
            # be accounted

            # TODO: implement functions to find robots using points
            # dictionary

            # TODO: some rudamentary logic can be implemented here
            # along with connection to the robot
            # Better to have two classes, one for robot logic
            # Another for communication handling

            World.set_points(self.points)
            w = World.get_world()

            for l1 in range(0,640,128):
                cv2.line(image, (l1,0), (l1,480), (209,192,142), thickness=1)
            for l2 in range(0,480,96):
                cv2.line(image, (0,l2), (640,l2), (209,192,142), thickness=1)

            for i3 , robot in enumerate(w.robots):
                if robot != None:
                    #print "Angle:" + str(robot.rot)
                    rads = radians(robot.rot)
                    x1, y1 = (robot.x_px, robot.y_px)
                    x2 = int(x1 + cos(rads) * 50);
                    y2 = int(y1 + sin(rads) * 50);
                    cv2.arrowedLine(image, (int(x1), int(y1)), (x2,y2), BGR_COMMON[ World.our_team_colour if i3 < 2 else World.oposite_team_colour], 2)
                    corners = [(int(x1 + cos(rads + radians(45) + 90*pi/180*i)*20) , (int(y1 + sin(rads + radians(45)+ 90*pi/180*i)*20))) for i in range(4)]
                    cv2.putText	(img=image,
                                text=str(i3),
                                org=(int(x1-10), int(y1+10)),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1,
                                color=(255,255,255))

                    for i2 in range(4):
                        col = BGR_COMMON[ World.our_primary if i3  % 2 == 0 else World.other_primary]
                        cv2.line(image, corners[i2] , corners[(i2+1)%4] , col , 2)

            if w.ball != None :
                ball = World.cm_to_px(w.ball.x , w.ball.y)
                ball = (int(ball[0]) , int(ball[1]) )
                cv2.circle(image , (ball[0] , ball[1]) , 10 , (255,0,0))
                cv2.arrowedLine(image , (ball[0] , ball[1]) ,(int(ball[0] + w.ball.dir[0] ), int(ball[1] + w.ball.dir[1])) ,(255, 0 ,0) , 2)

            #cv2.imshow('test', frame)

            #cv2.waitKey(0)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # display FPS
            time = ((tools.current_milli_time()-time))/1000.0
            fps = 1.0 / time
            cv2.putText(image, "FPS: "+str(round(fps)), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

            cv2.imshow(self.GUI_name, image)

            # Display the resulting frame
            #cv2.imshow('Killer Robot App', image)

        # When everything is doen, release the capture
        cv2.destroyAllWindows()



if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pitch", help="[0] Main pitch, [1] Secondary pitch")
    args = parser.parse_args()
    pitch_number = int(args.pitch)


    wrapper = VisionWrapper(pitch=pitch_number)
    wrapper.run()
