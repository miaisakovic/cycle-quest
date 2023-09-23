import pygame 
from random import randint

class Relief(pygame.sprite.Sprite):
    def __init__(self, relief_item):
        super().__init__()

        self.type = relief_item
        self.relief = pygame.image.load('graphics/relief/'+relief_item+'.png').convert_alpha()
        
        self.image = pygame.transform.scale_by(self.relief, 0.75)

        self.rect = self.image.get_rect(midbottom=(randint(100,1000), 0))

    def update(self):
        if self.rect.y >= 768:
            self.kill()
        self.rect.y += 5
