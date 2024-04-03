import KeyBoard
import cv2
import numpy as np

from djitellopy import tello
from time import sleep

def Color_Detection(image):
    # Set color hsv values
    b_l_threhold = (100, 100, 100)
    b_h_threhold = (150, 255, 255)
    g_l_threhold = (30, 80, 80)
    g_h_threhold = (90, 255, 255)
    r_l_threhold = (-30, 100, 100)
    r_h_threhold = (30, 255, 255)
    frame = image

    # Convert color BGR to HSV
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Making HSV mask
    g_mask = cv2.inRange(hsv_img, g_l_threhold, g_h_threhold)
    b_mask = cv2.inRange(hsv_img, b_l_threhold, b_h_threhold)
    r_mask = cv2.inRange(hsv_img, r_l_threhold, r_h_threhold)

    # Each image covered mask
    blue_img = cv2.bitwise_and(frame, frame, mask=b_mask)
    green_img = cv2.bitwise_and(frame, frame, mask=g_mask)
    red_img = cv2.bitwise_and(frame, frame, mask=r_mask)

    print('blue frame values : {}'.format(np.average(blue_img)))
    print('green frame values : {}'.format(np.average(green_img)))
    print('red frame values : {}\n'.format(np.average(red_img)))

    # 각 이미지 마다 평균값이 10이상이면 색상 감지 한 것으로 간주
    bgr_img = []
    bgr_img.append(np.average(blue_img) if np.average(blue_img) >= 10 else 0)
    bgr_img.append(np.average(green_img) if np.average(green_img) >= 10 else 0)
    bgr_img.append(np.average(red_img) if np.average(red_img) >= 10 else 0)

    if max(bgr_img) != 0:
        if bgr_img.index(max(bgr_img)) == 0: # Detecting Blue and Flip right
            drone.flip_right()
            print('find blue\n\n')
        elif bgr_img.index(max(bgr_img)) == 1: # Detecting Greed and Flip back
            drone.flip_back()
            print('find green\n\n')
        elif bgr_img.index(max(bgr_img)) == 2: # Detecting Red and Flip left
            drone.flip_left()
            print('find re;d\n\n')

    cv2.imshow('FRAME', frame)
    cv2.waitKey(1000)

def getInput():
    left_right, front_back, up_down, clock_counter = 0, 0, 0, 0

    if KeyBoard.getKey('1'): front_back = 100    # 전진 속도 100
    if KeyBoard.getKey('q'): front_back = 50    # 전진 속도 50
    if KeyBoard.getKey('w'): front_back = 30    # 전진 속도 30
    if KeyBoard.getKey('e'): front_back = 15    # 전진 속도 15
    if KeyBoard.getKey('a'): left_right = -25   # 왼쪽 속도 30
    if KeyBoard.getKey('z'): left_right = -15   # 왼쪽 속도 15
    if KeyBoard.getKey('s'): front_back = -30   # 후진
    if KeyBoard.getKey('d'): left_right = 25    # 오른쪽 속도 30
    if KeyBoard.getKey('c'): left_right = 15    # 오른쪽 속도 15

    if KeyBoard.getKey('u'): up_down = 30       # 상승
    if KeyBoard.getKey('i'): up_down = -25      # 하강
    if KeyBoard.getKey('h'): clock_counter = -50# 반시계
    if KeyBoard.getKey('j'): clock_counter = 50 # 시계

    if KeyBoard.getKey('o'): drone.takeoff()    # 이륙
    if KeyBoard.getKey('p'): drone.land()       # 착륙

    return [left_right, front_back, up_down, clock_counter]

def video_stream():
    image = drone.get_frame_read().frame
    image = cv2.resize(image, (360, 240))
    cv2.imshow('Image', image)
    cv2.waitKey(50)

if __name__ == '__main__':
    drone = tello.Tello()

    drone.connect()     # Connecting drone as Wifi [Tello]
    print(drone.get_battery())

    KeyBoard.init()     # Setting Keyboard at Pygame
    drone.streamon()    # Turn on video at Drone

    mode = 0 # 0이면 일반 모드 1이면 color detection 모드

    while True:
        if KeyBoard.getKey('m'): mode = 0
        if KeyBoard.getKey('n'): mode = 1

        if mode == 0:
            video_stream()
        elif mode == 1:
            image = drone.get_frame_read().frame
            image = cv2.resize(image, (360, 240))
            Color_Detection(image)
            mode = 0

        results = getInput()
        drone.send_rc_control(results[0], results[1], results[2], results[3])
        # sleep(1)
