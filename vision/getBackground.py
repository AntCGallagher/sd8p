import cv2
from vision import Camera
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("pitch", help="[0] Main pitch, [1] Secondary pitch")
args = parser.parse_args()
pitch_number = int(args.pitch)

capture = Camera(pitch=pitch_number)

while True:

        frame = capture.get_frame()

        cv2.imwrite("currBg_" + str(pitch_number) + ".png", frame)
        #cv2.imwrite("../currBg_" + str(pitch_number) + ".png", frame)

        cv2.imshow('Background view', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

print "done"
