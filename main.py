import pygame, sys, random
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(3, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.newBlock = False

        # snake head
        self.head = self.HeadUp = pygame.image.load('snakeHeadUp.png').convert_alpha()
        self.head = self.HeadDown = pygame.image.load('snakeHeadDown.png').convert_alpha()
        self.head = self.HeadLeft = pygame.image.load('snakeHeadLeft.png').convert_alpha()
        self.head = self.HeadRight = pygame.image.load('snakeHeadRight.png').convert_alpha()

        # tail
        self.tail = self.TailUp = pygame.image.load('snakeTailUp.png').convert_alpha()
        self.tail = self.TailDown = pygame.image.load('snakeTailDown.png').convert_alpha()
        self.tail = self.TailLeft = pygame.image.load('snakeTailLeft.png').convert_alpha()
        self.tail = self.TailRight = pygame.image.load('snakeTailRight.png').convert_alpha()

        #body
        self.body_vertical = pygame.image.load('bodyVertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('bodyHorizontal.png').convert_alpha()

        #turns
        self.body_tr = pygame.image.load('body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('body_bl.png').convert_alpha()
        self.crunchSound = pygame.mixer.Sound('crunch.wav')
        #self.backgroundSong = pygame.mixer.Sound('you-can-do-more-108602.wav')

    def drawSnake(self):
        #self.playBGSound()
        self.updateHead()
        self.updateTail()

        for index, block in enumerate(self.body):
            xPos = int(block.x * cellSize)
            yPos = int(block.y * cellSize)
            blockRect = pygame.Rect(xPos, yPos, cellSize, cellSize)

            # snake direction
            if index == 0:
                screen.blit(self.head, blockRect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, blockRect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, blockRect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, blockRect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, blockRect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, blockRect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, blockRect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, blockRect)

    def updateHead(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.HeadLeft
        elif head_relation == Vector2(-1, 0):
            self.head = self.HeadRight
        elif head_relation == Vector2(0, 1):
            self.head = self.HeadUp
        elif head_relation == Vector2(0, -1):
            self.head = self.HeadDown

    def updateTail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.TailLeft
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.TailRight
        elif tail_relation == Vector2(0, 1):
            self.tail = self.TailUp
        elif tail_relation == Vector2(0, -1):
            self.tail = self.TailDown

    def moveSnake(self):
        if self.newBlock == True:
            bodyCopy = self.body[:]
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy[:]
            self.newBlock = False
        else:
            bodyCopy = self.body[:-1]
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy[:]

    def addBlock(self):
        self.newBlock = True

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

    def playCrunchSound(self):
        self.crunchSound.play()

    #def playBGSound(self):
        #self.backgroundSong.play()

class Food:
    def __init__(self):
        # make x & y position
        self.random()

    # draw square
    def drawFood(self):
        # make rectangle
        foodRect = pygame.Rect(int(self.pos.x * cellSize), int(self.pos.y * cellSize), cellSize, cellSize)
        screen.blit(burger, foodRect)
        # pygame.draw.rect(screen, (126, 166, 114), fruitRect)

    def random(self):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = Vector2(self.x, self.y)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()

    def update(self):
        self.snake.moveSnake()
        self.checkSameSpot()
        self.setGameOver()

    def drawElements(self):
        self.drawGrass()
        self.food.drawFood()
        self.snake.drawSnake()
        self.draw_score()

    # Make sure snake and fruit are not at the same spot
    def checkSameSpot(self):
        if self.food.pos == self.snake.body[0]:
            self.food.random()

            # now make snake longer
            self.snake.addBlock()

            #play sound
            self.snake.playCrunchSound()

    def setGameOver(self):
        # see if snake has hit the walls
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
            self.gameOver()

        # see if snake has hit its body
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()

    def gameOver(self):
        self.snake.reset()

    def drawGrass(self):
        grass_color = (216, 245, 214)
        for row in range(cellNumber):
            if row % 2 == 0:
                for col in range(cellNumber):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cellNumber):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cellSize * cellNumber - 60)
        score_y = int(cellSize * cellNumber - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        foodRect = burger.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(foodRect.left, foodRect.top, foodRect.width + score_rect.width + 6,
                              foodRect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(burger, foodRect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

pygame.init()
cellSize = 40
cellNumber = 20
screen = pygame.display.set_mode((cellNumber * cellSize, cellNumber * cellSize))
clock = pygame.time.Clock()
burger = pygame.image.load('burger.png').convert_alpha()
game_font = pygame.font.Font(None, 25)

screenUpdate = pygame.USEREVENT
pygame.time.set_timer(screenUpdate, 150)

mainGame = Main()

# drawing all the elements here
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == screenUpdate:
            mainGame.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if mainGame.snake.direction.y != 1:
                    mainGame.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if mainGame.snake.direction.x != -1:
                    mainGame.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if mainGame.snake.direction.x != 1:
                    mainGame.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_DOWN:
                if mainGame.snake.direction.y != -1:
                    mainGame.snake.direction = Vector2(0, 1)

    screen.fill((214, 245, 243))
    mainGame.drawElements()
    pygame.display.update()
    clock.tick(60)  # 60fps
