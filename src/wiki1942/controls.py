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
        self.enemy = EnemyFactory()
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
        
        for plane in pygame.sprite.groupcollide(self.enemy.planes, self.player.bullets, False, True):
            plane.hit()
            
        for player in pygame.sprite.groupcollide(self.player_group, self.enemy.bullets, False, True):
            self.player.main_plane.hit()
            self.statusbar.set_current_life(self.player.main_plane.life)
            
    def update(self):
        tick = self.clock.tick(24)
        
        if not self.player.show_warp_zone:
            self.warp.reset()
            self.player.update(tick)
            self.enemy.update(tick)
            self.bg.update(tick)
            self.cloud.update(tick)
            self.gems.update(tick)
            self.ui_group.update(tick)
            self.manage_collisions()
            
        self.screen.blit(self.bg.image, (0, 0), self.bg.rect)
        self.screen.blit(self.cloud.image, self.cloud.rect)

        self.screen.blit(self.player.main_plane.image, self.player.rect)
        self.enemy.planes.draw(self.screen)
        self.player.bullets.draw(self.screen)
        self.enemy.bullets.draw(self.screen)
        self.gems.gems.draw(self.screen)
        self.gems.tooltips.draw(self.screen)
        self.ui_group.draw(self.screen)

        if self.player.show_warp_zone:
            self.warp.set_found_links(self.player.gems)
            self.warp.update(tick)
            self.screen.blit(self.warp.image, self.warp.rect)
            
            if self.warp.accept:
                self.player.show_warp_zone = False
                self.player.gems = []
                self.gems.change_page(self.warp.warp_to_word)
                
        pygame.display.update()
    
class GemFactory(pygame.sprite.Group):
    
    def __init__(self, statusbar):
        self.gems = pygame.sprite.Group()
        self.tooltips = pygame.sprite.Group()
        self.current_page = wiki.randomize_page()
        self.links = wiki.gemify_page(self.current_page)
        self.tick_count = 0
        self.statusbar = statusbar
        self.update_status_bar()
        
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
        
    def update_status_bar(self):
        self.statusbar.set_current_page(self.current_page.title)
        self.statusbar.set_total_links(len(self.links))
        self.statusbar.set_links_left(len(self.links))
        
    def change_page(self, word):
        self.current_page = wiki.open_page(word)
        self.links = wiki.gemify_page(self.current_page)
        self.tick_count = 0
        self.gems.empty()
        self.tooltips.empty()
        self.update_status_bar()
        
class AircraftAI(pygame.sprite.Sprite):
    
    def __init__(self, plane, bullets):
        pygame.sprite.Sprite.__init__(self)
        self.plane = plane
        self.bullets = bullets
        self.gun_cooldown = 0
        self.decision_cooldown = 0
        self.x_move = 0
        self.y_move = 1
        self.y_speed = 100
        self.init = True
        self.bulletv = pygame.math.Vector2()
        self.bulletv.y = 1
        
    def shoot_bullet(self):
        self.bullets.add(sprites.OrangeBullet(self.bulletv, (self.plane.rect.x + self.plane.rect.w / 2 + 4, self.plane.rect.y + 20)))

    def update(self, tick):
        if not self.plane.alive():
            self.kill()
            
        if self.init:
            self.plane.rect.y += 1000 / tick
            if self.plane.rect.y >= 20:
                self.init = False
            else:
                return
        
        self.gun_cooldown -= tick
        if self.gun_cooldown <= 0:
            self.gun_cooldown = 300
            self.shoot_bullet()
            
        self.decision_cooldown -= tick
        if self.decision_cooldown <= 0:
            self.decision_cooldown = 1000
            if self.plane.rect.x > pygame.mouse.get_pos()[0]:
                self.x_move = -1
            else:
                self.x_move = 1
            if self.plane.rect.y > 400:
                self.y_move = -1
            elif self.plane.rect.y < 200:
                self.y_move = 1
                
        move_x = 200 / tick * self.x_move
        move_y = 100 / tick * self.y_move
        
        self.plane.rect.x += move_x
        self.plane.rect.y += move_y

class EnemyFactory():
    
    def __init__(self):
        self.bullets = pygame.sprite.Group()
        self.planes = pygame.sprite.Group()
        self.ais = pygame.sprite.Group()
        self.tick_count = 1000
        
    def update(self, tick):
        self.ais.update(tick)
        self.bullets.update(tick)
        self.planes.update(tick)
        
        self.tick_count -= tick
        if self.tick_count <= 0:
            self.tick_count = 3000
            plane = sprites.Aircraft01()
            ai = AircraftAI(plane, self.bullets)
            self.ais.add(ai)
            self.planes.add(plane)
            
class Player(pygame.sprite.Sprite):

    def __init__(self, statusbar):
        pygame.sprite.Sprite.__init__(self)
        
        self.quit = False
        self.left_click = False
        self.show_warp_zone = False
        self.tick_count = 0
        self.main_plane = sprites.Aircraft10()
        self.main_plane.rect.x = 500
        self.main_plane.rect.y = 800
        self.bullets = pygame.sprite.Group()
        self.rect = self.main_plane.rect
        self.gems = []
        self.statusbar = statusbar
        self.bulletv = pygame.math.Vector2()
        self.bulletv[1] = -1
        
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
            self.bullets.add(sprites.BlueBullet(self.bulletv, (self.main_plane.rect.x + self.main_plane.rect.w / 2 - 4, self.main_plane.rect.y - 20)))
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
        
    