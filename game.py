import pygame
from random import choice
from sys import exit

from blood_drop import BloodDrop
from symptom import Symptom
from relief import Relief

class CycleQuest:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Cycle Quest')
        self.screen = pygame.display.set_mode((1024, 768))

        self.states = ["Start Screen", "Map", "Phase Intro", "Bloody Mess",
                       "Badge", "Hormone Party"]
        self.current_state = 0

        self.frame_rate = pygame.time.Clock()

        # Start Screen Graphics
        self.start_screen = pygame.image.load('graphics/start-screen/start_screen.png')
        self.phase = 0

        self.play_button = pygame.image.load('graphics/start-screen/play_button.png')
        self.play_rect = self.play_button.get_rect(center = (468, 690))

        self.info_img = pygame.image.load('graphics/start-screen/info_button.png')
        self.info_rect = self.info_img.get_rect(midleft = (618,690))
        self.popup = pygame.image.load('graphics/start-screen/popup.png')
        self.popup_rect = self.popup.get_rect(center = (512,384))

        self.close_popup = pygame.image.load('graphics/start-screen/continue_button.png')
        self.close_popup_rect = self.close_popup.get_rect(center = (512,480))

        self.show_popup = False

        # Map Graphics
        self.game_maps = [pygame.image.load('graphics/maps/map_phase_1.png'),
                          pygame.image.load('graphics/maps/map_phase_2.png'),
                          pygame.image.load('graphics/maps/map_phase_3.png'),
                          pygame.image.load('graphics/maps/map_phase_4.png')]
        self.start_level_button = pygame.image.load('graphics/maps/start_level_button.png')
        self.start_level_rect = self.start_level_button.get_rect(center = (330, 567))

        # Loading Screens
        self.bloody_mess_intro = pygame.image.load('graphics/bloody-mess/bloody_mess_intro_screen.png')
        self.hormone_party_intro = pygame.image.load('graphics/hormone-party/hormone_party_intro_screen.png')
        self.game_intro_screen = [self.bloody_mess_intro, self.hormone_party_intro]
        self.current_game = 0
        self.start_game_button = pygame.image.load('graphics/start-screen/start_game_button.png')
        self.start_game_rect = self.start_game_button.get_rect(center = (512, 663))

        # Bloody Mess Game Elements
        self.bloody_mess_background = pygame.image.load('graphics/bloody-mess/bloody_mess_background.png')
        self.empty_heart = pygame.image.load('graphics/bloody-mess/empty_heart.png')
        self.filled_heart = pygame.image.load('graphics/bloody-mess/filled_heart.png')
        self.lives = 3

        self.blood_drop = pygame.sprite.GroupSingle()
        self.blood_drop.add(BloodDrop())

        self.create_symptom = pygame.USEREVENT + 1
        pygame.time.set_timer(self.create_symptom, 1000)
        self.create_relief = pygame.USEREVENT + 2
        pygame.time.set_timer(self.create_relief, 7500)
        self.current_symptoms = pygame.sprite.Group()
        self.current_relief = pygame.sprite.Group()

        self.total_game_time = 120000
        self.start_time = 0

        self.game_font = pygame.font.Font('font/Rubik-Regular.ttf', 40)

        # Badge Graphics
        self.bloody_mass_badge = pygame.image.load('graphics/badges/phase_1_badge.png')
        
    
    def run_game(self):
        while True:
            if self.states[self.current_state] == "Start Screen":
                self.start_event() 
                self.screen.blit(self.start_screen, (-4,0))
                self.screen.blit(self.info_img, self.info_rect)
                self.screen.blit(self.play_button, self.play_rect)

                if self.show_popup == True:
                    self.screen.blit(self.popup, self.popup_rect)
                    self.screen.blit(self.close_popup, self.close_popup_rect)
        
            if self.states[self.current_state] == "Map":
                self.map_event()
                self.screen.blit(self.game_maps[self.phase], (0,0))

                if self.phase == 1:
                    self.start_level_rect = self.start_level_button.get_rect(center = (825, 448))
                if self.phase == 2:
                    pass
                if self.phase == 3:
                    pass

                self.screen.blit(self.start_level_button, self.start_level_rect)
            
            if self.states[self.current_state] == "Phase Intro":
                self.screen.blit(self.game_intro_screen[self.current_game], (-4,0))
                self.phase_event()
                self.screen.blit(self.start_game_button, self.start_game_rect)
            
            if self.states[self.current_state] == "Bloody Mess":
                self.bloody_mess()
                self.screen.blit(self.bloody_mess_background, (-4,0))
                if self.lives == 0:
                    self.screen.blit(self.empty_heart, (702,104))
                    self.screen.blit(self.empty_heart, (802,104))
                    self.screen.blit(self.empty_heart, (902,104))
                elif self.lives == 1:
                    self.screen.blit(self.filled_heart, (700, 95))
                    self.screen.blit(self.empty_heart, (802, 104))
                    self.screen.blit(self.empty_heart, (902, 104))
                elif self.lives == 2:
                    self.screen.blit(self.filled_heart, (700, 95))
                    self.screen.blit(self.filled_heart, (800, 95))
                    self.screen.blit(self.empty_heart, (902, 104))
                elif self.lives == 3:
                    self.screen.blit(self.filled_heart, (700, 95))
                    self.screen.blit(self.filled_heart, (800, 95))
                    self.screen.blit(self.filled_heart, (900, 95))
                self.blood_drop.draw(self.screen)
                self.blood_drop.update()
                self.current_symptoms.draw(self.screen)
                self.current_symptoms.update()
                self.current_relief.draw(self.screen)
                self.current_relief.update()
                self.bloody_mess_timer()

            if self.states[self.current_state] == "Badge":
                self.badge()
                self.screen.blit(self.bloody_mass_badge, (-4,0))
                self.close_popup_rect = self.close_popup.get_rect(center = (497,570))
                self.screen.blit(self.close_popup, self.close_popup_rect)
            
            if self.states[self.current_state] == "Hormone Party":
                self.hormone_party()

            pygame.display.update()

            # Set a maximum frame rate
            self.frame_rate.tick(60)


    def start_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.info_rect.collidepoint(mouse_pos):
                    self.show_popup = True
                if self.close_popup_rect.collidepoint(mouse_pos):
                    self.show_popup = False
                if self.play_rect.collidepoint(mouse_pos):
                    self.current_state += 1


    def map_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN and self.start_level_rect.collidepoint(mouse_pos):
                self.current_state = 2

                self.phase += 1


    def phase_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            mouse_pos = pygame.mouse.get_pos()
            
            if event.type == pygame.MOUSEBUTTONDOWN and self.start_game_rect.collidepoint(mouse_pos):
                if self.current_game == 0:
                    self.current_state = 3
                if self.current_game == 1:
                    self.current_state = 5
                self.current_game += 1
                self.start_time = int(pygame.time.get_ticks())


    def bloody_mess(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            available_symptoms = ["acne", "backache", "bloating", 
                                  "breast_soreness", "cravings", "diarrhea", 
                                  "fatigue", "mood_swings"]
            
            available_relief = ["heat_pack", "herbal_tea", "painkiller", 
                                "supplements"]

            if event.type == self.create_symptom:
                self.current_symptoms.add(Symptom(choice(available_symptoms)))   
            if event.type == self.create_relief:
                self.current_relief.add(Relief(choice(available_relief)))
        
            hit_list = pygame.sprite.spritecollide(self.blood_drop.sprite, self.current_symptoms, True)   
            for i in hit_list:
                self.lives -= 1
            hit_list = pygame.sprite.spritecollide(self.blood_drop.sprite, self.current_relief, True)   
            for i in hit_list:
                if self.lives < 3:
                    self.lives += 1

            if self.lives == 0:
                self.current_state += 1
            
    
    def bloody_mess_timer(self):
        score = self.start_time + self.total_game_time - int(pygame.time.get_ticks())
        score_surface = self.game_font.render(str(int(score/1000)), False, (255,255,255))
        score_rectangle = score_surface.get_rect(topright=(945, 30))
        self.screen.blit(score_surface, score_rectangle)
        if score == 0:
            self.current_state += 1

    def badge(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            mouse_pos = pygame.mouse.get_pos()
            
            if event.type == pygame.MOUSEBUTTONDOWN and self.popup_rect.collidepoint(mouse_pos):
                self.current_state = 1


    def hormone_party(self):
        pass
