import numpy as np
import pygame

from utils import *
from scenes import *


def get_random_direction(n = 1):
    """
    Get a random direction (left/right)
    """
    return [np.random.choice(['left', 'right']) for _ in range(n)]

def get_random_task(tasks: list):
    """
    Get a random task from input list.
    """
    return np.random.choice(tasks)

def get_random_position(window_width : int, window_height : int):
    """
    Get a random position within the window.
    """
    return [np.random.choice([int(0.33*window_width), int(0.67*window_width)]), np.random.choice([int(0.4*window_height), int(0.6*window_height)])]


class Task(object):
    '''
    Task class
    '''
    def __init__(self, screen: Stage, timer: Timer):
        '''
        Task class constructor
        '''
        self.display = screen
        self.timer = timer

    def createSceneMovement(self, object_type: str = 'arrow', direction: list = None, speed: int = None, 
                    time: float = None, radius: int = None, arrow_dims: list = None, plus_dims: list = None, sound_dims: list = None,
                    color: tuple = None, position: list = None):
        '''
        Create a scene

        Parameters:
            object_type (str): type of the object
            direction (list): direction of the object
            speed (int): speed of the object
            time (float): time of the object
            radius (int): radius of the object
            arrow_dims (list): dimensions of the arrow
            plus_dims (list): dimensions of the plus
        '''
        if ('beep' in object_type):
            beep = Movement(color, position, self.display, self.timer)
            beep.createObject(['beep'], sound_dims = sound_dims)
            beep.move(direction, speed, time)
        if ('dot' in object_type):
            dot = Movement(color, position, self.display, self.timer)
            dot.createObject(['dot'], radius=radius)
            dot.move(direction, speed, time)
        if ('arrow' in object_type):
            arrow = Movement(color, position, self.display, self.timer)
            arrow.createObject(['arrow'], arrow_dims=arrow_dims)
            arrow.move(direction, speed, time)
        if ('plus' in object_type):
            plus = Movement(color, position, self.display, self.timer)
            plus.createObject(['plus'], plus_dims=plus_dims)
            plus.move(direction, speed, time)
        if ('beep' not in object_type and 'dot' not in object_type and 'arrow' not in object_type and 'plus' not in object_type):
            print("Invalid object type!")

    def createSceneSound(self, frequency: int, duration: int, volume: int, direction: str):
        '''
        Create a scene

        Parameters:
            frequency (int): frequency of the sound
            duration (int): duration of the sound
            volume (int): volume of the sound
            direction (str): direction of the sound
        '''
        beep = Sound(self.display, self.timer)
        beep.createBeep(frequency, duration, volume)
        beep.play(direction)

    def createSceneDirection(self, position: list = None, color: tuple = None, arrow_dims: list = None, time : float = None):
        '''
        Create a scene

        Parameters:
            position (list): position of the object
            color (tuple): color of the object
        '''
        direction = Direction(color, position, self.display, self.timer)
        direction.showArrow(arrow_dims, time)

screen = Stage((255, 255, 255), width=1500, height=900)
timer = Timer(screen, 50)
screen.createWindow(1500, 900, 'Trial Run 1')

# task = Task(screen, timer)
# task.createSceneMovement(object_type='plus', direction='left', speed=250, time=1, color=(255,255,0), position=[390, 290], plus_dims=[100, 100])
# task.createSceneMovement(object_type='dot', direction='right', speed=400, time=1, color=(255,0,0), position=[390, 290], radius=20)
# task.createSceneSound(frequency=500, duration=2, volume=10, direction='left')
# task.createSceneDirection(position=[390, 290], color=(0,0,255), arrow_dims=[100, 20, 30, 'right'], time = 3)


