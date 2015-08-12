import pygame
import sprites
import wiki

class GameControl:
    
    def __init__(self, screen):
        self.clock = pygame.time.Clock()
        self.screen = screen
        
        self.bg = sprites.Background()
        self.cloud = sprites.EndlessCloud()
        
        self.statusbar = sprites.StatusBar()
        self.player = Player(self.statusbar)
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.enemy = Enemy()
        self.ui_group = pygame.sprite.Group()
        self.ui_group.add(self.statusbar)
        self.gems = GemFactory(self.statusbar)
        
        self.warp = sprites.WarpPage()
        self.warp.current_page = 1
                
    def manage_event(self, e):
        if e.type == pygame.MOUSEBUTTONUP:
            if self.player.show_warp_zone:
                self.warp.click()
        self.player.manage_key(e)
        
    def manage_collisions(self):
        for gem in pygame.sprite.groupcollide(self.gems.gems, self.player_group, True, False):
            self.player.add_gem(gem.name)
        
    def update(self):
        tick = self.clock.tick(24)
        
        if not self.player.show_warp_zone:
            self.warp.reset()
            self.player.update(tick)
            self.bg.update(tick)
            self.cloud.update(tick)
            self.gems.update(tick)
            self.ui_group.update(tick)
            self.manage_collisions()
            
        self.screen.blit(self.bg.image, (0, 0), self.bg.rect)
        self.screen.blit(self.cloud.image, self.cloud.rect)

        self.screen.blit(self.player.image, self.player.rect)
        self.player.bullets.draw(self.screen)
        self.gems.gems.draw(self.screen)
        self.gems.tooltips.draw(self.screen)
        self.ui_group.draw(self.screen)

        if self.player.show_warp_zone:
            self.warp.set_found_links(self.player.gems)
            self.warp.update(tick)
            self.screen.blit(self.warp.image, self.warp.rect)
            
        pygame.display.update()
    
class GemFactory(pygame.sprite.Group):
    
    def __init__(self, statusbar):
        self.gems = pygame.sprite.Group()
        self.tooltips = pygame.sprite.Group()
        self.current_page = wiki.randomize_page()
        self.links = wiki.gemify_page(self.current_page)
        self.tick_count = 0
        self.statusbar = statusbar
        self.statusbar.set_current_page(self.current_page.title)
        self.statusbar.set_total_links(len(self.links))
        self.statusbar.set_links_left(len(self.links))
        
    def update(self, tick):
        self.tick_count += tick
        gem = wiki.next_gem(self.tick_count, self.links)
        if gem is not None:
            gem_sprite = sprites.Gem(gem)
            self.gems.add(gem_sprite)
            tooltip = sprites.GemTooltip(gem_sprite)
            self.tooltips.add(tooltip)
            self.statusbar.set_links_left(len(self.links))
        self.gems.update(tick)
        self.tooltips.update(tick)
        
class AircraftAI:
    pass

class Enemy():
    
    def __init__(self):
        self.bullets = pygame.sprite.Group()
        self.planes = pygame.sprite.Group()
        
    def update(self, tick):
        pass
    
class Player(pygame.sprite.Sprite):

    def __init__(self, statusbar):
        pygame.sprite.Sprite.__init__(self)
        
        self.quit = False
        self.left_click = False
        self.show_warp_zone = False
        self.tick_count = 0
        self.main_plane = sprites.Aircraft10()
        self.bullets = pygame.sprite.Group()
        self.image = self.main_plane.image
        self.rect = self.main_plane.rect
        self.gems = []
        self.statusbar = statusbar
        
    def add_gem(self, gem):
        self.gems.append(gem)
        self.statusbar.set_collected(len(self.gems))
        
    def manage_key(self, e):
        if e.type == pygame.QUIT:
            self.quit = True
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_ESCAPE:
                self.show_warp_zone = not self.show_warp_zone
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                self.left_click = True
            
        elif e.type == pygame.MOUSEBUTTONUP:
            buttons = pygame.mouse.get_pressed()
            if buttons[0] == 0:
                self.left_click = False
        
    def shoot_bullet(self, tick):
        if self.tick_count <= 0:
            self.bullets.add(sprites.BlueBullet(True, (self.main_plane.rect.x + self.main_plane.rect.w / 2 - 4, self.main_plane.rect.y - 20)))
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
        
    def update(self, tick):
        self.bullets.update(tick)
        self.move_main_plane_mouse(tick)
        if self.left_click and not self.show_warp_zone:
            self.shoot_bullet(tick)
        self.tick_count -= tick
        self.main_plane.update(tick)
        
        self.image = self.main_plane.image
        self.rect = self.main_plane.rect

    