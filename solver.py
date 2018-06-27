import numpy as np
from collections import deque


def solve(labirynth, i_start, i_end):
    path = []

    # start = i_start
    # end = i_end

    start = (i_start[1], i_start[0])
    end = (i_end[1], i_end[0])

    path.append(start)
    path.append(end)

    labirynth[start[0]][start[1]] = 'S'
    labirynth[end[0]][end[1]] = 'E'

    labirynth[end[0]][end[1]] = ' '

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
            if labirynth[index[0]][index[1] - 1] == ' ':
                labirynth[index[0]][index[1] - 1] = 'd'
                temp = (index[0], index[1] - 1)
                queue.append(temp)

            # down
            if labirynth[index[0]][index[1] + 1] == ' ':
                labirynth[index[0]][index[1] + 1] = 'u'
                temp = (index[0], index[1] + 1)
                queue.append(temp)

            # left
            if labirynth[index[0] - 1][index[1]] == ' ':
                labirynth[index[0] - 1][index[1]] = 'r'
                temp = (index[0] - 1, index[1])
                queue.append(temp)

            # right
            if labirynth[index[0] + 1][index[1]] == ' ':
                labirynth[index[0] + 1][index[1]] = 'l'
                temp = (index[0] + 1, index[1])
                queue.append(temp)
        except IndexError:
            return path
    # go through solution

    # print("dziala bez kitu xD")

    shortest_path = end
    try:
        if labirynth[shortest_path[0]][shortest_path[1]] == ' ':
            is_solved = False
        else:
            is_solved = True

            path.append(shortest_path)

            while labirynth[shortest_path[0]][shortest_path[1]] != 'S':
                # print("paf: ",shortest_path, labirynth[shortest_path[0]][shortest_path[1]])

                if labirynth[shortest_path[0]][shortest_path[1]] == 'u':
                    path.append(shortest_path)
                    labirynth[shortest_path[0]][shortest_path[1]] = 'U'
                    shortest_path = (shortest_path[0], shortest_path[1] - 1)

                if labirynth[shortest_path[0]][shortest_path[1]] == 'd':
                    path.append(shortest_path)
                    labirynth[shortest_path[0]][shortest_path[1]] = 'D'
                    shortest_path = (shortest_path[0], shortest_path[1] + 1)

                if labirynth[shortest_path[0]][shortest_path[1]] == 'l':
                    path.append(shortest_path)
                    labirynth[shortest_path[0]][shortest_path[1]] = 'L'
                    shortest_path = (shortest_path[0] - 1, shortest_path[1])

                if labirynth[shortest_path[0]][shortest_path[1]] == 'r':
                    path.append(shortest_path)
                    labirynth[shortest_path[0]][shortest_path[1]] = 'R'
                    shortest_path = (shortest_path[0] + 1, shortest_path[1])
    except IndexError:
        return path

    return path
