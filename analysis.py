"""

In progress ...


This script is used to analyze the data collected from the experiment.
The data is stored in a csv file for eaach participant in the data folder.
The format is: polarity,todotask,othertask,correct,total_time,key_pressed,time_taken

"""

import pandas as pd
import os
import matplotlib.pyplot as plt

class UserPerformance:
    """
    Class to analyze the user performance
    """
    def __init__(self, data_path):
        """
        data is a df created from the csv file of the user
        """
        self.data = pd.read_csv(data_path)

    def get_accuracy_and_time(self):
        """
        this function calculates the accuracy and time taken by the user
        """
        total_correct = 0
        for i in range(len(self.data)):
            
            correct = self.data.iloc[i, 3]
            key_pressed = self.data.iloc[i, 5]

            if correct == key_pressed:
                total_correct += 1

        accuracy = total_correct / len(self.data)
        accuracy = (accuracy * 100)
        time_taken = (self.data["time_taken"].sum())
        total_time = (self.data["total_time"].sum())

        # round off the time to 2 decimal places
        time_taken = round(time_taken, 2)
        total_time = round(total_time, 2)
        accuracy = round(accuracy, 2)

        final_score = f"Your accuracy is " + str(accuracy) + "\nYou took " + str(time_taken) + "/" + str(total_time) + " seconds to complete the task."
        return final_score, accuracy, time_taken
    
    def get_task_data(self):
        """
        this function returns the data of the user task wise 
        movement-direction, direction-sound, movement-sound
        """
        len_data = len(self.data)
        task_1 = self.data[:len_data//3]
        task_2 = self.data[len_data//3:2*len_data//3]
        task_3 = self.data[2*len_data//3:]

        mov_dir = pd.DataFrame()
        mov_sound = pd.DataFrame()
        dir_sound = pd.DataFrame()

        for i in range(len(task_1)):
            if task_1.iloc[i, 0] == "congruent":
                tasks = (task_1.iloc[i, 1], task_1.iloc[i, 2])
                if "Movement" in tasks and "Direction" in tasks:
                    mov_dir = task_1
                elif "Movement" in tasks and "Sound" in tasks:
                    mov_sound = task_1
                elif "Direction" in tasks and "Sound" in tasks:
                    dir_sound = task_1

                break

        for i in range(len(task_2)):
            if task_2.iloc[i, 0] == "congruent":
                tasks = (task_2.iloc[i, 1], task_2.iloc[i, 2])
                if "Movement" in tasks and "Direction" in tasks:
                    mov_dir = task_2
                elif "Movement" in tasks and "Sound" in tasks:
                    mov_sound = task_2
                elif "Direction" in tasks and "Sound" in tasks:
                    dir_sound = task_2

                break

        for i in range(len(task_3)):
            if task_3.iloc[i, 0] == "congruent":
                tasks = (task_3.iloc[i, 1], task_3.iloc[i, 2])
                if "Movement" in tasks and "Direction" in tasks:
                    mov_dir = task_3
                elif "Movement" in tasks and "Sound" in tasks:
                    mov_sound = task_3
                elif "Direction" in tasks and "Sound" in tasks:
                    dir_sound = task_3

                break

        return mov_dir, mov_sound, dir_sound

class Task_Analysis:
    """
    Class to analyze task
    """
    def __init__(self, task_data: pd.DataFrame, tasks: tuple):
        """
        takes in the task data of the user
        task_data is the combined df for a task across all users
        tasks is a tuple of the tasks in the task
        """
        self.task_data = task_data
        self.tasks = tasks

    def get_accuracy(self, task_data):
        """
        this function returns the accuracy of all user in the task
        """
        total_correct = 0
        for i in range(len(task_data)):
            correct = task_data.iloc[i, 3]
            key_pressed = task_data.iloc[i, 5]
            if correct == key_pressed:
                total_correct += 1

        accuracy = total_correct / len(task_data)
        accuracy = (accuracy * 100)
        return round(accuracy, 2)
    
    def get_avg_reaction_time(self, task_data):
        """
        this function returns the average reaction time of all user in the task
        """
        return round(task_data["time_taken"].mean(), 2)
    
    def get_score(self, task_data):
        """
        this function returns the score of all user in the task
        """
        def get_correct_score(data_point):
            alpha = 10
            gamma = 2.5
            time_taken = data_point["time_taken"]
            score = alpha/(gamma + time_taken)
            score = (score / 2) - 1
            return round(score, 2)

        def get_incorrect_score(data_point):
            beta = -1
            time_taken = data_point["time_taken"]
            total_time = data_point["total_time"]
            score = beta * time_taken / total_time
            return round(score, 2)

        def get_none_score(data_point):
            return 0
        
        score = 0
        for i in range(len(task_data)):
            correct = task_data.iloc[i, 3]
            key_pressed = task_data.iloc[i, 5]
            if correct == key_pressed:
                score += get_correct_score(task_data.iloc[i])
            elif key_pressed == "none":
                score += get_none_score(task_data.iloc[i])
            else:
                score += get_incorrect_score(task_data.iloc[i])
        
        return round(score/len(task_data), 2)
    
    def get_polarity_performance(self, polarity: str):
        """
        this function returns the performance of all user in the neutral task
        """
        data = self.task_data[self.task_data["polarity"] == polarity]
        task_1_data = data[data["todotask"] == self.tasks[0]]
        task_2_data = data[data["todotask"] == self.tasks[1]]

        times = (self.get_avg_reaction_time(task_1_data), self.get_avg_reaction_time(task_2_data))
        accuracies = (self.get_accuracy(task_1_data), self.get_accuracy(task_2_data))
        scores = (self.get_score(task_1_data), self.get_score(task_2_data))

        results = {"avg_reaction_time": {self.tasks[0]: times[0], self.tasks[1]: times[1]},
                "accuracy": {self.tasks[0]: accuracies[0], self.tasks[1]: accuracies[1]},
                "score": {self.tasks[0]: scores[0], self.tasks[1]: scores[1]}
                }
        return results



class PerformanceMetrics:
    def __init__(self, data_folder):
        """
        takes in a folder of data which contains a csv file for each participant
        """
        self.data_folder = data_folder
        self.combined_mov_dir, self.combined_mov_sound, self.combined_dir_sound = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        # store the combined data of all the participants
        self.get_combined_task_wise_data()

    def get_combined_task_wise_data(self):
        """
        this function returns the combined data of all the participants
        """
        for file in os.listdir(self.data_folder):
            if file.endswith(".csv"):
                user = UserPerformance(os.path.join(self.data_folder, file))
                mov_dir, mov_sound, dir_sound = user.get_task_data()
                self.combined_mov_dir = pd.concat([self.combined_mov_dir, mov_dir])
                self.combined_mov_sound = pd.concat([self.combined_mov_sound, mov_sound])
                self.combined_dir_sound = pd.concat([self.combined_dir_sound, dir_sound])

    def get_results_task_wise(self):
        task_analyser = Task_Analysis(self.combined_mov_dir, ("Movement", "Direction"))
        results_mov_dir = {}
        for polarity in ("neutral", "congruent", "conflict"):
            results_mov_dir[polarity] = task_analyser.get_polarity_performance(polarity)

        task_analyser = Task_Analysis(self.combined_mov_sound, ("Movement", "Sound"))
        results_mov_sound = {}
        for polarity in ("neutral", "congruent", "conflict"):
            results_mov_sound[polarity] = task_analyser.get_polarity_performance(polarity)

        task_analyser = Task_Analysis(self.combined_dir_sound, ("Direction", "Sound"))
        results_dir_sound = {}
        for polarity in ("neutral", "congruent", "conflict"):
            results_dir_sound[polarity] = task_analyser.get_polarity_performance(polarity)

        return results_mov_dir, results_mov_sound, results_dir_sound
    
    def plot_results(self):
        results_mov_dir, results_mov_sound, results_dir_sound = self.get_results_task_wise()

        # on x axis we have neutral, congruent and conflict for each task
        # each row represents a task (for eg Direction and Movement, Movement and Sound, Direction and Sound)
        # each column is a performance measure (time, accuracy, score)
        # it is a 3x3 grid

        print("\n\n")
        print(results_mov_dir)
        print("\n\n")
        print(results_mov_sound)
        print("\n\n")
        print(results_dir_sound)
        print("\n\n")

        
