import pygame
import sys
import random
highscore = 0
games = 0
class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screenWidth/2), (screenHeight/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (77, 136, 255)#snake color
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        global highscore
        global games
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridSize))%screenWidth), (cur[1]+(y*gridSize))%screenHeight)
        if len(self.positions) > 2 and new in self.positions[2:]:
            if self.score > highscore:
                highscore = self.score
            games = games+1
            text = pygame.font.SysFont("showcard gothic",18).render("Present Score: {0}    High Score: {1}".format(snake.score, highscore), 1, (0,0,0))
            screen.blit(text, (90,250))
            pygame.display.update()
            pygame.time.delay(7000)#waits for 7000 milli sec
            
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screenWidth/2), (screenHeight/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridSize,gridSize))
            pygame.draw.rect(surface, self.color, r)

    def handle_keys(self):
        global highscore
        global games
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.score > 0:
                    if self.score > highscore:
                        highscore = self.score
                    games = games+1
                print("Number of games played is:",games, "\nHigh score is:",highscore)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = (230, 0, 38)#color of food
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, gridWidth-1)*gridSize, random.randint(0, gridHeight-1)*gridSize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridSize, gridSize))
        pygame.draw.rect(surface, self.color, r)

def printScreen(surface):
    #here we will try to draw a chess board shape background
    for x in range(gridWidth):
        for y in range(gridHeight):
            if (x+y)%2 == 0:#leftmost block
                r1 = pygame.Rect((x*gridSize, y*gridSize), (gridSize,gridSize))
                pygame.draw.rect(surface,(85, 255, 0), r1)
            else:
                r2 = pygame.Rect((x*gridSize, y*gridSize), (gridSize,gridSize))
                pygame.draw.rect(surface, (0, 230, 38), r2)

screenWidth = 500
screenHeight = 500
gridSize = 25 #Number of squares we want in one length strip
gridWidth = screenWidth//gridSize
gridHeight = screenWidth//gridSize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

pygame.init()#This will initialize whole module
clock = pygame.time.Clock() #This returns a object of class type Clock
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Snake Game")
surface = pygame.Surface(screen.get_size())#get_size will return a tuple of width and height
running = True
snake = Snake()
food = Food()

while(running):
    clock.tick(10)
    snake.handle_keys()
    printScreen(surface)#the surface object is sent to a function which will draw the screen
    snake.move()
    if snake.get_head_position() == food.position:
        snake.length += 1
        snake.score += 1
        food.randomize_position()
    snake.draw(surface)
    food.draw(surface)
    screen.blit(surface, (0,0))
    text = pygame.font.SysFont("showcard gothic",16).render("Score {0}".format(snake.score), 1, (0,0,0))
    screen.blit(text, (5,10))
    pygame.display.update()
