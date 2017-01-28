
setWindow()

def setWindow():

cv2.namedWindow("test frame")

createTrackbar = lambda setting, \
                        value: \
                            cv2.createTrackbar(
                                setting,
                                "test frame",
                                int(value),
                                255, self.nothing)

createTrackbar('min', 1)
createTrackbar('max', 100)

def nothing(x):
return


########################################

getTrackbarPos = lambda setting: cv2.getTrackbarPos(setting, "test frame")

alpha = getTrackbarPos('min')
beta = getTrackbarPos('max')

#print alpha, beta

#test_frame = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
#gray_frame = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
#cv2.normalize(src=frame, dst=test_frame, alpha=alpha, beta=beta, norm_type=cv2.NORM_MINMAX)

lab_image = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV)
channels = cv2.split(lab_image)

clahe = cv2.createCLAHE();
clahe.setClipLimit(alpha);

h_chan = channels[0].copy()
s_chan = channels[1].copy()
v_chan = channels[2].copy()


#test_chan = channels[0].copy()
#clahe.apply(channels[0], test_chan)

#clahe.apply(channels[0], h_chan)
clahe.apply(channels[1], s_chan)
clahe.apply(channels[2], v_chan)

#channels[0] = test_chan.copy()
#cv2.merge(channels, lab_image)

#channels[0] = h_chan.copy()
channels[1] = s_chan.copy()
channels[2] = v_chan.copy()
cv2.merge(channels, lab_image)

result_image = cv2.cvtColor(lab_image, cv2.COLOR_HSV2BGR)


cv2.imshow("test frame", result_image)
########################################