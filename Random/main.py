from tasks import *
import argparse
from analysis import *

parser = argparse.ArgumentParser(description='Run the experiment')
parser.add_argument('--num_neutral', type=int, default=1, help='Number of neutral tasks')
parser.add_argument('--num_block', type=int, default=0, help='Number of block tasks')
parser.add_argument('--num_mixed', type=int, default=0, help='Number of mixed tasks')
parser.add_argument('--screen_width', type=int, default=1700, help='Width of the screen')
parser.add_argument('--screen_height', type=int, default=900, help='Height of the screen')
parser.add_argument('--speed', type=int, default=250, help='Speed of the arrow')

args = parser.parse_args()
config = vars(args)

screen_width = 1700
screen_height = 900
text_pause_time = 2
screen = Stage((255, 255, 255), width=screen_width, height=screen_height)
timer = Timer(screen, 50)
screen.createWindow(screen_width, screen_height, 'Trial Run 1')

parameters = {
    'speed': 250,
    'time': 2.5,
    'color': (0, 0, 0),
    'radius': 50,
    'arrow_dims': [150, 90, 90, None]
}

pause(1)

def movement_direction(num_neutral, num_block, num_mixed):

    write_and_pause(screen, 'Movement and Direction', text_pause_time)

    write_and_pause(screen, 'Neutral Mode', text_pause_time)
    Neutral_obj = Neutral(screen, timer)

    write_and_pause(screen, 'Movement', text_pause_time)
    Neutral_obj.createScene(tasks=['Movement'], num_scenes= num_neutral, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'])
    
    write_and_pause(screen, 'Direction', text_pause_time)
    Neutral_obj.createScene(tasks=['Direction'], num_scenes=num_neutral, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
        
    write_and_pause(screen, 'Mixed Cases - BLOCK', text_pause_time)
    
    # block design
    choice_array = ['Conflict' for i in range(num_block)] + ['Congruent' for i in range(num_block)]
    np.random.shuffle(choice_array)
    for task_arr in [['Movement', 'Direction'], ['Direction', 'Movement']]:
        write_and_pause(screen, task_arr[0], text_pause_time)
        for i in range(len(choice_array)):
            if choice_array[i] == 'Conflict':
                Conflict_obj = Conflict(screen, timer)
                Conflict_obj.createScene(is_block = True, tasks=task_arr, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'])
            elif choice_array[i] == 'Congruent':
                Congruent_obj = Congruent(screen, timer)
                Congruent_obj.createScene(is_block = True, tasks=task_arr, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'])
            else:
                print("Invalid case - (Needs to Be either Congruent or Conflict)!")

    """
    # mixed design
    write_and_pause(screen, 'Mixed Cases - RANDOM', text_pause_time)
    choice_mat = np.ones((2, 2))*num_mixed
    choice_array_mixed = ['00' for i in range(num_mixed)] + ['01' for i in range(num_mixed)] + ['10' for i in range(num_mixed)] + ['11' for i in range(num_mixed)]
    np.random.shuffle(choice_array_mixed)
    # cases_Movement_and_Direction = [np.random.choice(['Congruent', 'Conflict']) for i in range(num_mixed)]
    congruent_obj = Congruent(screen, timer)
    conflict_obj = Conflict(screen, timer)
    for i in range(len(choice_array_mixed)):
        if choice_array_mixed[i][0] == '0' and choice_array_mixed[i][1] == '0': #congruent and movement
            object = congruent_obj
            task_arr = ['Movement', 'Direction']
        elif choice_array_mixed[i][0] == '0' and choice_array_mixed[i][1] == '1': #congruent and direction
            object = congruent_obj
            task_arr = ['Direction', 'Movement']
        elif choice_array_mixed[i][0] == '1' and choice_array_mixed[i][1] == '0': #conflict and movement
            object = conflict_obj
            task_arr = ['Movement', 'Direction']
        elif choice_array_mixed[i][0] == '1' and choice_array_mixed[i][1] == '1': #conflict and direction
            object = conflict_obj
            task_arr = ['Direction', 'Movement']
        else:
            print("Invalid case - (Needs to Be either Congruent or Conflict)!")
        choice_mat[int(choice_array_mixed[i][0])][int(choice_array_mixed[i][1])] -= 1
        
        object.createScene(is_block=True, tasks=task_arr,speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'])
    """

def sound_movement(num_neutral, num_block, num_mixed):
    
    write_and_pause(screen, 'Sound and Movement', text_pause_time)
    
    write_and_pause(screen, 'Neutral Mode', text_pause_time)
    Neutral_obj = Neutral(screen, timer)

    write_and_pause(screen, 'Sound', text_pause_time)
    Neutral_obj.createScene(tasks=['Sound'], num_scenes= num_neutral, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
    
    write_and_pause(screen, 'Movement', text_pause_time)
    Neutral_obj.createScene(tasks=['Movement'], num_scenes=num_neutral, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'])
        
    write_and_pause(screen, 'Mixed Cases - BLOCK', text_pause_time)
    
    # block design
    choice_array = ['Conflict' for i in range(num_block)] + ['Congruent' for i in range(num_block)]
    np.random.shuffle(choice_array)
    for task_arr in [['Sound', 'Movement'], ['Movement', 'Sound']]:
        write_and_pause(screen, task_arr[0], text_pause_time)
        for i in range(len(choice_array)):
            if choice_array[i] == 'Conflict':
                Conflict_obj = Conflict(screen, timer)
                Conflict_obj.createScene(is_block = True, tasks=task_arr, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
            elif choice_array[i] == 'Congruent':
                Congruent_obj = Congruent(screen, timer)
                Congruent_obj.createScene(is_block = True, tasks=task_arr, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
            else:
                print("Invalid case - (Needs to Be either Congruent or Conflict)!")

    """
    # mixed design
    write_and_pause(screen, 'Mixed Cases - RANDOM', text_pause_time)
    choice_mat = np.ones((2, 2))*num_mixed
    choice_array_mixed = ['00' for i in range(num_mixed)] + ['01' for i in range(num_mixed)] + ['10' for i in range(num_mixed)] + ['11' for i in range(num_mixed)]
    np.random.shuffle(choice_array_mixed)
    # cases_Movement_and_Direction = [np.random.choice(['Congruent', 'Conflict']) for i in range(num_mixed)]
    congruent_obj = Congruent(screen, timer)
    conflict_obj = Conflict(screen, timer)

    for i in range(len(choice_array_mixed)):
        if choice_array_mixed[i][0] == '0' and choice_array_mixed[i][1] == '0':
            object = congruent_obj
            task_arr = ['Sound', 'Movement']
        elif choice_array_mixed[i][0] == '0' and choice_array_mixed[i][1] == '1':
            object = congruent_obj
            task_arr = ['Movement', 'Sound']
        elif choice_array_mixed[i][0] == '1' and choice_array_mixed[i][1] == '0':
            object = conflict_obj
            task_arr = ['Sound', 'Movement']
        elif choice_array_mixed[i][0] == '1' and choice_array_mixed[i][1] == '1':
            object = conflict_obj
            task_arr = ['Movement', 'Sound']
        else:
            print("Invalid case - (Needs to Be either Congruent or Conflict)!")
        choice_mat[int(choice_array_mixed[i][0])][int(choice_array_mixed[i][1])] -= 1
        object.createScene(is_block=True, tasks=task_arr, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
    """

def direction_sound(num_neutral, num_block, num_mixed):
        
    write_and_pause(screen, 'Direction and Sound', text_pause_time)
    
    write_and_pause(screen, 'Neutral Mode', text_pause_time)
    Neutral_obj = Neutral(screen, timer)

    write_and_pause(screen, 'Direction', text_pause_time)
    Neutral_obj.createScene(tasks=['Direction'], num_scenes= num_neutral, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'])
    
    write_and_pause(screen, 'Sound', text_pause_time)
    Neutral_obj.createScene(tasks=['Sound'], num_scenes=num_neutral, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
        
    write_and_pause(screen, 'Mixed Cases - BLOCK', text_pause_time)
    
    # block design
    choice_array = ['Conflict' for i in range(num_block)] + ['Congruent' for i in range(num_block)]
    np.random.shuffle(choice_array)
    for task_arr in [['Direction', 'Sound'], ['Sound', 'Direction']]:
        write_and_pause(screen, task_arr[0], text_pause_time)
        for i in range(len(choice_array)):
            if choice_array[i] == 'Conflict':
                Conflict_obj = Conflict(screen, timer)
                Conflict_obj.createScene(is_block = True, tasks=task_arr, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
            elif choice_array[i] == 'Congruent':
                Congruent_obj = Congruent(screen, timer)
                Congruent_obj.createScene(is_block = True, tasks=task_arr, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
            else:
                print("Invalid case - (Needs to Be either Congruent or Conflict)!")

    """
    # mixed design
    write_and_pause(screen, 'Mixed Cases - RANDOM', text_pause_time)
    choice_mat = np.ones((2, 2))*num_mixed
    choice_array_mixed = ['00' for i in range(num_mixed)] + ['01' for i in range(num_mixed)] + ['10' for i in range(num_mixed)] + ['11' for i in range(num_mixed)]
    np.random.shuffle(choice_array_mixed)
    # cases_Movement_and_Direction = [np.random.choice(['Congruent', 'Conflict']) for i in range(num_mixed)]
    congruent_obj = Congruent(screen, timer)
    conflict_obj = Conflict(screen, timer)
    
    for i in range(len(choice_array_mixed)):
        if choice_array_mixed[i][0] == '0' and choice_array_mixed[i][1] == '0':
            object = congruent_obj
            task_arr = ['Direction', 'Sound']
        elif choice_array_mixed[i][0] == '0' and choice_array_mixed[i][1] == '1':
            object = congruent_obj
            task_arr = ['Sound', 'Direction']
        elif choice_array_mixed[i][0] == '1' and choice_array_mixed[i][1] == '0':
            object = conflict_obj
            task_arr = ['Direction', 'Sound']
        elif choice_array_mixed[i][0] == '1' and choice_array_mixed[i][1] == '1':
            object = conflict_obj
            task_arr = ['Sound', 'Direction']
        else:
            print("Invalid case - (Needs to Be either Congruent or Conflict)!")
        choice_mat[int(choice_array_mixed[i][0])][int(choice_array_mixed[i][1])] -= 1
        object.createScene(is_block=True, tasks=task_arr, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
    """

def get_user_id():
    # starts with 0 written in the file
    with open('user_ids.txt', 'r') as file:
        lines = file.readlines()
        last_line = lines[-1]
        last_id = int(last_line.strip())
        new_id = last_id + 1
    # write new id to the file
    with open('user_ids.txt', 'a') as file:
        file.write(f'{new_id}\n')
    return new_id

def randomize_order_of_tasks():
    """
    Randomizes the order of tasks for a user
    """
    list_of_tasks = ['mov_dir', 'sound_mov', 'dir_sound']
    np.random.shuffle(list_of_tasks)
    return list_of_tasks


def driver():
    with open('data.csv', 'w') as file:
        file.write('polarity,todotask,othertask,correct,total_time,key_pressed,time_taken\n')

    no_use_obj = Neutral(screen, timer)

    write_and_pause(screen, 'Welcome !!', text_pause_time)
    
    # refractory test  -> get refractory time as output

    order_of_tasks = randomize_order_of_tasks()
    for task in order_of_tasks:
        if task == 'mov_dir':
            movement_direction(10, 5, 5)
        elif task == 'sound_mov':
            sound_movement(10, 5, 5)
        elif task == 'dir_sound':
            direction_sound(10, 5, 5)
        else:
            print("Invalid task")
    
    write_and_pause(screen, 'Thank you for participating :)', text_pause_time)

    user_id = get_user_id()
    with open('data.csv', 'r') as file:
        data = file.read()
    with open(f'data/{user_id}.csv', 'w') as file:
        file.write(data)

    user_perf = UserPerformance(f'data/{user_id}.csv')
    final_score, accuracy, time_taken = user_perf.get_accuracy_and_time()

    with open('results/individual_scores.csv', 'a') as file:
        file.write(f'{user_id},{accuracy},{time_taken}\n')

    print("\n\n",final_score,"\n\n")

driver()
