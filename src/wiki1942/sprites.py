import pygame
import media
import random

#http://opengameart.org/content/rotating-crystal-animation-8-step

GEM_FRAMES = 8
GEM_ROTATE_TICK = 150

GEM_COLORS = ("blue", "green", "grey", "orange", "pink", "yellow")

class Gem(pygame.sprite.Sprite):
    
    def __init__(self, size=32):
        pygame.sprite.Sprite.__init__(self)
        color = random.randint(0, len(GEM_COLORS) -1)
        
        self.base_image = getattr(media, "gem" + str(size) + GEM_COLORS[color])
        self.next_rotate = GEM_ROTATE_TICK
        self.image_cursor = 1
        self.size = size
        self.image = self.get_area(0)
        
    def get_area(self, position):
        rect = pygame.Rect(self.size * position, 0, self.size, self.size)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.base_image, (0, 0), rect)
        colorkey = image.get_at((0,0))        
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    
    def update(self, tick):
        self.next_rotate -= tick
        if self.next_rotate <= 0:
            self.next_rotate = GEM_ROTATE_TICK
            self.image_cursor += 1
            if self.image_cursor == GEM_FRAMES:
                self.image_cursor = 0
        self.image = self.get_area(self.image_cursor)
        
