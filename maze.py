import cv2
import numpy as np
from time import sleep
import copy
import solver

cap = cv2.VideoCapture(0)

'''
def mask_to_text_and_to_file(mask):
    result = [['X'] * len(mask[0])] * len(mask)
    
    
    str_text = ""

    for row in mask:
        for pixel in row:
            if pixel == 255:
                str_text = str_text + '#'
            else:
                str_text = str_text + '.'
        str_text = str_text + '\n'


    with open("data.txt", "w") as f:
        f.write(str_text)
        
        
            #save file

        
'''

'''
    for row_num, row in enumerate(mask):
        for pixel_num, pixel in enumerate(row):
            if pixel == 255:
                result[row_num][pixel_num] = '#'
            else:
                result[row_num][pixel_num] = '.'


    str_text = ""

    for row_num, row in enumerate(result):
        for pixel_num, pixel in enumerate(row):
            str_text = str_text + result[row_num][pixel_num]
        str_text = str_text + '\n'
        
        
        
            str_text = ""

    for row_num, row in enumerate(result):
        for pixel_num, pixel in enumerate(row):
            str_text = str_text + result[row_num][pixel_num]
        str_text = str_text + '\n'

    with open("dataxD.txt", "w") as f:
        f.write(str_text)
'''


# result = [['X'] * (len(mask[0]))] * (len(mask))


def mask_to_text(mask):
    result = [['x' for x in range(len(mask[0]))] for y in range(len(mask))]

    # print("result:", len(result), len(result[0]))
    # print("mask:", len(mask), len(mask[0]))

    for row_num, row in enumerate(mask):
        for pixel_num, pixel in enumerate(row):
            if pixel > 250:
                result[row_num][pixel_num] = '#'
            else:
                result[row_num][pixel_num] = ' '

    return result


def find_largest_groups_in_mask(mask):
    pass


def show_end_points(frame):
    # save normal frame
    original_frame = frame

    # convert color scale to HSV
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green = np.array([40, 100, 85])
    upper_green = np.array([75, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(frame, lower_green, upper_green)

    # dilate for better effect
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)

    positions = position_of_end_points(mask)

    if len(positions) == 2:
        copy_frame = copy.copy(original_frame)
        cv2.circle(copy_frame, (positions[0][0], positions[0][1]), positions[0][2], (0, 255, 0), -1)
        cv2.circle(copy_frame, (positions[1][0], positions[1][1]), positions[1][2], (0, 255, 0), -1)
        # print("Pierwsze kolo:", (positions[0][0], positions[0][1]), '\n',"Drugie kolo:", (positions[1][0], positions[1][1]), '\n', )
        original_frame = cv2.addWeighted(original_frame, 0.7, copy_frame, 0.3, 0)

    # original frame is overlayed by detected path
    return original_frame


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
        # todo not sure if sorted ascend
        x, y, w, h = cv2.boundingRect(sorted_contours[-2])
        positions.append((int(round(x + (w / 2))), int(round(y + (h / 2))), int(round(max(w, h)))))
        x, y, w, h = cv2.boundingRect(sorted_contours[-1])
        positions.append((int(round(x + (w / 2))), int(round(y + (h / 2))), int(round(max(w, h)))))

    return positions


def show_path(frame):
    labirynth = mask_to_text(frame)


def draw_path_on_frame(frame, path):
    blank_image = np.zeros((len(frame), len(frame[0]), 3), np.uint8)
    for p in path:
        blank_image[p[0]][p[1]] = (255, 255, 255)

    frame = cv2.addWeighted(frame, 0.5, blank_image, 0.5, 0)

    return frame


def what_the_hell():
    _, frame1 = cap.read()
    #sleep(0.2)
    _, frame2 = cap.read()
    #sleep(0.2)
    _, frame3 = cap.read()
    #sleep(0.2)

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

    positions = position_of_end_points(mask1)

    print("poz1", positions)
    # print(positions[0][0],positions[0][1], positions[0][2])

    if len(positions) == 2:
        copy_frame = copy.copy(original_frame)
        cv2.circle(copy_frame, (positions[0][0], positions[0][1]), positions[0][2], (0, 255, 0), -1)
        cv2.circle(copy_frame, (positions[1][0], positions[1][1]), positions[1][2], (0, 255, 0), -1)
        original_frame = cv2.addWeighted(original_frame, 1, copy_frame, 1, 0)

        # mask_to_text(final_maze_masked - final_mask)

        labirynth = mask_to_text(final_maze_masked)
        pos = positions

        path = solver.solve(labirynth, (positions[0][0], positions[0][1]), (positions[1][0], positions[1][1]))

        original_frame = draw_path_on_frame(original_frame, path)

        #original_frame = cv2.addWeighted(original_frame, 1, blank_image, 1, 0)

    cv2.imshow('stuff sovled, kinda', original_frame)
    
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


# path = solver.solve(result, (1, 8), (1, 18))


if __name__ == '__main__':
    while True:

        what_the_hell()

        k = cv2.waitKey(5) & 0xFF
        if k == ord('q'):
            cv2.destroyAllWindows()
            break
        elif k == ord('t'):
            cv2.destroyAllWindows()
            mazeMagic()
            break
        elif k == ord('/'):
            cv2.destroyAllWindows()
            what_the_hell()
            break
