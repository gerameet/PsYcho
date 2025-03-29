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
        pass

    def createScene(self, tasks: list = None, num_scenes: int = 1, 
                    object_name: str = None, direction: str = None, speed: int = None,
                    time: float = None, radius: int = None, arrow_dims: list = None, plus_dims: list = None,
                    color: tuple = None, position: list = None, frequency: int = None, volume: int = None, is_block: bool = False):
        '''
        Create a scene

        Parameters:
            tasks (list): list of tasks
            arrow_dims (list): dimensions of the arrow (4 values , keep last none)
            num_scenes (int): number of scenes
        '''
        movement_bgd_color = (220, 50, 50)
        sound_bgd_color = (50, 220, 50)
        direction_bgd_color = (50, 50, 220)


        for i in range(num_scenes):
            dir_0 = get_random_direction()[0]
            dir_1 = 'right' if dir_0 == 'left' else 'left'
            arrow_dims[3] = dir_0 if tasks[0] == 'Direction' else dir_1
            if (is_block):
                to_do_task  = tasks[0]
            else:
                to_do_task = get_random_task(tasks)
            if (to_do_task == 'Movement'):
                self.display.setColor(movement_bgd_color)
            elif (to_do_task == 'Sound'):
                self.display.setColor(sound_bgd_color)
            elif (to_do_task == 'Direction'):
                self.display.setColor(direction_bgd_color)
            else:
                print("Invalid task!")

            other_task = [i for i in tasks if i != to_do_task]

            with open("data.csv", 'a') as f:
                f.write(f"conflict,{to_do_task},{other_task[0]},{dir_0},{time},")

            if('Movement' in tasks and 'Sound' in tasks):
                task = Movement(color, position=get_random_position(self.display.width, self.display.height), screen=self.display, timer=self.timer)
                task.createObject(['beep', 'dot'], radius= radius, sound_dims=[frequency, time, volume])
                if to_do_task == 'Sound':
                    task.move(direction=[dir_0,dir_1], speed=speed, time=time)
                else:
                    task.move(direction=[dir_1,dir_0], speed=speed, time=time)
            
            elif ('Movement' in tasks and 'Direction' in tasks):
                task = Movement(color, position=get_random_position(self.display.width, self.display.height), screen=self.display, timer=self.timer)
                task.createObject(['arrow'], arrow_dims=arrow_dims)
                if to_do_task == 'Movement':
                    task.move(direction=[dir_0], speed=speed, time=time)
                else:
                    task.move(direction=[dir_1], speed=speed, time=time)
            
            elif ('Sound' in tasks and 'Direction' in tasks):
                task = Movement(color, position=get_random_position(self.display.width, self.display.height), screen=self.display, timer=self.timer)
                task.createObject(['beep', 'arrow'], arrow_dims = arrow_dims ,sound_dims=[frequency, time, volume])
                if to_do_task == 'Sound':
                    task.move(direction=[dir_0,dir_1], speed=0, time=time)
                else:
                    task.move(direction=[dir_1,dir_0], speed=0, time=time)

            else:
                print("Invalid task combination!")
    pass


