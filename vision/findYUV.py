import cv2
import numpy as np
import matplotlib.pyplot as plt
import consol

import vision
import tools
import subprocess

CONTROL = ["Lower threshold for brightness",
           "Upper threshold for brightness",
           "Lower threshold for color U",
           "Upper threshold for color U",
           "Lower threshold for color V",
           "Upper threshold for color V",
           "Contrast",
           "Gaussian blur",
           "Open kernel",
           "Close kernel",
           "Erode",
           'High pass',
           'Object count']

MAXBAR = {"Lower threshold for brightness":360,
          "Upper threshold for brightness":360,
          "Lower threshold for color U":255,
          "Upper threshold for color U":255,
          "Lower threshold for color V":255,
          "Upper threshold for color V":255,
          "Contrast":100,
          "Gaussian blur":100,
          "Open kernel": 10,
          "Close kernel": 10,
          "Erode":100,
          'High pass':255,
          'Object count':20,
        }

INDEX = {"Lower threshold for brightness":0,
         "Upper threshold for brightness":0,
         "Lower threshold for color U":1,
         "Upper threshold for color U":1,
         "Lower threshold for color V":2,
         "Upper threshold for color V":2
        }

KEYS = {ord('y'):'yellow',
        ord('r'):'red',
        ord('b'):'blue',
        ord('d'):'dot'}

def nothing(x):
    pass

