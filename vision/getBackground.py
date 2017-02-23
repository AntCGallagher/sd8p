import cv2
from vision import Camera

camera = Camera(pitch=0)
frame = camera.get_frame()
cv2.imwrite("/SDP/sd8p/vision/currBg.jpeg", frame)
print "done"