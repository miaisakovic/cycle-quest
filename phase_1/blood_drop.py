import pygame 

class BloodDrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.blood_drop = pygame.image.load('graphics/bloody-mess/blood_drop.png')
        self.image = pygame.transform.scale_by(self.blood_drop, 0.75)
        self.rect = self.image.get_rect(midbottom=(512, 750))
    
    def update(self):
        keys_pressed = pygame.key.get_pressed()
    
        if keys_pressed[pygame.K_RIGHT] and self.rect.midright[0] <= 1024:
            self.rect.x += 5

        if keys_pressed[pygame.K_LEFT] and self.rect.midleft[0] >= 0:
            self.rect.x -= 5
