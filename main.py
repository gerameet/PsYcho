from tasks import *

text_pause_time = 2
screen = Stage((255, 255, 255), width=1500, height=900)
timer = Timer(screen, 50)
screen.createWindow(1500, 900, 'Trial Run 1')

parameters = {
    'speed': 220,
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
        
        object.createScene(is_block=True, tasks=task_arr,speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'])


def sound_movement(num_neutral, num_block, num_mixed):
    
        write_and_pause(screen, 'Sound and Movement', text_pause_time)
        
        write_and_pause(screen, 'Neutral Mode', text_pause_time)
        Neutral_obj = Neutral(screen, timer)
    
        write_and_pause(screen, 'Sound', text_pause_time)
        Neutral_obj.createScene(tasks=['Sound'], num_scenes= num_neutral, speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
        
        write_and_pause(screen, 'Movement', text_pause_time)
        Neutral_obj.createScene(tasks=['Movement'], num_scenes=num_neutral, speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'])
            
        write_and_pause(screen, 'Mixed Cases - BLOCK', text_pause_time)
        
        # block design
        choice_array = ['Conflict' for i in range(num_block)] + ['Congruent' for i in range(num_block)]
        np.random.shuffle(choice_array)
        for task_arr in [['Sound', 'Movement'], ['Movement', 'Sound']]:
            write_and_pause(screen, task_arr[0], text_pause_time)
            for i in range(len(choice_array)):
                if choice_array[i] == 'Conflict':
                    Conflict_obj = Conflict(screen, timer)
                    Conflict_obj.createScene(is_block = True, tasks=task_arr, speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
                elif choice_array[i] == 'Congruent':
                    Congruent_obj = Congruent(screen, timer)
                    Congruent_obj.createScene(is_block = True, tasks=task_arr, speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
                else:
                    print("Invalid case - (Needs to Be either Congruent or Conflict)!")
    
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
            object.createScene(is_block=True, tasks=task_arr, speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)


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
                object.createScene(is_block=True, tasks=task_arr, speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)


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


def driver():
    with open('data.csv', 'w') as file:
        file.write('polarity,todotask,othertask,correct,total_time,key_pressed,time_taken\n')

    movement_direction(5, 5, 5)
    sound_movement(5, 5, 5)
    direction_sound(5, 5, 5)

    write_and_pause(screen, 'Thank you for participating :)', text_pause_time)

    user_id = get_user_id()
    with open('data.csv', 'r') as file:
        data = file.read()
    with open(f'data/{user_id}.csv', 'w') as file:
        file.write(data)

driver()
