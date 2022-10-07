from random import randint

import pygame
from dino_runner.components.powerups.shield import Shield


class PoweUpManager:
    def __init__(self):
        self.power_ups =[]
        self.when_appears = 0

    def generate_power_up(self,save_score):
        if len(self.power_ups)==0  and self.when_appears== save_score:
            self.when_appears += randint(200,300)
            self.power_ups.append(Shield())

    def update(self,game_speed,player,save_score):
        self.generate_power_up(save_score)
        for power_up in self.power_ups:
            power_up.update(game_speed,self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                power_up.start_time=pygame.time.get_ticks()
                self.power_ups.remove(power_up)

    def draw(self,screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups=[]
        self.when_appears = randint(200,300)