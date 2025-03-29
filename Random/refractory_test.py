import pygame
from tasks import *
import numpy as np

class ReflexTest:
    def __init__(self, screen_size: tuple=(800, 600)):
        """Initialize pygame and display"""
        pygame.init()
        self.display = pygame.display.set_mode(screen_size)
        
    def show_split_screen(self, color1, color2, text, stay_time):
        """
        Display split colored screen with centered text
        
        Parameters:
            color1: RGB tuple for left side
            color2: RGB tuple for right side  
            text: string to display
            stay_time: duration in milliseconds
        """
        width = self.display.get_width()
        height = self.display.get_height()
        
        # Draw left and right halves
        pygame.draw.rect(self.display, color1, (0, 0, width//2, height))
        pygame.draw.rect(self.display, color2, (width//2, 0, width//2, height))
        
        # Create black rectangle at center
        text_bg = pygame.Surface((400, 100))
        text_bg.fill((0, 0, 0))
        text_bg_rect = text_bg.get_rect(center=(width//2, height//2))
        self.display.blit(text_bg, text_bg_rect)
        
        # Render text
        font = pygame.font.Font(None, 48)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width//2, height//2))
        self.display.blit(text_surface, text_rect)
        
        # Update display and wait
        pygame.display.flip()
        pygame.time.wait(stay_time)
        
    def cleanup(self):
        """Cleanup pygame resources"""
        pygame.quit()

# reflex_test = ReflexTest()
# reflex_test.show_split_screen((255, 0, 0), (0, 255, 0), "Left", 10000)

color_assoc = {
    'Movement': ['rg', 'gr', 'rb', 'br'],
    'Direction': ['bg', 'gb', 'br', 'rb'],
    'Sound': ['gr', 'rg', 'bg', 'gb']
}

# list of tuples with color associations - 12 elements in total
color_assoc_extended = []
for key, val in color_assoc.items():
    for v in val:
        color_assoc_extended.append((key, v))

color_vals = {
    'r': (255, 0, 0),
    'g': (0, 255, 0),
    'b': (0, 0, 255)
}

def run_refractory_test(color_assoc: dict=color_assoc, color_vals: dict=color_vals, pause_time: float=1, screen_size: tuple=(800, 600)):
    """Run refractory period test"""

    Test = ReflexTest(screen_size=screen_size)
    num_cases = 1
    count_array = len(color_assoc_extended)*[num_cases]
    print(count_array)

    while sum(count_array) > 0:
        choose_non_zero = np.random.choice(np.nonzero(count_array)[0])
        count_array[choose_non_zero] -= 1
        color_type, color_pair = color_assoc_extended[choose_non_zero]
        color1, color2 = color_vals[color_pair[0]], color_vals[color_pair[1]]
        Test.show_split_screen(color1, color2, color_type, pause_time*1000)
        Test.show_split_screen((0, 0, 0), (0, 0, 0), '', pause_time*1000)

    Test.cleanup()
    

run_refractory_test(screen_size=(1700, 900))







