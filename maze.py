import cv2
import numpy as np
from time import sleep

cap = cv2.VideoCapture(0)


def mazeMagic():
    _, frame1 = cap.read()
    sleep(0.2)
    _, frame2 = cap.read()
    sleep(0.2)
    _, frame3 = cap.read()
    sleep(0.2)


    edges1 = cv2.Canny(frame1,100,200)
    edges2 = cv2.Canny(frame2,100,200)
    edges3 = cv2.Canny(frame3,100,200)
    
    final_edges = edges1 + edges2 + edges3

    kernel = np.ones((3,3),np.uint8)
    fat_edges = cv2.dilate(final_edges,kernel,iterations = 1)
    '''
    for row in final_edges:
        for pixel in row:
            if pixel == 0:
                print(' ', end="")
            else:
                print('#', end="")
        print('')
    '''
    cv2.imshow('me', frame1)
    cv2.imshow('before', final_edges)
    cv2.imshow('after', fat_edges)
    cv2.waitKey(0)
while(1):

    # Take each frame
    _, frame = cap.read()
    
    #frame/=2.0

    # edges detection - used to extract the maze shape
    edges = cv2.Canny(frame,100,200)



    cv2.imshow('frame',frame)
    cv2.imshow('edges',edges)

    
    k = cv2.waitKey(5) & 0xFF
    if k == 113:
        cv2.destroyAllWindows()
        break
    elif k == 116:
        cv2.destroyAllWindows()
        mazeMagic()
        break


