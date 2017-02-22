import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import tools
import math
import test_tracker
import time

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)

class Camera(object):
    """
    Camera access wrapper.
    """

    def __init__(self, port=0, pitch=0):
        self.pitch              = pitch
        self.capture            = cv2.VideoCapture(port)

        calibration             = tools.get_colors(pitch=pitch)
        self.camera_settings    = calibration["camera"]

        self.reset_camera_settings()

        # Parameters used to fix radial distortion
        self.radial_data        = tools.get_radial_data()
        self.nc_matrix          = self.radial_data['new_camera_matrix']
        self.c_matrix           = self.radial_data['camera_matrix']
        self.dist               = self.radial_data['dist']

        self.background         = cv2.imread('pitch_photos/pitch_'+str(pitch)+".jpeg")

    def release(self):
        self.capture.release()


    def get_frame(self):
        """
        Retrieve a frame from the camera

        Returns the frame if available, otherwise returns None.
        """

        # status, frame = True, cv2.imread('img/i_all/00000003.jpg')

        #status = True
        #frame = cv2.imread('snap-1.jpeg')
        #frame = cv2.resize(frame, (640, 480))
        status, frame = self.capture.read()

        frame = self.fix_radial_distortion(frame)

        frame = self.fix_perspective(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #frame[:, :, 1] = cv2.equalizeHist(frame[:, :, 1])
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)


        # fix noise
        #frame = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)

        if status:
            return frame


    def get_raw_frame(self):
        """
         Retrieve a raw frame from the camera.
        """
        status, frame = self.capture.read()

        if status:
            return frame

    def fix_radial_distortion(self, frame):
        return cv2.undistort(
            frame, self.c_matrix, self.dist, None, self.nc_matrix)

    def get_adjusted_center(self, frame):
        return (320-self.crop_values[0], 240-self.crop_values[2])

    def rotate(self, frame, deg):
        rows,cols,nfn = frame.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2), deg, 1)
        return cv2.warpAffine(frame, M, (cols, rows))

    def fix_perspective(self, frame):
        rows,cols,nfn = frame.shape

        pts  = tools.get_perspective(self.pitch)
        pts1 = np.float32([pts[0],pts[1],pts[2],pts[3]])
        pts2 = np.float32([(0,0),(cols,0),(cols, rows),(0,rows)])

        M   = cv2.getPerspectiveTransform(pts1,pts2)
        dst = cv2.warpPerspective(frame,M,(cols,rows))

        return dst

    def reset_camera_settings(self, settings=None):

        if settings:
            BRIGHTNESS  = settings['brightness']    /100.0
            CONTRAST    = settings['contrast']      /100.0
            SATURATION  = settings['saturation']    /100.0
            HUE         = settings['hue']           /100.0
        else:
            BRIGHTNESS  = self.camera_settings['brightness']    /100.0
            CONTRAST    = self.camera_settings['contrast']      /100.0
            SATURATION  = self.camera_settings['saturation']    /100.0
            HUE         = self.camera_settings['hue']           /100.0

        self.capture.set(cv2.CAP_PROP_BRIGHTNESS,   BRIGHTNESS)
        self.capture.set(cv2.CAP_PROP_CONTRAST,     CONTRAST)
        self.capture.set(cv2.CAP_PROP_SATURATION,   SATURATION)
        self.capture.set(cv2.CAP_PROP_HUE,          HUE)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pitch", help="[0] Main pitch, [1] Secondary pitch")
    args = parser.parse_args()

    pitch_number = int(args.pitch)

    calibration = tools.get_colors(pitch_number)

    tracker = test_tracker.MyTracker(calibration=calibration)

    cam = Camera(pitch=pitch_number)

    while(True):

        time = tools.current_milli_time()

        # capture frame by frame
        frame = cam.get_frame()

        # Our operations on the frame come here
        points, frame = tracker.get_world_state(frame)

        # display FPS
        time = ((tools.current_milli_time()-time))/1000.0
        fps = 1.0 / time
        cv2.putText(frame, "FPS: "+str(round(fps)), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        cv2.imshow('image', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is doen, release the capture
    cv2.destroyAllWindows()
