import cv2
from vision import Camera

capture = Camera(pitch=0)

while True:

        frame = capture.get_frame()

        cv2.imwrite("vision/currBg.jpeg", frame)

        cv2.imshow('Tracker', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

print "done"
