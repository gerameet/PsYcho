import pygame
import os
import random
import time
import csv
from audio_processing.transcriber import *
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
parser.add_argument('--stimulus_duration', type=float, default=1, help='Duration of the stimulus')
parser.add_argument('--inter_stimulus_interval', type=float, default=0.25, help='Interval between stimuli')
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

# print(neutral_words_array)

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


def run_case(word_color_pair: tuple, filename: str):
    def display():
        display_text_for_duration(word_color_pair[0], word_color_pair[1], stimulus_duration)

    def record():
        record_audio(filename, duration=stimulus_duration + 0.25 * inter_stimulus_interval)

    # Start two separate threads
    display_thread = threading.Thread(target=display)
    record_thread = threading.Thread(target=record)

    display_thread.start()
    record_thread.start()

    # Wait for both to complete
    display_thread.join()
    record_thread.join()

    # Inter-stimulus interval
    screen.fill(background_color)
    pygame.display.flip()
    time.sleep(inter_stimulus_interval * 0.75)

def play_neutral(usr_folder_path: str):
    neutral_count = 0
    display_text_for_duration("Say the WORD", text_color, 1.5)
    while neutral_count < num_neutral:
        file_name = f"{usr_folder_path}/neutral_{neutral_count}_word.wav"
        run_case(neutral_words_array[neutral_count], file_name)
        neutral_count += 1
    neutral_count = 0
    display_text_for_duration("Say the COLOR", text_color, 1.5)
    while neutral_count < num_neutral:
        file_name = f"{usr_folder_path}/neutral_{neutral_count}_color.wav"
        run_case(neutral_words_array[neutral_count], file_name)
        neutral_count += 1

def play_congruent(usr_folder_path: str):
    COLOR_NAMES_CONGRUENT = COLOR_NAMES * 3
    COLOR_NAMES_CONGRUENT = np.random.permutation(COLOR_NAMES_CONGRUENT)
    congruent_count = 0
    display_text_for_duration("Say the WORD", text_color, 1.5)
    while congruent_count < num_congruent:
        file_name = f"{usr_folder_path}/congruent_{congruent_count}_word.wav"
        run_case((COLOR_NAMES_CONGRUENT[congruent_count], COLORS[COLOR_NAMES_CONGRUENT[congruent_count]]), file_name)
        congruent_count += 1
    congruent_count = 0
    display_text_for_duration("Say the COLOR", text_color, 1.5)
    while congruent_count < num_congruent:
        file_name = f"{usr_folder_path}/congruent_{congruent_count}_color.wav"
        run_case((COLOR_NAMES_CONGRUENT[congruent_count], COLORS[COLOR_NAMES_CONGRUENT[congruent_count]]), file_name)
        congruent_count += 1

def play_conflict(usr_folder_path: str):
    COLOR_NAMES_CONFLICT = []
    for color in COLOR_NAMES:
        for c in COLOR_NAMES:
            if c != color:
                COLOR_NAMES_CONFLICT.append((color, c))
    COLOR_NAMES_CONFLICT = np.random.permutation(COLOR_NAMES_CONFLICT)
    conflict_count = 0
    display_text_for_duration("Say the WORD", text_color, 1.5)
    while conflict_count < num_conflict:
        file_name = f"{usr_folder_path}/conflict_{conflict_count}_word.wav"
        run_case(COLOR_NAMES_CONFLICT[conflict_count], file_name)
        conflict_count += 1
    conflict_count = 0
    display_text_for_duration("Say the COLOR", text_color, 1.5)
    while conflict_count < num_conflict:
        file_name = f"{usr_folder_path}/conflict_{conflict_count}_color.wav"
        run_case(COLOR_NAMES_CONFLICT[conflict_count], file_name)
        conflict_count += 1

# Main function to run the experiment
def main():
    usr_folder_path = "./audio_outputs_abhinav"
    os.makedirs(usr_folder_path, exist_ok=True)
    play_neutral(usr_folder_path)
    play_congruent(usr_folder_path)
    play_conflict(usr_folder_path)
    pygame.quit()

if __name__ == "__main__":
    main()

