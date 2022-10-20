from distutils.command.config import config

import pygame
from SnakeIA1 import Snake_game
import neat
import os
import pickle
import numpy as np
import pandas as pd
class Snake:
    def __init__(self,window, width, height):
        self.game= Snake_game(window,width,height)
        self.snake_pos= self.game.snake_pos
        self.snake_body= self.game.snake_body
        self.direction= self.game.direction
        self.score = self.game.score
        self.fruit= self.game.fruit 
        self.width= width
        self.height= height

    def test_ai(self,net):
        
        
        
        run = True
        while run:
            game_info = self.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            output = net.activate((self.game.getInputs()))
            decision= output.index(max(output))
            if decision==0:
                pass
            elif decision==-1:
                self.game.moveLeft()
            elif decision==1:
                self.game.moveRight()

            self.game.loop()
            if self.game.is_game_over:
                self.game.game_over()
        




    def train_ai(self ,genome1, config):
        net= neat.nn.FeedForwardNetwork.create(genome1,config)
        run = True
        iteration=0
        iterationsWithoutFood=0
        game_information=0
        distance=14
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   
                    quit()
            
        
            output1= net.activate((self.game.getInputs()))
            decision= output1.index(max(output1))
            if decision==0:
                pass
            elif decision==0.5:
                self.game.moveLeft()
            elif decision==1:
                self.game.moveRight()
            
            self.game.loop()
            
            
            #Game Information
            if self.game.ate == True: 
                game_information += 10
                iterationsWithoutFood=0
            

            elif self.game.distance_to_food() < distance: game_information += 1
            else: game_information -= 1.5
            
            
            iterationsWithoutFood += 1
            iteration += 1

            if self.game.is_game_over or iteration >= 1000 or iterationsWithoutFood >= 30 :
                
                self.calculate_fitness(genome1,game_information)
                break

        #[Score, Steps, StepsDeath Game_Information]  
        return np.array([self.game.score, iteration, iterationsWithoutFood, game_information])
                
    def calculate_fitness(self, genome, game_information):
        if self.game.score>1: print("Game Score: ",self.game.score)
        genome.fitness += game_information
        
           


def eval_genomes(genomes, config):
    width, height = 500,500
    window= pygame.display.set_mode((width,height))
    df = pd.DataFrame(columns=['GameScore','Steps','StepsDeath','SnakeScore'])
    for genome_id, genome in genomes:
        genome.fitness = 0.0
        snake= Snake(window,width,height)
        report=snake.train_ai(genome, config,)
        df.loc[len(df)] = report

    try:
        dfLoaded=pd.read_csv("SnakeDF.csv")
        dfMerge= pd.concat([dfLoaded,df])
        dfMerge.to_csv("SnakeDF.csv",index=False)
    except:
        df.to_csv("SnakeDF.csv",index=False)

            

def run_neat(config):
    #getCheckpoint
    #p=neat.Checkpointer.restore_checkpoint('neat-checkpoint-539')
    p= neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats= neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))

    winner= p.run(eval_genomes, 500)
    with open("best.pickle","wb") as f:
        pickle.dump(winner,f)


def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    width, height = 500, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("IA")
    snake = Snake(win, width, height)
    snake.test_ai(winner_net)


if __name__ == "__main__":
    local_dir= os.path.dirname(__file__)
    config_path= os.path.join(local_dir,"config.txt")
    config = neat.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    run_neat(config)
    #test_best_network(config)