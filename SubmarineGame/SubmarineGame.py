# -*- coding: utf-8 -*-
"""
Created on Tue May 12 19:47:33 2020

@author: Jonathan C
"""

import pygame

successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

displayWidth = 800
displayHeight = 600

#screen = pygame.display.set_mode((displayWidth, displayHeight))
clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

submarineImg = pygame.image.load('submarineV3.PNG')
submarineImg = pygame.transform.scale(submarineImg, (int(displayWidth/10), int(displayHeight/10)))
    
x = (displayWidth * 0.45)
y = (displayHeight * 0.8)

class Window():
    def __init__(self):
        super().__init__()
        self.width = displayWidth
        self.height = displayHeight
        self.gridWidth = int(self.width/10)
        self.gridHeight = int(self.height/10)
        self.FPS = 60
        self.screen = pygame.display.set_mode((self.width, self.height))
    
    def background(self,color):
        self.screen.fill(color)  # Fill the screen with background color.
        
    def grid(self):
        for i in range(0,self.width+self.gridWidth,self.gridWidth):
            pygame.draw.line(self.screen,WHITE,(i-1,-1),(i-1,self.height),2)
        for i in range(0,self.height+self.gridHeight,self.gridHeight):
            pygame.draw.line(self.screen,WHITE,(-1,i-1),(self.width,i-1),2)
        
        
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = submarineImg
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.rect.move_ip([200,200])
        self.velocity = [0, 0]
        self.imageOriention = "left"
        self.direction = "left"

    def orientation(self):
        if self.imageOriention != self.direction:
            self.image = pygame.transform.flip(self.image,True,False)
            self.imageOriention = self.direction
            
    def update(self):
        self.rect.move_ip(*self.velocity)
        self.orientation()


window = Window()
    
def gameLoop():
    player = Player()
    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Returns milliseconds between each call to 'tick'. The convert time to seconds.
        window.background(BLACK) # Fill the screen with background color.
        window.grid()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.velocity[1] = -200 * dt  # 200 pixels per second
                elif event.key == pygame.K_s:
                    player.velocity[1] = 200 * dt
                elif event.key == pygame.K_a:
                    player.velocity[0] = -200 * dt
                    player.direction = "left"
                elif event.key == pygame.K_d:
                    player.velocity[0] = 200 * dt
                    player.direction = "right"
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.velocity[1] = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    player.velocity[0] = 0
        
        player.update()
    
        window.screen.blit(player.image, player.rect)
        
        pygame.display.update()  # Or pygame.display.flip()
    
    print("Exited the game loop. Game will quit...")
    pygame.quit()  # Not actually necessary since the script will exit anyway.
    
gameLoop()