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


def movement_direction(num_neutral, num_mixed):

    write_and_pause(screen, 'Movement and Direction', text_pause_time)
    
    write_and_pause(screen, 'Get familiar\nNeutral Mode', text_pause_time)
    Neutral_obj = Neutral(screen, timer)
    
    cases_Movement_or_Direction = [np.random.choice(['Movement', 'Direction']) for i in range(num_neutral)]

    for subcase in cases_Movement_or_Direction:
        if subcase == 'Movement':
            Neutral_obj.createScene(tasks=['Movement'], num_scenes= 1, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'])
            pause(1)
        elif subcase == 'Direction':
            Neutral_obj.createScene(tasks=['Direction'], num_scenes=1, speed=parameters['speed'], time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
            pause(0.5)
        else:
            print("Invalid case - (Needs to Be either Movement or Direction)!")

    write_and_pause(screen, 'Get ready to play ...', text_pause_time)

    cases_Movement_and_Direction = [np.random.choice(['Congruent', 'Conflict']) for i in range(num_mixed)]
    congruent_obj = Congruent(screen, timer)
    conflict_obj = Conflict(screen, timer)
    
    for i in range(len(cases_Movement_and_Direction)):
        if cases_Movement_and_Direction[i] == 'Congruent':
            object = congruent_obj
        elif cases_Movement_and_Direction[i] == 'Conflict':
            object = conflict_obj
        else:
            print("Invalid case - (Needs to Be either Congruent or Conflict)!")
        
        object.createScene(tasks=['Movement', 'Direction'],speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'])


def sound_movement(num_neutral, num_mixed):

    write_and_pause(screen, 'Movement and Sound', text_pause_time)
    
    write_and_pause(screen, 'Get familiar\nNeutral Mode', text_pause_time)
    Neutral_obj = Neutral(screen, timer)
    
    cases_Movement_or_Sound = [np.random.choice(['Movement', 'Sound']) for i in range(num_neutral)]

    for subcase in cases_Movement_or_Sound:
        if subcase == 'Movement':
            Neutral_obj.createScene(tasks=['Movement'], num_scenes= 1, speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'])
            pause(1)
        elif subcase == 'Sound':
            Neutral_obj.createScene(tasks=['Sound'], num_scenes=1, speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
            pause(0.5)
        else:
            print("Invalid case - (Needs to Be either Movement or Sound)!")

    write_and_pause(screen, 'Get ready to play ...', text_pause_time)

    cases_Movement_and_Sound = [np.random.choice(['Congruent', 'Conflict']) for i in range(num_mixed)]
    congruent_obj = Congruent(screen, timer)
    conflict_obj = Conflict(screen, timer)
    
    for i in range(len(cases_Movement_and_Sound)):
        if cases_Movement_and_Sound[i] == 'Congruent':
            object = congruent_obj
        elif cases_Movement_and_Sound[i] == 'Conflict':
            object = conflict_obj
        else:
            print("Invalid case - (Needs to Be either Congruent or Conflict)!")

        object.createScene(tasks=['Movement', 'Sound'],speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)


def direction_sound(num_neutral, num_mixed):

    write_and_pause(screen, 'Direction and Sound', text_pause_time)
    
    write_and_pause(screen, 'Get familiar\nNeutral Mode', text_pause_time)
    Neutral_obj = Neutral(screen, timer)

    cases_Direction_or_Sound = [np.random.choice(['Direction', 'Sound']) for i in range(num_neutral)]

    for subcase in cases_Direction_or_Sound:
        if subcase == 'Direction':
            Neutral_obj.createScene(tasks=['Direction'], num_scenes= 1, speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'])
            pause(1)
        elif subcase == 'Sound':
            Neutral_obj.createScene(tasks=['Sound'], num_scenes=1, speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)
            pause(0.5)
        else:
            print("Invalid case - (Needs to Be either Direction or Sound)!")

    write_and_pause(screen, 'Get ready to play ...', text_pause_time)

    cases_Direction_and_Sound = [np.random.choice(['Congruent', 'Conflict']) for i in range(num_mixed)]
    congruent_obj = Congruent(screen, timer)
    conflict_obj = Conflict(screen, timer)
    
    for i in range(len(cases_Direction_and_Sound)):
        if cases_Direction_and_Sound[i] == 'Congruent':
            object = congruent_obj
        elif cases_Direction_and_Sound[i] == 'Conflict':
            object = conflict_obj
        else:
            print("Invalid case - (Needs to Be either Congruent or Conflict)!")

        object.createScene(tasks=['Direction', 'Sound'],speed=400, time= parameters['time'], color= parameters['color'], radius= parameters['radius'], arrow_dims= parameters['arrow_dims'], frequency=500, volume=10)


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

    movement_direction(4, 8)
    sound_movement(4, 8)
    direction_sound(4, 8)

    write_and_pause(screen, 'Thank you for participating :)', text_pause_time)

    user_id = get_user_id()
    with open('data.csv', 'r') as file:
        data = file.read()
    with open(f'data/{user_id}.csv', 'w') as file:
        file.write(data)

driver()
