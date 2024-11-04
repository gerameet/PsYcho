import pygame
import numpy as np

from utils import *

class Movement(object):
    '''
    Movement class
    '''
    def __init__(self, color: tuple, position, screen: Stage):
        self.object_creator = Item(color, position)
        self.screen = screen
        self.object_history = []
        pass

    def createObject(self, mode: str, radius: int = None, arrow_dims: list = None, plus_dims: list = None):
        if (mode == 'dot'):
            self.object_creator.dot(radius)
        elif (mode == 'arrow'):
            self.object_creator.arrow(arrow_dims)
        elif (mode == 'plus'):
            self.object_creator.plus(plus_dims)
        else:
            print("Invalid mode!")
        self.object = self.object_creator.object
        self.object_history.append(self.object)
        pass
    
    def move(self, direction: str, speed: int):
        if (direction == 'left'):
            pass
        elif (direction == 'right'):
            pass
        else:
            print("Invalid direction!")
        self.dir = direction
        self.speed = speed
        pass

class Direction(object):
    '''
    Direction class
    '''
    def __init__(self, position: list, color: tuple, screen: Stage):
        self.position = position
        self.object_creator = Item(color, position)
        self.screen = screen
        pass

    def createArrow(self, arrow_dims: list):
        self.arrow = self.object_creator.arrow(arrow_dims)
        pass
        
class Sound(object):
    '''
    Sound class
    '''
    def __init__(self, screen: Stage):
        self.object_creator = Item()
        self.screen = screen
        pass

    def createBeep(self, frequency: int, duration: int, aplitude: int):
        self.sound = self.object_creator.beep(frequency, duration, aplitude)
        pass

    def play(self, ear: str):
        if (ear == 'left'):
            pass
        elif (ear == 'right'):
            pass
        else:
            print("Invalid ear!")
        pass

class Timer(object):
    '''
    Timer class
    '''
    def __init__(self, screen: Stage):
        self.screen = screen
        pass

    def draw_timer_ring(self, time_elapsed, max_time):
        proportion = time_elapsed / max_time
        angle = 2 * 3.14 * proportion
        # self.timer = pygame.draw.arc(self.screen, (0, 255 - int(255 * proportion), 0), (700, 10, 50, 50), 0, angle, 5)
        pass