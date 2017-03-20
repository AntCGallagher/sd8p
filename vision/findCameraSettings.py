import cv2
import numpy as np
import consol
import tracker
import tracker

import vision
import tools

CONTROL = ["Brightness",
           "Contrast",
           "Saturation",
           "Hue"]

MAXBAR = {"Brightness":100,
          "Contrast":100,
          "Saturation":100,
          "Hue":100
        }

INDEX = {"Brightness":50,
         "Contrast":50,
         "Saturation":50,
         "Hue":50
        }

def nothing(x):
    pass

class CameraCalibrationGUI(object):
    """
    This class caters for the setting of camera settings
    """
    def __init__(self, calibration, name="Camera calibration"):

        consol.log('set camera settings so that all objects are detected', None)

        self.calibration        = calibration
        self.frameWindowName    = name
        self.frame              = None
        self.setting            = 'camera'

        self.setWindow()

    def setWindow(self):

        cv2.namedWindow(self.frameWindowName)

        createTrackbar = lambda setting, \
                                value: \
                                    cv2.createTrackbar(
                                        setting,
                                        self.frameWindowName,
                                        int(value),
                                        MAXBAR[setting], nothing)

        createTrackbar('Brightness',
                       self.calibration[self.setting]['brightness'])
        createTrackbar('Contrast',
                       self.calibration[self.setting]['contrast'])
        createTrackbar('Saturation',
                       self.calibration[self.setting]['saturation'])
        createTrackbar('Hue',
                       self.calibration[self.setting]['hue'])

    def update(self):

        getTrackbarPos = lambda setting: cv2.getTrackbarPos(setting, self.frameWindowName)

        values = {}
        for setting in CONTROL:
            values[setting] = float(getTrackbarPos(setting))

        self.calibration[self.setting]['brightness']  = values['Brightness']
        self.calibration[self.setting]['contrast']    = values['Contrast']
        self.calibration[self.setting]['saturation']  = values['Saturation']
        self.calibration[self.setting]['hue']         = values['Hue']

    def getSettings(self):
        return self.calibration[self.setting]



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pitch", help="[0] Main pitch, [1] Secondary pitch")
    args = parser.parse_args()

    pitch_number = int(args.pitch)

    # Initialize calibration window
    colors          = ['red', 'blue', 'bright_green','pink','yellow']
    calibration     = tools.get_colors(pitch=pitch_number)

    print calibration['yellow']

    # Initializecamera
    cam = vision.Camera(pitch=pitch_number)

    auto_brightness = True
    settings        = calibration['camera']
    desired         = 50

    while(auto_brightness):
        print "Getting best brightness"
        best_brightness = 0;
        best_distance   = 100;


        for test_brightness in range(100):

            settings['brightness']  = test_brightness

            # Update camera settings
            cam.reset_camera_settings(settings=settings)

            gray_frame = cv2.cvtColor(cam.get_frame(), cv2.COLOR_BGR2GRAY)

            median = np.median(gray_frame)

            # get distance from desired brightness
            distance = abs(desired - median)

            # check if test_brightness is a better walue
            if distance < best_distance:
                best_distance   = distance
                best_brightness = test_brightness

        print "Best brightness: "+str(best_brightness)
        settings['brightness']  = best_brightness
        auto_brightness = False


    auto_contrast   = False
    desired         = 50

    while(auto_contrast):
        print "Getting best brightness"
        best_contrast   = 0;
        best_distance   = 100;


        for test_contrast in range(100):

            settings['contrast']  = test_contrast

            # Update camera settings
            cam.reset_camera_settings(settings=settings)

            gray_frame = cv2.cvtColor(cam.get_frame(), cv2.COLOR_BGR2GRAY)

            std = np.std(gray_frame)

            # get distance from desired brightness
            distance = abs(desired - std)

            # check if test_brightness is a better walue
            if distance < best_distance:
                best_distance = distance
                best_contrast = test_contrast

        print "Best contrast: "+str(best_contrast)
        settings['contrast']  = best_contrast
        auto_contrast = False

    calibration['camera'] = settings

    #tracker         = my_tracker.MyTracker(colors=colors, calibration=calibration)
    tracker         = tracker.MyTracker(calibration=calibration)

    GUI_name        = "Camera calibration"
    calibration_gui = CameraCalibrationGUI(calibration=calibration, name=GUI_name)

    while(True):

        if auto_brightness:
            calibration_gui.auto_brightness_calibration(cam.get_frame(), desired=50)
            auto_brightness = False

        # Update trackbars
        calibration_gui.update()

        # get updated camera settings
        settings = calibration_gui.getSettings()

        # Update camera settings
        cam.reset_camera_settings(settings=settings)

        # capture frame by frame
        frame = cam.get_frame()

        # show tracking info
        data, modified_frame = tracker.get_world_state(frame)

        cv2.imshow(GUI_name, modified_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('s'):
            tools.save_colors(pitch_number, calibration)
            print "Calibration saved."
            break

    # When everything is doen, release the capture
    cam.capture.release()
    cv2.destroyAllWindows()
