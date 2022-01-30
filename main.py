import mediapipe as mp
import numpy as np
import math
import cv2
import datetime
import mouse
from win32api import GetSystemMetrics

screen_x = GetSystemMetrics(78)
screen_y = GetSystemMetrics(79)
print(screen_x, screen_y)
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

draw_cool_down = 1
stop_draw_cool_down = 0.2
drawing = False
draw_start = False
draw_stop = False


def distance(p1, p2):
    return math.sqrt(((p1.x - p2.x) ** 2) + ((p1.y - p2.y) ** 2))


cap = cv2.VideoCapture(1)
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            print(results.multi_hand_landmarks[0].landmark[4])
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if results.multi_hand_landmarks[0].landmark[4]:
                pos_x = results.multi_hand_landmarks[0].landmark[4].x * screen_x
                pos_y = results.multi_hand_landmarks[0].landmark[4].y * screen_y
                mouse.move(pos_x, pos_y, True)

            if distance(results.multi_hand_landmarks[0].landmark[8],
                        results.multi_hand_landmarks[0].landmark[4]) < 0.05:
                    mouse.press("left")
            else :
                mouse.release("left")

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()