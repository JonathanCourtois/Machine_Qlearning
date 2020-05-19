# -*- coding: utf-8 -*-
"""
Created on Tue May 12 19:47:33 2020

Game Name : Submarine Game

Version : 
    - V.0.0.1 "Add grid deplacement" 2020
    - V.0.0.2 "Add Win objectif" 2020
    - V.0.0.3 "random playing" 2020
    - V.0.0.4 "IA base work and rebuild game as class, mlp can play the game" 2020
    - V.0.0.5 "Implementing Qlearning " 2020
    - V.0.1 "Changing score method and reward " 2020

@author: Jonathan C
"""
# %% Import section
import pygame
import numpy as np
import torch as th
import pylab as pl
import time
from deepQ import Agent


# %% Option control section
IA = True

# %% Game Init
successes, failures = pygame.init()
pygame.display.set_caption('Underwater')
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
    submarineImg.append(pygame.image.load('../image/objects/submarineV'+str(i)+'.PNG'))
    submarineImg[i+1] = pygame.transform.scale(submarineImg[i+1], (int((displayWidth-infoPanelWidth)/10), int(displayHeight/10)))
 
# import Signal image
signalImg = []
for i in range(0,4,1):
    signalImg.append(pygame.image.load('../image/objects/signal'+str(i)+'.PNG'))
    signalImg[i] = pygame.transform.scale(signalImg[i], (int((displayWidth-infoPanelWidth)/10), int(displayHeight/10))) 

# import Mine image
mineImg = []
for i in range(0,2,1):
    mineImg.append(pygame.image.load('../image/objects/mine'+str(i)+'.PNG'))
    mineImg[i] = pygame.transform.scale(mineImg[i], (int((displayWidth-infoPanelWidth)/10), int(displayHeight/10)))

# %% Class declaration
class Window():         
    def __init__(self):
        super().__init__()
        self.width = displayWidth-infoPanelWidth
        self.height = displayHeight
        self.gridWidth = int(self.width/10)
        self.gridHeight = int(self.height/10)
        self.FPS = 60
        self.screenState = False # false = window off, True = window on
        self.screen = None
        self.gridCoordinate = []
        self.gridInit()
        # Variable for score
        self.displayTime = False # ~18 ms / loop
        
    def toggle(self):
        if(self.screenState):
            self.screenState = False
            self.screen = None
        else : 
            self.screenState = True
            self.screen = pygame.display.set_mode((self.width+infoPanelWidth, self.height))
        
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
        self.images = submarineImg
        self.image = submarineImg[self.life+1]
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        #self.rect.move_ip([200,200])
        self.position = [0, 0]
        self.coordinate = [0, 0]
        self.imageOriention = "left"
        self.direction = "left"
        self.mine_map = np.zeros((10,10),dtype=int)
        self.sonar_map = np.zeros((10,10),dtype=int)

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
                
    def update(self,game):
        grid = game.window.gridCoordinate
        # check border limit
        self.border()
        # change coordinate
        self.coordinate = grid[self.position[0],self.position[1],:]
        self.rect = pygame.rect.Rect(self.coordinate[0], self.coordinate[1], 30, 30)
        # change orientation
        self.orientation()
        if (self.life < 0):
            print('Game Over, You die !')
            game.endFlag = True
 
class Signal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = signalImg
        self.image = signalImg[0]
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.position = [9, 9]
        self.coordinate = [0, 0]
        
    def update(self,game): # change coordinate
        grid = game.window.gridCoordinate
        self.coordinate = grid[self.position[0],self.position[1],:]
        self.rect = pygame.rect.Rect(self.coordinate[0], self.coordinate[1], 30, 30)
        frame_ctr = game.count_turn % game.window.FPS
        if (frame_ctr == 0):
            self.images.append(self.images.pop(0))
            self.image = signalImg[0]
            
 
