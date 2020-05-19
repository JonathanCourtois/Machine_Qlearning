# -*- coding: utf-8 -*-
"""
Created on Tue May 12 19:47:33 2020

Game Name : Submarine Game

Version : 
    - V.0.0.1 "Add grid deplacement" 2020
    - V.0.0.2 "Add Win objectif" 2020
    - V.0.0.3 "random playing" 2020
    - V.0.0.4 "IA base work and rebuild game as class, mlp can play the game" 2020

@author: Jonathan C
"""
# %% Import section
import pygame
import numpy as np
import torch as th
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
        # Variable for score
        self.displayTime = False # ~18 ms / loop
        self.actionEach = 1
        self.count_turn = 0
        self.scoreEvolution = []
        self.score = th.zeros(1,requires_grad=True)
    
    def updateScore(self, player, signal):
        # distance between signal and player
        dist = np.sum(np.abs(np.array(signal.position)-np.array(player.position)))
        self.score = self.score + self.count_turn + (3-player.life)*10 + dist
        self.scoreEvolution.append(self.score)
        
    def background(self, color):
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
        
# %% neuronal model  preconstruct MLP
class MLP(th.nn.Module):
    def __init__(self):
        super(MLP, self).__init__()
        # network parameter
        self.step = 0.1
        self.nb_hidden= 50
        self.outputChoice = 5
        # layers creation
        # input : [player.x,player.y,signal.x,signal.y] : 4       
        self.c1 = th.nn.Linear(4,self.nb_hidden).double()
        self.c2 = th.nn.Linear(self.nb_hidden,self.outputChoice).double()
        # output : [up, down, left, right, sonar] : 5
        # optimizer
        self.optimizer = th.optim.SGD(self.parameters(), lr = self.step)
        # input memories
        self.inputList = []
        
    def forward(self,x):
        # do a move
        y1 = th.relu(self.c1(th.tensor(np.array(x,dtype=float),requires_grad=True)))
        y2 = th.softmax(self.c2(y1),0)
        # chosing the highest probability choice
        y2 = y2.detach().numpy()
        chosenActionIndex = int(y2.argmax())
        # check if the proba is up to 0.6 else random mouvement
        print(y2[chosenActionIndex])
        if (y2[chosenActionIndex] < 0.96):
            chosenActionIndex = np.random.randint(self.outputChoice);
            
        return chosenActionIndex
    
    def learnGame(self, n = 3):
        scoreEvolution = []
        
        for i in range(n):
            # launching game
            successes, failures = pygame.init()
            print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))
            game = underwater()
            
            game.gameLoop(IA=True,mlp=self)
            
            loss = game.window.score
            
            loss.backward()
            # correcion avec optimiseur
            self.optimizer.step()
            print(self.parameters())
            for P in self.parameters():
                print()
                print(P)
                P.grad.data.zero_()
            score = loss.detach.numpy()
            scoreEvolution.append(score)
        return scoreEvolution
    
    def Play(self):
        # launching game
        successes, failures = pygame.init()
        print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))
        game = underwater()
        game.gameLoop(IA=IA,mlp=self)
        print('score = {}'.format(game.window.score.detach().numpy()))
    
  
# %% Game 

class underwater() :
    def __init__(self):
        super().__init__()
        self.window = Window()
        self.player = Player()
        self.signal = Signal()
        self.boomb = Signal()
        # init player position
        self.objectContainer = {'player':self.player,
                               'signal':self.signal,
                               'boomb' :self.boomb,
                               }
        self.player.position = self.window.gridCoordinate[0,0]

    # Game function
    def moveUp(self):
        self.player.position[1] -= 1 # go up 
        
    def moveDown(self):
        self.player.position[1] += 1 # go down 
        
    def moveLeft(self):
        self.player.position[0] -= 1 # go left
        self.player.direction = "left"
        
    def moveRight(self):
        self.player.position[0] += 1 # go right
        self.player.direction = "right"
        
    def sonar(self):
        print("bing")
                   
    def gameLoop(self,IA = False , mlp = None):
        running = True
        while running:  
            startTime = time.time()
            # Fill the screen with background color.
            self.window.background(BLACK) 
            # draw background grid
            self.window.drawGrid()
            
            
            action = {0 : self.moveUp,
                      1 : self.moveDown,
                      2 : self.moveLeft,
                      3 : self.moveRight,
                      4 : self.sonar,
                }
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        action[0]()
                        
                    elif event.key == pygame.K_s:
                        action[1]()
                        
                    elif event.key == pygame.K_a:
                        action[2]()
                        
                    elif event.key == pygame.K_d:
                        action[3]()
                        
            # easy win template:
            # if (alternate == 0  ):
            #     player.position[0] += 1 # go right
            #     alternate = 1
            # else:
            #     player.position[1] += 1 # go down
            #     alternate = 0
            
            #### IA PART ####
            if(IA and self.window.count_turn % self.window.actionEach == 0): 
                # input : [player.x,player.y,signal.x,signal.y] : 4
                x = [self.player.position[0],
                     self.player.position[1],
                     self.signal.position[0],
                     self.signal.position[1]]
                
                mlp.inputList.append(x)
                
                nb = mlp.forward(x)
                action[nb]()
            
            #### END IA ####
                        
            for o in self.objectContainer:
                self.objectContainer[o].update(self.window.gridCoordinate)
                
            if (self.player.rect.colliderect(self.signal.rect)):
                    running = False
                    print("You win !")
            else :
                self.window.screen.blit(self.player.image, self.player.rect)
                self.window.screen.blit(self.signal.image, self.signal.rect)
               
                pygame.display.update()  # Or pygame.display.flip()
           
            # increment turn count
            self.window.count_turn += 1 
            # update score
            self.window.updateScore(self.player,self.signal)
            
            if (self.window.displayTime):
                print(" --- %s seconds --- " % (time.time() - startTime))
                
        # END OF THE LOOP #
        print("Exited the game loop. Game will quit...")
        pygame.quit()  # Not actually necessary since the script will exit anyway.
        print(self.window.count_turn)
    
# %% try IA
mlp = MLP()
mlp.Play()