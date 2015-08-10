import pygame
import media
import random

#http://opengameart.org/content/rotating-crystal-animation-8-step
#http://opengameart.org/content/aircrafts
#http://opengameart.org/content/wwii-top-down-usaaf-bombers
#http://opengameart.org/content/wwii-top-down-usaaf-bombers

GEM_FRAMES = 8
GEM_ROTATE_TICK = 150
GEM_FONT_SIZE = 8
TOOLTIP_WIDTH = 100
GEM_COLORS = ("blue", "green", "grey", "orange", "pink", "yellow")

ROTOR_ROTATE_TICK = 30

class Gem(pygame.sprite.Sprite):
    
    def __init__(self, name, size=32):
        pygame.sprite.Sprite.__init__(self)
        color = random.randint(0, len(GEM_COLORS) -1)
        self.name = name
        self.base_image = getattr(media, "gem" + str(size) + GEM_COLORS[color])
        self.next_rotate = GEM_ROTATE_TICK
        self.image_cursor = 1
        self.size = size
        self.frames = self.create_frames()
        self.image = self.frames[0]
        
    def create_frames(self):
        return [self.create_gem_frame(i) for i in range(0, GEM_FRAMES)]
    
    def create_name(self):
        font = media.get_font(GEM_FONT_SIZE)
        s = font.render(self.name, True, (255, 255, 255))
        image = pygame.Surface((TOOLTIP_WIDTH, GEM_FONT_SIZE))
        image.blit(s, (s.get_rect().w / 2.0, 0), s.get_rect())
        return image
    
    def create_gem_frame(self, position):
        rect = pygame.Rect(self.size * position, 0, self.size, self.size)
        image = pygame.Surface((100, self.size + GEM_FONT_SIZE)).convert()
        image.blit(self.base_image, ((TOOLTIP_WIDTH - self.size) / 2, 0), rect)
        colorkey = self.base_image.get_at((0,0))        
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        tooltip = self.create_name()
        image.blit(tooltip, (0, self.size), tooltip.get_rect())
        return image
    
    def update(self, tick):
        self.next_rotate -= tick
        if self.next_rotate <= 0:
            self.next_rotate = GEM_ROTATE_TICK
            self.image_cursor += 1
            if self.image_cursor == GEM_FRAMES:
                self.image_cursor = 0
        self.image = self.frames[self.image_cursor]
        
class MainAircraft(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = media.B29
        
    def update(self, tick):
        pass
    
class EnemyAircraft01(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = media.Aircraft_01
        self.rotor_image = media.rotor01
        self.hit_image = media.Aircraft_01_hit
        self.frames = (self.create_image(True), self.create_image(False))
        self.image = self.frames[0]
        self.show_rotor = True
        self.rotor_tick = ROTOR_ROTATE_TICK
        
    def create_image(self, show_rotor):
        image = pygame.Surface(self.base_image.get_size()).convert()
        image.blit(self.base_image, (0, 0), self.base_image.get_rect())
        
        if show_rotor:
            image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 - 18, 10), self.rotor_image.get_rect())
            image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 4, 0), self.rotor_image.get_rect())
            image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 24, 10), self.rotor_image.get_rect())

        colorkey = self.base_image.get_at((0,0))        
        image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image
    
    def update(self, tick):
        self.rotor_tick -= tick
        if self.rotor_tick <= 0:
            self.rotor_tick = ROTOR_ROTATE_TICK
            self.show_rotor = not self.show_rotor
        if self.show_rotor:
            self.image = self.frames[0]
        else:
            self.image = self.frames[1]
        
    