class CalibrationGUI(object):
    """
    This class caters for the creation of
    the brightness, color U, color V, contrast and
    blur threshold trackbars
    """
    def __init__(self, calibration):
        consol.log('use y r b d p and click on objects in video to calibrate', None)
        self.color = 'red'
        # self.pre_options = pre_options
        self.calibration = calibration
        self.maskWindowName = "Mask " + self.color
        self.frameWindowName = "Frame window"
        self.frame = None

        self.setWindow()

    def setWindow(self):



        cv2.namedWindow(self.maskWindowName)
        cv2.namedWindow(self.frameWindowName)

        cv2.setMouseCallback(self.frameWindowName, self.mouse_call)

        # print self.calibration
        createTrackbar = lambda setting, \
                                color_V: \
                                    cv2.createTrackbar(
                                        setting,
                                        self.maskWindowName,
                                        int(color_V),
                                        MAXBAR[setting], nothing)

        createTrackbar('Lower threshold for brightness',
                       self.calibration[self.color]['min'][0])
        createTrackbar('Upper threshold for brightness',
                       self.calibration[self.color]['max'][0])
        createTrackbar('Lower threshold for color U',
                       self.calibration[self.color]['min'][1])
        createTrackbar('Upper threshold for color U',
                       self.calibration[self.color]['max'][1])
        createTrackbar('Lower threshold for color V',
                       self.calibration[self.color]['min'][2])
        createTrackbar('Upper threshold for color V',
                       self.calibration[self.color]['max'][2])
        createTrackbar('Contrast',
                       self.calibration[self.color]['contrast'])

        createTrackbar('Gaussian blur',
                       self.calibration[self.color]['blur'])
        createTrackbar('Open kernel',
                       self.calibration[self.color]['open_kernel'])
        createTrackbar('Close kernel',
                       self.calibration[self.color]['close_kernel'])
        createTrackbar('Erode',
                       self.calibration[self.color]['erode'])
        createTrackbar('Object count',
                       self.calibration[self.color]['object_count'])


        hp = self.calibration[self.color].get('highpass')
        hp = hp if hp is not None else 0
        createTrackbar('High pass', hp)

    def change_color(self, color):
        """
        Changes the color mask within the GUI
        """
        cv2.destroyWindow(self.maskWindowName)
        self.color = color
        self.maskWindowName = "Mask " + self.color
        self.setWindow()



    def show(self, frame, key=None):


        if key != 255:
            try:
                self.change_color(KEYS[key])
            except:
                pass

        getTrackbarPos = lambda setting: cv2.getTrackbarPos(setting, self.maskWindowName)

        color_Vs = {}
        for setting in CONTROL:
            color_Vs[setting] = float(getTrackbarPos(setting))
        color_Vs['Gaussian blur'] = int(color_Vs['Gaussian blur'])

        self.calibration[self.color]['min'] = np.array(
                                                [color_Vs['Lower threshold for brightness'],
                                                 color_Vs['Lower threshold for color U'],
                                                 color_Vs['Lower threshold for color V']])
        self.calibration[self.color]['max'] = np.array(
                                                    [color_Vs['Upper threshold for brightness'],
                                                     color_Vs['Upper threshold for color U'],
                                                     color_Vs['Upper threshold for color V']])
        self.calibration[self.color]['contrast']        = color_Vs['Contrast']
        self.calibration[self.color]['blur']            = color_Vs['Gaussian blur']
        self.calibration[self.color]['open_kernel']     = int(color_Vs['Open kernel'])
        self.calibration[self.color]['close_kernel']    = int(color_Vs['Close kernel'])
        self.calibration[self.color]['erode']           = int(color_Vs['Erode'])
        self.calibration[self.color]['highpass']        = color_Vs['High pass']
        self.calibration[self.color]['object_count']    = color_Vs['Object count']

        mask = self.get_mask(frame)
        cv2.imshow(self.frameWindowName, mask)

    # Duplicated from tracker.py
    def get_mask(self, frame):
        """
        NOTE THIS IS ONLY USED FOR DISLPAY PURPOSES
        GaussianBlur blur:
            G =     [[G11, ..., G1N],
                1/L      ...,
                     [GN1, ..., GNN]]
            G is the bluring kernel
            L = sqrt(dot(blur, blur))
            GII Gaussian number

        params:
            frame:
                description: camera image
                type: numpy array

        output:
            frame_mask;
                description: filtered (blured) camera image.
                    it is blured by the GUI given parameters.
                type: numpy array

        """
        # plt.imshow(frame)
        # plt.show()

        blur = self.calibration[self.color]['blur']
        if blur >= 1:
            if blur % 2 == 0:
                blur += 1
            frame = cv2.GaussianBlur(frame, (blur, blur), 0)



        contrast = self.calibration[self.color]['contrast']
        if contrast >= 1.0:
            frame = cv2.add(frame, np.array([contrast]))

        self.frame = frame

        frame_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)

        min_color = self.calibration[self.color]['min']
        max_color = self.calibration[self.color]['max']
        frame_mask = cv2.inRange(frame_yuv, min_color, max_color)

        if self.calibration[self.color]['open_kernel'] >= 1:
                k = self.calibration[self.color]['open_kernel']
                kernel = np.ones((k,k ),np.uint8)
                frame_mask = cv2.morphologyEx(frame_mask,
                                              cv2.MORPH_OPEN,
                                              kernel,
                                              iterations=1)
        if self.calibration[self.color]['close_kernel'] >= 1:
                k = self.calibration[self.color]['close_kernel']
                kernel = np.ones((k,k ),np.uint8)
                frame_mask = cv2.morphologyEx(frame_mask,
                                              cv2.MORPH_CLOSE,
                                              kernel,
                                              iterations=1)
        if self.calibration[self.color]['erode'] >= 1:
                k = self.calibration[self.color]['erode']
                kernel = np.ones((k,k ),np.uint8)
                frame_mask = cv2.erode(frame_mask,
                                        kernel,
                                        iterations=1)


        #frame_mask = cv2.inRange(frame_yuv, 0.0,0.0)
        #return frame
        #return frame_mask



        out = frame

        hp = int(self.calibration[self.color]['highpass'])
        f_mask = CalibrationGUI.highpass(frame_mask, frame, hp)

        cv2.imshow('f_mask', f_mask)

        mask_inv = cv2.bitwise_not(f_mask)

        img1_bg = cv2.bitwise_and(out,out,mask = mask_inv)

        return img1_bg


    @staticmethod
    def highpass(frame_mask, frame, hp):
        hp = int(hp)

        if(hp >= 1):
            blur = 10
            if blur % 2 == 0:
                blur += 1
            f2 = cv2.GaussianBlur(frame, (blur, blur), 0)


            lap = cv2.Laplacian(f2, ddepth=cv2.CV_16S, ksize=5, scale=1)
            lap = cv2.convertScaleAbs( lap );



            blur = 5
            if blur % 2 == 0:
                blur += 1
            lap = cv2.GaussianBlur(lap, (blur, blur), 0)



            frame_yuv = cv2.cvtColor(lap, cv2.COLOR_BGR2YUV)


            frame_mask_lap = cv2.inRange(frame_yuv, np.array([0,0,hp]), np.array([360,255,255]))
            f_mask = cv2.bitwise_and(frame_mask, frame_mask_lap)


            return f_mask

        return frame_mask


    # mouse callback function
    def mouse_call(self, event,x,y,flags,param):
        #global ix,iy,drawing,mode
        consol.log('param', param, 'Find YUV')

        if event == cv2.EVENT_LBUTTONDOWN:
            consol.log_time('Find YUV', 'mouse click')

            frame_yuv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2YUV)



            col = self.get_pixel_col(x, y)


            # fliped on purpose
            yuv = frame_yuv[y][x]
            consol.log('pixel color (yuv)', yuv, 'Find YUV')

            yuv_delta = np.array([15, 50, 50])


            yuv_min = yuv - yuv_delta
            yuv_max = yuv + yuv_delta

            consol.log('max (yuv)', yuv_max, 'Find YUV')
            consol.log('min (yuv)', yuv_min, 'Find YUV')


            self.set_slider(yuv_min, yuv_max)




            consol.log('pixel color', col, 'Find YUV')
            consol.log('pixel xy', [x, y], 'Find YUV')
            consol.log('frame size', [len(self.frame[0]), len(self.frame)], 'Find YUV')


    def set_slider(self, yuv_min, yuv_max):
        setTrackbarPos = lambda setting, pos: cv2.setTrackbarPos(setting, self.maskWindowName, pos)
        color_Vs = {}

        setTrackbarPos('Lower threshold for brightness', yuv_min[0])
        setTrackbarPos('Lower threshold for color U', yuv_min[1])
        setTrackbarPos('Lower threshold for color V', yuv_min[2])

        setTrackbarPos('Upper threshold for brightness', yuv_max[0])
        setTrackbarPos('Upper threshold for color U', yuv_max[1])
        setTrackbarPos('Upper threshold for color V', yuv_max[2])


    def get_pixel_col(self, x, y):
        if self.frame != None:
            return self.frame[y][x]
        else:
            return np.array([0.0,0,0])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pitch", help="[0] Main pitch, [1] Secondary pitch")
    parser.add_argument("color", help="The color to adjust")
    args = parser.parse_args()

    pitch_number = int(args.pitch)
           
    subprocess.call("vision/xawtv.sh")

    # Initialize calibration window
    calibration = tools.get_colors(pitch_number)
    calibration_gui = CalibrationGUI(calibration)
    calibration_gui.change_color(args.color)

    print "Color JSON"
    print calibration[args.color]

    # Initializecamera
    cam = vision.Camera(pitch=pitch_number)

    while(True):
        # capture frame by frame
        frame = cam.get_frame()

        # TODO TESTING/IDEA - For green dots, plates, and blue dots, use a HSV normalised frame.
        # if (args.color == "blue" or args.color == "green" or args.color == "bright_green" or args.color == "plate"):
        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #     frame[:, :, 1] = cv2.equalizeHist(frame[:, :, 1])
        #     frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)

        # Display the resulting frame
        calibration_gui.show(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('s'):
            tools.save_colors(pitch_number, calibration)
            print "Calibration saved."
            break

    # When everything is doen, release the capture
    cam.capture.release()
    cv2.destroyAllWindows()
