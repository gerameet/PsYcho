import pygame
from tasks import *

class ReflexTest:
    def __init__(self):
        """Initialize pygame and display"""
        pygame.init()
        self.display = pygame.display.set_mode((800, 600))
        
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

reflex_test = ReflexTest()
reflex_test.show_split_screen((255, 0, 0), (0, 255, 0), "Left", 10000)

color_assoc = {
    'Movement': ['rg', 'gr', 'rb', 'br'],
    'Direction': ['bg', 'gb', 'br', 'rb'],
    'Sound': ['gr', 'rg', 'bg', 'gb']
}


