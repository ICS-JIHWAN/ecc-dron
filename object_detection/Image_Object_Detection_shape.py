import cv2
import numpy as np

def setLabel(img, pts, label):
    (x, y, w, h) = cv2.boundingRect(pts)
    pt1 = (x, y)
    pt2 = (x + w, y + h)
    cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
    cv2.putText(img, label, (pt1[0], pt1[1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))


img = cv2.imread('../video/frame_image/snapshot_7.jpg')

img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
channel = list(cv2.split(img_ycrcb))
channel[0] = cv2.equalizeHist(channel[0])
dst_ycrcb = cv2.merge(channel)
dst1 = cv2.cvtColor(dst_ycrcb, cv2.COLOR_YCrCb2BGR)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thr = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for cont in contours:
    approx = cv2.approxPolyDP(cont, cv2.arcLength(cont, True) * 0.02, True)
    vtc = len(approx)

    if vtc == 4:
        setLabel(img, cont, 'Rec')
        print('find_rectangle')

cv2.imshow('img', img)
cv2.imshow('binary', thr)

cv2.waitKey()
cv2.destroyAllWindows()