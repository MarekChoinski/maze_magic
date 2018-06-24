import numpy as np
from collections import deque


'''
get: matrix of chars, tuples of position of start and end
return: 
'''

'''
labirynth = [
    ['#', '#', '#', '#', '#', '#', '#'],
    ['#', 'S', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', ' ', '#', '#', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', 'E', '#'],
    ['#', '#', '#', '#', '#', '#', '#'],
]'''

def solve(labirynth, start, end):

    size = len(labirynth)

    print("wielkosc ", size)

    labirynth[start[0]][start[1]] = 'S'
    labirynth[end[0]][end[1]] = 'E'



    # find end and start
    # we search for S and E

    # indexes of S and E
    '''
    start = (-1, -1)
    end = (-1, -1)

    for i, row in enumerate(labirynth):
        for j, x in enumerate(row):
            if x == 'S':
                start = (i, j)
            if x == 'E':
                end = (i, j)
                '''

    # change E to free field

    labirynth[end[0]][end[1]] = ' '

    print(start, end)

    # make queue

    queue = deque()

    queue.append(start)

    find = False

    while len(queue) != 0:
        index = queue.popleft()

        if index == end:
            find = True
            break

        # up
        if labirynth[index[0] - 1][index[1]] == ' ':
            labirynth[index[0] - 1][index[1]] = 'd'
            temp = (index[0] - 1, index[1])
            queue.append(temp)

        # down
        if labirynth[index[0] + 1][index[1]] == ' ':
            labirynth[index[0] + 1][index[1]] = 'u'
            temp = (index[0] + 1, index[1])
            queue.append(temp)

        # left
        if labirynth[index[0]][index[1] - 1] == ' ':
            labirynth[index[0]][index[1] - 1] = 'r'
            temp = (index[0], index[1] - 1)
            queue.append(temp)

        # right
        if labirynth[index[0]][index[1] + 1] == ' ':
            labirynth[index[0]][index[1] + 1] = 'l'
            temp = (index[0], index[1] + 1)
            queue.append(temp)

    # go through solution

    print("dziala bez kitu xD")

    path = []

    shortest_path = end
    if labirynth[shortest_path[0]][shortest_path[1]] == ' ':
        is_solved = False
    else:
        is_solved = True

        path.append(shortest_path)

        while labirynth[shortest_path[0]][shortest_path[1]] != 'S':

            if labirynth[shortest_path[0]][shortest_path[1]] == 'u':
                path.append(shortest_path)
                labirynth[shortest_path[0]][shortest_path[1]] = 'U'
                shortest_path = (shortest_path[0] - 1, shortest_path[1])

            if labirynth[shortest_path[0]][shortest_path[1]] == 'd':
                path.append(shortest_path)
                labirynth[shortest_path[0]][shortest_path[1]] = 'D'
                shortest_path = (shortest_path[0] + 1, shortest_path[1])

            if labirynth[shortest_path[0]][shortest_path[1]] == 'l':
                path.append(shortest_path)
                labirynth[shortest_path[0]][shortest_path[1]] = 'L'
                shortest_path = (shortest_path[0], shortest_path[1] - 1)

            if labirynth[shortest_path[0]][shortest_path[1]] == 'r':
                path.append(shortest_path)
                labirynth[shortest_path[0]][shortest_path[1]] = 'R'
                shortest_path = (shortest_path[0], shortest_path[1] + 1)

    labirynth[end[0]][end[1]] = 'E'

    return path


'''
    for row in labirynth:
        for x in row:
            print(x, end='')
        print('\n')
'''