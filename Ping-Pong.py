import pygame
import time
import sys

lightWhite = (180, 180, 180)

# creating game
sizeMultip = 45
width = 16*sizeMultip
height = 9*sizeMultip

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong")

# setting fps
fps = 60

# setting speeds
racketSpeed = 6
ballSpeedX = 5
ballOrgSpeedX = ballSpeedX
ballSpeedY = 0
ballMaxSpeed = 7

finalScore = 3

clock = pygame.time.Clock()

racketWidth = 10
racketHeight = sizeMultip*5/3
ballRadius = 7

p1Score, p2Score = 0, 0

scoreFont = pygame.font.SysFont("comicsans", 50)
wonFont = pygame.font.SysFont("comicsans", 100)
mainFont = pygame.font.SysFont("comicsans", 75)
playFont = pygame.font.SysFont("comicsans", 30)

icon = pygame.image.load("assets\images\icon.png")
pygame.display.set_icon(icon)


# creating racket
class Racket:
    def __init__(self, x, y, width, height):
        self.x = self.originalX = x
        self.y = self.originalY = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, "white", (self.x, self.y, self.width, self.height))

    def reset(self):
        self.x = self.originalX
        self.y = self.originalY

# creating ball
class Ball:
    def __init__(self, x, y, radius):
        self.x = self.firstX = x
        self.y = self.firstY = y
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.radius)

    def reset(self):
        self.x = self.firstX
        self.y = self.firstY

# creating objects
p1 = Racket(10, height/2-racketHeight/2, racketWidth, racketHeight)
p2 = Racket(width-10-racketWidth, height/2-racketHeight/2, racketWidth, racketHeight)
ball = Ball(width/2, height/2, ballRadius)

# main menu
def menu(screen):
    screen.fill("black")
    mainMenuText = mainFont.render("Main Menu", 1, "white")
    screen.blit(mainMenuText, (width/2 - mainMenuText.get_width()/2, height/6 - mainMenuText.get_height()/2))
    playGame = pygame.Rect(width/3, 3*height/5, width/3, height/5)
    pygame.draw.rect(screen, "white", playGame)
    playGameText = playFont.render("Play Game", 1, "black")
    screen.blit(playGameText, (width/2 - playGameText.get_width()/2, 7*height/10 - playGameText.get_height()/2))
    mouse = pygame.mouse.get_pos()
    if playGame.collidepoint(mouse):
        pygame.draw.rect(screen, lightWhite, playGame)
        playGameText = playFont.render("Play Game", 1, "black")
        screen.blit(playGameText, (width/2 - playGameText.get_width()/2, 7*height/10 - playGameText.get_height()/2))

# game
def drawScreen(screen):
    screen.fill("black")
    p1ScoreText = scoreFont.render(f"{p1Score}", 1, "white")
    p2ScoreText = scoreFont.render(f"{p2Score}", 1, "white")
    pygame.draw.circle(screen, "white", (width/2, height/2), 100)
    pygame.draw.circle(screen, "black", (width/2, height/2), 97)
    pygame.draw.circle(screen, "white", (width/2, height/2), 8)
    pygame.draw.rect(screen, "white", (width/2-2, 0, 4, height))
    screen.blit(p1ScoreText, (width/4 - p1ScoreText.get_width()/2, 15))
    screen.blit(p2ScoreText, (3*width/4 - p1ScoreText.get_width()/2, 15))
    p1.draw(screen)
    p2.draw(screen)
    ball.draw(screen)

# resetting game after every goal
def resetGame(screen):
    p1.reset()
    p2.reset()
    ball.reset()
    drawScreen(screen)
    pygame.display.flip()


gameState = 0


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

            
    clock.tick(fps)

    if gameState == 0:
        ballSpeedX = 0
        menu(screen)
        playGame = pygame.Rect(width/3, 3*height/5, width/3, height/5)
        mouse = pygame.mouse.get_pos()
        left, _, right = pygame.mouse.get_pressed()
        if playGame.collidepoint(mouse) and left == 1:
            ballSpeedX = ballOrgSpeedX
            gameState = 1

    elif gameState == 1:
        drawScreen(screen)

    # creating and setting keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and p1.y > 0:
        p1.y -= racketSpeed
    if keys[pygame.K_s] and p1.y + p1.height < height:
        p1.y += racketSpeed

    if keys[pygame.K_UP] and p2.y > 0:
        p2.y -= racketSpeed
    if keys[pygame.K_DOWN] and p2.y + p2.height < height:
        p2.y += racketSpeed

    # setting ball movement
    ball.x += ballSpeedX
    ball.y += ballSpeedY

    if ball.y + ballRadius > height or ball.y - ballRadius < 0:
        ballSpeedY *= -1
    if ballSpeedX < 0:
        if ball.y >= p1.y and ball.y <= p1.y + p1.height:
            if ball.x - ball.radius - ballSpeedY <= p1.x + p1.width:
                ballSpeedX *= -1
                middleY = p1.y + p1.height/2
                differenceY = middleY - ball.y
                decreasae = (p1.height/2) / ballMaxSpeed
                ySpeed = differenceY / decreasae
                ballSpeedY = -1 * ySpeed
    if ballSpeedX > 0:
        if ball.y >= p2.y and ball.y <= p2.y + p2.height:
            if ball.x + ball.radius + ballSpeedX >= p2.x:
                ballSpeedX *= -1
                middleY = p2.y + p2.height/2
                differenceY = middleY - ball.y
                decreasae = (p2.height/2) / ballMaxSpeed
                ySpeed = differenceY / decreasae
                ballSpeedY = -1 * ySpeed
    

    # goal control for p1
    if ball.x + ballRadius + ballSpeedX > width:
        p1Score += 1
        if p1Score < finalScore:
            resetGame(screen)
            time.sleep(1)
        ballSpeedX = ballOrgSpeedX
        ballSpeedY = 0
        ball.reset()
        
    # goal control for p2
    if ball.x - ballRadius - ballSpeedX < 0:
        p2Score += 1
        if p2Score < finalScore:
            resetGame(screen)
            time.sleep(1)
        ballSpeedX = ballOrgSpeedX * -1
        ballSpeedY = 0
        ball.reset()
    

    # end game screen
    p1WonText = wonFont.render("P1 WON!", 1, "white")
    p2WonText = wonFont.render("P2 WON!", 1, "white")
    pressSpace = playFont.render("Press space for main menu", 1, "white")

    if p1Score >= finalScore:
        screen.blit(p1WonText, (width/2-p1WonText.get_width()/2, height/2-p1WonText.get_height()/2))
        screen.blit(pressSpace, (width/2 - pressSpace.get_width()/2, 5*height/6 - pressSpace.get_height()/2))
        ballSpeedX = 0
        ballSpeedY = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            p1Score = p2Score = 0
            resetGame(screen)
            gameState = 0

    if p2Score >= finalScore:
        screen.blit(p2WonText, (width/2-p2WonText.get_width()/2, height/2-p2WonText.get_height()/2))
        screen.blit(pressSpace, (width/2 - pressSpace.get_width()/2, 5*height/6 - pressSpace.get_height()/2))
        ballSpeedX = 0
        ballSpeedY = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            p1Score = p2Score = 0
            resetGame(screen)
            gameState = 0


    pygame.display.flip()
