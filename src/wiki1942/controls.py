import pygame
import sprites

class GameControl:
    
    def __init__(self, screen):
        self.key_down = False
        self.key_up = False
        self.key_left = False
        self.key_right = False
        self.key_space = False
        self.keep_playing = True
        self.quit = False

        self.clock = pygame.time.Clock()
        self.screen = screen
        
        self.gem = sprites.Gem("patate")
        
    def reset(self):
        self.key_down = False
        self.key_up = False
        self.key_left = False
        self.key_right = False
        self.key_space = False

    def manage_key(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                self.key_down = True
            elif e.key == pygame.K_d:
                self.key_right = True
            elif e.key == pygame.K_w:
                self.key_up = True
            elif e.key == pygame.K_s:
                self.key_down = True
            elif e.key == pygame.K_SPACE:
                self.key_space = True
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_a:
                self.key_left = False
            elif e.key == pygame.K_d:
                self.key_right = False
            elif e.key == pygame.K_w:
                self.key_up = False
            elif e.key == pygame.K_s:
                self.key_down = False
            elif e.key == pygame.K_SPACE:
                self.key_space = False                
            elif e.key == pygame.K_ESCAPE:
                self.keep_playing = False  
                self.quit = True
    
    def update(self):
        tick = self.clock.tick()
        self.screen.fill((0,0,0))
        self.gem.update(tick)
        self.screen.blit(self.gem.image, (110,110,32,32))
        pygame.display.update()
        pygame.time.delay(16)
        return tick
    