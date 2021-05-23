import pygame
import math
import random
GREY = (150, 150, 150)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
rows = 50
cols = 50
grid = []
openSet = []
closeSet = []
route = []
screenWidth = 700
screenHeight = 700
w = screenWidth/cols
h = screenHeight/rows


def heuristic(a, b):
    d = math.pow(b.i-a.i, 2) + math.pow(b.j - a.j, 2)
    dis = math.sqrt(d)
    #dis = math.fabs(b.i-a.i) + math.fabs(b.j-a.j)
    return dis
class Spot:
    f = 0
    g = 0
    h = 0
    wall = False
    prev = None
    def __init__(self, i, j):
        self.i = i
        self.j = j
        if random.random() < 0:
            self.wall = True
    def show(self, screen, COLOR):
        #pygame.draw.rect(screen, COLOR, (self.i * w + 1, self.j * h + 1, w-2, h-2))
        pygame.draw.circle(screen, COLOR, (self.i * w + w/2, self.j * h + h/2), w/2, width = 0)
    def addNeighbors(self, neighbors, grid):
        i = self.i
        j = self.j
        if j < cols - 1:
            neighbors.append(grid[i][j + 1])
        if i < rows - 1:
            neighbors.append(grid[i + 1][j])
        if i > 0:
            neighbors.append(grid[i - 1][j])
        if j > 0:
            neighbors.append(grid[i][j - 1])
        #if i > 0 and j > 0:
        #    neighbors.append(grid[i-1][j-1])
        #if i > 0 and j < cols -1:
        #    neighbors.append(grid[i-1][j+1])
        #if i < rows - 1 and j > 0:
        #    neighbors.append(grid[i+1][j-1])
        #if i < rows - 1 and j < cols - 1:
        #    neighbors.append(grid[i+1][j+1])
        self.neighbors = neighbors

for i in range(cols):
    grid.append([])
    for j in range(rows):
        grid[i].append(Spot(i, j))


for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors([], grid)

start = grid[0][0]
end = grid[rows-1][cols-1]
start.wall = False
end.wall = False
openSet.append(start)
route.append(start)
running = True
noSolution = 0;
pygame.init()
while(running):
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if len(openSet) > 0:
        # keep going
        winner = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[winner].f:
                winner = i

        current = openSet[winner]
        if current != end:
            openSet.remove(current)
            closeSet.append(current)

            neighbors = current.neighbors
            for neighbor in neighbors:
                if neighbor not in closeSet and neighbor.wall == False:
                    tempG = current.g + 1
                    newPath = False
                    if neighbor in openSet:
                        if tempG < neighbor.g:
                            neighbor.g = tempG
                            newPath = True
                    else:
                        neighbor.g = tempG
                        openSet.append(neighbor)
                        newPath = True
                    if newPath == True:
                        neighbor.h = heuristic(neighbor, end)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.prev = current

    else:
        noSolution = noSolution+1
        if noSolution == 1:
            print("No solution")
    for i in range(rows):
        for j in range(cols):
            if grid[i][j].wall == True:
                grid[i][j].show(screen, BLACK)
            else:
                grid[i][j].show(screen, WHITE)

    route = []
    routeDraw = []
    temp = current

    route.append(temp)
    routeDraw.append((temp.i * w + w / 2, temp.j * h + h / 2))
    while temp.prev:

        route.append(temp.prev)
        routeDraw.append((temp.prev.i * w + w/2, temp.prev.j * h + h/2))
        temp = temp.prev
    #routeDraw.append((start.i * w + w / 2, start.j * h + h / 2))
    routeDraw.append((start.i * w, start.j * h))

    #for i in range(len(route)):
    #   route[i].show(screen, BLUE)
    pygame.draw.lines(screen, BLUE, False, routeDraw, 6)
    pygame.display.flip()
    #pygame.time.wait(20)
pygame.quit()