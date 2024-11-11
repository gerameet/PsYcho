from main import *


Num_Scenes_Neutral = {
    'Movement': 5,
    'Direction': 5,
    'Sound': 5
}

Num_Scenes_Mixed = {
    'Movement and Direction': 5,
    'Movement and Sound': 5,
    'Direction and Sound': 5
}

text_pause_time = 3

screen = Stage((255, 255, 255), width=1500, height=900)
timer = Timer(screen, 50)
screen.createWindow(1500, 900, 'Trial Run 1')
pause(1)

write_and_pause(screen, 'Neutral Mode', 3)
Neutral_obj = Neutral(screen, timer)
Neutral_obj.createScene(tasks=['Movement'], num_scenes= Num_Scenes_Neutral['Movement'], speed=400, time=1, color=(0,0,0), position=[390, 290], radius=20, arrow_dims=[100, 20, 30, None])
pause(1)
Neutral_obj.createScene(tasks=['Direction'], num_scenes=Num_Scenes_Neutral['Direction'], speed=400, time=1, color=(0,0,0), position=[390, 290], radius=20, arrow_dims=[100, 20, 30, None], frequency=500, volume=10)
pause(0.5)
Neutral_obj.createScene(tasks=['Sound'], num_scenes=Num_Scenes_Neutral['Sound'], speed=400, time=1, color=(0,0,0), position=[390, 290], radius=20, arrow_dims=[100, 20, 30, None], frequency=500, volume=10)
pause(3)

write_and_pause(screen, 'Movement and Direction', text_pause_time)
cases_Movement_and_Direction = [np.random.choice(['Congruent', 'Conflict']) for i in range(Num_Scenes_Mixed['Movement and Direction'])]
for i in range(len(cases_Movement_and_Direction)):
    if cases_Movement_and_Direction[i] == 'Congruent':
        object = Congruent(screen, timer)
    elif cases_Movement_and_Direction[i] == 'Conflict':
        object = Conflict(screen, timer)
    else:
        print("Invalid case - (Needs to Be either Congruent or Conflict)!")
    object.createScene(tasks=['Movement', 'Direction'],speed=400, time=1, color=(0,0,0), position=[390, 290], radius=20, arrow_dims=[100, 20, 30, None])

write_and_pause(screen, 'Movement and Sound', text_pause_time)
cases_Movement_and_Sound = [np.random.choice(['Congruent', 'Conflict']) for i in range(Num_Scenes_Mixed['Movement and Sound'])]
for i in range(len(cases_Movement_and_Sound)):
    if cases_Movement_and_Sound[i] == 'Congruent':
        object = Congruent(screen, timer)
    elif cases_Movement_and_Sound[i] == 'Conflict':
        object = Conflict(screen, timer)
    else:
        print("Invalid case - (Needs to Be either Congruent or Conflict)!")
    object.createScene(tasks=['Movement', 'Sound'], speed=400, time=1, color=(0,0,0), position=[390, 290], radius=20, arrow_dims=[100, 20, 30, None], frequency=500, volume=10)

write_and_pause(screen, 'Direction and Sound', text_pause_time)
cases_Direction_and_Sound = [np.random.choice(['Congruent', 'Conflict']) for i in range(Num_Scenes_Mixed['Direction and Sound'])]
for i in range(len(cases_Direction_and_Sound)):
    if cases_Direction_and_Sound[i] == 'Congruent':
        object = Congruent(screen, timer)
    elif cases_Direction_and_Sound[i] == 'Conflict':
        object = Conflict(screen, timer)
    else:
        print("Invalid case - (Needs to Be either Congruent or Conflict)!")
    object.createScene(tasks=['Direction', 'Sound'], speed=400, time=1, color=(0,0,0), position=[390, 290], radius=20, arrow_dims=[100, 20, 30, None], frequency=500, volume=10)

write_and_pause(screen, 'End of Trial Run 1', 3)