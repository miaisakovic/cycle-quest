import pygame 

class TopObstacle(pygame.sprite.Sprite):
    def __init__(self, obs, x_coor):
        super().__init__()

        self.type = obs
        self.top_obstacle = pygame.image.load('graphics/eggscape/pipe_top_'+str(obs)+'.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.top_obstacle, 0.75)
        self.rect = self.image.get_rect(topleft=(x_coor, -35))

    def update(self):
        self.rect.x -= 3
        if self.rect.x <= -300:
            self.kill()
