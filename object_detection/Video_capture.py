import cv2
import os

dir_path = '../video/frame_image2'
video_path = '../video/hard_board_paper_handing.mp4'
cap = cv2.VideoCapture(video_path)

l = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print("length :", l)
print("width :", w)
print("height :", h)
print("fps :", fps)

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

count = 0

while (cap.isOpened()):
    ret, image = cap.read()  # 앞서 불러온 fps 값을 사용하여 1초마다 추출
    if ret:
        cv2.imwrite(dir_path + "/frame%d.jpg" % count, image)
        print('Saved frame number :', str(int(cap.get(1))))
        count += 1
    else:
        break
cap.release()