import tools
import numpy as np
import cv2

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




cap = cv2.VideoCapture(0)
sides = cv2.imread('sides.png', 0)
og = cv2.imread('currBg_1.png')
og = fix_radial_distortion(og)
og = fix_perspective(og)
og = cv2.GaussianBlur(og,(3,3),0)
og = cv2.cvtColor(og,cv2.COLOR_BGR2YUV)


while(cap.isOpened()):
    time = tools.current_milli_time()

    ret, frame = cap.read()


    frame = fix_radial_distortion(frame)
    frame = fix_perspective(frame)
    frame = cv2.GaussianBlur(frame,(3,3),0)
    yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
    yuv = cv2.absdiff(yuv, og)
    cv2.imshow('', yuv)
    #yuv[:,:,1] = cv2.equalizeHist(yuv[:,:,1])

    ################## GRAY colorspace compresses, thus,  the loss of info may help
    yuv = cv2.cvtColor(yuv,cv2.COLOR_BGR2GRAY )
    mask = cv2.inRange(yuv, 14, 255) ################# variable - increase if extra bits, decrease otherwise
	##################
    #mask = cv2.inRange(yuv, (0,8,0), (255,255,255))
    ##################

    ################ not sure this is the best place
    # removes the side ares that are outide the pitch
    mask = cv2.bitwise_and(mask, mask, mask=sides)
    ################

    ###############
    #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)), iterations=3)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)), iterations=1)
    #mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)), iterations = 3)
    ################
    mask = cv2.GaussianBlur(mask,(11,11),0) ############## variable 15,15, 5
    retval,mask = cv2.threshold(mask,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mask = cv2.GaussianBlur(mask,(19,19), 0) ############## variable 5,5,2
    cv2.imshow('fga', mask)
    #cv2.imshow('post threshold', mask)
    objects = cv2.bitwise_and(frame, frame, mask=mask)
    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        (x,y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(objects,center,radius,(61, 245, 255),2)


    time = ((tools.current_milli_time()-time))/1000.0
    fps = 1.0 / time
    cv2.putText(objects, "FPS: "+str(round(fps)), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
    cv2.imshow('feed', frame)
    cv2.imshow('objects',objects)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
