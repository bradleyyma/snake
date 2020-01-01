import pygame
import random
import tkinter
from tkinter import messagebox

pygame.init()


import pygame
class Cell(object):
    def __init__(self, position, xdir = 0, ydir = 0, color=(255, 0, 0)):
        self.position = position
        self.xdir = xdir
        self.ydir = ydir
        self.color = color

    def move(self, xdir, ydir):
        self.xdir = xdir
        self.ydir = ydir
        self.position = (self.position[0] + xdir, self.position[1] + ydir)
        pass

    def draw(self, window):
        x = self.position[0] * cell_size
        y = self.position[1] * cell_size
        pygame.draw.rect(window, self.color, (x, y, cell_size, cell_size) )

class Snake(object):
    body = []
    turns = {}
    length = 1
    def __init__(self, color = (255, 0, 0), position = (10, 10)):
        self.color = color
        self.head = Cell(position, color = (173, 216, 230))
        self.body.append(self.head)
        self.xdir = 0
        self.ydir = 0

    def move(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT] and self.xdir != 1:
                    self.xdir = -1
                    self.ydir = 0
                elif keys[pygame.K_RIGHT] and self.xdir != -1:
                    self.xdir = 1
                    self.ydir = 0
                elif keys[pygame.K_UP] and self.ydir != 1:
                    self.xdir = 0
                    self.ydir = -1
                elif keys[pygame.K_DOWN] and self.ydir != -1:
                    self.xdir = 0
                    self.ydir = 1
            self.turns[self.head.position] = [self.xdir, self.ydir]
        for cell in self.body:
            pos = cell.position
            if pos in self.turns:
                turn = self.turns[pos]
                cell.move(turn[0], turn[1])
                if cell == self.body[-1]:
                    self.turns.pop(pos)
            else:
                cell.move(cell.xdir, cell.ydir)
    def draw(self, window):
        for cell in self.body:
            cell.draw(window)

    def add_cell(self):
        tail = self.body[-1]
        if tail.xdir == 1:
            position = (tail.position[0] - 1, tail.position[1])
        elif tail.xdir == -1:
            position = (tail.position[0] + 1, tail.position[1])
        elif tail.ydir == 1:
            position = (tail.position[0], tail.position[1] - 1)
        elif tail.ydir == -1:
            position = (tail.position[0], tail.position[1] + 1)
        new_cell = Cell(position, tail.xdir, tail.ydir)
        self.body.append(new_cell)
        self.length += 1

    def reset(self):
        self.body = []
        self.turns = {}
        self.length = 1
        self.__init__()


def message(score):
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo('Game Over', f'Score: {score}')
    try:
        root.destroy()
    except:
        pass

def drawGrid(window):
    x = 0
    y = 0

    for i in range(rows):
        x = x + cell_size
        y = y + cell_size

        pygame.draw.line(window, (255, 255, 255), (x, 0) , (x, width))
        pygame.draw.line(window, (255, 255, 255), (0, y) , (width, y))

def redrawWindow(window):
    window.fill( (0,0,0) )
    score = s.length
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = window.get_rect().centerx
    window.blit(text, textpos)
    s.draw(window)
    snack.draw(window)
    drawGrid(window)
    pygame.display.update()

def randomFruit(rows, snake):
    position = s.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.position == (x,y), position))) > 0:
            continue
        else:
            break

    return (x, y)


def main():
    global width, rows, cell_size
    width = 500
    rows = 20
    cell_size = width // rows
    snake_color = (255, 0, 0)
    win = pygame.display.set_mode((width, width+ 100))
    global s, snack
    s = Snake(snake_color, (10, 10))
    snack = Cell(randomFruit(rows, s), color=(0, 255, 0))

    clock = pygame.time.Clock()
    run = True
    while run:
        pygame.time.delay(100)
        clock.tick(60)

        s.move();

        if s.head.position == snack.position:
            s.add_cell()
            snack = Cell(randomFruit(rows, s), color=(0, 255, 0))

        # collision check
        score = s.length
        for cell in range(len(s.body)):
            if s.body[cell].position in list(map(lambda z:z.position, s.body[cell+1:])):
                message(score)
                s.reset()
                print(s.body)
                break
        head_x = s.head.position[0]
        head_y = s.head.position[1]
        if head_x >= rows or head_x < 0 or head_y >= rows or head_y < 0:
            message(score)
            s.reset()



        redrawWindow(win)

if __name__ == '__main__':
    main()
