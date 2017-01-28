
import cv2
import numpy as np
import tools
from colors import BGR_COMMON
from findHSV import CalibrationGUI


# For OpenCV2 image display
WINDOW_NAME = 'Tracker' 

class MyTracker(object):

    def __init__(self, colors, calibration):
        self.colors = colors
        self.calibration = calibration
        self.time = tools.current_milli_time()

    def track_points(self, image, draw=True):

        '''Accepts BGR image as Numpy array
           Returns: Disctionary of color => list of tuples
                    positions of color centroids
        '''

        # for processing speed check
        #self.time = tools.current_milli_time()

        # reset point dictionary
        points = {}
        # For each color make a mask and detect objects

        for color in self.colors:
    
            BLUR_VALUE      = self.calibration[color]['blur'] 
            MIN_VALUE       = self.calibration[color]['min']
            MAX_VALUE       = self.calibration[color]['max']
            CONTRAST_VALUE  = self.calibration[color]['contrast']
            OPEN_KERNEL      = (int)(self.calibration[color]['open_kernel'])
            CLOSE_KERNEL     = (int)(self.calibration[color]['close_kernel'])
            ERODE_KERNEL     = (int)(self.calibration[color]['erode'])
            HIGHPASS_VALUE  = self.calibration[color]['highpass']
            OBJECT_COUNT    = (int)(self.calibration[color]['object_count'])

            # initial frame mask
            frame = image

            blur = BLUR_VALUE
            if blur >= 1:
                if blur % 2 == 0:
                    blur += 1
                frame = cv2.GaussianBlur(frame, (blur, blur), 0)



            contrast = CONTRAST_VALUE
            if contrast >= 1.0:
                frame = cv2.add(frame, np.array([contrast]))

            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            min_color = MIN_VALUE
            max_color = MAX_VALUE
            frame_mask = cv2.inRange(frame_hsv, min_color, max_color)

            if OPEN_KERNEL >= 1:
                    k = OPEN_KERNEL
                    kernel = np.ones((k,k ),np.uint8)
                    frame_mask = cv2.morphologyEx(frame_mask,
                                                  cv2.MORPH_OPEN,
                                                  kernel,
                                                  iterations=1)
            if CLOSE_KERNEL >= 1:
                    k = CLOSE_KERNEL
                    kernel = np.ones((k,k ),np.uint8)
                    frame_mask = cv2.morphologyEx(frame_mask,
                                                  cv2.MORPH_CLOSE,
                                                  kernel,
                                                  iterations=1)
            if ERODE_KERNEL >= 1:
                    k = ERODE_KERNEL
                    kernel = np.ones((k,k ),np.uint8)
                    frame_mask = cv2.erode(frame_mask,
                                            kernel,
                                            iterations=1)

            out = frame
            hp = int(HIGHPASS_VALUE)
            frame_mask = CalibrationGUI.highpass(frame_mask, frame, hp)
            #cv2.imshow('frame mask'+str(color),frame_mask)

            
            # Detect multiple centroids
            _, contours0, _ = cv2.findContours( frame_mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            sorted_countours = sorted(contours0, key=lambda cnt: cv2.contourArea(cnt))
            largest_contours = sorted_countours[-OBJECT_COUNT:]      # Select OBJECT_COUNT largest contours
            #print color
            #print sorted_countours
            moments  = [cv2.moments(cnt) for cnt in largest_contours]
            # Nota Bene: I rounded the centroids to integer.
            centroids = [( int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ) for m in moments if m['m00'] != 0.0]

            cv2.drawContours(image, sorted_countours, -1, (0,0,0), 1) # for debuging centroids 

            # point data collection 
            color_points = []

            for c in centroids:
                # I draw a black little empty circle in the centroid position
                if draw:
                    #font = cv2.FONT_HERSHEY_SIMPLEX
                    #cv2.putText(image,str(c),c, font, 0.4,(0,0,0),1,cv2.LINE_AA)
                    cv2.circle(image,c,4,(0,0,0))
                    cv2.circle(image,c,5,BGR_COMMON[color])
                    cv2.circle(image,c,6,(0,0,0))

                # Add color points
                color_points.append(c)

            points[color] = color_points

        # Pring processing speed
        #print('Tracking delay: '+str(tools.current_milli_time()-self.time))

        # add points to dictionary by color
        return points

# Test tracking objects of certain color
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pitch", help="[0] Main pitch, [1] Secondary pitch")
   # parser.add_argument("color", help="The color to adjust")
    args = parser.parse_args()

    pitch_number = int(args.pitch)

    capture = vision.Camera(pitch=pitch_number)
    calibration = tools.get_colors(pitch_number)
    tracker = MyTracker(colors=['red', 'blue', 'bright_green','pink','yellow'], calibration=calibration)

    while True:

        frame = capture.get_frame()

        #tracker.adjust_color(image)
        tracker.track_points(frame)

        cv2.imshow('Tracker', frame)
      
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()