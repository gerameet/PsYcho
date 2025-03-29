"""

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
            
            correct = self.data.iloc[i, 2]
            response = self.data.iloc[i, 5]

            correct = ''.join(e for e in str(correct).strip().lower() if e.isalnum())
            response = ''.join(e for e in str(response).strip().lower() if e.isalnum())

            if correct == response:
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
            correct = task_data.iloc[i, 2]
            response = task_data.iloc[i, 5]

            correct = ''.join(e for e in str(correct).strip().lower() if e.isalnum())
            response = ''.join(e for e in str(response).strip().lower() if e.isalnum())

            if correct == response:
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
            correct = task_data.iloc[i, 2]
            response = task_data.iloc[i, 5]

            correct = ''.join(e for e in str(correct).strip().lower() if e.isalnum())
            response = ''.join(e for e in str(response).strip().lower() if e.isalnum())

            if correct == response:
                score += get_correct_score(task_data.iloc[i])
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
        get_what can be block, random or both
        refer to the get_task_data function in UserPerformance class
        """
        self.data_folder = data_folder
        self.combined_data = pd.DataFrame()
        self.get_combined_task_wise_data()

    def get_combined_task_wise_data(self):
        """
        this function returns the combined data of all the participants
        """
        for user_folder in os.listdir(self.data_folder):
            file = os.path.join(self.data_folder, user_folder, "data.csv")
            if file.endswith(".csv"):
                user = UserPerformance(file)
                data = user.data
                self.combined_data = pd.concat([self.combined_data, data])

    def get_results_task_wise(self):
        task_analyser = Task_Analysis(self.combined_data, ("word", "color"))
        results = {}
        for polarity in ("neutral", "congruent", "conflict"):
            results[polarity] = task_analyser.get_polarity_performance(polarity)

        return results

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
    
    def plot_results(self, save_path=None):
        results = self.get_results_task_wise()

        tasks = ["word", "color"]
        polarities = ("neutral", "congruent", "conflict")
        metrics = ("avg_reaction_time", "accuracy", "score")

        times, accuracies, scores = self.get_distribution_for_plot(metrics, tasks, results)

        plt.figure(figsize=(15, 5))

        plt.subplot(1, 3, 1)
        plt.plot(polarities, times[0], label="word")
        plt.plot(polarities, times[1], label="color")
        # plt.ylim(0.5, 1.1)
        plt.title("Time(s)")
        plt.legend()

        plt.subplot(1, 3, 2)
        plt.plot(polarities, accuracies[0], label="word")
        plt.plot(polarities, accuracies[1], label="color")
        plt.title("Accuracy(%)")
        # plt.ylim(60, 105)
        plt.legend()
        
        plt.subplot(1, 3, 3)
        plt.plot(polarities, scores[0], label="word")
        plt.plot(polarities, scores[1], label="color")
        plt.title("Score")
        # plt.ylim(0.1, 0.7)
        plt.legend()

        plt.suptitle("Task Performance Analysis")
        plt.tight_layout()
        if save_path:
            plt.savefig(os.path.join(save_path, "og_stroop_pilot.png"))
            print("Plots saved in " + save_path)
        else:
            plt.show()
