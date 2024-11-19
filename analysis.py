"""

In progress ...


This script is used to analyze the data collected from the experiment.
The data is stored in a csv file for eaach participant in the data folder.
The format is: polarity,todotask,othertask,correct,total_time,key_pressed,time_taken

"""

import pandas as pd
import os
import matplotlib.pyplot as plt


def get_score(data_point):
    """
    polarity,todotask,othertask,correct,total_time,key_pressed,time_taken
    This is the input format of the data point
    """
    
    polarity = data_point[0]
    todotask = data_point[1]
    othertask = data_point[2]
    correct = data_point[3]
    total_time = data_point[4]
    key_pressed = data_point[5]
    time_taken = data_point[6]

    score = 0

        
    return score
        


def read_data(per_participant=False, participant_id=0):
    '''
    Read the data from the csv files
    '''

    data = pd.DataFrame()

    if per_participant == True:
        if participant_id == 0:
            print("Please provide the participant id")
            return
        data = pd.read_csv(f"data/{participant_id}.csv")

    else:
        for file in os.listdir("data"):
            data = pd.concat([data, pd.read_csv(f"data/{file}")])

    return data

def get_3_category_scores(data):
    mov_dir = []
    mov_sound = []
    dir_sound = []

    for i in range(len(data)):
        task_1 = data.iloc[i, 1]
        task_2 = data.iloc[i, 2]

        if task_1 == "Movement" and task_2 == "Direction":
            mov_dir.append(data.iloc[i])
        elif task_1 == "Movement" and task_2 == "Sound":
            mov_sound.append(data.iloc[i])
        elif task_1 == "Direction" and task_2 == "Sound":
            dir_sound.append(data.iloc[i])

    for i in range(len(mov_dir)):
        score = get_score(mov_dir[i])
        print(score)
        mov_dir[i].append(score)

    for i in range(len(mov_sound)):
        score = get_score(mov_sound[i])
        mov_sound[i].append(score)

    for i in range(len(dir_sound)):
        score = get_score(dir_sound[i])
        dir_sound[i].append(score)

    mov_dir = pd.DataFrame(mov_dir)
    mov_sound = pd.DataFrame(mov_sound)
    dir_sound = pd.DataFrame(dir_sound)

    return mov_dir, mov_sound, dir_sound

def get_per_participant_scores(mov_dir, mov_sound, dir_sound):
    mov_dir_score = (0, 0)
    mov_sound_score = (0, 0)
    dir_sound_score = (0, 0)

    mov_dir_count = (0, 0)
    mov_sound_count = (0, 0)
    dir_sound_count = (0, 0)

    for i in range(len(mov_dir)):
        if mov_dir.iloc[i, 1] == "Movement":
            mov_dir_score[0] += mov_dir.iloc[i, 7]
            mov_dir_count[0] += 1
        else:
            mov_dir_score[1] += mov_dir.iloc[i, 7]
            mov_dir_count[1] += 1

    for i in range(len(mov_sound)):
        if mov_sound.iloc[i, 1] == "Movement":
            mov_sound_score[0] += mov_sound.iloc[i, 7]
            mov_sound_count[0] += 1
        else:
            mov_sound_score[1] += mov_sound.iloc[i, 7]
            mov_sound_count[1] += 1

    for i in range(len(dir_sound)):
        if dir_sound.iloc[i, 1] == "Direction":
            dir_sound_score[0] += dir_sound.iloc[i, 7]
            dir_sound_count[0] += 1
        else:
            dir_sound_score[1] += dir_sound.iloc[i, 7]
            dir_sound_count[1] += 1

    mov_dir_score = (mov_dir_score[0]/mov_dir_count[0], mov_dir_score[1]/mov_dir_count[1])
    mov_sound_score = (mov_sound_score[0]/mov_sound_count[0], mov_sound_score[1]/mov_sound_count[1])
    dir_sound_score = (dir_sound_score[0]/dir_sound_count[0], dir_sound_score[1]/dir_sound_count[1])

    scores = {"Movement-Direction": mov_dir_score, "Movement-Sound": mov_sound_score, "Direction-Sound": dir_sound_score}

    return scores


def main():
    per_participant = True
    participant_id = 1
    data = read_data(per_participant=per_participant, participant_id=participant_id)
    mov_dir, mov_sound, dir_sound = get_3_category_scores(data)
    if per_participant:
        participant_score = get_per_participant_scores(mov_dir, mov_sound, dir_sound)
        print(participant_score)

    else:
        # to csv
        mov_dir.to_csv("results/mov_dir.csv")
        mov_sound.to_csv("results/mov_sound.csv")
        dir_sound.to_csv("results/dir_sound.csv")




if __name__ == "__main__":
    main()