class Mine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = mineImg
        self.image = mineImg[0]
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.position = [5,5]
        self.coordinate = [0, 0]
        # animation
        self.blow_up = False
        self.animation_time = 0
        self.animation_limit = 3
        self.hidden = True
    
    def spawn(self, games):
        wrong_position = True
        while(wrong_position):
            x = np.random.randint(10)
            y = np.random.randint(10)
            if(( x != 0 or y != 0) and ( x != 9 or y != 9)):
                wrong_position = False
            
            for m in games.mine:
                if (x == m.position[0] and y == m.position[1]):
                    wrong_position = True
                    
        self.position = [x,y]
        
    def update(self,game): # change coordinate
        grid = game.window.gridCoordinate
        self.coordinate = grid[self.position[0],self.position[1],:]
        self.rect = pygame.rect.Rect(self.coordinate[0], self.coordinate[1], 30, 30)
        if (self.blow_up):
            frame_ctr = game.count_turn % game.window.FPS
            if (frame_ctr == 0):
                self.hidden = False
                self.animation_time += 1
                if(self.animation_time > self.animation_limit):
                    game.mine.remove(self)
            
  
# %% Game 

class underwater() :
    def __init__(self):
        super().__init__()
        self.window = Window()
        self.player = [Player()]
        self.signal = [Signal()]
        self.mine = []
        self.mine_nb = 9
        for i in range(self.mine_nb):
            m = Mine()
            m.spawn(self)
            self.mine.append(m)
        # init player position
        self.objectContainer = {'player':self.player,
                               'signal':self.signal,
                               'boomb' :self.mine,
                               }
        self.player[0].position = self.window.gridCoordinate[0,0]
        # score
        self.win_flag = False
        self.count_turn = 0
        self.actionEach = 1
        self.scoreEvolution = []
        self.score = th.zeros(1,requires_grad=True)
        # define actions
        self.action = {0 : self.moveUp,
                      1 : self.moveDown,
                      2 : self.moveLeft,
                      3 : self.moveRight,
                      4 : self.sonar,
                }
        
        # State and memory
        self.last_player_position = [0,0]
        self.endFlag = False
        self.old_distance_factor = 0
        self.old_life_factor = 0 
        self.berserker = False
        self.turn_factor = 0
    
    def updateScore(self):
        # distance between signal and player
        # 1 > dist_factor > 0 1 on signal 0 at th opposite 
        dist = np.sum(np.abs(np.array(self.signal[0].position)-np.array(self.player[0].position)))
        dist_factor = 1-(dist/18)
        reward_dist_factor = dist_factor - self.old_distance_factor
        self.old_distance_factor = dist_factor
        
        #life factor could deacrease to 0 if losing life
        life_factor = -(3-self.player[0].life)/4
        if( life_factor - self.old_life_factor != 0):
            reward_life_factor = life_factor
        else:
            reward_life_factor = 0        
        self.old_life_factor = life_factor
        
        # turn factor could decrease th reward to 0.2 if to loong
        if(self.count_turn % 500 == 0):
            if(self.score > 0.2):
                self.turn_factor -= 0 #0.01
        
        
        # wall berserker bug <0
        berserker_factor = 0
        if(self.berserker == True and self.score > 0.1):
            berserker_factor = -0.01
            print('berserker + [{},{}]'.format(self.player[0].position[0],self.player[0].position[1]))
            self.berserker = False
    
        self.score = round(dist_factor  + reward_life_factor + berserker_factor + self.turn_factor)
        if (self.score < 0):
            self.score = 0
        
        #print('score {}, turn {}'.format(self.score,self.turn_factor))
        if (self.player[0].life < 0 ):
            self.score = 0
            
        print('score %.2f' % self.score)
        self.scoreEvolution.append(self.score)
        
    # Game function
    def moveUp(self):
        print('Up + [{},{}]'.format(self.player[0].position[0],self.player[0].position[1]))
        if(self.player[0].position[1] == 0):
            self.berserker = True
        self.player[0].position[1] -= 1 # go up
        self.last_player_position = list(self.player[0].position)
        
    def moveDown(self):
        print('Down + [{},{}]'.format(self.player[0].position[0],self.player[0].position[1]))
        if(self.player[0].position[1] == 9):
            self.berserker = True
        self.player[0].position[1] += 1 # go down
        self.last_player_position = list(self.player[0].position)
        
        
    def moveLeft(self):
        print('Left + [{},{}]'.format(self.player[0].position[0],self.player[0].position[1]))
        if(self.player[0].position[0] == 0):
            self.berserker = True
        self.player[0].position[0] -= 1 # go left
        self.last_player_position = list(self.player[0].position)
        self.player[0].direction = "left"
        
    def moveRight(self):
        print('Right + [{},{}]'.format(self.player[0].position[0],self.player[0].position[1]))
        if(self.player[0].position[0] == 9):
            self.berserker = True
        self.player[0].position[0] += 1 # go right
        self.player[0].direction = "right"
        self.last_player_position = list(self.player[0].position)
        
        
    def sonar(self):
        if (self.player[0].sonar_map[self.player[0].position[0],
                                     self.player[0].position[1]] == 1):
            self.berserker = True
        self.player[0].sonar_map[self.player[0].position[0],
                                 self.player[0].position[1]] = 1
        
        x_s = self.player[0].position[0]-2
        x_e = self.player[0].position[0]+2
        y_s = self.player[0].position[1]-2
        y_e = self.player[0].position[1]+2
        print("bing")
        for c in range(x_e-x_s+1):
            if (x_s + c > -1 and x_s + c < 10):
                for l in range(y_e-y_s+1):
                    if (y_s + l > -1 and y_s + l < 10):
                        for m in self.mine:
                            if ([c+x_s,l+y_s] == m.position):
                                m.hidden = False
                                print("bang")
                                self.player[0].mine_map[l+y_s,c+x_s]=1
        
        
                   
    def start(self,IA = False , agent = None):
        self.endFlag = False
        while not self.endFlag:  
            startTime = time.time()
            # Fill the screen with background color.
            self.window.background(BLACK) 
            # draw background grid
            self.window.drawGrid()
            action_id = 5
            # IA assist
            observation = self.observation()# IA command
            if(IA):
                action_id = agent.choose_action(observation)
                self.action[action_id]()
            #palyer command
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.endFlag = True
                    
                elif event.type == pygame.KEYDOWN:
                    moove = True
                    if event.key == pygame.K_w:
                        action_id = 0
                        self.action[action_id]()
                        
                    elif event.key == pygame.K_s:
                        action_id = 1
                        self.action[action_id]()
                        
                    elif event.key == pygame.K_a:
                        action_id = 2
                        self.action[action_id]()
                        
                    elif event.key == pygame.K_d:
                        action_id = 3
                        self.action[action_id]()
                        
                    elif event.key == pygame.K_e:
                        action_id = agent.choose_action(observation)
                        print('IA hint : use ' + str(self.action[action_id]))
                        moove = False
                        
                    elif event.key == pygame.K_SPACE:
                        action_id = 4
                        self.action[action_id]()
                    
                    if(moove):
                        agent.store_transition(observation, action_id, self.score, 
                                               self.observation(), self.endFlag)
                        agent.learn()
                        
            for o_list in self.objectContainer:
                for o in self.objectContainer[o_list]:
                    o.update(self)
                    
                
            if (self.player[0].rect.colliderect(self.signal[0].rect)):
                    self.endFlag = True
                    self.win_flag = True  
                    print("You win !")

            else :
                for m in self.mine:
                    if (self.player[0].rect.colliderect(m.rect) and not m.blow_up):
                            print("Boum !")
                            m.image = m.images[1]
                            self.player[0].life -= 1
                            m.blow_up = True
                            self.player[0].mine_map[m.position[1]][m.position[0]] = 0
                            
                        
                for o_list in self.objectContainer:
                    for o in self.objectContainer[o_list]:
                        if (o.__class__.__name__ == 'Mine'):
                            if (not o.hidden):
                                self.window.screen.blit(o.image, o.rect)
                        else :
                            self.window.screen.blit(o.image, o.rect)
               
                pygame.display.update()  # Or pygame.display.flip()
           
            # increment turn count
            self.count_turn += 1 
            # update score
            self.updateScore()
            
            if (self.window.displayTime):
                print(" --- %s seconds --- " % (time.time() - startTime))  
                
        # END OF THE LOOP #
        print("Exited the game loop. Game will quit...")
        pygame.quit()  # Not actually necessary since the script will exit anyway.
        print('count turn = {}'.format(self.count_turn))
        print('score = {}'.format(self.score))
        pl.figure(0)
        pl.ion()
        pl.plot(self.scoreEvolution)
        pl.title('game reward evolution')
        pl.show()
        return agent
    
    def observation(self):
        obs = [float(self.player[0].position[0]),float(self.player[0].position[1]),
            float(self.player[0].life),
            float(self.signal[0].position[0]),float(self.signal[0].position[1])]
        obs = obs + list(self.player[0].mine_map.reshape(-1))
        return obs
    
    def step(self, action_number):
        
        # choose action
        self.action[action_number]()
        
        # maj window
        # Fill the screen with background color.
        self.window.background(BLACK) 
        # draw background grid
        self.window.drawGrid()
        for o_list in self.objectContainer:
            for o in self.objectContainer[o_list]:
                o.update(self)
            
        if (self.player[0].rect.colliderect(self.signal[0].rect)):
                self.endFlag = True
                self.win_flag = True  
                print("You win !")

        else :
            for m in self.mine:
                if (self.player[0].rect.colliderect(m.rect) and not m.blow_up):
                        print("Boum !")
                        m.image = m.images[1]
                        self.player[0].life -= 1
                        m.blow_up = True
                        self.player[0].mine_map[m.position[1]][m.position[0]] = 0
                    
            for o_list in self.objectContainer:
                for o in self.objectContainer[o_list]:
                    if (o.__class__.__name__ == 'Mine'):
                        if (not o.hidden):
                            self.window.screen.blit(o.image, o.rect)
                    else :
                        self.window.screen.blit(o.image, o.rect)
           
            pygame.display.update()  # Or pygame.display.flip()
       
        # increment turn count
        self.count_turn += 1 
        # update score
        self.updateScore()
        
        return [self.observation(), self.score, self.endFlag, {}]
    
