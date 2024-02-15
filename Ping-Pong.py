import pygame
import time

pygame.init()

sizeMultip = 45

width = 16*sizeMultip
height = 9*sizeMultip

fps = 60

racketSpeed = 4
ballSpeedX = 5
ballOrgSpeedX = ballSpeedX
ballSpeedY = 0
ballMaxSpeed = 7

clock = pygame.time.Clock()

racketWidth = 10
racketHeight = sizeMultip*5/3
ballRadius = 7

p1Score, p2Score = 0, 0

scoreFont = pygame.font.SysFont("comicsans", 50)
wonFont = pygame.font.SysFont("comicsans", 150)
winScore = 3


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong")

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


p1 = Racket(10, height/2-racketHeight/2, racketWidth, racketHeight)
p2 = Racket(width-10-racketWidth, height/2-racketHeight/2, racketWidth, racketHeight)
ball = Ball(width/2, height/2, ballRadius)

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

def resetGame(screen):
    p1.reset()
    p2.reset()
    ball.reset()
    drawScreen(screen)
    pygame.display.flip()
    time.sleep(1)

while True:
    clock.tick(fps)

    drawScreen(screen)

    p1WonText = wonFont.render("P1 WON!", 1, "white")
    p2WonText = wonFont.render("P2 WON!", 1, "white")

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and p1.y > 0:
        p1.y -= racketSpeed
    if keys[pygame.K_s] and p1.y + p1.height < height:
        p1.y += racketSpeed

    if keys[pygame.K_UP] and p2.y > 0:
        p2.y -= racketSpeed
    if keys[pygame.K_DOWN] and p2.y + p2.height < height:
        p2.y += racketSpeed


    ball.x += ballSpeedX
    ball.y += ballSpeedY

    if ball.y + ballRadius > height or ball.y - ballRadius < 0:
        ballSpeedY *= -1
    if ballSpeedX < 0:
        if ball.y >= p1.y and ball.y <= p1.y + p1.height:
            if ball.x - ball.radius - ballSpeedY <= p1.x + p1.width:
                ballSpeedX *= -1.05
                middleY = p1.y + p1.height/2
                differenceY = middleY - ball.y
                decreasae = (p1.height/2) / ballMaxSpeed
                ySpeed = differenceY / decreasae
                ballSpeedY = -1 * ySpeed
    if ballSpeedX > 0:
        if ball.y >= p2.y and ball.y <= p2.y + p2.height:
            if ball.x + ball.radius + ballSpeedX >= p2.x:
                ballSpeedX *= -1.05
                middleY = p2.y + p2.height/2
                differenceY = middleY - ball.y
                decreasae = (p2.height/2) / ballMaxSpeed
                ySpeed = differenceY / decreasae
                ballSpeedY = -1 * ySpeed
    

    if ball.x + ballRadius + ballSpeedX > width:
        p1Score += 1
        resetGame(screen)
        ballSpeedX = ballOrgSpeedX
        ballSpeedY = 0
        
    if ball.x - ballRadius - ballSpeedX < 0:
        p2Score += 1
        resetGame(screen)
        ballSpeedX = ballOrgSpeedX * -1
        ballSpeedY = 0

    
    if p1Score >= 3:
        screen.blit(p1WonText, (width/2-p1WonText.get_width()/2, height/2-p1WonText.get_height()/2))
        ballSpeedX = 0
        ballSpeedY = 0

    if p2Score >= 3:
        screen.blit(p2WonText, (width/2-p1WonText.get_width()/2, height/2-p1WonText.get_height()/2))
        ballSpeedX = 0
        ballSpeedY = 0



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break


    pygame.display.update()