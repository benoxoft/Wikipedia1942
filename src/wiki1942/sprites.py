import pygame
import media
import random

#http://opengameart.org/content/rotating-crystal-animation-8-step

GEM_FRAMES = 8
GEM_ROTATE_TICK = 150
GEM_FONT_SIZE = 8
TOOLTIP_WIDTH = 100

GEM_COLORS = ("blue", "green", "grey", "orange", "pink", "yellow")

class Gem(pygame.sprite.Sprite):
    
    def __init__(self, name, size=32):
        pygame.sprite.Sprite.__init__(self)
        color = random.randint(0, len(GEM_COLORS) -1)
        self.name = name
        self.base_image = getattr(media, "gem" + str(size) + GEM_COLORS[color])
        self.next_rotate = GEM_ROTATE_TICK
        self.image_cursor = 1
        self.size = size
        self.image = self.get_gem_frame(0)
        
        

    def create_name(self):
        font = media.get_font(GEM_FONT_SIZE)
        s = font.render(self.name, True, (255,255,255))
        image = pygame.Surface((TOOLTIP_WIDTH, GEM_FONT_SIZE))
        image.blit(s, (s.get_rect().w/2.0,0), s.get_rect())
        return image
    
    def get_gem_frame(self, position):
        rect = pygame.Rect(self.size * position, 0, self.size, self.size)
        image = pygame.Surface((100, self.size + GEM_FONT_SIZE)).convert()
        image.blit(self.base_image, ((TOOLTIP_WIDTH - self.size) / 2, 0), rect)
        colorkey = self.base_image.get_at((0,0))        
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    
    def update(self, tick):
        self.next_rotate -= tick
        if self.next_rotate <= 0:
            self.next_rotate = GEM_ROTATE_TICK
            self.image_cursor += 1
            if self.image_cursor == GEM_FRAMES:
                self.image_cursor = 0
        self.image = self.get_gem_frame(self.image_cursor)
        tooltip = self.create_name()
        self.image.blit(tooltip, (0,self.size), tooltip.get_rect())
        
