import pygame
import random
from Cell import *

class Plant(Cell):
    ID = 2
    plantAmount = 0

    def __init__(self):
        updateRate = random.randint(20, 200)
        color = pygame.Color(random.randint(0, 40), random.randint(50, 150), random.randint(0, 40))
        super().__init__(updateRate, color)
        Plant.plantAmount += 1
    
    def update(self):
        result = super().update()

        return result