class Neutral(object):
    '''
    Neutral class
    '''
    def __init__(self, screen: Stage, timer: Timer):
        '''
        Neutral class constructor
        '''
        self.display = screen
        self.timer = timer
        self.task = Task(screen, timer)
        pass
    
    def createScene(self, tasks: list = None, num_scenes: int = None, 
                    object_name: list = None, direction: list = None, speed: int = None,
                    time: float = None, radius: int = None, arrow_dims: list = None, plus_dims: list = None,
                    color: tuple = None, position: list = None, frequency: int = None, volume: int = None):
        '''
        Create a scene

        Parameters:
            tasks (list): list of tasks
            num_scenes (int): number of scenes
            object_name (list): list of object names
            direction (list): list of directions
            speed (int): speed of the object
            time (float): time of the object
            radius (int): radius of the object
            arrow_dims (list): dimensions of the arrow
            plus_dims (list): dimensions of the plus
            color (tuple): color of the object
            position (list): position of the object
            frequency (int): frequency of the sound
            volume (int): volume of the sound
        '''
        movement_bgd_color = (220, 50, 50)
        sound_bgd_color = (50, 220, 50)
        direction_bgd_color = (50, 50, 220)

        for i in range(num_scenes):
            task_name = get_random_task(tasks)
            if (task_name == 'Movement'):
                self.display.setColor(movement_bgd_color)
                self.task.createSceneMovement(object_type='dot', direction=get_random_direction(), speed=speed, time=time, 
                                              radius=radius, arrow_dims=arrow_dims, plus_dims=plus_dims, 
                                              color=color, position=get_random_position(self.display.width, self.display.height))
            elif (task_name == 'Sound'):
                self.display.setColor(sound_bgd_color)
                self.task.createSceneSound(frequency=frequency, duration=time, volume=volume, direction=get_random_direction()[-1])
            elif (task_name == 'Direction'):
                self.display.setColor(direction_bgd_color)
                arrow_dims[3] = get_random_direction()[-1]
                self.task.createSceneDirection(position=get_random_position(self.display.width, self.display.height), color=color, arrow_dims=arrow_dims, time=time)
        pass

# n = Neutral(screen, timer)
# n.createScene(tasks=['Movement', 'Direction'], num_scenes=10, speed=400, time=1, color=(0,0,0), position=[390, 290], radius=20, arrow_dims=[100, 20, 30, None])

class Conflict(object):
    '''
    Conflict class
    '''
    def __init__(self, screen: Stage, timer: Timer):
        '''
        Conflict class constructor
        '''
        self.display = screen
        self.timer = timer
        self.task = Task(screen, timer)
        pass

    def createScene(self, tasks: list = None, num_scenes: int = None, 
                    object_name: str = None, direction: str = None, speed: int = None,
                    time: float = None, radius: int = None, arrow_dims: list = None, plus_dims: list = None,
                    color: tuple = None, position: list = None, frequency: int = None, volume: int = None):
        '''
        Create a scene

        Parameters:
            tasks (list): list of tasks
            num_scenes (int): number of scenes
        '''
        movement_bgd_color = (220, 50, 50)
        sound_bgd_color = (50, 220, 50)
        direction_bgd_color = (50, 50, 220)

        for i in range(num_scenes):
            # task_name = get_random_task(tasks)
            # print(task_name)
            # if (task_name == 'Movement'):
            #     self.display.setColor(movement_bgd_color)
            #     if ('Movement' in tasks and 'Direction' in tasks):
            #         self.task.createSceneMovement(object_type='arrow', direction=get_random_direction(), speed=speed, time=time, 
            #                                 radius=radius, arrow_dims=arrow_dims, plus_dims=plus_dims, 
            #                                 color=color, position=get_random_position(self.display.width, self.display.height))
            if ('Movement' in tasks and 'Sound' in tasks):
                task = get_random_task(tasks)
                if (task == 'Movement'):
                    self.display.setColor(movement_bgd_color)
                elif (task == 'Sound'):
                    self.display.setColor(sound_bgd_color)
                task = Movement(color, position=get_random_position(self.display.width, self.display.height), screen=self.display, timer=self.timer)
                task.createObject(['beep', 'arrow'], arrow_dims=arrow_dims, sound_dims=[frequency, time, volume])
                task.move(direction=get_random_direction(2), speed=speed, time=time)
            # elif (task_name == 'Sound'):
            #     self.display.setColor(sound_bgd_color)
            #     self.task.createSceneSound(frequency=frequency, duration=time, volume=volume, direction=get_random_direction())
            # elif (task_name == 'Direction'):
            #     self.display.setColor(direction_bgd_color)
            #     arrow_dims[3] = get_random_direction()
            #     self.task.createSceneDirection(position=get_random_position(self.display.width, self.display.height), color=color, arrow_dims=arrow_dims, time=time)
    pass

con = Conflict(screen, timer)
con.createScene(tasks=['Movement','Sound'], num_scenes=10, speed=400, time=2, color=(0,0,0), position=[390, 290], radius=20, arrow_dims=[100, 20, 30, None], frequency=500, volume=10)

class Congruent(object):
    pass

