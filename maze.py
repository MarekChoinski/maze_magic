import cv2
import numpy as np
import copy
import solver

import threading


class Maze:
    _lower_green = np.array([40, 100, 85])
    _upper_green = np.array([75, 255, 255])

    _kernel = np.ones((3, 3), np.uint8)

    def __init__(self, cap, title):

        _, self._frame = cap.read()

        self._maze_mask = np.zeros((len(self._frame), len(self._frame[0]), 3), np.uint8)
        self._lab_mask = np.zeros((len(self._frame), len(self._frame[0]), 3), np.uint8)
        self._circles = np.zeros((len(self._frame), len(self._frame[0]), 3), np.uint8)
        # self._blank_image = np.zeros((len(self._frame), len(self._frame[0]), 3), np.uint8)

        self._sensitivity = 90

        self._thread_running = True



        maze_calculation_thread = threading.Thread(target=self._maze_calculation)

        maze_calculation_thread.start()

        while True:
            _, self._frame = cap.read()

            actual_frame = self._frame

            # circles
            actual_frame = cv2.addWeighted(actual_frame, 1, self._maze_mask, 0.5, 0)
            actual_frame = cv2.addWeighted(actual_frame, 1, self._circles, 0.3, 0)

            cv2.imshow(title, actual_frame)

            k = cv2.waitKey(5) & 0xFF
            if k == ord('q'):
                self._thread_running = False
                maze_calculation_thread.join()
                cv2.destroyAllWindows()
                break


    # we should find position of end points
    # there could be a lot of green elements on frame
    # so we should find two the biggest
    # returns position of start and end and diameter of found point
    def _position_of_end_points(self, mask):
        r, thresh = cv2.threshold(mask, 40, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        positions = []

        if len(contours) >= 2:
            contours.sort(key=cv2.contourArea, reverse=True)

            for i, con in enumerate(contours):
                if i == 0:
                    x, y, w, h = cv2.boundingRect(con)
                    positions.append((int(round(x + (w / 2))),  # center
                                      int(round(y + (h / 2))),
                                      int(round(max(w, h)))))
                    bx, by, bh = x, y, max(w, h)

                else:
                    x, y, w, h = cv2.boundingRect(con)

                    if (x>=bx and x<bx+bh) or (x>=by and x<by+bh):
                            break
                    positions.append((int(round(x + (w / 2))), # center
                                      int(round(y + (h / 2))),
                                      int(round(max(w, h)))))
                    break



        return positions

    def _draw_path_on_frame(self, path):
        blank_image = np.zeros((len(self._frame), len(self._frame[0]), 3), np.uint8)
        for p in path:
            blank_image[p] = (255, 255, 255)

        frame = blank_image

        return frame


    def _maze_calculation(self):
        while self._thread_running:

            #self._circles = np.zeros((len(self._frame), len(self._frame[0]), 3), np.uint8)
            #self._maze_mask = np.zeros((len(self._frame), len(self._frame[0]), 3), np.uint8)

            # gray
            gray_frame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)
            r, labirynth_mask = cv2.threshold(gray_frame, self._sensitivity, 255, cv2.THRESH_BINARY_INV)

            # Threshold the HSV image to get only blue colors
            hsv_frame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV)
            points_mask = cv2.inRange(hsv_frame, self._lower_green, self._upper_green)



            # dilate final pieces for better effect
            labirynth_mask = cv2.dilate(labirynth_mask, self._kernel, iterations=2)
            points_mask = cv2.dilate(points_mask, self._kernel, iterations=2)

            # connect all pieces to ones
            final_maze_masked = labirynth_mask - points_mask

            positions = self._position_of_end_points(points_mask)

            if len(positions) == 2:
                self._circles = np.zeros((len(self._frame), len(self._frame[0]), 3), np.uint8)
                cv2.circle(self._circles, (positions[0][0], positions[0][1]), positions[0][2], (0, 255, 0), -1)
                cv2.circle(self._circles, (positions[1][0], positions[1][1]), positions[1][2], (0, 255, 0), -1)

                path = solver.solve(final_maze_masked, positions[1], positions[0])
                if len(path) > 2:
                    self._maze_mask = self._draw_path_on_frame(path)
