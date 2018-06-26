import cv2


cap = cv2.VideoCapture(0)


path = []
_, frame1 = cap.read()
#print(frame1)

running = True


del cap
