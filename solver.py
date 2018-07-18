import numpy as np
from collections import deque

class Direction:
    WALL = 255
    WAY = 0

    START = 1
    END = 2

    UP = 3
    DOWN = 4
    LEFT = 5
    RIGHT = 6

    UP_FOUND = 7
    DOWN_FOUND = 8
    LEFT_FOUND = 9
    RIGHT_FOUND = 10



def solve(labirynth, i_start, i_end):
    path = []
    labirynth = np.pad(labirynth, pad_width=0, mode='constant', constant_values=255)

    # start = i_start
    # end = i_end

    start = (i_start[1], i_start[0])
    end = (i_end[1], i_end[0])

    path.append(start)
    path.append(end)

    labirynth[start[0]][start[1]] = Direction.START
    #labirynth[end[0]][end[1]] = Direction.END

    #labirynth[end[0]][end[1]] = Direction.WAY

    queue = deque()

    queue.append(start)

    find = False

    while len(queue) != 0:
        index = queue.popleft()

        if index == end:
            find = True
            break
        try:
            # up
            if labirynth[index[0]][index[1] - 1] == Direction.WAY:
                labirynth[index[0]][index[1] - 1] = Direction.DOWN
                temp = (index[0], index[1] - 1)
                queue.append(temp)

            # down
            if labirynth[index[0]][index[1] + 1] == Direction.WAY:
                labirynth[index[0]][index[1] + 1] = Direction.UP
                temp = (index[0], index[1] + 1)
                queue.append(temp)

            # left
            if labirynth[index[0] - 1][index[1]] == Direction.WAY:
                labirynth[index[0] - 1][index[1]] = Direction.RIGHT
                temp = (index[0] - 1, index[1])
                queue.append(temp)

            # right
            if labirynth[index[0] + 1][index[1]] == Direction.WAY:
                labirynth[index[0] + 1][index[1]] = Direction.LEFT
                temp = (index[0] + 1, index[1])
                queue.append(temp)
        except IndexError:
            return path
    # go through solution

    # print("dziala bez kitu xD")

    shortest_path = end
    try:
        if labirynth[shortest_path] == Direction.WAY:
            is_solved = False
        else:
            is_solved = True

            path.append(shortest_path)

            while labirynth[shortest_path[0]][shortest_path[1]] != Direction.START:

                if labirynth[shortest_path] == Direction.UP:
                    path.append(shortest_path)
                    labirynth[shortest_path] = Direction.UP_FOUND
                    shortest_path = (shortest_path[0], shortest_path[1] - 1)

                if labirynth[shortest_path] == Direction.DOWN:
                    path.append(shortest_path)
                    labirynth[shortest_path] = Direction.DOWN_FOUND
                    shortest_path = (shortest_path[0], shortest_path[1] + 1)

                if labirynth[shortest_path] == Direction.LEFT:
                    path.append(shortest_path)
                    labirynth[shortest_path] = Direction.LEFT_FOUND
                    shortest_path = (shortest_path[0] - 1, shortest_path[1])

                if labirynth[shortest_path] == Direction.RIGHT:
                    path.append(shortest_path)
                    labirynth[shortest_path] = Direction.RIGHT_FOUND
                    shortest_path = (shortest_path[0] + 1, shortest_path[1])
    except IndexError:
        return path

    return path
