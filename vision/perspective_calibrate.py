import cv2
import numpy as np
from vision import Camera
import tools

"""
    IMPORTANT!!!
    Only need to select 4 points, start at the top left,
    then clock-wise top right, bottom right, bottom left.

    After 4 points are selected, it should automatically save 
    the points to calibrations/perspective.json

    Then Camera object the stretches the four points to corners in
    the order specidfied.
"""


class Perspective(object):

    def __init__(self, pitch=0):
        self.points = []
        self.pitch = pitch

    # mouse callback function
    def add_point(self, event,x,y,flags,param):
    
        if event == cv2.EVENT_LBUTTONDBLCLK:

            self.points.append((x,y))

            # Only taking one point for each corner
            if len(self.points) == 4:
                print 'saving'
                self.save()
                self.points = []

            print self.points
            print len(self.points)

    def draw_points(self, frame):
        for point in self.points:
            cv2.circle(frame,point,5,(0,0,0))
            cv2.circle(frame,point,4,(0,255,0))
            cv2.circle(frame,point,3,(0,0,0))
            cv2.circle(frame,point,1,(0,0,0))
        return frame

    def save(self):
        """
            Save perspetive point fixes
        """
        tools.save_data(self.pitch, self.points, 'calibrations/perspective.json')

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pitch", help="[0] Main pitch, [1] Secondary pitch")
    args = parser.parse_args()
    pitch_number = int(args.pitch)

    WINDOW_NAME = 'Perspective Calibration'
    cam = Camera(pitch=pitch_number)
    perspective = Perspective(pitch_number)

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, perspective.add_point)

    while(1):
        frame = cam.get_raw_frame();
        frame = cam.fix_radial_distortion(frame)
        frame = perspective.draw_points(frame)

        cv2.imshow(WINDOW_NAME,frame)

        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

