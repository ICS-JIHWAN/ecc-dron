import numpy as np
import cv2

# image load
img = cv2.imread('./video/frame_image/snapshot_17.jpg', 1)
cv2.imshow('color', img)
cv2.waitKey(0)

# convert gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)
cv2.waitKey(0)

# dividing object and background from image
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cv2.imshow('thresh', thresh)
cv2.waitKey(0)

# object 가 있을 수 있는 background region 을 추출
# opening -> noise removal
# dilate -> 팽창(dilate) 연산
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
sure_bg = cv2.dilate(opening, kernel, iterations=3)

cv2.imshow('sure_bg', sure_bg)
cv2.waitKey(0)

cv2.destroyAllWindows()

dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
result_dist_transform = cv2.normalize(dist_transform, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8UC1)
ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, cv2.THRESH_BINARY)

cv2.imshow('dist_transform', result_dist_transform)
cv2.waitKey(0)
cv2.imshow('sure_fg', sure_fg)
cv2.waitKey(0)

sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)

ret, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0

markers = cv2.watershed(img, markers)

img[markers == -1] = [255, 0, 0]
img[markers == 1] = [255, 255, 0]