import cv2
import numpy as np
from time import sleep
import copy
import solver

import globals

import threading


# Define range of green color in HSV
lower_green = np.array([40, 100, 85])
upper_green = np.array([75, 255, 255])

kernel = np.ones((3, 3), np.uint8)



def mask_to_text(mask):
    result = [['x' for x in range(len(mask[0]))] for y in range(len(mask))]

    for row_num, row in enumerate(mask):
        for pixel_num, pixel in enumerate(row):
            if pixel > 250:
                result[row_num][pixel_num] = '#'
            else:
                result[row_num][pixel_num] = ' '

    return result


def show_end_points():
    while globals.running:



        # save normal frame
        frame = copy.copy(globals.frame1)
        original_frame = frame

        # convert color scale to HSV
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(frame, lower_green, upper_green)

        # dilate for better effect
        mask = cv2.dilate(mask, kernel, iterations=2)

        positions = position_of_end_points(mask)

        if len(positions) == 2:
            globals.main_circles = np.zeros((len(globals.frame1), len(globals.frame1[0]), 3), np.uint8)
            copy_frame = globals.main_circles#copy.copy(original_frame)
            cv2.circle(copy_frame, (positions[0][0], positions[0][1]), positions[0][2], (0, 255, 0), -1)
            cv2.circle(copy_frame, (positions[1][0], positions[1][1]), positions[1][2], (0, 255, 0), -1)



# we should find position of end points
# there could be a lot of green elements on frame
# so we should find two the biggest
# returns position of start and end and diameter of found point
def position_of_end_points(mask):
    # idk
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    # idk
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    positions = []

    if len(contours) >= 2:
        sorted_contours = sorted(contours, key=cv2.contourArea)

        # find the biggest area point
        x, y, w, h = cv2.boundingRect(sorted_contours[-2])
        positions.append((int(round(x + (w / 2))), int(round(y + (h / 2))), int(round(max(w, h)))))
        x, y, w, h = cv2.boundingRect(sorted_contours[-1])
        positions.append((int(round(x + (w / 2))), int(round(y + (h / 2))), int(round(max(w, h)))))

    return positions


def draw_path_on_frame():
    blank_image = np.zeros((len(globals.frame1), len(globals.frame1[0]), 3), np.uint8)
    for p in globals.path:
        blank_image[p[0]][p[1]] = (255, 255, 255)

    frame = blank_image

    return frame


def maze_calculation_loop():

    while globals.running:
        # take  e d g y  frames
        edges1 = cv2.Canny(globals.frame1, 100, 200)

        # convert color scale to HSV
        copied_frame = cv2.cvtColor(globals.frame1, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only blue colors
        mask1 = cv2.inRange(copied_frame, lower_green, upper_green)

        # connect all pieces to one
        final_edges = edges1
        final_mask = mask1

        # dilate final pieces for better effect
        final_edges = cv2.dilate(final_edges, kernel, iterations=1)
        final_mask = cv2.dilate(final_mask, kernel, iterations=2)

        final_maze_masked = final_edges - final_mask

        positions = position_of_end_points(mask1)

        if len(positions) == 2:
            labirynth = mask_to_text(final_maze_masked)
            globals.path = solver.solve(labirynth, positions[0], positions[1])
            globals.main_mask = draw_path_on_frame()


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)

    t1 = threading.Thread(target=maze_calculation_loop)
    t1.start()

    t2 = threading.Thread(target=show_end_points)
    t2.start()



    while True:

        _, globals.frame1 = cap.read()

        frame = globals.frame1

        #frame = show_end_points(globals.frame1)


        frame = cv2.addWeighted(frame, 1, globals.main_mask, 0.5, 0)
        frame = cv2.addWeighted(frame, 1, globals.main_circles, 0.3, 0)


        cv2.imshow('stuff', frame)

        k = cv2.waitKey(5) & 0xFF
        if k == ord('q'):
            globals.running = False
            t1.join()
            cv2.destroyAllWindows()
            break
