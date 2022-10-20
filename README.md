# SnakeIA
Project in the free time to create a snake game from scratch with pygame, and using a neural network to play the game. 09/2022

<div id="header" align="center">
    <img src="https://github.com/AdriaTorija/SnakeIA/blob/main/images/snake.png"/>
</div>

Analysing the results with different inputs to the Neural network.

## Inputs:
  -Matrix of the game (snake, fruits, walls)
  -Vision of the snake in different directions()
  -Vision of the snake in different directions + distance to fruit in each direction

## Outputs:
  -Move Straight
  -Move Right
  -Move Left
  
## Rewards:
  +Snake going to the direction of the fruit.
  +Snake eating the fruit.
  -Snake moving opposite direction of the fruit.
