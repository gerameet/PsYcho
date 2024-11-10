import pygame
import numpy as np
import soundfile as sf

from utils import *
from scenes import *


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

class Movement(object):
    '''
    Movement class
    '''
    def __init__(self, color: tuple, position, screen: Stage, timer : Timer):
        '''
        Movement class constructor

        Parameters:
            color (tuple): color of the object
            position (list): initial position of the object
            screen (Stage): stage object 
        '''
        self.object_creator = Item(color, position)
        self.position = position
        self.display = screen
        self.timer = timer
        self.object_history = []
        pass

    def createObject(self, mode: str, radius: int = None, arrow_dims: list = None, plus_dims: list = None):
        '''
        Create an object

        Parameters:
            mode (str): mode of the object
            radius (int): radius of the object
            arrow_dims (list): dimensions of the arrow
            plus_dims (list): dimensions of the plus
        '''
        if (mode == 'dot'):
            self.object_creator.dot(radius)
        elif (mode == 'arrow'):
            self.object_creator.arrow(arrow_dims[0:3], arrow_dims[3])
        elif (mode == 'plus'):
            self.object_creator.plus(plus_dims)
        else:
            print("Invalid mode!")
        self.object = self.object_creator.object
        self.object_history.append(self.object)
        pass
    
    def move(self, direction: str, speed: int, time: float):
        '''
        Move the object

        Parameters:
            direction (str): direction of the movement
            speed (int): speed of the movement
            time (float): time of the movement
        '''
        self.dir = direction
        self.speed = speed

        if (direction == 'left'):
            dir = -1
            self.start_pos_x = self.position[0]
            self.start_pos_y = self.position[1]
        elif (direction == 'right'):
            dir = 1
            self.start_pos_x = self.position[0]
            self.start_pos_y = self.position[1]
        else:
            print("Invalid direction!")
        self.end_pos_x = self.start_pos_x + dir * speed * time
        self.end_pos_y = self.start_pos_y

        start_time = pygame.time.get_ticks()
        while True:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000.0
            if elapsed_time > time:
                break
            progress = elapsed_time / time
            current_x = self.start_pos_x + progress * (self.end_pos_x - self.start_pos_x)
            current_y = self.start_pos_y + progress * (self.end_pos_y - self.start_pos_y)
            self.position = (current_x, current_y)
            self.display.screen.fill(self.display.color)
            self.display.screen.blit(self.object, self.position)

            self.timer.draw_timer_ring(elapsed_time, time)

            pygame.display.update()
            pygame.display.flip()
            self.display.clock.tick(60)
        self.position = (self.end_pos_x, self.end_pos_y)
        self.display.screen.blit(self.object, self.position)
        pygame.display.update()

        pass

class Direction(object):
    '''
    Direction class
    '''
    def __init__(self, position: list, color: tuple, screen: Stage):
        '''
        Direction class constructor

        Parameters:
            position (list): position of the object
            color (tuple): color of the object
            screen (Stage): stage object
        '''
        self.position = position
        self.object_creator = Item(color, position)
        self.display = screen
        pass

    def createArrow(self, arrow_dims: list):
        '''
        Create an arrow

        Parameters:
            arrow_dims (list): dimensions of the arrow
        '''
        self.arrow = self.object_creator.arrow(arrow_dims)
        return self.arrow
        
class Sound(object):
    '''
    Sound class
    '''
    def __init__(self, screen: Stage, timer: Timer):
        '''
        Sound class constructor

        Parameters:
            screen (Stage): stage object
        '''
        self.object_creator = Item()
        self.display = screen
        self.timer = timer
        pass

    def createBeep(self, frequency: int, duration: int, amplitude: int):
        '''
        Create a beep sound

        Parameters:
            frequency (int): frequency of the beep
            duration (int): duration of the beep
            amplitude (int): amplitude of the beep
        '''
        amplitude = amplitude*1000
        self.freq = frequency
        self.dur = duration
        self.amp = amplitude
        self.sound = self.object_creator.beep(frequency, duration, amplitude)
        self.file_name = f"beep_f{frequency}_dur{duration}_amp{amplitude}.wav"
        sf.write(f"beep_f{frequency}_dur{duration}_amp{amplitude}.wav", self.sound, 44100, format='WAV', subtype='PCM_16')

    def play(self, ear: str):
        '''
        Plays the sound

        Parameters:
            ear (str): ear to play the sound
        '''
        pygame.mixer.init()
        beep = pygame.mixer.Sound(self.file_name)
        channel = pygame.mixer.Channel(0)
        if (ear == 'left'):
            channel.set_volume(1.0, 0.0)
        elif (ear == 'right'):
            channel.set_volume(0.0, 1.0)
        else:
            print("Invalid ear!")
        channel.play(beep)

        start_time = pygame.time.get_ticks()
        while True:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000.0
            if elapsed_time > self.dur:
                break
            progress = elapsed_time / self.dur
            self.display.screen.fill(self.display.color)
            self.timer.draw_timer_ring(elapsed_time, self.dur)

            pygame.display.update()
            pygame.display.flip()
            self.display.clock.tick(60)
        pygame.display.update()


