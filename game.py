import pygame
from random import choice
from sys import exit

class CycleQuest:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Cycle Quest')
        self.screen = pygame.display.set_mode((1024, 768))

        self.states = ["Start Screen", "Map", "Phase 1 Intro", "Bloody Mess",
                       "Badge 1", "Phase 2 Intro", "Hormone Party", "Badge 2"]
        self.current_state = 0

        self.frame_rate = pygame.time.Clock()
    
    def run_game(self):
        if self.states[self.current_state] == "Start Screen":
            self.start_event() 
    
    def start_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
    """Future Game States
    def map_event(self):
        pass

    def phase_1_event(self):
        pass

    def bloody_mess(self):
        pass
    """
