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


def detect_end_points(frame):
    # save normal frame
    original_frame = frame

    # take  e d g y  frames
    # edges1 = cv2.Canny(frame, 100, 200)

    # convert color scale to HSV
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green = np.array([40, 100, 85])
    upper_green = np.array([75, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(frame, lower_green, upper_green)

    # dilate final pieces for better effect
    kernel = np.ones((3, 3), np.uint8)
    # final_edges = cv2.dilate(final_edges, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # substrate walls with start and end
    # final_maze_masked = final_edges - final_mask

    backtorgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    # original frame is overlayed by detected path
    return cv2.addWeighted(original_frame, 1.0, backtorgb, 0.1, 0)


def mazeMagic():
    # to achieve better edgy detection we take three frame
    _, frame1 = cap.read()
    sleep(0.2)
    _, frame2 = cap.read()
    sleep(0.2)
    _, frame3 = cap.read()
    sleep(0.2)

    # save normal frame
    original_frame = frame1

    # take  e d g y  frames
    edges1 = cv2.Canny(frame1, 100, 200)
    edges2 = cv2.Canny(frame2, 100, 200)
    edges3 = cv2.Canny(frame3, 200, 200)

    # convert color scale to HSV
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green = np.array([40, 100, 85])
    upper_green = np.array([75, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask1 = cv2.inRange(frame1, lower_green, upper_green)
    mask2 = cv2.inRange(frame2, lower_green, upper_green)
    mask3 = cv2.inRange(frame3, lower_green, upper_green)

    # connect all pieces to one
    final_edges = edges1 + edges2 + edges3
    final_mask = mask1 + mask2 + mask3

    # dilate final pieces for better effect
    kernel = np.ones((3, 3), np.uint8)
    final_edges = cv2.dilate(final_edges, kernel, iterations=1)
    final_mask = cv2.dilate(final_mask, kernel, iterations=2)

    # substrate walls with start and end
    final_maze_masked = final_edges - final_mask

    backtorgb = cv2.cvtColor(final_mask, cv2.COLOR_GRAY2RGB)

    # original frame is overlayed by detected path
    original_frame = cv2.addWeighted(original_frame, 1.0, backtorgb, 0.1, 0)

    # show windows
    cv2.imshow('mask', final_mask)
    cv2.imshow('mask2', original_frame)
    # cv2.imshow('edges_masked', final_maze_masked - final_mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


'''


    final_maze_masked = cv2.imread(final_maze_masked, 0)
    final_maze_masked = cv2.cvtColor(final_maze_masked, cv2.COLOR_BGR2GRAY)
    img_expanded = final_maze_masked[:, :, np.newaxis]
'''
# cv2.imshow('edges_masked2', img_expanded)


if __name__ == '__main__':
    while True:

        # Take each frame
        goodFrame, frame = cap.read()

        # check if frame is taken properly
        if goodFrame:
            # edges detection - used to extract the maze shape
            edges = cv2.Canny(frame, 200, 200)

            frame = detect_end_points(frame)

            cv2.imshow('frame', frame)
            # cv2.imshow('edges', edges)

            k = cv2.waitKey(5) & 0xFF
            if k == ord('q'):
                cv2.destroyAllWindows()
                break
            elif k == ord('t'):
                cv2.destroyAllWindows()
                mazeMagic()
                break
