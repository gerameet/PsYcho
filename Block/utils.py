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
        self.timer = pygame.draw.arc(self.display.screen, (255, 255, 255), arc_rect, 0, angle, 5)
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

    # def arrow(self, arrow_dims: list, head_dir: str):
    #     '''
    #     Create an arrow item

    #     Parameters:
    #         arrow_dims (list): dimensions of the arrow
    #     '''
    #     self.length = arrow_dims[0]
    #     self.width = arrow_dims[1]
    #     self.head_height = arrow_dims[2]
    #     self.head_dir = head_dir
    #     arrow = pygame.Surface((2*self.length, 2*self.width), pygame.SRCALPHA)
    #     # pygame.draw.polygon(arrow, self.color, [(0, 0), (self.length, self.width//2), (0, self.width)])
    #     pygame.draw.polygon(arrow, self.color, [(0, self.width//2), (0,-self.width//2), (self.length,self.width//2), (self.length, -self.width//2)]) # Body Part
    #     pygame.draw.polygon(arrow, self.color, [(self.length,self.head_height//2), (self.length, -self.head_height//2), (self.length + self.head_height, 0)]) # Head Part
        
    #     if (self.head_dir == 'right'):
    #         self.object = arrow
    #     else:
    #         arrow = pygame.transform.flip(arrow, True, False)
    #         self.object = arrow
    #     return arrow


    def arrow(self, arrow_dims: list, head_dir: str):
        '''
        Create an arrow item

        Parameters:
            arrow_dims (list): dimensions of the arrow (length, width, head_height)
            head_dir (str): direction of the arrow head ('right' or 'left')
        '''
        self.length = arrow_dims[0]          # Length of the arrow body
        self.width = arrow_dims[1]           # Width of the arrow body
        self.head_height = arrow_dims[2]     # Height of the arrow head
        self.head_dir = head_dir

        # Surface to draw the arrow on, transparent background
        arrow = pygame.Surface((self.length + self.head_height, self.width), pygame.SRCALPHA)

        # Define points for the body of the arrow (a rectangle)
        body_points = [
            (0, self.width // 2 - self.width // 4),  # Top left of the body
            (self.length, self.width // 2 - self.width // 4),  # Top right of the body
            (self.length, self.width // 2 + self.width // 4),  # Bottom right of the body
            (0, self.width // 2 + self.width // 4)   # Bottom left of the body
        ]

        # Define points for the head of the arrow (a triangle)
        head_points = [
            (self.length, self.width // 2 + self.head_height // 2),   # Bottom of the head
            (self.length, self.width // 2 - self.head_height // 2),   # Top of the head
            (self.length + self.head_height, self.width // 2)         # Tip of the head
        ]

        # Draw the arrow body
        pygame.draw.polygon(arrow, self.color, body_points)

        # Draw the arrow head
        pygame.draw.polygon(arrow, self.color, head_points)

        # Flip the arrow if needed
        if self.head_dir == 'left':
            arrow = pygame.transform.flip(arrow, True, False)

        # Store the arrow image
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
        t = np.linspace(0, duration, int(sample_rate * duration))
        beep = aplitude * np.sin(2 * np.pi * frequency*t)

        beep = beep.astype(np.int16)
        self.object = beep
        return beep


def write_and_pause(screen, text, time, change_background = True, background_color = (0, 0, 0), text_color = (255, 255, 255), position = 'center'):
    '''
    Write text on the screen and pause for a specified time

    Parameters:
        screen (Stage): the screen object to write on
        text (str): the text to display
        time (int): time(in SECONDS) to pause the program
    '''
    if change_background:
        screen.setColor(background_color)
    if position == 'center':
        loc_screen = (screen.width // 2, screen.height // 2)
    elif isinstance(position,tuple):
        loc_screen = position
    font = pygame.font.Font(None, 74)
    rendered_text = font.render(text, True, text_color)
    text_rect = rendered_text.get_rect(center = loc_screen)
    screen.screen.blit(rendered_text, text_rect)
    pygame.display.flip()
    pause(time)