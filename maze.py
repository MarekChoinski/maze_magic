import cv2
import numpy as np
from time import sleep
import copy
import solver

import globals

import threading


class Maze:
    __lower_green = np.array([40, 100, 85])
    __upper_green = np.array([75, 255, 255])

    __kernel = np.ones((3, 3), np.uint8)


    def __init__(self, cap, title):

        _,self.__frame = cap.read()

        self.__maze_mask = np.zeros((len(self.__frame), len(self.__frame[0]), 3), np.uint8)
        self.__circles = np.zeros((len(self.__frame), len(self.__frame[0]), 3), np.uint8)
        self.__blank_image = np.zeros((len(self.__frame), len(self.__frame[0]), 3), np.uint8)

        self.__thread_running = True

        maze_calculation_thread = threading.Thread(target=self.__maze_calculation)
        draw_end_circles_thread = threading.Thread(target=self.__show_end_points)

        maze_calculation_thread.start()
        draw_end_circles_thread.start()

        while True:

            _, self.__frame = cap.read()

            actual_frame = self.__frame

            # frame = show_end_points(globals.frame1)

            actual_frame = cv2.addWeighted(actual_frame, 1, self.__maze_mask, 0.5, 0)
            actual_frame = cv2.addWeighted(actual_frame, 1, self.__circles, 0.3, 0)

            cv2.imshow(title, actual_frame)

            k = cv2.waitKey(5) & 0xFF
            if k == ord('q'):
                self.__thread_running = False
                maze_calculation_thread.join()
                draw_end_circles_thread.join()
                cv2.destroyAllWindows()
                break

    def __mask_to_text(self, mask):
        result = [['x' for x in range(len(mask[0]))] for y in range(len(mask))]

        for row_num, row in enumerate(mask):
            for pixel_num, pixel in enumerate(row):
                if pixel > 250:
                    result[row_num][pixel_num] = '#'
                else:
                    result[row_num][pixel_num] = ' '

        return result

    def __show_end_points(self):
        while self.__thread_running:

            # save normal frame
            frame = copy.copy(self.__frame)

            # convert color scale to HSV
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(frame, self.__lower_green, self.__upper_green)

            # dilate for better effect
            mask = cv2.dilate(mask, self.__kernel, iterations=2)

            positions = self.__position_of_end_points(mask)

            if len(positions) == 2:
                self.__circles = copy.copy(self.__blank_image)
                copy_frame = self.__circles
                cv2.circle(copy_frame, (positions[0][0], positions[0][1]), positions[0][2], (0, 255, 0), -1)
                cv2.circle(copy_frame, (positions[1][0], positions[1][1]), positions[1][2], (0, 255, 0), -1)

    # we should find position of end points
    # there could be a lot of green elements on frame
    # so we should find two the biggest
    # returns position of start and end and diameter of found point
    def __position_of_end_points(self, mask):
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

    def __draw_path_on_frame(self, path):
        blank_image = copy.copy(self.__blank_image)
        for p in path:
            blank_image[p[0]][p[1]] = (255, 255, 255)

        frame = blank_image

        return frame

    def __maze_calculation(self):
        print("a")
        while self.__thread_running:
            # take  e d g y  frames
            edges1 = cv2.Canny(self.__frame, 100, 200)

            # convert color scale to HSV
            copied_frame = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2HSV)

            # Threshold the HSV image to get only blue colors
            mask1 = cv2.inRange(copied_frame, self.__lower_green, self.__upper_green)

            # connect all pieces to one
            final_edges = edges1
            final_mask = mask1

            # dilate final pieces for better effect
            final_edges = cv2.dilate(final_edges, self.__kernel, iterations=1)
            final_mask = cv2.dilate(final_mask, self.__kernel, iterations=2)

            final_maze_masked = final_edges - final_mask

            positions = self.__position_of_end_points(mask1)

            if len(positions) == 2:
                labirynth = self.__mask_to_text(final_maze_masked)
                path = solver.solve(labirynth, positions[0], positions[1])
                self.__maze_mask = self.__draw_path_on_frame(path)

