from random import randint
from collections import deque
from size_and_color import *
import pygame

def distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


class Monkey:
    def __init__(self):
        self.position = (0, 0)
        self.have_chair, self.have_stick, self.have_banana = False, False, False

    def move(self, pos):
        if self.position[0] < pos[0]:
            for _ in range(pos[0] - self.position[0]):
                print('Down')
        else:
            for _ in range(self.position[0] - pos[0]):
                print('Up')

        if self.position[1] < pos[1]:
            for _ in range(pos[1] - self.position[1]):
                print('Right')
        else:
            for _ in range(self.position[1] - pos[1]):
                print('Left')

        self.position = pos

    def pick_chair(self, map):
        if map.chair == self.position:
            self.have_chair = True
            print('Have chair')

    def pick_stick(self, map):
        if map.stick == self.position:
            self.have_stick = True
            print('Have stick')

    def take_banana(self, map):
        if map.banana == self.position and self.have_stick and self.have_chair:
            print('Have banana')


class Main:

    def __init__(self) -> None:
        self.grid = [[0 for _ in range(ROW)] for _ in range(COLUMN)]
        self.visited = set()
        self.chair, self.stick, self.banana = (0, 0), (0, 0), (0, 0)

    def set_location_object(self):
        # set the chair as number 1, stick as number 2 and bananas as number 3
        visited = set()
        yet_created, is_created_chair, is_created_stick, is_created_banana = False, False, False, False
        while not yet_created:
            temp_row, temp_column = randint(0, ROW - 1), randint(0, COLUMN - 1)
            if (temp_row, temp_column) in visited:
                continue
            visited.add((temp_row, temp_column))

            if not is_created_chair:
                self.grid[temp_row][temp_column] = 1
                is_created_chair = True

            elif not is_created_stick:
                self.grid[temp_row][temp_column] = 2
                is_created_stick = True
            else:
                self.grid[temp_row][temp_column] = 3
                is_created_banana = True

            if is_created_chair and is_created_stick and is_created_banana:
                yet_created = True

    def get_all_object(self):
        return self.chair != (0, 0) and self.stick != (0, 0) and self.banana != (0, 0)

    def find_location_object(self, rows, columns):
        queue = deque()
        self.visited.add((rows, columns))
        queue.append((rows, columns))
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        while queue:
            temp_row, temp_column = queue.popleft()
            if self.get_all_object():
                break
            for direct_row, direct_column in directions:
                r, c = temp_row + direct_row, temp_column + direct_column
                if (r not in range(ROW)
                        or c not in range(COLUMN)):
                    continue

                if (self.grid[r][c] == 0
                        and (r, c) not in self.visited):
                    queue.append((r, c))
                    self.visited.add((r, c))

                if self.get_all_object():
                    break
                if self.grid[r][c] == 1:
                    self.chair = (r, c)
                if self.grid[r][c] == 2:
                    self.stick = (r, c)
                if self.grid[r][c] == 3:
                    self.banana = (r, c)

    def pick_chair_first(self):
        return distance((0, 0), self.chair) + distance(self.chair, self.stick) + distance(self.stick, self.banana)

    def pick_stick_first(self):
        return distance((0, 0), self.stick) + distance(self.stick, self.chair) + distance(self.chair, self.banana)

    def movement(self, player):
        if self.pick_chair_first() < self.pick_stick_first():
            player.move(self.chair)
            player.pick_chair(self)
            player.move(self.stick)
            player.pick_stick(self)
        else:
            player.move(self.stick)
            player.pick_stick(self)
            player.move(self.chair)
            player.pick_chair(self)

        player.move(self.banana)
        player.take_banana(self)

pygame.init()

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Monkey and Banana')

clock = pygame.time.Clock()

monkey = pygame.image.load('monkey.png')
chair = pygame.image.load('chair.png')
stick = pygame.image.load('stick.png')
banana = pygame.image.load('banana.png')
floor = pygame.image.load('floor.jpg')
icon = pygame.image.load('monkeyIcon.png')

pygame.display.set_icon(icon)

def quitgame():
    pygame.quit()
    quit()


def show_image(x, y, image):
    gameDisplay.blit(image, (x, y))


def game_loop():
    play = Main()
    player = Monkey()
    play.set_location_object()
    print(play.grid)
    play.find_location_object(0, 0)
    print(play.chair, play.stick, play.banana)
    pos_chair = play.chair
    pos_stick = play.stick
    pos_banana = play.banana

    x_monkey, y_monkey = 0, 0
    x_chair, y_chair = pos_chair[1] * 100, pos_chair[0] * 100
    x_stick, y_stick = pos_stick[1] * 100, pos_stick[0] * 100
    x_banana, y_banana = pos_banana[1] * 100, pos_banana[0] * 100
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_monkey >= 100:
                    x_monkey -= 100
                elif event.key == pygame.K_RIGHT and x_monkey < 800:
                    x_monkey += 100
                elif event.key == pygame.K_UP and y_monkey >= 100:
                    y_monkey -= 100
                elif event.key == pygame.K_DOWN and y_monkey < 700:
                    y_monkey += 100

        gameDisplay.blit(floor, (0, 0))

        if x_monkey == x_stick and y_monkey == y_stick:
            player.have_stick = True

        if x_monkey == x_chair and y_monkey == y_chair:
            player.have_chair = True

        if x_monkey == x_banana and y_monkey == y_banana and player.have_chair and player.have_stick:
            player.have_banana = True

        if not player.have_stick:
            show_image(x_stick, y_stick, stick)
        if not player.have_chair:
            show_image(x_chair, y_chair, chair)
        show_image(x_monkey, y_monkey, monkey)
        if not player.have_banana:
            show_image(x_banana, y_banana, banana)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    game_loop()
