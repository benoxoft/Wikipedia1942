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
        self.plane3 = sprites.Aircraft03()
        self.plane4 = sprites.Aircraft04()
        self.plane5 = sprites.Aircraft05()
        self.plane6 = sprites.Aircraft06()
        self.plane7 = sprites.Aircraft07()
        self.plane8 = sprites.Aircraft08()
        self.plane9 = sprites.Aircraft09()
        self.main_plane = sprites.Aircraft10()
        self.cloud = sprites.EndlessCloud()
        self.cloud2 = sprites.EndlessCloud(15000)
        
        self.bullets = pygame.sprite.Group()
        self.tick_count = 0
        
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
    
    def shoot_bullet(self, tick):
        if self.tick_count <= 0:
            self.bullets.add(sprites.Bullet("blue", True, (self.main_plane.rect.x + self.main_plane.rect.w / 2, self.main_plane.rect.y)))
            self.tick_count = 60
    
    def move_main_plane_mouse(self, tick):
        move = 600 / tick 
        x, y = pygame.mouse.get_pos()
        x -= self.main_plane.rect.w / 2
        y -= self.main_plane.rect.h / 2
        
        if self.main_plane.rect.x > x:
            if self.main_plane.rect.x - move <= x:
                self.main_plane.rect.x = x
            else:
                self.main_plane.rect.x -= move
        elif self.main_plane.rect.x < x:
            if self.main_plane.rect.x + move >= x:
                self.main_plane.rect.x = x
            else:
                self.main_plane.rect.x += move
                
        if self.main_plane.rect.y > y:
            if self.main_plane.rect.y - move <= y:
                self.main_plane.rect.y = y
            else:
                self.main_plane.rect.y -= move
        elif self.main_plane.rect.y < y:
            if self.main_plane.rect.y + move >= y:
                self.main_plane.rect.y = y
            else:
                self.main_plane.rect.y += move
        
        
    def update(self):
        tick = self.clock.tick(24)
        self.move_main_plane_mouse(tick)
        if self.key_space:
            self.shoot_bullet(tick)
        self.tick_count -= tick

        self.screen.fill((110,110,0))
        self.gem.update(tick)
        self.plane1.update(tick)
        self.plane2.update(tick)
        self.plane3.update(tick)
        self.plane4.update(tick)
        self.plane5.update(tick)
        self.plane6.update(tick)
        self.plane7.update(tick)
        self.plane8.update(tick)
        self.plane9.update(tick)
        self.main_plane.update(tick)
        self.bg.update(tick)
        self.cloud.update(tick)
        self.cloud2.update(tick)
        self.bullets.update(tick)
        self.screen.blit(self.bg.image, (0, 0), self.bg.rect)
        self.screen.blit(self.cloud.image, self.cloud.rect)
        #self.screen.blit(self.cloud2.image, self.cloud2.rect)

        self.screen.blit(self.gem.image, self.gem.rect)
        self.screen.blit(self.main_plane.image, self.main_plane.rect)
        self.screen.blit(self.plane1.image, (110,110,self.plane1.image.get_rect().w,self.plane1.image.get_rect().h))
        self.screen.blit(self.plane2.image, (220,110,self.plane2.image.get_rect().w,self.plane2.image.get_rect().h))
        self.screen.blit(self.plane3.image, (330,110,self.plane3.image.get_rect().w,self.plane3.image.get_rect().h))
        self.screen.blit(self.plane4.image, (440,110,self.plane4.image.get_rect().w,self.plane4.image.get_rect().h))
        self.screen.blit(self.plane5.image, (550,110,self.plane5.image.get_rect().w,self.plane5.image.get_rect().h))
        self.screen.blit(self.plane6.image, (660,110,self.plane6.image.get_rect().w,self.plane6.image.get_rect().h))
        self.screen.blit(self.plane7.image, (110,220,self.plane7.image.get_rect().w,self.plane7.image.get_rect().h))
        self.screen.blit(self.plane8.image, (220,220,self.plane8.image.get_rect().w,self.plane8.image.get_rect().h))
        self.screen.blit(self.plane9.image, (330,220,self.plane9.image.get_rect().w,self.plane9.image.get_rect().h))
        self.bullets.draw(self.screen)
        
        pygame.display.update()
        #pygame.time.delay(1000 / 24 - tick)
        return tick
    