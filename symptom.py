import pygame 
from random import randint

class Symptom(pygame.sprite.Sprite):
    def __init__(self, symp):
        super().__init__()

        
        self.type = symp
        self.symptom = pygame.image.load('graphics/symptoms/'+symp+'.png').convert_alpha()

        self.image = pygame.transform.scale_by(self.symptom, 0.75)

        self.rect = self.image.get_rect(midbottom=(randint(100,1000), 0))
        
    
    def update(self):
        if self.rect.y >= 768:
            self.kill()
        self.rect.y += 5
