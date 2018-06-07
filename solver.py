import numpy as np
from collections import deque

labirynth = [
['#','#','#','#','#','#','#'],
['#','S',' ',' ',' ',' ','#'],
['#',' ','#',' ','#','#','#'],
['#',' ','#',' ','#',' ','#'],
['#',' ','#','#','#',' ','#'],
['#',' ',' ',' ',' ','E','#'],
['#','#','#','#','#','#','#'],

]

size = 7


# #######

# find end and start
# we search for S and E

#indexes of S and E
start = (-1, -1)
end = (-1, -1)

for i, row in enumerate(labirynth):
    for j, x in enumerate(row):
        if x == 'S':
            start = (i, j)
        if x == 'E':
            end = (i, j)

#change E to free field

labirynth[end[0]][end[1]] = ' '


print(start, end)

#make queue

queue = deque()

queue.append(start)

#

find = False

while len(queue) != 0:
    index = queue.popleft()

    if index == end:
        find = True
        break

    #up
    if labirynth[index[0]-1][index[1]]==' ':
        labirynth[index[0]-1][index[1]]='d'
        temp = (index[0]-1, index[1])
        queue.append(temp)

    #down
    if labirynth[index[0]+1][index[1]]==' ':
        labirynth[index[0]+1][index[1]]='u'
        temp = (index[0]+1, index[1])
        queue.append(temp)
    
    #left
    if labirynth[index[0]][index[1]-1]==' ':
        labirynth[index[0]][index[1]-1]='r'
        temp = (index[0], index[1]-1)
        queue.append(temp)

    #right
    if labirynth[index[0]][index[1]+1]==' ':
        labirynth[index[0]][index[1]+1]='l'
        temp = (index[0], index[1]+1)
        queue.append(temp)




for row in labirynth:
    for x in row:
        print(x, end='')
    print('\n')
