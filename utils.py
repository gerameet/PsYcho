import numpy as np
import pygame

class Stage(object):
    '''
    Stage class 
    '''
    def __init__(self, color: tuple, width = 100, height = 100):
        self.color = color
        self.width = width
        self.height = height
        self.running = False
        pass

    def setColor(self, color):
        self.color = color
        return None

    def createWindow(self, width, height, caption: str):
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.screen.fill(self.color)
        pygame.display.update()
        self.running = True
        pass

    def quit(self):
        pygame.quit()
        pass

class Item(object):
    '''
    Item class
    '''
    def __init__(self, color: tuple = None, position = None):
        self.color = color
        self.position = position
        self.object = None
        pass

    def dot(self, radius):
        dot = None
        self.object = dot
        return dot

    def arrow(self, arrow_dims: list):
        arrow = None
        self.length = arrow_dims[0]
        self.width = arrow_dims[1]
        self.head_height = arrow_dims[2]
        self.object = arrow
        return arrow

    def plus(self, plus_dims: list):
        plus = None
        self.object = plus
        return plus
    
    def beep(self, frequency: int, duration: int, aplitude: int):
        beep = None
        self.sound = beep
        return beep