class Congruent(object):
    '''
    Congruent class
    '''
    def __init__(self, screen: Stage, timer: Timer):
        '''
        Congruent class constructor
        '''
        self.display = screen
        self.timer = timer
        pass

    def createScene(self, tasks: list = None, position: list = None, num_scenes: int = 1, 
                    object_name: str = None, speed: int = None,
                    time: float = None, radius: int = None, arrow_dims: list = None, plus_dims: list = None,
                    color: tuple = None, frequency: int = None, volume: int = None, is_block: bool = False):
        

        '''
        Create a scene

        Parameters:
            tasks (list): list of tasks
            arrow_dims (list): dimensions of the arrow (4 values , keep last none)
            num_scenes (int): number of scenes
        '''
        movement_bgd_color = (220, 50, 50)
        sound_bgd_color = (50, 220, 50)
        direction_bgd_color = (50, 50, 220)

        for i in range(num_scenes):
            direction = get_random_direction()[0]
            arrow_dims[3] = direction
            if (is_block):
                to_do_task  = tasks[0]
            else:
                to_do_task = get_random_task(tasks)
            if (to_do_task == 'Movement'):
                self.display.setColor(movement_bgd_color)
            elif (to_do_task == 'Sound'):
                self.display.setColor(sound_bgd_color)
            elif (to_do_task == 'Direction'):
                self.display.setColor(direction_bgd_color)
            else:
                print("Invalid task!")

            other_task = [i for i in tasks if i != to_do_task]

            with open("data.csv", 'a') as f:
                f.write(f"congruent,{to_do_task},{other_task[0]},{direction},{time},")

            if('Movement' in tasks and 'Sound' in tasks):
                task = Movement(color, position=get_random_position(self.display.width, self.display.height), screen=self.display, timer=self.timer)
                task.createObject(['beep', 'dot'], radius= radius, sound_dims=[frequency, time, volume])
                task.move(direction=[direction, direction], speed=speed, time=time)
            
            elif ('Movement' in tasks and 'Direction' in tasks):
                task = Movement(color, position=get_random_position(self.display.width, self.display.height), screen=self.display, timer=self.timer)
                task.createObject(['arrow'], arrow_dims=arrow_dims)
                task.move(direction=[direction], speed=speed, time=time)
            
            elif ('Sound' in tasks and 'Direction' in tasks):
                task = Movement(color, position=get_random_position(self.display.width, self.display.height), screen=self.display, timer=self.timer)
                task.createObject(['beep', 'arrow'], arrow_dims = arrow_dims ,sound_dims=[frequency, time, volume])
                task.move(direction=[direction, direction], speed=0, time=time)

            else:
                print("Invalid task combination!")

            
    pass


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

        task_map = {
            'Movement': 'dot',
            'Sound': 'beep',
            'Direction': 'arrow'
        }

        for i in range(num_scenes):
            dir = get_random_direction()
            arrow_dims[3] = dir[0]
            task_name = tasks[0]
            if (task_name == 'Movement'):
                self.display.setColor(movement_bgd_color)
            elif (task_name == 'Sound'):
                self.display.setColor(sound_bgd_color)
            elif (task_name == 'Direction'):
                self.display.setColor(direction_bgd_color)
            else:
                print(f"Invalid task!{i}")
            task = Movement(color, position=get_random_position(self.display.width, self.display.height), screen=self.display, timer=self.timer)
            task.createObject(task_map[task_name], radius= radius, arrow_dims=arrow_dims, plus_dims=plus_dims, sound_dims=[frequency, time, volume])
            with open("data.csv", 'a') as f:
                f.write(f"neutral,{task_name},{task_name},{dir[0]},{time},")
            task.move(direction=dir, speed= 0 if task_name == 'Direction' else speed, time=time)
        pass


# con = Conflict(screen, timer)
# con.createScene(tasks=['Direction','Sound'], num_scenes=5, speed=400, time=2, color=(0,0,0), position=[390, 290], radius = 50, frequency=500, volume=10, arrow_dims=[100, 20, 30, None])
# con.createScene(tasks=['Movement','Sound'], num_scenes=5, speed=400, time=2, color=(0,0,0), position=[390, 290], radius = 50, frequency=500, volume=10, arrow_dims=[100, 20, 30, None])
# con.createScene(tasks=['Movement','Direction'], num_scenes=5, speed=400, time=2, color=(0,0,0), position=[390, 290], radius = 50, frequency=500, volume=10, arrow_dims=[100, 20, 30, None])

# cong = Congruent(screen, timer)
# cong.createScene(tasks=['Direction','Sound'], num_scenes=5, speed=400, time=2, color=(0,0,0), position=[390, 290], radius = 50, frequency=500, volume=10, arrow_dims=[100, 20, 30, None])
# cong.createScene(tasks=['Movement','Sound'], num_scenes=5, speed=400, time=2, color=(0,0,0), position=[390, 290], radius = 50, frequency=500, volume=10, arrow_dims=[100, 20, 30, None])
# cong.createScene(tasks=['Movement','Direction'], num_scenes=5, speed=400, time=2, color=(0,0,0), position=[390, 290], radius = 50, frequency=500, volume=10, arrow_dims=[100, 20, 30, None])

# Neutral_obj = Neutral(screen, timer)
# Neutral_obj.createScene(tasks=['Movement'], num_scenes=5, speed=400, time=1, color=(0,0,0), position=[390, 290], radius=20, arrow_dims=[100, 20, 30, None])
# Neutral_obj.createScene(tasks=['Direction'], num_scenes=5, speed=400, time=1, color=(0,0,0), position=[390, 290], radius=20, arrow_dims=[100, 20, 30, None], frequency=500, volume=10)
# Neutral_obj.createScene(tasks=['Sound'], num_scenes=5, speed=400, time=1, color=(0,0,0), position=[390, 290], radius=20, arrow_dims=[100, 20, 30, None], frequency=500, volume=10)

