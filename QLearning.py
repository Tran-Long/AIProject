import pandas as pd
import numpy as np
from collections import namedtuple
import random
import pygame
GREEN = (0, 255, 0)
GREY = (150, 150, 150)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
screen_width = 700
screen_height = 700
best_route = []

Agent = namedtuple('Agent', ['i', 'j'])


class Agent:
    def __init__ (self, i = 0, j = 0):
        self.i = i
        self.j = j

    @property
    def loc(self):
        return self.i, self.j

    def vertical_move(self, direction):
        return Agent(self.i + direction, self.j)

    def horizontal_move (self, direction):
        return Agent(self.i, self.j + direction)

    def __repr__ (self):
        return str(self.loc)


class Qlearning:
    def __init__ (self, num_states, num_actions, lr = 0.7, discount_factor = 0.9):
        self.q = np.zeros((num_states, num_actions))
        self.alpha = lr
        self.gamma = discount_factor

    def update (self, st, at, rt, st1):
        q = self.q
        alpha = self.alpha
        gamma = self.gamma
        self.q[st, at] = (1 - alpha) * q[st, at] + alpha * (rt + gamma * np.max(q[st1]))


class Maze:
    def __init__ (self, rows = 4, cols = 4):
        self.env = np.zeros((rows, cols))
        self.agent = Agent(0, 0)
        self.rewards = []
        #self.q = np.zeros((rows * cols, 4))

    def reset (self):
        self.agent.i = 0
        self.agent.j = 0
        for pos in self.rewards:
            self.env[pos] = 2

    def state_of_agent (self, a):
        num_rows, num_cols = self.env.shape
        return a.i * num_cols + a.j

    def idx_in_bounds (self, i, j):
        num_rows, num_cols = self.env.shape
        return 0 <= i < num_rows and 0 <= j < num_cols

    def agent_in_bounds (self, a):
        return self.idx_in_bounds(a.i, a.j)

    def agent_not_die (self, a):
        return not self.env[a.i, a.j] == -1

    def is_new_pos_valid (self, a):
        return self.agent_in_bounds(a) and self.agent_not_die(a)

    @property
    def list_actions (self):
        a = self.agent
        return [a.vertical_move(1), a.vertical_move(-1), a.horizontal_move(1), a.horizontal_move(-1)]

    def count_possible_moves (self):
        moves = self.list_actions
        return [(m, ii) for ii, m in enumerate(moves) if self.is_new_pos_valid(m)]

    def make_move (self, a):
        assert self.is_new_pos_valid(a), "Agent cant go there"
        self.agent = a
        if self.won():
            return 100
        elif self.reward_won():
            self.env[a.i, a.j] = 0
            return 70
        else:
            return -1

    def won (self):
        a = self.agent
        return self.env[a.i, a.j] == 1

    def reward_won(self):
        a = self.agent
        return self.env[a.i, a.j] == 2


    def visualize (self):
        assert self.idx_in_bounds(*self.agent.loc), "Agent is out of bounds"
        e = self.env.copy()
        a = self.agent
        e[a.i, a.j] = 6
        print(e)


def make_maze (s = 4):
    m = Maze(s, s)
    e = m.env
    h, w = e.shape
    for i in range(len(e)):
        for j in range(len(e[i])):
            if i in [0, h - 1] and j in [0, w - 1]:
                continue
            if random.random() < 0.25:
                e[i, j] = -1
    e[-1, -1] = 1  # goal
    return m

def make_maze_from_file(file_name):
    x = np.array(pd.read_csv(file_name))
    row, col = x.shape
    m = Maze(row, col)
    e = m.env
    for i in range(len(e)):
        for j in range(len(e[i])):
            if x[i, j] == -1:
                e[i, j] = -1
            elif x[i, j] == 2:
                m.rewards.append((i, j))
                e[i, j] = 2
    #m.rewards.append((2, 2))
    e[-1, -1] = 1
    return m


def epsilon(current_ep, start_ep, max_eps, start_epsilon):
    return start_epsilon + (1-start_epsilon) * (current_ep - start_ep) / (max_eps - start_ep)

def main():
    s = 20
    q = Qlearning(s ** 2, 4)
    m = make_maze(s)
    #m = make_maze_from_file("input10.csv")
    print(m.env)

    total_episode = 1000
    switch_episode = 300
    for i in range(total_episode):
        m.reset()
        final_score = 0
        itr = 0
        while not m.won():
            itr += 1
            if i < switch_episode or random.random() > epsilon(i, switch_episode, total_episode, 0.5):
                moves = m.count_possible_moves()
                random.shuffle(moves)
                move = moves[0][0]
                move_index = moves[0][1]
            else:
                moves = m.list_actions
                s = m.state_of_agent(m.agent)
                move_index = np.argmax(q.q[s])
                move = moves[move_index]
            at = move_index
            st = m.state_of_agent(m.agent)
            score = m.make_move(move)
            final_score += score
            rt = score
            st1 = m.state_of_agent(m.agent)
            q.update(st, at, rt, st1)

        print(f"Finish episode {i} with finalsore: {final_score} and after: {itr} iterations")
    #print(q.q)
    m.reset()
    best_route.append(m.agent)
    while not m.won():
        s = m.state_of_agent(m.agent)
        action_idx = np.argmax(q.q[s])
        m.make_move(m.list_actions[action_idx])
        best_route.append(m.agent)
    show(m, best_route)

def show (maze, route):
    rows, cols = maze.env.shape
    w = screen_width / cols
    h = screen_height / rows
    pygame.init()
    running = True
    bestRouteClone = route
    drawLine = [(w / 2, h / 2)]
    while running:
        screen = pygame.display.set_mode((screen_width, screen_height))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for i in range(rows):
            for j in range(cols):
                if maze.env[i][j] == -1:
                    pygame.draw.rect(screen, BLACK, (j * w + 1, i * h + 1, w - 1, h - 1))
                elif (i, j) in maze.rewards:
                    pygame.draw.rect(screen, GREEN, (j * w + 1, i * h + 1, w - 1, h - 1))
                else:
                    pygame.draw.rect(screen, WHITE, (j * w + 1, i * h + 1, w - 1, h - 1))

        if len(bestRouteClone) > 0:
            x, y = bestRouteClone[0].loc
            pygame.draw.rect(screen, RED, (y * w + 1, x * h + 1, w - 1, h - 1))
            bestRouteClone.pop(0)
            drawLine.append((y * w + w / 2, x * h + h / 2))

        pygame.draw.lines(screen, BLUE, False, drawLine, 6)
        pygame.display.flip()
        pygame.time.wait(100)
    pygame.quit()

if __name__ == '__main__':
    main()