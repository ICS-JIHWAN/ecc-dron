import cv2, random
from matplotlib import pyplot as plt

mode = [cv2.RETR_EXTERNAL, cv2.RETR_LIST, cv2.RETR_CCOMP, cv2.RETR_TREE]

def show_image(img):
    b, g, r = cv2.split(img)
    plt.imshow(cv2.merge([r, g, b]))
    plt.show()

def setLabel(img, pts, label):
    (x, y, w, h) = cv2.boundingRect(pts)
    pt1 = (x, y)
    pt2 = (x + w, y + h)
    cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
    cv2.putText(img, label, (pt1[0], pt1[1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))


img_path = '../video/frame_image2/frame29.jpg'

color_img = cv2.imread(img_path)
show_image(color_img)

gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

sobel = cv2.Sobel(gray_img, cv2.CV_8U, 1, 0, 3)
laplacian = cv2.Laplacian(gray_img, cv2.CV_8U, ksize=5)
canny = cv2.Canny(color_img, 100, 255)

cv2.imshow("sobel", sobel)
cv2.imshow("laplacian", laplacian)
cv2.imshow("canny", canny)
cv2.waitKey(0)
cv2.destroyAllWindows()

ret, thr = cv2.threshold(canny, 125, 255, cv2.THRESH_OTSU)
contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(color_img, contours, 3, (0, 255, 0), )

for cont in contours:
    approx = cv2.approxPolyDP(cont, cv2.arcLength(cont, True) * 0.02, True)
    vtc = len(approx)

    if vtc == 4:
        setLabel(color_img, cont, 'Rec')
        cv2.imshow('d', color_img)
        cv2.waitKey(0)
        print('find_rectangle')
cv2.destroyAllWindows()