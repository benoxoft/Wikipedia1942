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
        self.bg = sprites.Background()
        self.plane1 = sprites.Aircraft01()
        self.plane2 = sprites.Aircraft02()
        self.mainplane = sprites.MainAircraft()
        self.cloud = sprites.EndlessCloud()
        self.cloud2 = sprites.EndlessCloud(10000)
        #self.cloud3 = sprites.EndlessCloud(20000)
        
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
        self.screen.fill((110,110,0))
        self.gem.update(tick)
        self.plane1.update(tick)
        self.plane2.update(tick)
        self.mainplane.update(tick)
        self.bg.update(tick)
        self.cloud.update(tick)
        self.cloud2.update(tick)
        #self.cloud3.update(tick)
        self.screen.blit(self.bg.image, (0, 0), self.bg.rect)
        self.screen.blit(self.cloud.image, self.cloud.rect)
        self.screen.blit(self.cloud2.image, self.cloud2.rect)
        #self.screen.blit(self.cloud3.image, self.cloud3.rect)
        self.screen.blit(self.gem.image, (110,110,32,32))
        self.screen.blit(self.plane1.image, (500,110,self.plane1.image.get_rect().w,self.plane1.image.get_rect().h))
        self.screen.blit(self.plane2.image, (500,220,self.plane2.image.get_rect().w,self.plane2.image.get_rect().h))
        self.screen.blit(self.mainplane.image, (210,210,self.mainplane.image.get_rect().w,self.mainplane.image.get_rect().h))
        pygame.display.update()
        pygame.time.delay(1000 / 24 - tick)
        return tick
    