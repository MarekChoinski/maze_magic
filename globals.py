import cv2
import numpy as np


cap = cv2.VideoCapture(0)


path = []
_, frame1 = cap.read()
main_mask=  np.zeros((len(frame1), len(frame1[0]), 3), np.uint8)
main_circles=  np.zeros((len(frame1), len(frame1[0]), 3), np.uint8)

running = True


del cap