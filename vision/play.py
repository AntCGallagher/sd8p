import tools
import numpy as np
import cv2
import pandas as pd

def fix_perspective(frame):
    rows,cols,nfn = frame.shape

    pts  = tools.get_perspective(1)
    pts1 = np.float32([pts[0],pts[1],pts[2],pts[3]])
    pts2 = np.float32([(0,0),(cols,0),(cols, rows),(0,rows)])

    M   = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(frame,M,(cols,rows))

    return dst

def fix_radial_distortion(frame):
    a=tools.get_radial_data()
    return cv2.undistort(
        frame, a['camera_matrix'], a['dist'], None, a['new_camera_matrix'])




cap = cv2.VideoCapture('output.avi')

og = cv2.imread('1_9x6.jpeg')
og = fix_radial_distortion(og)
og = fix_perspective(og)
og = cv2.cvtColor(og,cv2.COLOR_BGR2YUV)

while(cap.isOpened()):
    ret, frame = cap.read()
    frame = fix_radial_distortion(frame)
    frame = fix_perspective(frame)
    yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)

    cv2.absdiff(yuv, og, yuv)
    yuv = cv2.cvtColor(yuv,cv2.COLOR_BGR2GRAY)
    yuv = cv2.inRange(yuv, 17, 255) #################variable - increase if extra bits, decrease otherwise
    #yuv = cv2.inRange(yuv, (9,11,7), (255,255,255))
    yuv = cv2.GaussianBlur(yuv,(15,15),5)
    ret3,th3 = cv2.threshold(yuv,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    th3 = cv2.GaussianBlur(th3,(11,11), 2)
    frame = cv2.bitwise_and(frame, frame, mask=th3)
    _, contours, _ = cv2.findContours(th3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],0,(0,0,255),2)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
