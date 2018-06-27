import cv2
import maze

if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    maze.Maze(cap, "test")
