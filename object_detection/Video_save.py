import cv2
import KeyBoard

from djitellopy import tello
from time import sleep

video_file = './video/hard_board_paper_long_distance111111.mp4'  # Save file path & file name

fps = 1.00      # frame of seconds --> drone camera frame 이랑 video frame 이 동일 하게 나와야 함
"""
Fourcc : 4-문자 코드 -> 동영상 파일의 코덱, 압축 방식, 색상, 픽셀 포맷
*'DIVX' | *'XVID' | *'FMP4' | *'X264' | *'MJPG'
"""
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

out = cv2.VideoWriter(video_file, fourcc, fps, (360, 240)) # Creating and opening video file

drone = tello.Tello()
drone.connect()

KeyBoard.init()  # Setting Keyboard at Pygame
drone.streamon()

while True:
    if drone.stream_on:
        image = drone.get_frame_read().frame
        image = cv2.resize(image, (360, 240))
        cv2.imshow('Image', image)
        out.write(image)
        cv2.waitKey(1)
    else:
        print('stream off !!!')
        out.release()
        cv2.destroyAllWindows()
        break

    if KeyBoard.getKey('q'): # press q from keyboard, display of all windows will be closed
        out.release()
        drone.streamoff()
        cv2.destroyAllWindows()
        break
    sleep(1)
