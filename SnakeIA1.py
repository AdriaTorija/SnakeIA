# importing libraries
from asyncio.windows_events import NULL
from cmath import pi
from contextlib import nullcontext
from re import X
from tarfile import BLOCKSIZE
from turtle import width
from webbrowser import get
import pygame
import time
import random
import math
import numpy as np

class Snake_game:
    
    #Basic Specs
    def __init__(self, window, width, height):
        self.snake_speed=5
        self.width=width
        self.heigth= height
        self.green= pygame.Color(0,255,0)
        self.red= pygame.Color(255,0,0)
        self.black= pygame.Color(0,0,0)
        self.white= pygame.Color(255,255,255)
        self.is_game_over=False
        self.ate=False
        #Init
        pygame.init()
        pygame.display.set_caption("IA Snake")
        self.window= window
        #Snake settings
        self.snake_pos= [250,250]
        self.snake_body= [[250,250],[300,250],[350,250]]

        #Fruit
        self.fruit= [random.randrange(1,(self.width//50))*50, random.randrange(1,(self.heigth//50))*50]
        self.fruit_spawn= True

        #Default direction
        self.direction= 2
        self.change_to=self.direction
        
        #Score
        self.score=0
        self.fps = pygame.time.Clock()

    # game over function
    def game_over(self):

        # creating font object my_font
        my_font = pygame.font.SysFont('times new roman', 30)
        
        #Set text
        game_over_surface = my_font.render('Score : ' + str(self.score), True, self.white)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.width/2, self.heigth/4)
        
        self.window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        quit()

    def show_score(self, choice,color,font,size):
        score_font= pygame.font.SysFont(font,size)
        display_surface= score_font.render('Score : '+str(self.score),True,color)

        text=display_surface.get_rect()
        self.window.blit(display_surface, text)
    
    def move(self):
         #Snake directions not posible
            if self.change_to== 0 and self.direction !=  1:
                self.direction = 0
            if self.change_to == 1 and self.direction != 0:
                self.direction = 1
            if self.change_to == 2 and self.direction != 3:
                self.direction= 2
            if self.change_to == 3 and self.direction != 2:
                self.direction= 3
            
            #Move of the snake
            if self.direction == 0:
                self.snake_pos[1] -= 50
            if self.direction == 1:
                self.snake_pos[1] += 50
            if self.direction == 2:
                self.snake_pos[0] -= 50
            if self.direction == 3:
                self.snake_pos[0] +=50
    
    #For the IA
    def changeDirection(self, newDirection):
        self.change_to= newDirection
        #print(self.change_to)


    def eat(self):
         #Snake Eating
        ate=False
        self.snake_body.insert(0, list (self.snake_pos))
        if self.snake_pos[0] == self.fruit[0] and self.snake_pos[1] == self.fruit[1]:
            self.score +=1
            self.fruit_spawn = False
            ate=True
        else:
            self.snake_body.pop()
        if not self.fruit_spawn:
            self.fruit= [random.randrange(1,(self.width//50))*50, random.randrange(1,(self.heigth//50))*50]
        self.fruit_spawn = True
    
        #Drawing in window Snake & Fruit
        self.window.fill(self.black)
        for x in self.snake_body:
            pygame.draw.rect(self.window, self.green, pygame.Rect(x[0],x[1],50,50))
        
        pygame.draw.rect(self.window, self.red, pygame.Rect(self.fruit[0],self.fruit[1],50,50))
        return ate
    #Game Over     
    def checkGameOver(self):
        #Out of bounds
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.width-50 or self.snake_pos[1] < 0 or self.snake_pos[1] > self.heigth-50:
            self.is_game_over=True
            #self.game_over()

        #Eat itself
        for x in self.snake_body[1:]:
            if x[0] == self.snake_pos[0] and x[1] ==self.snake_pos[1]:
                self.is_game_over=True
                #self.game_over(self)
    #Main

    def loop(self):
        self.ate=False
        self.move()
        self.ate=self.eat()
        self.checkGameOver()
        self.show_score(1,self.white,'times new roman', 15)
        pygame.display.update()
        self.fps.tick(self.snake_speed)
        return self.score



    def normalLoop(self):
        while True:
            #Keys events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_to= 0
                    if event.key == pygame.K_DOWN:
                        self.change_to =  1
                    if event.key == pygame.K_LEFT:
                        self.change_to = 2
                    if event.key == pygame.K_RIGHT:
                        self.change_to = 3
            self.move()
            self.eat()
            self.checkGameOver()
            self.show_score(1,self.white,'times new roman', 15)
            pygame.display.update()
            self.fps.tick(self.snake_speed)

    def distance_to_food(self):
        return abs(math.sqrt(math.pow(self.snake_pos[0]/50-self.fruit[0]/50,2)+math.pow(self.snake_pos[1]/50-self.fruit[1]/50,2)))

    def distance_to_food_score(self):
        return abs(10*math.sqrt(2)-math.sqrt(math.pow(self.snake_pos[0]/50-self.fruit[0]/50,2)+math.pow(self.snake_pos[1]/50-self.fruit[1]/50,2)))
        
    def distance_to_food_pos(self,snake_pos):
        return abs(10*math.sqrt(2)-math.sqrt(math.pow(snake_pos[0]/50-self.fruit[0]/50,2)+math.pow(snake_pos[1]/50-self.fruit[1]/50,2)))
    
    def moveRight(self):
        if self.direction==3:
            self.change_to=1
        elif self.direction==1 :
            self.change_to=2
        elif self.direction==2:
            self.change_to=0
        else: self.change_to=3


    def moveLeft(self):
        if self.direction==2:
            self.change_to=1
        elif self.direction==1:
            self.change_to=3
        elif self.direction==3:
            self.change_to=0
        else: self.change_to=2


    def checkGameOverMove(self,snake_pos):
        end=0
        if snake_pos[0] < 0 or snake_pos[0] > self.width-50 or snake_pos[1] < 0 or snake_pos[1] > self.heigth-50:
            end=-1
            
        #Eat itself
        for x in self.snake_body[1:]:
            if x[0] == snake_pos[0] and x[1] == snake_pos[1]:
                end=-1
        if snake_pos[0] == self.fruit[0] and snake_pos[1] == self.fruit[1]:
            end=1
        return end

    def getMove(self, direction):
        x=self.snake_pos[1]
        y=self.snake_pos[0]
        if direction == 0:
            x -= 50
        if direction == 1:
            x += 50
        if direction == 2:
            y -= 50
        if direction == 3:
            y +=50
        return (x,y)
    
    def getMovePlus(self, snake_pos, direction):
        x=snake_pos[1]
        y=snake_pos[0]
        if direction == 0:
            x -= 50
        if direction == 1:
            x += 50
        if direction == 2:
            y -= 50
        if direction == 3:
            y +=50
        return (x,y)
        
    def checkMoveRight(self,direction):
        if direction==3:
            change_to=1
        elif direction==1 :
            change_to=2
        elif direction==2:
            change_to=0
        else: change_to=3
        return change_to

    def checkMoveLeft(self,direction):
        if direction==2:
            change_to=1
        elif direction==1:
            change_to=3
        elif direction==3:
            change_to=0
        else: change_to=2
        return change_to
    
    def lowDirFruit(self, line, dim):
        low=False
        if self.snake_pos[line] <= dim/2:
            low=False
        return low

    

    '''
    Check if it goes left
    Check if it goes straight
    Check if it goes right
    Check angle
    '''
    def getInputs(self):
        out=[]
        out.append(self.checkGameOverMove(self.getMove(self.checkMoveLeft(self.direction))))
        out.append(self.checkGameOverMove(self.getMove(self.checkMoveRight(self.direction))))
        out.append(self.checkGameOverMove(self.getMove(self.direction)))
        #out.append(self.distance_to_food_pos(self.getMove(self.checkMoveLeft(self.direction))))
        #out.append(self.distance_to_food_pos(self.getMove(self.checkMoveRight(self.direction))))
        #out.append(self.distance_to_food_pos(self.getMove(self.direction)))
        RS=-1
        RR=-1
        LL=-1
        RL=-1
        LR=-1
        LS=-1
        SS=-1
        SR=-1
        SL=-1
        pLL=0
        pLR=0
        pLS=0
        pRL=0
        pRR=0
        pRS=0
        pSL=0
        pSR=0
        pSS=0
        if out[0] > -1 : 
            aux_dir= self.checkMoveLeft(self.direction)
            aux=self.getMovePlus(self.getMove(aux_dir),self.checkMoveLeft(aux_dir))
            LL=self.checkGameOverMove(aux)
            if LL >=0 : pLL= self.distance_to_food_pos(aux)

            aux=self.getMovePlus(self.getMove(aux_dir),self.checkMoveRight(aux_dir))
            LR=self.checkGameOverMove(aux)
            if LR >= 0: pLR= self.distance_to_food_pos(aux)

            aux=self.getMovePlus(self.getMove(aux_dir),aux_dir)
            LS=self.checkGameOverMove(aux)
            if LS >= 0: pLS= self.distance_to_food_pos(aux)

        if out[1] > -1:
            aux_dir= self.checkMoveRight(self.direction)
            aux=self.getMovePlus(self.getMove(aux_dir),self.checkMoveLeft(aux_dir))
            RL=self.checkGameOverMove(aux)
            if RL >= 0: pRL= self.distance_to_food_pos(aux)

            aux=self.getMovePlus(self.getMove(aux_dir),self.checkMoveRight(aux_dir))
            RR=self.checkGameOverMove(aux)
            if RR >= 0: pRR= self.distance_to_food_pos(aux)

            aux=self.getMovePlus(self.getMove(aux_dir),aux_dir)
            RS=self.checkGameOverMove(aux)
            if RS >= 0: pRS= self.distance_to_food_pos(aux)

        if out[2] > -1:
            aux=self.getMovePlus(self.getMove(self.direction),self.checkMoveLeft(self.direction))
            SL=self.checkGameOverMove(aux)
            if SL >= 0: pSL= self.distance_to_food_pos(aux)

            aux=self.getMovePlus(self.getMove(self.direction),self.checkMoveRight(self.direction))
            SR=self.checkGameOverMove(aux)
            if SR >= 0: pSR= self.distance_to_food_pos(aux)

            aux=self.getMovePlus(self.getMove(self.direction),self.direction)
            SS=self.checkGameOverMove(aux)
            if SS >= 0: pSS= self.distance_to_food_pos(aux)

        out.append(LL)
        out.append(LR)
        out.append(LS)
        out.append(RL)
        out.append(RR)
        out.append(RS)
        out.append(SL)
        out.append(SR)
        out.append(SS)

        
        out.append(pLL)
        out.append(pLR)
        out.append(pLS)
        out.append(pRL)
        out.append(pRR)
        out.append(pRS)
        out.append(pSL)
        out.append(pSR)
        out.append(pSS)
        #left or Right
        #out.append(self.lowDirFruit(0,self.width))
        #Up or down
        #out.append(self.lowDirFruit(1,self.heigth))
        
        
        unit_vector_1 = self.fruit / np.linalg.norm(self.fruit)

        if self.snake_pos[0] > 0 and self.snake_pos[1] > 0:
            unit_vector_2 = self.snake_pos / np.linalg.norm(self.snake_pos)
        else: unit_vector_2= [0,0]

        dot_product = np.dot(unit_vector_2, unit_vector_1)

        angle = np.arccos(dot_product)
        out.append(angle)
        
        return out

        
    def getInputs2(self):
        matrix= np.full((12,12),0.5)
        for x in self.snake_body:
            i=int(x[0]/50 +1)
            j= int(x[1]/50 +1) 
            matrix[j][i]=0
        for i in range(12):
            matrix[i][0]=0
            matrix[0][i]=0
            matrix[11][i]=0
            matrix[i][11]=0

        i= int(self.fruit[0]/50 +1) 
        j=int(self.fruit[1]/50 +1) 

        matrix[i][j]=1
        return matrix.flatten()