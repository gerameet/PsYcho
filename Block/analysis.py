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
    
    def get_task_data(self, get_what: str = "both"):
        """
        this function returns the data of the user task wise 
        movement-direction, direction-sound, movement-sound
        both (block and random) refers to all the data - neutral, block and random concatenated
        get_what can be block, random or both
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

        # need to change values based on the data length

        # neutral is the first 20 rows
        # block is the next 20 rows
        # random is the last 20 rows

        neutral_mov_dir = mov_dir[:20]
        neutral_mov_sound = mov_sound[:20]
        neutral_dir_sound = dir_sound[:20]

        block_mov_dir = mov_dir[20:40]
        block_mov_sound = mov_sound[20:40]
        block_dir_sound = dir_sound[20:40]

        random_mov_dir = mov_dir[40:]
        random_mov_sound = mov_sound[40:]
        random_dir_sound = dir_sound[40:]

        if get_what == "block":
            # return neutral and block data concatenated
            mov_dir = pd.concat([neutral_mov_dir, block_mov_dir])
            mov_sound = pd.concat([neutral_mov_sound, block_mov_sound])
            dir_sound = pd.concat([neutral_dir_sound, block_dir_sound])

        elif get_what == "random":
            # return neutral and random data concatenated
            mov_dir = pd.concat([neutral_mov_dir, random_mov_dir])
            mov_sound = pd.concat([neutral_mov_sound, random_mov_sound])
            dir_sound = pd.concat([neutral_dir_sound, random_dir_sound])

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
    def __init__(self, data_folder, get_what: str = "both"):
        """
        takes in a folder of data which contains a csv file for each participant
        get_what can be block, random or both
        refer to the get_task_data function in UserPerformance class
        """
        self.data_folder = data_folder
        self.combined_mov_dir, self.combined_mov_sound, self.combined_dir_sound = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        # store the combined data of all the participants
        self.get_what = get_what
        self.get_combined_task_wise_data()

    def get_combined_task_wise_data(self):
        """
        this function returns the combined data of all the participants
        """
        for file in os.listdir(self.data_folder):
            if file.endswith(".csv"):
                user = UserPerformance(os.path.join(self.data_folder, file))
                mov_dir, mov_sound, dir_sound = user.get_task_data(self.get_what)
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

    def get_distribution_for_plot(self, metrics, tasks, results):
        """
        this function returns the distribution of the results for a task
        """
        polarities = ("neutral", "congruent", "conflict")

        times = [results[polarity][metrics[0]] for polarity in polarities]
        time_task_1 = [time[tasks[0]] for time in times]
        time_task_2 = [time[tasks[1]] for time in times]
        times = [time_task_1, time_task_2]

        accuracies = [results[polarity][metrics[1]] for polarity in polarities]
        accuracies_task_1 = [accuracy[tasks[0]] for accuracy in accuracies]
        accuracies_task_2 = [accuracy[tasks[1]] for accuracy in accuracies]
        accuracies = [accuracies_task_1, accuracies_task_2]

        scores = [results[polarity][metrics[2]] for polarity in polarities]
        scores_task_1 = [score[tasks[0]] for score in scores]
        scores_task_2 = [score[tasks[1]] for score in scores]
        scores = [scores_task_1, scores_task_2]

        return times, accuracies, scores
    
    def plot_results(self):
        results_mov_dir, results_mov_sound, results_dir_sound = self.get_results_task_wise()

        tasks = (["Movement", "Direction"], ["Movement", "Sound"], ["Direction","Sound"])
        polarities = ("neutral", "congruent", "conflict")
        metrics = ("avg_reaction_time", "accuracy", "score")

        mov_dir_times, mov_dir_accuracies, mov_dir_scores = self.get_distribution_for_plot(metrics, tasks[0], results_mov_dir)
        mov_sound_times, mov_sound_accuracies, mov_sound_scores = self.get_distribution_for_plot(metrics, tasks[1], results_mov_sound)
        dir_sound_times, dir_sound_accuracies, dir_sound_scores = self.get_distribution_for_plot(metrics, tasks[2], results_dir_sound)

        plt.figure(figsize=(15, 8))
        ######################## mov_dir ########################
        plt.subplot(3, 3, 1)
        plt.plot(polarities, mov_dir_times[0], label="Movement")
        plt.plot(polarities, mov_dir_times[1], label="Direction")
        plt.ylim(0.5, 1.1)
        plt.title("Time(s)")
        plt.legend()

        plt.subplot(3, 3, 2)
        plt.plot(polarities, mov_dir_accuracies[0], label="Movement")
        plt.plot(polarities, mov_dir_accuracies[1], label="Direction")
        plt.title("Accuracy(%)")
        plt.ylim(60, 105)
        plt.legend()
        
        plt.subplot(3, 3, 3)
        plt.plot(polarities, mov_dir_scores[0], label="Movement")
        plt.plot(polarities, mov_dir_scores[1], label="Direction")
        plt.title("Score")
        plt.ylim(0.1, 0.7)
        plt.legend()

        ######################## mov_sound ########################
        plt.subplot(3, 3, 4)
        plt.plot(polarities, mov_sound_times[0], label="Movement")
        plt.plot(polarities, mov_sound_times[1], label="Sound")
        plt.title("Time(s)")
        plt.ylim(0.5, 1.1)
        plt.legend()

        plt.subplot(3, 3, 5)
        plt.plot(polarities, mov_sound_accuracies[0], label="Movement")
        plt.plot(polarities, mov_sound_accuracies[1], label="Sound")
        plt.title("Accuracy(%)")
        plt.ylim(60, 105)
        plt.legend()

        plt.subplot(3, 3, 6)
        plt.plot(polarities, mov_sound_scores[0], label="Movement")
        plt.plot(polarities, mov_sound_scores[1], label="Sound")
        plt.title("Score")
        plt.ylim(0.1, 0.7)
        plt.legend()

        ######################## dir_sound ########################
        plt.subplot(3, 3, 7)
        plt.plot(polarities, dir_sound_times[0], label="Direction")
        plt.plot(polarities, dir_sound_times[1], label="Sound")
        plt.title("Time(s)")
        plt.ylim(0.5, 1.1)
        plt.legend()

        plt.subplot(3, 3, 8)
        plt.plot(polarities, dir_sound_accuracies[0], label="Direction")
        plt.plot(polarities, dir_sound_accuracies[1], label="Sound")
        plt.title("Accuracy(%)")
        plt.ylim(60, 105)
        plt.legend()

        plt.subplot(3, 3, 9)
        plt.plot(polarities, dir_sound_scores[0], label="Direction")
        plt.plot(polarities, dir_sound_scores[1], label="Sound")
        plt.title("Score")
        plt.ylim(0.1, 0.7)
        plt.legend()

        plt.suptitle(f"Performance Metrics: {self.get_what}")
        plt.tight_layout()
        # plt.show()
        plt.savefig(f"figures/analysis_{self.get_what}.png")

        # print("\n", results_mov_dir, "\n")
        # print("\n", results_mov_sound, "\n")
        # print("\n", results_dir_sound, "\n")
