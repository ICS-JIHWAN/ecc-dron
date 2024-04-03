import numpy as np
import cv2

def Color_Detection(image):
    b_l_threhold = (100, 100, 100)
    b_h_threhold = (150, 255, 255)
    g_l_threhold = (30, 80, 80)
    g_h_threhold = (90, 255, 255)
    r_l_threhold = (-30, 100, 100)
    r_h_threhold = (30, 255, 255)
    ret, frame = cap.read()

    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    g_mask = cv2.inRange(hsv_img, g_l_threhold, g_h_threhold)
    b_mask = cv2.inRange(hsv_img, b_l_threhold, b_h_threhold)
    r_mask = cv2.inRange(hsv_img, r_l_threhold, r_h_threhold)

    blue_img = cv2.bitwise_and(frame, frame, mask=b_mask)
    green_img = cv2.bitwise_and(frame, frame, mask=g_mask)
    red_img = cv2.bitwise_and(frame, frame, mask=r_mask)

    print('blue frame values : {}'.format(np.average(blue_img)))
    print('green frame values : {}'.format(np.average(green_img)))
    print('red frame values : {}\n'.format(np.average(red_img)))

    bgr_img = []
    bgr_img.append(np.average(blue_img) if np.average(blue_img) >= 10 else 0)
    bgr_img.append(np.average(green_img) if np.average(green_img) >= 10 else 0)
    bgr_img.append(np.average(red_img) if np.average(red_img) >= 10 else 0)

    if max(bgr_img) != 0:
        if bgr_img.index(max(bgr_img)) == 0: # blue
            print('find blue\n\n')
        elif bgr_img.index(max(bgr_img)) == 1: # green
            print('find green\n\n')
        elif bgr_img.index(max(bgr_img)) == 2: # red
            print('find red\n\n')

    cv2.imshow('FRAME', frame)
    cv2.imshow('BLUE', blue_img)
    cv2.imshow('GREEN', green_img)
    cv2.imshow('RED', red_img)
    cv2.waitKey(1000)

if __name__ == '__main__':
    # video load
    video_file = '../video/hard_board_paper_handing.mp4'  # Save file path & file name

    cap = cv2.VideoCapture(video_file)
    while cap.isOpened():
        Color_Detection(cap)
        if 0xff == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()
