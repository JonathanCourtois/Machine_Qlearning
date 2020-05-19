# -*- coding: utf-8 -*-
"""
Created on Tue May 12 19:47:33 2020

Game Name : Submarine Game

Version : 
    - V.0.0.1 "Add grid deplacement" 2020
    - V.0.0.2 "Add Win objectif" 2020
    - V.0.0.3 "random playing" 2020

@author: Jonathan C
"""
# %% Import section
import pygame
import numpy as np
import time


# %% Option control section
IA = True

# %% Game Init
successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

displayWidth = 900
displayHeight = 600

infoPanelWidth = 200
#screen = pygame.display.set_mode((displayWidth, displayHeight))
clock = pygame.time.Clock()
FPS = 60

# color def
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (135, 135, 135)


# import submarine image
submarineImg = []
for i in range(-1,4,1):
    submarineImg.append(pygame.image.load('submarineV'+str(i)+'.PNG'))
for i in range(len(submarineImg)):
    submarineImg[i] = pygame.transform.scale(submarineImg[i], (int((displayWidth-infoPanelWidth)/10), int(displayHeight/10)))
 
# import Signal image
signalImg = pygame.image.load('signal3.PNG')
signalImg = pygame.transform.scale(signalImg, (int((displayWidth-infoPanelWidth)/10), int(displayHeight/10)))
    

# %% Class declaration
class Window():         
    def __init__(self):
        super().__init__()
        self.width = displayWidth-infoPanelWidth
        self.height = displayHeight
        self.gridWidth = int(self.width/10)
        self.gridHeight = int(self.height/10)
        self.FPS = 60
        self.screen = pygame.display.set_mode((self.width+infoPanelWidth, self.height))
        self.gridCoordinate = []
        self.gridInit()
    
    def background(self,color):
        self.screen.fill(color)  # Fill the screen with background color.
            
            
    def gridInit(self): # Init the array of coordinates
        self.gridCoordinate = []
        for c in range(0,self.width,self.gridWidth):
            for l in range(0,self.height,self.gridHeight):
                self.gridCoordinate.append([c,l-2])
        # The array contain the center of each box in shape 10*10*2
        self.gridCoordinate = np.array(self.gridCoordinate).reshape(10,10,2)
        
    def drawGrid(self,color = GRAY):
        # draw grid in background
        for i in range(0,self.width+self.gridWidth,self.gridWidth):
            pygame.draw.line(self.screen,color,(i-1,-1),(i-1,self.height),2)
        for i in range(0,self.height+self.gridHeight,self.gridHeight):
            pygame.draw.line(self.screen,color,(-1,i-1),(self.width,i-1),2)
        
        
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.life = 3
        self.image = submarineImg[self.life+1]
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        #self.rect.move_ip([200,200])
        self.position = [0, 0]
        self.coordinate = [0, 0]
        self.imageOriention = "left"
        self.direction = "left"

    def orientation(self):
        # change image according to life
        self.image = submarineImg[self.life+1]
        self.imageOriention = "left"
        if self.imageOriention != self.direction:
            self.image = pygame.transform.flip(self.image,True,False)
            self.imageOriention = self.direction
            
    def border(self):
        # fix border limit
        for i in range(len(self.position)):
            if (self.position[i] > 9):
                self.position[i] = 9
            if (self.position[i] < 0):
                self.position[i] = 0
                
    def update(self,grid):
        # check border limit
        self.border()
        # change coordinate
        self.coordinate = grid[self.position[0],self.position[1],:]
        self.rect = pygame.rect.Rect(self.coordinate[0], self.coordinate[1], 30, 30)
        # change orientation
        self.orientation()
 
class Signal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = signalImg
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.position = [9, 9]
        self.coordinate = [0, 0]
        
    def update(self,grid): # change coordinate
        self.coordinate = grid[self.position[0],self.position[1],:]
        self.rect = pygame.rect.Rect(self.coordinate[0], self.coordinate[1], 30, 30)

# %% Game var init
        
window = Window()
player = Player()
signal = Signal()
boomb = Signal()
# init player position
objectContainer = {'player':player,
                   'signal':signal,
                   'boomb' :boomb,
                   }
player.position = window.gridCoordinate[0,0]


# %% Game function
def moveUp(player,window):
    player.position[1] -= 1 # go up 
    
def moveDown(player,window):
    player.position[1] += 1 # go down 
    
def moveLeft(player,window):
    player.position[0] -= 1 # go left
    player.direction = "left"
    
def moveRight(player,window):
    player.position[0] += 1 # go right
    player.direction = "right"
    
def sonar(player,window):
    print("bing")
                    
def gameLoop(IA = False):
    running = True
    alternate = 2
    displayTime = False # ~18 ms / loop
    actionEach = 1
    count_turn = 0
    count_action = 0
    while running:  
        startTime = time.time()
        # Returns milliseconds between each call to 'tick'. The convert time to seconds
        dt = clock.tick(FPS) / 500
        # Fill the screen with background color.
        window.background(BLACK) 
        # draw background grid
        window.drawGrid()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    moveUp(player,window)
                    
                elif event.key == pygame.K_s:
                    moveDown(player,window)
                    
                elif event.key == pygame.K_a:
                    moveLeft(player,window)
                    
                elif event.key == pygame.K_d:
                    moveRight(player,window)
        # without window game :
        # easy win template:
        # if (alternate == 0  ):
        #     player.position[0] += 1 # go right
        #     alternate = 1
        # else:
        #     player.position[1] += 1 # go down
        #     alternate = 0
        
        #### IA PART ####
        if(IA and count_turn%actionEach == 0): 
            action = {0 : moveUp,
                      1 : moveDown,
                      2 : moveLeft,
                      3 : moveRight,
                      4 : sonar,
                }
            nb = np.random.randint(5);
            action[nb](player,window)
            count_action += 1
        count_turn += 1
        
        #### END IA ####
                    
        for o in objectContainer:
            objectContainer[o].update(window.gridCoordinate)
            
        if (player.rect.colliderect(signal.rect)):
                running = False
                print("You win !")
        else :
            window.screen.blit(player.image, player.rect)
            window.screen.blit(signal.image, signal.rect)
           
            pygame.display.update()  # Or pygame.display.flip()
        
        if (displayTime):
            print(" --- %s seconds --- " % (time.time() - startTime))
    print("Exited the game loop. Game will quit...")
    pygame.quit()  # Not actually necessary since the script will exit anyway.
    print(count_action)
    print(count_turn)
  
# %% main
gameLoop(IA=IA)