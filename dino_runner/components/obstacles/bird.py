import random
from .obstacle import Obstacle
class Bird(Obstacle):
    POSITIONS = [230,290,300,250]
    def __init__(self, images):
        type = random.randint(0, 1) 
        super().__init__(images, type)
        self.rect.y = random.choice(self.POSITIONS)