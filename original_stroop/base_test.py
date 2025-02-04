import pygame
import random
import time
import csv

# Initialize Pygame
pygame.init()
color_dict = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0)

}

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stroop Test")

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
NUM_TRIALS = 20  # Adjust as needed
Neutral_count = 5 # Adjust as needed
STIMULUS_DURATION = 1.5  # seconds
INTER_STIMULUS_INTERVAL = 0.5  # seconds
background_color = color_dict["black"]
neutral_words_array = ["XXXXX", "YYYYY", "ZZZZZ", "WWWWW", "UUUUU", "TTTTT", "SSSSS", "RRRRR", "QQQQQ", "PPPPP", "OOOOO", "NNNNN", "MMMMM", "LLLLL", "KKKKK", "JJJJJ", "IIIII", "HHHHH", "GGGGG", "FFFFF", "EEEEE", "DDDDD", "CCCCC", "BBBBB", "AAAAA"]

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
def display_text(text, color):
    screen.fill((255, 255, 255))  # White background
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()


# Function to run a single trial
def run_trial(case = "non-neutral"):
    if case == "neutral":
        word, color, condition = generate_neutral_trial()
    else:
        word, color, condition = generate_trial()
    display_text(word, color)

    start_time = time.time()
    reaction = None
    response_time = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reaction = "RED"
                elif event.key == pygame.K_g:
                    reaction = "GREEN"
                elif event.key == pygame.K_b:
                    reaction = "BLUE"
                elif event.key == pygame.K_y:
                    reaction = "YELLOW"

                if reaction:
                    response_time = time.time() - start_time
                    break

        # If time exceeds stimulus duration, break
        if time.time() - start_time > STIMULUS_DURATION:
            break

    # Determine correctness
    correct = (
        1
        if reaction
        and reaction == [key for key, val in COLORS.items() if val == color][0]
        else 0
    )
    results.append(
        [word, condition, reaction, response_time if response_time else "N/A", correct]
    )

    # Inter-stimulus interval
    screen.fill((255, 255, 255))
    pygame.display.flip()
    time.sleep(INTER_STIMULUS_INTERVAL)


# Main function to run the experiment
def main():
    running = True
    trial_count = 0
    neutral_trail_count = 0
    while running and neutral_trail_count < Neutral_count:
        run_trial("neutral")
        neutral_trail_count += 1

    while running and trial_count < NUM_TRIALS:
        run_trial()
        trial_count += 1

    # Save results to CSV
    with open("stroop_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Word", "Condition", "Response", "Reaction Time (s)", "Correct"]
        )
        writer.writerows(results)

    print("Experiment complete! Results saved to stroop_results.csv")
    pygame.quit()


# Run the experiment
if __name__ == "__main__":
    main()
