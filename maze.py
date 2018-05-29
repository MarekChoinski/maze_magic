import cv2
import numpy as np
from time import sleep

cap = cv2.VideoCapture(0)


def mask_to_text(mask):

    result = [[None] * len(mask[0])] * len(mask)

    for row_num, row in enumerate(mask):
        for pixel_num, pixel in enumerate(row):
            if pixel == 0:
                result[row_num][pixel_num] = ' '
            else:
                result[row_num][pixel_num] = '#'

    return result
    
    
def find_largest_groups_in_mask(mask):
    pass

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

    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    hsv3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([40,100,85])
    upper_blue = np.array([75,255,255])

    # Threshold the HSV image to get only blue colors
    mask1 = cv2.inRange(hsv1, lower_blue, upper_blue)
    mask2 = cv2.inRange(hsv2, lower_blue, upper_blue)
    mask3 = cv2.inRange(hsv3, lower_blue, upper_blue)

    final_edges = edges1 + edges2 + edges3
    kernel = np.ones((3,3),np.uint8)

    final_mask = mask1 + mask2 + mask3
    final_mask = cv2.dilate(final_mask,kernel,iterations = 1)

    final_maze_masked = final_edges - final_mask
    

    final_maze_masked = cv2.dilate(final_maze_masked, kernel, iterations = 1)
    cv2.imshow('edges_masked', final_maze_masked)
    cv2.imshow('mask', final_mask)
    cv2.waitKey(0)


if __name__ == '__main__':
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


