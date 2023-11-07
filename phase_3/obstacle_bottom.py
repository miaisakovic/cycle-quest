import pygame 

class BottomObstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_item, x_pos):
        super().__init__()

        self.bottom_obstacle = pygame.image.load('graphics/eggscape/pipe_bottom_' + str(obstacle_item) + '.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.bottom_obstacle, 0.75)
        self.rect = self.image.get_rect(bottomleft=(x_pos, 810))

    def update(self):
        self.rect.x -= 3
        if self.rect.x <= -300:
            self.kill()
