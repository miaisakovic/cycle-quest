import pygame
from random import choice, randint
from sys import exit

from phase_1.blood_drop import BloodDrop
from phase_1.symptom import Symptom
from phase_1.relief import Relief
from phase_3.egg import Egg
from phase_3.obstacle_top import TopObstacle
from phase_3.obstacle_bottom import BottomObstacle

class CycleQuest:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Cycle Quest')
        self.screen = pygame.display.set_mode((1024, 768))
        self.frame_rate = pygame.time.Clock()
        self.game_font = pygame.font.Font('font/Rubik-ExtraBold.ttf', 40)

        self.states = ["Start Screen", "Map", "Phase Intro", "Bloody Mess",
                       "Hormone Party", "Eggscape", "Eggscape Stage",
                       "Badge", "Unachieved Badge"]
        self.current_state = 0
        self.phase = 0

        # Start Screen Graphics
        self.start_screen_background = pygame.image.load('graphics/start-screen/start_screen.png')

        self.play_button = pygame.image.load('graphics/start-screen/play_button.png')
        self.play_rect = self.play_button.get_rect(center = (468, 690))

        self.info_button = pygame.image.load('graphics/start-screen/info_button.png')
        self.info_rect = self.info_button.get_rect(midleft = (618,690))

        self.show_popup = False
        self.popup = pygame.image.load('graphics/start-screen/popup.png')
        self.popup_rect = self.popup.get_rect(center = (512,384))

        self.continue_button = pygame.image.load('graphics/start-screen/continue_button.png')
        self.continue_rect = self.continue_button.get_rect(center = (512,480))

        # Map Graphics
        self.game_maps = [pygame.image.load('graphics/maps/map_phase_1.png'),
                          pygame.image.load('graphics/maps/map_phase_2.png'),
                          pygame.image.load('graphics/maps/map_phase_3.png'),
                          pygame.image.load('graphics/maps/map_phase_4.png')]

        self.start_level_button = pygame.image.load('graphics/maps/start_level_button.png')
        self.start_level_rect = self.start_level_button.get_rect(center = (330, 567))

        # Phase Intro Graphics
        self.phase_intro_screens = [pygame.image.load('graphics/bloody-mess/bloody_mess_intro_screen.png'), 
                                    pygame.image.load('graphics/hormone-party/hormone_party_intro_screen.png'), 
                                    pygame.image.load('graphics/eggscape/eggscape_intro_screen.png')]

        self.start_game_button = pygame.image.load('graphics/start-screen/start_game_button.png')
        self.start_game_rect = self.start_game_button.get_rect(center = (512, 663))

        # Bloody Mess Game Elements
        self.bloody_mess_background = pygame.image.load('graphics/bloody-mess/bloody_mess_background.png')
        self.empty_heart = pygame.image.load('graphics/bloody-mess/empty_heart.png')
        self.filled_heart = pygame.image.load('graphics/bloody-mess/filled_heart.png')
        self.lives = 3
    
        self.total_game_time = 15000
        self.start_time = 0

        self.blood_drop = pygame.sprite.GroupSingle()
        self.blood_drop.add(BloodDrop())

        self.create_symptom = pygame.USEREVENT + 1
        pygame.time.set_timer(self.create_symptom, 1000)
        self.current_symptoms = pygame.sprite.Group()

        self.create_relief = pygame.USEREVENT + 2
        pygame.time.set_timer(self.create_relief, 7500)
        self.current_relief = pygame.sprite.Group()

        # Hormone Party Game Elements
        self.cards = [pygame.image.load('graphics/hormone-party/myth_or_fact_round_1.png'),
                      pygame.image.load('graphics/hormone-party/myth_or_fact_answer_1.png'),
                      pygame.image.load('graphics/hormone-party/myth_or_fact_round_2.png'),
                      pygame.image.load('graphics/hormone-party/myth_or_fact_answer_2.png'),
                      pygame.image.load('graphics/hormone-party/myth_or_fact_round_3.png'),
                      pygame.image.load('graphics/hormone-party/myth_or_fact_answer_3.png'),
                      pygame.image.load('graphics/hormone-party/myth_or_fact_round_4.png'),
                      pygame.image.load('graphics/hormone-party/myth_or_fact_answer_4.png'),
                      pygame.image.load('graphics/hormone-party/myth_or_fact_round_5.png'),
                      pygame.image.load('graphics/hormone-party/myth_or_fact_answer_5.png'),
                      pygame.image.load('graphics/hormone-party/myth_or_fact_round_6.png'),
                      pygame.image.load('graphics/hormone-party/myth_or_fact_answer_6.png')]
        self.card_counter = 0
        self.score = 0

        self.fact_button = pygame.image.load('graphics/hormone-party/fact_button.png')
        self.fact_rect = self.fact_button.get_rect(center = (623, 572))

        self.myth_button = pygame.image.load('graphics/hormone-party/myth_button.png')
        self.myth_rect = self.myth_button.get_rect(center = (370, 572))

        # Eggscape Game Elements
        self.eggscape_background = pygame.image.load('graphics/eggscape/eggscape_background.png')
        self.eggscape_stages = [pygame.image.load('graphics/eggscape/stage_1.png'),
                                pygame.image.load('graphics/eggscape/stage_2.png'),
                                pygame.image.load('graphics/eggscape/stage_3.png')]
        self.current_eggscape_stage = 0

        self.next_stage_button = pygame.image.load('graphics/eggscape/next_stage_button.png')
        self.next_stage_rect = self.next_stage_button.get_rect(center = (510, 660))

        self.play_again_button = pygame.image.load('graphics/eggscape/play_again_button.png')
        self.play_again_rect = self.play_again_button.get_rect(center = (498, 570))

        self.egg = pygame.sprite.GroupSingle()
        self.egg.add(Egg())

        self.create_obstacle = pygame.USEREVENT + 3
        pygame.time.set_timer(self.create_obstacle, 3500)
        self.current_obstacles = pygame.sprite.Group()
        self.num_obstacles_passed = 0

        # Badge Graphics
        self.badges = [pygame.image.load('graphics/badges/phase_1_badge.png'),
                       pygame.image.load('graphics/badges/phase_2_badge.png')]
        
        self.unachieved_badge_eggscape = pygame.image.load('graphics/badges/phase_3_unachieved_badge.png')

    def run_game(self):
        while True:
            if self.states[self.current_state] == "Start Screen":
                self.start_screen() 

            if self.states[self.current_state] == "Map":
                self.game_map()

            if self.states[self.current_state] == "Phase Intro":
                self.phase_intro()

            if self.states[self.current_state] == "Bloody Mess":
                self.bloody_mess()

            if self.states[self.current_state] == "Hormone Party":
                self.hormone_party()

            if self.states[self.current_state] == "Eggscape":
                 self.eggscape()

            if self.states[self.current_state] == "Eggscape Stage":
                self.eggscape_stage()

            if self.states[self.current_state] == "Badge":
                self.badge()

            if self.states[self.current_state] == "Unachieved Badge":
                self.unachieved_badge()

            pygame.display.update()

            # Set a maximum frame rate
            self.frame_rate.tick(60)

    def quit_game(self, event):
        if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def start_screen(self):
        for event in pygame.event.get():
            self.quit_game(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.info_rect.collidepoint(mouse_pos):
                    self.show_popup = True
                if self.continue_rect.collidepoint(mouse_pos):
                    self.show_popup = False
                if self.play_rect.collidepoint(mouse_pos):
                    self.current_state += 1

        self.screen.blit(self.start_screen_background, (-4,0))
        self.screen.blit(self.info_button, self.info_rect)
        self.screen.blit(self.play_button, self.play_rect)

        if self.show_popup == True:
            self.screen.blit(self.popup, self.popup_rect)
            self.screen.blit(self.continue_button, self.continue_rect)

    def game_map(self):
        for event in pygame.event.get():
            self.quit_game(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN and self.start_level_rect.collidepoint(mouse_pos):
                self.current_state = 2

        self.screen.blit(self.game_maps[self.phase], (0,0))

        if self.phase == 1:
            self.start_level_rect = self.start_level_button.get_rect(center = (825, 448))
        if self.phase == 2:
            self.start_level_rect = self.start_level_button.get_rect(center = (287, 270))

        self.screen.blit(self.start_level_button, self.start_level_rect)

    def phase_intro(self):
        for event in pygame.event.get():
            self.quit_game(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN and self.start_game_rect.collidepoint(mouse_pos):
                if self.phase == 0:
                    self.current_state = 3
                if self.phase == 1:
                    self.current_state = 4
                if self.phase == 2:
                    self.current_state = 6
                self.start_time = int(pygame.time.get_ticks())

        self.screen.blit(self.phase_intro_screens[self.phase], (-4,0))
        self.screen.blit(self.start_game_button, self.start_game_rect)

    def bloody_mess(self):
        for event in pygame.event.get():
            self.quit_game(event)

            available_symptoms = ["acne", "backache", "bloating", 
                                  "breast_soreness", "cravings", "diarrhea", 
                                  "fatigue", "mood_swings"]

            available_relief = ["heat_pack", "herbal_tea", "painkiller", 
                                "supplements"]

            if event.type == self.create_symptom:
                self.current_symptoms.add(Symptom(choice(available_symptoms)))

            if event.type == self.create_relief:
                self.current_relief.add(Relief(choice(available_relief)))

            symptom_hit_list = pygame.sprite.spritecollide(self.blood_drop.sprite, self.current_symptoms, True)   
            self.lives -= len(symptom_hit_list)
            if self.lives < 0:
                self.lives = 0

            relief_hit_list = pygame.sprite.spritecollide(self.blood_drop.sprite, self.current_relief, True)   
            self.lives += len(relief_hit_list)
            if self.lives > 3:
                self.lives = 3

            if self.lives == 0:
                self.current_symptoms.empty()
                self.current_relief.empty()
                self.current_state = 7

        self.screen.blit(self.bloody_mess_background, (-4,0))

        if self.lives == 0:
            self.screen.blit(self.empty_heart, (702,104))
            self.screen.blit(self.empty_heart, (802,104))
            self.screen.blit(self.empty_heart, (902,104))

        if self.lives == 1:
            self.screen.blit(self.filled_heart, (700, 95))
            self.screen.blit(self.empty_heart, (802, 104))
            self.screen.blit(self.empty_heart, (902, 104))

        if self.lives == 2:
            self.screen.blit(self.filled_heart, (700, 95))
            self.screen.blit(self.filled_heart, (800, 95))
            self.screen.blit(self.empty_heart, (902, 104))

        if self.lives == 3:
            self.screen.blit(self.filled_heart, (700, 95))
            self.screen.blit(self.filled_heart, (800, 95))
            self.screen.blit(self.filled_heart, (900, 95))

        self.bloody_mess_timer()
        self.blood_drop.draw(self.screen)
        self.blood_drop.update()
        self.current_symptoms.draw(self.screen)
        self.current_symptoms.update()
        self.current_relief.draw(self.screen)
        self.current_relief.update()

    def bloody_mess_timer(self):
        score = self.start_time + self.total_game_time - int(pygame.time.get_ticks())
        score_surface = self.game_font.render(str(int(score/1000)), False, (255,255,255))
        score_rectangle = score_surface.get_rect(topright=(945, 30))
        self.screen.blit(score_surface, score_rectangle)
        if score <= 0 : self.current_state = 7

    def hormone_party(self):
        for event in pygame.event.get():
            self.quit_game(event)

            mouse_pos = pygame.mouse.get_pos()

            if self.card_counter % 2 == 0:
                if event.type == pygame.MOUSEBUTTONDOWN and self.fact_rect.collidepoint(mouse_pos):
                    if self.card_counter == 4 or self.card_counter == 8 or self.card_counter == 10:
                        self.score += 1
                    self.card_counter += 1
                if event.type == pygame.MOUSEBUTTONDOWN and self.myth_rect.collidepoint(mouse_pos):
                    if self.card_counter == 0 or self.card_counter == 2 or self.card_counter == 6:
                        self.score += 1
                    self.card_counter += 1
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and self.continue_rect.collidepoint(mouse_pos):
                    self.card_counter += 1
                    if self.card_counter == 12:
                        self.current_state = 7

        if self.card_counter != 12:
            self.screen.blit(self.cards[self.card_counter], (-4,0))

            if self.card_counter % 2 == 0: 
                self.screen.blit(self.fact_button, self.fact_rect)
                self.screen.blit(self.myth_button, self.myth_rect)
            else:
                self.continue_rect = self.continue_button.get_rect(center = (497,563))
                self.screen.blit(self.continue_button, self.continue_rect)

            score_surface = self.game_font.render(str(self.score) + '/6', False, (255,255,255))
            score_rectangle = score_surface.get_rect(topright=(945, 30))
            self.screen.blit(score_surface, score_rectangle)

    def eggscape(self):
        for event in pygame.event.get():
            self.quit_game(event)

            if event.type == self.create_obstacle:
                self.num_obstacles_passed += 1
                x_pos = randint(1080, 1600)
                obstacle_item = randint(1,4)
                self.current_obstacles.add(TopObstacle(obstacle_item, x_pos))
                self.current_obstacles.add(BottomObstacle(obstacle_item, x_pos))

            if self.num_obstacles_passed == 5:
                if not self.current_eggscape_stage == 2:
                    self.current_state = 6
                    self.current_eggscape_stage += 1

            hit_list = pygame.sprite.spritecollide(self.egg.sprite, self.current_obstacles, True)   
            if len(hit_list) > 0:
                self.current_state = 8

        self.screen.blit(self.eggscape_background, (0,0))
        self.egg.draw(self.screen)
        self.egg.update()
        self.current_obstacles.draw(self.screen)
        self.current_obstacles.update()

    def eggscape_stage(self):
        for event in pygame.event.get():
            self.quit_game(event)

            mouse_pos = pygame.mouse.get_pos()    

            if event.type == pygame.MOUSEBUTTONDOWN and self.next_stage_rect.collidepoint(mouse_pos):
                self.current_obstacles.empty()
                self.current_obstacles = pygame.sprite.Group()
                self.num_obstacles_passed = 0
                self.current_state -= 1

        self.screen.blit(self.eggscape_stages[self.current_eggscape_stage], (-4,0))
        self.screen.blit(self.next_stage_button, self.next_stage_rect)

    def badge(self):
        for event in pygame.event.get():
            self.quit_game(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN and self.continue_rect.collidepoint(mouse_pos):
                self.current_state = 1
                self.phase += 1

        if self.current_state == 7:
            self.screen.blit(self.badges[self.phase], (-4,0))
            self.continue_rect = self.continue_button.get_rect(center = (497,570))
            self.screen.blit(self.continue_button, self.continue_rect)

    def unachieved_badge(self):
        for event in pygame.event.get():
            self.quit_game(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN and self.play_again_rect.collidepoint(mouse_pos):
                self.current_obstacles.empty()
                self.current_obstacles = pygame.sprite.Group()
                self.num_obstacles_passed = 0
                self.current_eggscape_stage = 0
                self.current_state = 2

        self.screen.blit(self.unachieved_badge_eggscape, (-4,0))
        self.screen.blit(self.play_again_button, self.play_again_rect)
