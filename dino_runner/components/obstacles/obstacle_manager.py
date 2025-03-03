import pygame
import random
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import BIRD, SMALL_CACTUS,LARGE_CACTUS


class ObstacleManager:
    def __init__(self):
        self.obstacles =[]

    def update(self,game_speed,player,on_death,reset_score):
        if len(self.obstacles)==0:
           n= random.randint(0,2)
           if n==0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
           elif n == 1:
                 self.obstacles.append(Cactus(LARGE_CACTUS))
           else:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game_speed,self.obstacles)
            if player.dino_rect.colliderect(obstacle.rect):
                
                if on_death():
                    self.obstacles.remove(obstacle)
                else:
                    break
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    def reset_obstacles(self):
        self.obstacles=[]