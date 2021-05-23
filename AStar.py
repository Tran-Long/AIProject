import pygame
import math
import random
import pandas as pd
import numpy as np

GREY = (150, 150, 150)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
rows = 10
cols = 10
maze = []
open_set = []
close_set = []
screen_width = 700
screen_height = 700
w = screen_width / cols
h = screen_height / rows


def heuristic (a, b):
    d = math.pow(b.i-a.i, 2) + math.pow(b.j - a.j, 2)
    dis = math.sqrt(d)
    #dis = math.fabs(b.i - a.i) + math.fabs(b.j - a.j)
    return dis


class AgentState:
    f = 0
    g = 0
    h = 0
    wall = False
    prev = None
    def __init__ (self, i, j):
        self.i = i
        self.j = j
        self.wall = False
        #if random.random() < 0.3:
        #    self.wall = True

    def show (self, screen, COLOR):
        pygame.draw.rect(screen, COLOR, (self.j * w + 1, self.i * h + 1, w-1, h-1))
        # pygame.draw.circle(screen, COLOR, (self.i * w + w / 2, self.j * h + h / 2), w / 2, width = 0)

    def add_neighbors (self, neighbors, maze):
        i = self.i
        j = self.j
        if j < cols - 1:
            neighbors.append(maze[i][j + 1])
        if i < rows - 1:
            neighbors.append(maze[i + 1][j])
        if i > 0:
            neighbors.append(maze[i - 1][j])
        if j > 0:
            neighbors.append(maze[i][j - 1])
        self.neighbors = neighbors


def init():
    for i in range(cols):
        maze.append([])
        for j in range(rows):
            maze[i].append(AgentState(i, j))

    for i in range(rows):
        for j in range(cols):
            maze[i][j].add_neighbors([], maze)

def init_from_file(file_name):
    x = np.array(pd.read_csv(file_name))
    print(x)
    r, c = x.shape
    for i in range(r):
        maze.append([])
        for j in range(c):
            maze[i].append(AgentState(i, j))
            if x[i, j] == -1:
                maze[i][j].wall = True
    for i in range(rows):
        for j in range(cols):
            maze[i][j].add_neighbors([], maze)

def a_star (end, no_solution):
    if len(open_set) > 0:
        # keep going
        winner = 0
        for i in range(len(open_set)):
            if open_set[i].f < open_set[winner].f:
                winner = i

        current = open_set[winner]
        if current != end:
            open_set.remove(current)
            close_set.append(current)

            neighbors = current.neighbors
            for neighbor in neighbors:
                if neighbor not in close_set and neighbor.wall == False:
                    tempG = current.g + 1
                    new_path = False
                    if neighbor in open_set:
                        if tempG < neighbor.g:
                            neighbor.g = tempG
                            new_path = True
                    else:
                        neighbor.g = tempG
                        open_set.append(neighbor)
                        new_path = True
                    if new_path == True:
                        neighbor.h = heuristic(neighbor, end)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.prev = current

    else:
        no_solution = no_solution + 1
        if no_solution == 1:
            print("No solution")
        return None

    return current

def run (end, no_solution):
    pygame.init()
    running = True
    while running:
        screen = pygame.display.set_mode((screen_width, screen_height))
        screen.fill(BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for i in range(rows):
            for j in range(cols):
                if maze[i][j].wall == True:
                    maze[i][j].show(screen, BLACK)
                else:
                    maze[i][j].show(screen, WHITE)


        route = []
        temp = a_star(end, no_solution)
        route_draw = []
        route.append(temp)
        route_draw.append((temp.j * w + w / 2, temp.i * h + h / 2))
        while temp.prev:
            route.append(temp.prev)
            route_draw.append((temp.prev.j * w + w / 2, temp.prev.i * h + h / 2))
            temp = temp.prev
        route_draw.append((close_set[0].j * w + w / 2, close_set[0].i * h + h / 2))
        pygame.draw.lines(screen, BLUE, False, route_draw, 6)
        pygame.display.flip()
        pygame.time.wait(80)
    pygame.quit()


def main ():
    init_from_file("input10.csv")
    start = maze[0][0]
    end = maze[-1][-1]
    start.wall = False
    end.wall = False
    open_set.append(start)
    no_solution = 0
    run(end, no_solution)

if __name__ == '__main__':
    main()
