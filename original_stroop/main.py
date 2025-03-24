import pygame
import random
import time
import csv
from original_stroop.audio_processing.transcriber import *
import argparse
import threading

# Initialize Pygame
pygame.init()

parser = argparse.ArgumentParser(description='Run the og stroop test')
parser.add_argument('--num_neutral', type=int, default=12, help='Number of neutral trials')
parser.add_argument('--num_congruent', type=int, default=12, help='Number of congruent trials')
parser.add_argument('--num_conflict', type=int, default=12, help='Number of conflict trials')
parser.add_argument('--screen_width', type=int, default=1700, help='Width of the screen')
parser.add_argument('--screen_height', type=int, default=900, help='Height of the screen')
parser.add_argument('--stimulus_duration', type=float, default=1.5, help='Duration of the stimulus')
parser.add_argument('--inter_stimulus_interval', type=float, default=0.5, help='Interval between stimuli')
parser.add_argument('--background_color', type=str, default="black", help='Background color of the screen')
parser.add_argument('--neutral_words', type=str, default="./neutral_words.txt", help='File containing neutral words')
args = parser.parse_args()
config = vars(args)

# Screen settings
WIDTH, HEIGHT = config["screen_width"], config["screen_height"]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OG Stroop Test")

# Colors dictionary
COLORS = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
}
COLOR_NAMES = list(COLORS.keys())

# Font settings
FONT = pygame.font.Font(None, 80)

# Experiment parameters
num_neutral = config["num_neutral"]
num_congruent = config["num_congruent"]
num_conflict = config["num_conflict"]
stimulus_duration = config["stimulus_duration"]
inter_stimulus_interval = config["inter_stimulus_interval"]
bg_color = config["background_color"]

if bg_color == "black":
    background_color = (0, 0, 0)
elif bg_color == "white":
    background_color = (255, 255, 255)
else:
    print("Invalid background color. Please enter 'black' or 'white'.")
    exit()

text_color = (255, 255, 255)

# it contains tuple of (word, color)
neutral_words_array = []
with open(config["neutral_words"], "r") as f:
    for line in f:
        neutral_words_array.append(tuple(line.strip().split(",")))

print(neutral_words_array)

# Data storage
results = []


# Function to generate a trial
def generate_trial():
    word = random.choice(COLOR_NAMES)
    condition = random.choice(["congruent", "conflict"])

    if condition == "congruent":
        color_name = word
    elif condition == "conflict":
        color_name = random.choice([c for c in COLOR_NAMES if c != word])
    else:
        print("Something is worng with generate_trail functơn in base_test.py")
    # else:  # Neutral condition
    #     word = random.choice(neutral_words_array)
    #     color_name = random.choice(COLOR_NAMES)

    return word, COLORS[color_name], condition

def generate_neutral_trial():
    word = random.choice(neutral_words_array)
    color_name = random.choice(COLOR_NAMES)
    return word, COLORS[color_name], "neutral"

# Function to display text
# def display_text(text, color):
#     screen.fill(background_color)
#     text_surface = FONT.render(text, True, color)
#     text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#     screen.blit(text_surface, text_rect)
#     pygame.display.flip()

def display_text_until_space(text, color):
    screen.fill(background_color)
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def display_text_for_duration(text, color, duration):
    screen.fill(background_color)
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(duration)


# Function to run a single trial
# def run_trial(case = "non-neutral"):
#     if case == "neutral":
#         word, color, condition = generate_neutral_trial()
#     else:
#         word, color, condition = generate_trial()
#     display_text(word, color)

#     start_time = time.time()
#     reaction = None
#     response_time = None

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 return None

#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_r:
#                     reaction = "RED"
#                 elif event.key == pygame.K_g:
#                     reaction = "GREEN"
#                 elif event.key == pygame.K_b:
#                     reaction = "BLUE"
#                 elif event.key == pygame.K_y:
#                     reaction = "YELLOW"

#                 if reaction:
#                     response_time = time.time() - start_time
#                     break

#         # If time exceeds stimulus duration, break
#         if time.time() - start_time > stimulus_duration:
#             break

#     # Determine correctness
#     correct = (
#         1
#         if reaction
#         and reaction == [key for key, val in COLORS.items() if val == color][0]
#         else 0
#     )
#     results.append(
#         [word, condition, reaction, response_time if response_time else "N/A", correct]
#     )

#     # Inter-stimulus interval
#     screen.fill(background_color)
#     pygame.display.flip()
#     time.sleep(inter_stimulus_interval)

def run_neutral(word_color_pair: tuple, filename: str):

    def display_and_record():
        display_text_for_duration(word_color_pair[0], word_color_pair[1], stimulus_duration)
        record_audio(filename, duration=stimulus_duration + 0.25 * inter_stimulus_interval)

    # Start display and recording in a separate thread
    thread = threading.Thread(target=display_and_record)
    thread.start()
    thread.join()

    # Inter-stimulus interval
    screen.fill(background_color)
    pygame.display.flip()
    time.sleep(inter_stimulus_interval * 0.75)
    print(f"time: {time.time() - start_time}")


# Main function to run the experiment
def main():

    neutral_count = 0
    display_text_for_duration("Say the WORD", text_color, 1)
    while neutral_count < num_neutral:
        file_name = f"neutral_{neutral_count}_word.wav"
        run_neutral(neutral_words_array[neutral_count], file_name)
        neutral_count += 1
    # neutral_count = 0
    # display_text_for_duration("Say the COLOR", text_color, 1)
    # while neutral_count < num_neutral:
    #     file_name = f"neutral_{neutral_count}_color.wav"
    #     run_neutral(neutral_words_array[neutral_count], file_name)
    #     neutral_count += 1

    # while running and trial_count < NUM_TRIALS:
    #     run_trial()
    #     trial_count += 1

    # # Save results to CSV
    # with open("stroop_results.csv", "w", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(
    #         ["Word", "Condition", "Response", "Reaction Time (s)", "Correct"]
    #     )
    #     writer.writerows(results)

    # print("Experiment complete! Results saved to stroop_results.csv")
    # pygame.quit()


# Run the experiment
if __name__ == "__main__":
    main()