# # %% try IA
# mlp = MLP()
# mlp.learnGame(n=2)

# pl.figure(0)
# pl.scatter(np.arange(len(mlp.scoreEvolution)),mlp.scoreEvolution)
      
# %% manual Play
manual_play = True
load_agent = True
path = r'../DeepQ'
if (manual_play):
    agent = Agent(gamma=0.99, epsilon = 1.0, batch_size=1, n_actions = 5,
                  eps_end=0.01, input_dims=[105], lr=0.001)
    if (load_agent):
        agent.load(path)
    game = underwater()
    game.window.toggle()
    agent = game.start(IA = False , agent = agent)
    pygame.quit()
    # agent.save(path)
    
IA_play = False
load_agent = False
if (IA_play):
    agent = Agent(gamma=0.99, epsilon = 1.0, batch_size=1, n_actions = 5,
                  eps_end=0.01, input_dims=[105], lr=0.001)
    if (load_agent):
        agent.load(path)
    game = underwater()
    game.window.toggle()
    agent = game.start(IA = True , agent = agent)
    pygame.quit()
    #agent.save(path)

# %% Try Deep Q
train_deep_Q = False
load_agent = True
if (train_deep_Q):
    scores, eps_history, win, lifes= [], [], [], []
    n_games = 100
    
    agent = Agent(gamma=0.99, epsilon = 1, batch_size=10, n_actions = 5,
                  eps_end=0.01, input_dims=[105], lr=0.001)
    
    if (load_agent):
        agent.load(path)
        
        
    for i in range(n_games):
        pygame.init()
        pygame.display.set_caption('Underwater '+str(i)+'/'+str(n_games)+' game')
        score = 0
        done = False
        game = underwater()
        game.window.toggle()
        # input : [player.x,player.y, player.life ,signal.x,signal.y,mine_map] : 4+10*10
        observation = game.observation()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = game.step(action)
            score = reward
            agent.store_transition(observation, action, reward, observation_, done)
            agent.learn()
            observation = observation_
        # END WHILE
        scores.append(score)
        eps_history.append(agent.epsilon)
        avg_score = np.mean(scores[:])
        pl.figure(0)
        pl.plot(game.scoreEvolution, label='game'+str(i))
        pl.title('game reward evolution')
        pygame.quit()
        
        print('episode', i, 'score %.2f' % score,
                  'average score %.2f' % avg_score,
                  'epsilon %.2f' %agent.epsilon)
    agent.save(path)
    print('agent saved')
        
    # %% plot
    pl.figure(1)
    pl.title('agent gamma {}, batch_size {}, lr {}'.format(agent.gamma,agent.batch_size,agent.lr))
    pl.plot(scores)
    pl.plot(eps_history)
    pl.ylim(-1000,100)