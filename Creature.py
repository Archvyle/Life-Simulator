from Cell import *
import random
import pygame

class Creature(Cell):
    ID = 1

    def __init__(self):
        updateRate = random.randint(5, 30)
        color = pygame.Color(92+(5 + 30 - updateRate)*5, 15, 15+(5 + 30 - updateRate)*2)
        super().__init__(updateRate, color)
        self.hunger = -1000
        self.sexTimeLeft = 0
    
    def update(self):
        result = super().update()

        hungerRate = (5 + 30 - self.updateRate)/4

        self.hunger += hungerRate

        self.sexTimeLeft -= 1

        return result