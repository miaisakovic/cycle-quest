import pygame 

class Egg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.egg = pygame.image.load('graphics/eggscape/egg.png')
        self.image = pygame.transform.scale_by(self.egg, 0.75)
        self.rect = self.image.get_rect(midbottom=(225, 400))
        self.gravity = 0

    def get_input(self):
        keys_pressed = pygame.key.get_pressed()
    
        if keys_pressed[pygame.K_SPACE]:
            self.rect.y -= 15
            self.gravity = 0
            if self.rect.y <= 0:
                self.rect.y = 0

    def animate_egg(self):
        if self.rect.bottom < 768:
            self.gravity += 0.15
            self.rect.y += self.gravity
        else:
            self.gravity = 0

    def update(self):
        self.get_input()
        self.animate_egg()