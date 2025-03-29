import pygame
import numpy as np
import soundfile as sf

from utils import *

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
        self.object = []
        self.is_beep = False
        pass

    def createObject(self, mode: list = None, radius: int = None, arrow_dims: list = None, plus_dims: list = None, sound_dims: list = None):
        '''
        Create an object

        Parameters:
            mode (list): mode of the object
            radius (int): radius of the object
            arrow_dims (list): dimensions of the arrow
            plus_dims (list): dimensions of the plus
        '''
        self.mode = mode
        if ('beep' in mode):
            self.is_beep = True
            self.beep = Sound(self.display, self.timer)
            frequency = sound_dims[0]
            duration = sound_dims[1]
            amplitude = sound_dims[2]
            self.beep.createBeep(frequency, duration, amplitude)
            self.object.append(self.beep)
        if ('dot' in mode):
            self.object_creator.dot(radius)
            self.object.append(self.object_creator.object)
        if ('arrow' in mode):
            self.object_creator.arrow(arrow_dims[0:3], arrow_dims[3])
            self.object.append(self.object_creator.object)
        if ('plus' in mode):
            self.object_creator.plus(plus_dims)
            self.object.append(self.object_creator.object)
        elif ('plus' not in mode and 'arrow' not in mode and 'dot' not in mode and 'beep' not in mode):
            print("Invalid mode!")
        pass
    
    def move(self, direction: list, speed: int, time: float):
        '''
        Move the object

        Parameters:
            direction (list): direction of the movement of respective object in mode
            speed (int): speed of the movement
            time (float): time of the movement
        '''
        self.dir = direction
        self.speed = speed

        if (direction[-1] == 'left'):
            dir = -1
            self.start_pos_x = self.position[0]
            self.start_pos_y = self.position[1]
        elif (direction[-1] == 'right'):
            dir = 1
            self.start_pos_x = self.position[0]
            self.start_pos_y = self.position[1]
        else:
            print("Invalid direction!")
        self.end_pos_x = self.start_pos_x + dir * speed * time
        self.end_pos_y = self.start_pos_y

        if (self.is_beep):
            self.beep.play(direction[0], self.is_beep)
        
        key_pressed = "none"
        # default time taken is set to total time of the scene
        time_taken = time

        start_time = pygame.time.get_ticks()
        while True:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000.0
            if elapsed_time > time:
                pause(0.25)
                break
            
            # Check for key press
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        key_pressed = "left"
                        time_taken = elapsed_time
                        break
                    elif event.key == pygame.K_RIGHT:
                        key_pressed = "right"
                        time_taken = elapsed_time
                        break
            if key_pressed in ["left", "right"]:
                if(self.is_beep):
                    self.beep.stop_playing()
                pause(0.25)
                break

            progress = elapsed_time / time

            current_x = self.start_pos_x + progress * (self.end_pos_x - self.start_pos_x)
            current_y = self.start_pos_y + progress * (self.end_pos_y - self.start_pos_y)
            self.position = (current_x, current_y)

            self.display.screen.fill(self.display.color)
            if ('dot' in self.mode or 'plus' in self.mode or 'arrow' in self.mode):
                self.display.screen.blit(self.object[-1], self.position)

            # self.timer.draw_timer_ring(elapsed_time, time)

            pygame.display.update()
            pygame.display.flip()
            self.display.clock.tick(60)

        # self.position = (self.end_pos_x, self.end_pos_y)
        # if ('dot' in self.mode or 'plus' in self.mode or 'arrow' in self.mode):
        #     self.display.screen.blit(self.object[-1], self.position)
        # pygame.display.update()

        with open("data.csv", "a") as file:
            file.write(f"{key_pressed},{time_taken}\n")

        pass

class Direction(object):
    '''
    Direction class
    '''
    def __init__(self, color: tuple, position: list, screen: Stage, timer: Timer):
        '''
        Direction class constructor

        Parameters:
            position (list): position of the object
            color (tuple): color of the object
            screen (Stage): stage object
        '''
        self.position = position
        self.color = color
        self.timer = timer
        self.object_creator = Item(color, position)
        self.display = screen

    def showArrow(self, arrow_dims: list, time : float):
        '''
        Create an arrow

        Parameters:
            arrow_dims (list): dimensions of the arrow
        '''
        self.arrow = Movement(self.color, self.position, self.display, self.timer)
        self.arrow.createObject(['arrow'], arrow_dims=arrow_dims)
        self.arrow.move([arrow_dims[3]], 0, time)
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
        self.file_name = f"audio_files/beep_f{frequency}_dur{duration}_amp{amplitude}.wav"
        sf.write(f"audio_files/beep_f{frequency}_dur{duration}_amp{amplitude}.wav", self.sound, 44100, format='WAV', subtype='PCM_16')

    def play(self, ear: str, is_moving: bool = False):
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

        if (not is_moving):
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

    def stop_playing(self):
        '''
        Stops playing the sound
        '''
        pygame.mixer.stop()
        pass


