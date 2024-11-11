import numpy as np
import pygame
import sys

def pause(time: float):
    '''
    Pause the program for a specified time

    Parameters:
        time (float): time(in SECONDS) to pause the program
    '''
    pygame.time.wait(int(time*1e3))


class Stage(object):
    '''
    Stage class 
    '''
    def __init__(self, color: tuple, width = 100, height = 100):
        '''
        Stage class constructor

        Parameters:
            color (tuple): color of the stage
            width (int): width of the stage
            height (int): height of the stage 
        '''
        self.color = color
        self.width = width
        self.height = height
        self.running = False
        pass

    def setColor(self, color):
        ''' 
        Set the color of the stage

        Parameters:
            color (tuple): color of the stage
        '''
        self.color = color
        self.screen.fill(color)
        return None

    def createWindow(self, width, height, caption: str):
        '''
        Create a window for the stage

        Parameters:
            width (int): width of the window
            height (int): height of the window
            caption (str): caption of the window
        '''
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        pass

    def quit(self):
        '''
        Quit the stage
        '''
        pygame.quit()
        sys.exit()
        pass

class Timer(object):
    '''
    Timer class
    '''
    def __init__(self, screen: Stage, radius : float):
        '''
        Timer class constructor

        Parameters:
            screen (Stage): stage object
        '''
        self.display = screen
        self.radius = radius
        pass

    def draw_timer_ring(self, time_elapsed, max_time):
        '''
        Draw a timer ring

        Parameters:
            time_elapsed (int): time elapsed
            max_time (int): maximum time
        '''
        arc_rect = pygame.Rect(0.9*self.display.width, 0.1*self.display.height, 2*self.radius, 2*self.radius)
        proportion = time_elapsed / max_time
        angle = 2 * 3.14 * proportion
        self.timer = pygame.draw.arc(self.display.screen, (255, 255 - int(255 * proportion), 255 - int(128 * proportion)), (700, 10, 50, 50), 0, angle, 5)
        pass

class Item(object):
    '''
    Item class
    '''
    def __init__(self, color: tuple = None, position = None):
        '''
        Item class constructor

        Parameters:
            color (tuple): color of the item
            position (tuple): position of the item
        '''
        self.color = color
        self.position = position
        self.object = None
        pass

    def dot(self, radius):
        '''
        Create a dot item

        Parameters:
            radius (int): radius of the dot
        '''
        dot = pygame.Surface((radius, radius), pygame.SRCALPHA)
        pygame.draw.circle(dot, self.color, (radius//2, radius//2), radius//2)
        self.object = dot
        return dot

    def arrow(self, arrow_dims: list, head_dir: str):
        '''
        Create an arrow item

        Parameters:
            arrow_dims (list): dimensions of the arrow
        '''
        self.length = arrow_dims[0]
        self.width = arrow_dims[1]
        self.head_height = arrow_dims[2]
        self.head_dir = head_dir
        arrow = pygame.Surface((self.length, self.width), pygame.SRCALPHA)
        pygame.draw.polygon(arrow, self.color, [(0, 0), (self.length, self.width//2), (0, self.width)])
        pygame.draw.polygon(arrow, self.color, [(self.length - self.head_height, 0), (self.length, self.width//2), (self.length - self.head_height, self.width)])
        
        if (self.head_dir == 'right'):
            self.object = arrow
        else:
            arrow = pygame.transform.flip(arrow, True, False)
            self.object = arrow
        return arrow

    def plus(self, plus_dims: list):
        '''
        Create a plus item

        Parameters:
            plus_dims (list): dimensions of the plus
        '''
        plus = pygame.Surface((plus_dims[0], plus_dims[1]), pygame.SRCALPHA)
        pygame.draw.rect(plus, self.color, (0, plus_dims[1]//3, plus_dims[0], plus_dims[1]//3))
        pygame.draw.rect(plus, self.color, (plus_dims[0]//3, 0, plus_dims[0]//3, plus_dims[1]))
        self.object = plus
        return plus
    
    def beep(self, frequency: int, duration: int, aplitude: int):
        '''
        Create a beep item. Note that the sample rate is maintained at 44100 Hz.

        Parameters:
            frequency (int): frequency of the beep
            duration (int): duration of the beep
            aplitude (int): aplitude of the beep
        '''
        beep = None
        sample_rate = 44100
        t = np.linspace(0, duration, sample_rate * duration)
        beep = aplitude * np.sin(2 * np.pi * frequency*t)

        beep = beep.astype(np.int16)
        self.object = beep
        return beep


def write_and_pause(screen, text, time):
    '''
    Write text on the screen and pause for a specified time

    Parameters:
        screen (Stage): the screen object to write on
        text (str): the text to display
        time (int): time(in SECONDS) to pause the program
    '''
    screen.setColor((0, 0, 0))
    font = pygame.font.Font(None, 74)
    rendered_text = font.render(text, True, (255, 255, 255))
    text_rect = rendered_text.get_rect(center=(screen.width / 2, screen.height / 2))
    screen.screen.blit(rendered_text, text_rect)
    pygame.display.flip()
    pause(time)