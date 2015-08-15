import pygame
import sprites
import wiki
import random
import media

HITLER = "Adolf Hitler"
HITLER_LIFE = 100

class GameControl:
    
    def __init__(self, screen):
        self.clock = pygame.time.Clock()
        self.screen = screen
        
        self.bg = sprites.Background()
        self.bg_lava = sprites.BackgroundLava()
        
        self.cloud = sprites.EndlessCloud()

        self.explosions = pygame.sprite.Group()
        
        self.statusbar = sprites.StatusBar()
        self.powerupbar = sprites.PowerupBar()
        self.hitlet_hp = sprites.HitlerLifebar(HITLER_LIFE)
        
        self.player = Player(self.statusbar, self.powerupbar)
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.enemy = EnemyFactory(self.explosions)
        self.ui_group = pygame.sprite.Group()
        self.ui_group.add(self.statusbar)
        #self.ui_group.add(self.powerupbar)
        self.gems = GemFactory(self.statusbar, self.powerupbar, self.player.main_plane)
        
        self.warp = sprites.WarpPage()
        self.warp.current_page = 1
        self.gameover = sprites.Gameover()
        self.ending = sprites.Ending()
        
    def manage_event(self, e):
        if e.type == pygame.MOUSEBUTTONUP:
            if self.player.show_warp_zone:
                self.warp.click()
            elif self.player.gameover:
                self.gameover.click()
        self.player.manage_key(e)
        
    def manage_collisions(self):
        for gem in pygame.sprite.groupcollide(self.gems.gems, self.player_group, True, False):
            self.player.add_gem(gem)
            media.gem.play()
            
        for plane in self.enemy.planes:
            plane.set_collide()
            
        for plane in pygame.sprite.groupcollide(self.enemy.planes, self.player.bullets, False, True):
            if isinstance(plane, sprites.Bomb):
                plane.kill()
                self.explosions.add(sprites.Explosion((plane.rect.x, plane.rect.y)))
                v = pygame.math.Vector2(0, 1)
                for i in range(0, 8):
                    v = v.rotate(45)
                    d = sprites.Debris(v, (plane.rect.centerx, plane.rect.centery))
                    self.enemy.bullets.add(d)
            else:
                plane.hit()
            
        for plane in self.enemy.planes:
            plane.set_drawing()
        
        self.player.main_plane.set_collide()
        for player in pygame.sprite.groupcollide(self.player_group, self.enemy.bullets, False, True):
            if self.powerupbar.green_active:
                self.powerupbar.green_active -= 30000
                continue
            self.player.main_plane.hit()
            self.statusbar.set_current_life(self.player.main_plane.life)
            if self.player.main_plane.life == 0:
                self.player.gameover = True
                self.explosions.add(sprites.Explosion((self.player.main_plane.rect.x, self.player.main_plane.rect.y)))
                self.explosions.add(sprites.Explosion((self.player.main_plane.rect.x - 10, self.player.main_plane.rect.y - 40)))
                self.explosions.add(sprites.Explosion((self.player.main_plane.rect.x - 20, self.player.main_plane.rect.y - 30)))
                self.explosions.add(sprites.Explosion((self.player.main_plane.rect.x - 30, self.player.main_plane.rect.y - 20)))
                self.explosions.add(sprites.Explosion((self.player.main_plane.rect.x - 40, self.player.main_plane.rect.y - 10)))
                
        self.player.main_plane.set_drawing()
        
    def update(self):
        tick = self.clock.tick(24)
        
        if len(self.gems.links) == 0 and len(self.gems.gems) == 0:
           self.player.show_warp_zone = True
           self.player.main_plane.life = 10
           self.statusbar.set_current_life(self.player.main_plane.life)
           if len(self.player.gems) == 0:
                self.player.gems.append("random")
           self.warp.level_cleared = True
           
        if not self.player.show_warp_zone and not self.player.gameover and not self.enemy.hitler_beaten:
            self.warp.reset()
            self.player.update(tick)
            self.enemy.update(tick)
            if self.gems.current_page.title == HITLER:
                self.bg_lava.update(tick)
            else:
                self.bg.update(tick)
            self.cloud.update(tick)
            self.gems.update(tick)
            self.manage_collisions()
            self.powerupbar.update(tick)
        self.ui_group.update(tick)
        self.explosions.update(tick)
            
        if self.gems.current_page.title == HITLER:
            self.screen.blit(self.bg_lava.image, (0, 0), self.bg_lava.rect)
        else:
            self.screen.blit(self.bg.image, (0, 0), self.bg.rect)
            self.screen.blit(self.cloud.image, self.cloud.rect)

        self.screen.blit(self.player.main_plane.image, self.player.rect)
        self.enemy.planes.draw(self.screen)
        self.player.bullets.draw(self.screen)
        self.enemy.bullets.draw(self.screen)
        self.gems.gems.draw(self.screen)
        self.gems.tooltips.draw(self.screen)
        self.explosions.draw(self.screen)
        self.ui_group.draw(self.screen)
        self.screen.blit(self.powerupbar.image, self.powerupbar.rect)
        
        if self.gems.current_page.title == HITLER:
            if self.enemy.hitler_plane is not None:
                self.hitlet_hp.set_current_life(self.enemy.hitler_plane.life)
            self.hitlet_hp.update()
            self.screen.blit(self.hitlet_hp.image, self.hitlet_hp.rect)
        
        if self.player.gameover:
            self.screen.blit(self.gameover.image, self.gameover.rect)
            self.gameover.update(tick)
            
            if self.gameover.try_again:
                pygame.mixer.music.stop()
                self.player.gameover = False
                self.player.reset_hard()
                self.gems = GemFactory(self.statusbar, self.powerupbar, self.player.main_plane)
                self.enemy.reset(self.gems.current_page.title == HITLER)
                self.player.show_warp_zone = False
                self.gameover.try_again = False
                self.bg.reset()
                
            elif self.gameover.quit:
                self.player.quit = True
            
        elif self.player.show_warp_zone:
            if self.gems.current_page.title == HITLER:
                self.player.show_warp_zone = False
            else:
                self.warp.set_found_links(self.player.gems)
                self.warp.update(tick)
                self.screen.blit(self.warp.image, self.warp.rect)
                
                if self.warp.accept:
                    self.warp.level_cleared = False
                    self.player.show_warp_zone = False
                    self.player.reset()
                    self.gems.change_page(self.warp.warp_to_word)
                    self.enemy.reset(self.gems.current_page.title == HITLER)
                    self.bg.reset()
                    if self.gems.current_page.title == HITLER:
                        pygame.mixer.music.load(media.Confrontation_file)
                        pygame.mixer.music.play(-1)
                        self.enemy.tick_count = 60000
                        self.enemy.bomb_tick = 70000
                        self.player.main_plane.life = 10
                        self.statusbar.set_current_life(10)
                        
        if self.enemy.hitler_beaten:
            self.ending.update(tick)
            self.screen.blit(self.ending.image, self.ending.rect)

        pygame.display.update()
    
class GemFactory:
    
    def __init__(self, statusbar, powerupbar, main_plane):
        self.gems = pygame.sprite.Group()
        self.tooltips = pygame.sprite.Group()
        self.current_page = wiki.randomize_page()
        self.links = wiki.gemify_page(self.current_page)

        self.tick_count = 0
        self.statusbar = statusbar
        self.powerupbar = powerupbar
        self.main_plane = main_plane
        self.update_status_bar()
            
    def gravity_pull(self, tick):
        if self.powerupbar.grey_active > 0:
            rect = pygame.Rect((self.main_plane.rect.centerx - 180, self.main_plane.rect.centery - 180, 360, 360))
            
            for tooltip in self.tooltips:
                gem = tooltip.gem
                if rect.colliderect(gem.rect):
                    x = rect.centerx - gem.rect.centerx
                    y = rect.centery - gem.rect.centery
                    v = pygame.math.Vector2(x, y).normalize()
                    speed = 1000 / tick
                    gem.rect.x += v.x * speed
                    gem.rect.y += v.y * speed
                    tooltip.rect.x += v.x * speed
                    tooltip.rect.y += v.y * speed
                    
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
        self.gravity_pull(tick)
        
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
        
class SkullGrenade(pygame.sprite.Sprite):
    
    def __init__(self, skull, bullets):
        pygame.sprite.Sprite.__init__(self)
        self.skull = skull
        self.bullets = bullets
        self.grenade_cooldown = random.randint(1000, 2000)
        
    def shoot_grenade(self):
        v = pygame.math.Vector2(random.randint(0, 200) - 100, random.randint(0, 200) - 100).normalize()
        d = sprites.Debris(v, (self.skull.rect.centerx, self.skull.rect.centery))
        self.bullets.add(d)

    def update(self, tick):
        self.grenade_cooldown -= tick
        if self.grenade_cooldown <= 0:
            self.grenade_cooldown = random.randint(500, 1200)
            self.shoot_grenade()
        
class Hitler(pygame.sprite.Sprite):
    
    def __init__(self, plane, bullets, explosions):
        pygame.sprite.Sprite.__init__(self)
        self.plane = plane
        self.bullets = bullets
        self.explosions = explosions
        self.gun_cooldown = 5000
        self.decision_cooldown = 0
        self.x_move = 0
        self.y_move = 1
        self.y_speed = 100
        self.init = True
        self.bulletv = pygame.math.Vector2()
        self.bulletv.y = -1
        self.explosion_counter = 60
        
    def shoot_bullet(self):
        if self.plane.life <= 0:
            return
        self.bullets.add(sprites.PurpleBullet(self.bulletv, (self.plane.rect.x, self.plane.rect.y + 20)))
        self.bullets.add(sprites.PurpleBullet(self.bulletv, (self.plane.rect.x + self.plane.rect.w, self.plane.rect.y + 20)))
    
    def update(self, tick):
        if self.plane.life <= 0:
            self.plane.hit()
            self.explosions.add(sprites.Explosion((self.plane.rect.x + random.randint(0, 100) - 50, self.plane.rect.y + random.randint(0, 100) - 50)))
            self.explosion_counter -= 1
            if self.explosion_counter == 0:
                for i in range(0, 10):
                    self.explosions.add(sprites.Explosion((self.plane.rect.x + random.randint(0, 100) - 50, self.plane.rect.y + random.randint(0, 100) - 50)))
                self.plane.kill()
                self.kill()
            
        if self.init:
            self.plane.move_y(1000 / tick)
            if self.plane.rect.y >= 20:
                self.init = False
            else:
                return
                
        if self.plane.life <= HITLER_LIFE / 2 and self.gun_cooldown > 1000:
            self.gun_cooldown = 0
            
        self.gun_cooldown -= tick
        if self.gun_cooldown <= 0:
            self.gun_cooldown = 300
            self.shoot_bullet()
            
        self.decision_cooldown -= tick
        if self.decision_cooldown <= 0:
            self.decision_cooldown = random.randint(800, 1600)
            if random.randint(1, 2) == 1:
                self.x_move = -1
            else:
                self.x_move = 1
            if self.plane.rect.y > 400:
                self.y_move = -1
            elif self.plane.rect.y < 100:
                self.y_move = 1
                
        move_x = 350 / tick * self.x_move
        move_y = 100 / tick * self.y_move
        
        self.plane.move(move_x, move_y)
        if self.plane.rect.x < 160:
            self.x_move = 1
        elif self.plane.rect.x > 860:
            self.x_move = -1
    
class AircraftAIBack(pygame.sprite.Sprite):
    
    def __init__(self, plane, bullets, explosions):
        pygame.sprite.Sprite.__init__(self)
        self.plane = plane
        self.bullets = bullets
        self.explosions = explosions
        self.grenade_cooldown = 2000
        self.decision_cooldown = 0
        self.x_move = 0
        self.y_move = 1
        self.y_speed = 100
        self.init = True
    
    def shoot_grenade(self):
        v = pygame.math.Vector2(random.randint(0, 200) - 100, random.randint(0, 100)).normalize()
        d = sprites.Debris(v, (self.plane.rect.centerx, self.plane.rect.centery))
        self.bullets.add(d)
    
    def update(self, tick):
        if not self.plane.alive():
            self.kill()
            self.explosions.add(sprites.Explosion((self.plane.rect.x, self.plane.rect.y)))
                                
            v = pygame.math.Vector2(0, 1)
            for i in range(0, 8):
                v = v.rotate(45)
                d = sprites.Debris(v, (self.plane.rect.centerx, self.plane.rect.centery))
                self.bullets.add(d)
            
        if self.init:
            self.plane.move_y(1000 / tick)
            if self.plane.rect.y >= 20:
                self.init = False
            else:
                return
                
        self.grenade_cooldown -= tick
        if self.grenade_cooldown <= 0:
            self.grenade_cooldown = random.randint(300, 600)
            self.shoot_grenade()
            
        self.decision_cooldown -= tick
        if self.decision_cooldown <= 0:
            self.decision_cooldown = random.randint(1000, 2000)
            if random.randint(1, 2) == 1:
                self.x_move = -1
            else:
                self.x_move = 1
            if self.plane.rect.y > 200:
                self.y_move = -1
            elif self.plane.rect.y < 100:
                self.y_move = 1
                
        move_x = 160 / tick * self.x_move
        move_y = 60 / tick * self.y_move
        
        self.plane.move(move_x, move_y)
        if self.plane.rect.x < 60:
            self.x_move = 1
        elif self.plane.rect.x > 960:
            self.x_move = -1

class AircraftAIFront(pygame.sprite.Sprite):
    
    def __init__(self, plane, bullets, explosions):
        pygame.sprite.Sprite.__init__(self)
        self.plane = plane
        self.bullets = bullets
        self.explosions = explosions
        self.gun_cooldown = 2000
        self.decision_cooldown = 0
        self.x_move = 0
        self.y_move = 1
        self.y_speed = 100
        self.init = True
        self.bulletv = pygame.math.Vector2()
        self.bulletv.y = -1
            
    def shoot_bullet(self):
        self.bullets.add(sprites.OrangeBullet(self.bulletv, (self.plane.rect.x + self.plane.rect.w / 2 + 4, self.plane.rect.y + 20)))

    def update(self, tick):
        if not self.plane.alive():
            self.kill()
            self.explosions.add(sprites.Explosion((self.plane.rect.x, self.plane.rect.y)))
                                            
        if self.init:
            self.plane.move_y(1000 / tick)
            if self.plane.rect.y >= 20:
                self.init = False
            else:
                return
        
        self.gun_cooldown -= tick
        if self.gun_cooldown <= 0:
            self.gun_cooldown = random.randint(500, 800)
            self.shoot_bullet()
                        
        self.decision_cooldown -= tick
        if self.decision_cooldown <= 0:
            self.decision_cooldown = 1000
            if self.plane.rect.x > pygame.mouse.get_pos()[0]:
                self.x_move = -1
            else:
                self.x_move = 1
            if self.plane.rect.y > 500:
                self.y_move = -1
            elif self.plane.rect.y < 200:
                self.y_move = 1
                
        move_x = 230 / tick * self.x_move
        move_y = 120 / tick * self.y_move
        
        self.plane.move(move_x, move_y)

class EnemyFactory():
    
    def __init__(self, explosions):
        self.bullets = pygame.sprite.Group()
        self.planes = pygame.sprite.Group()
        self.ais = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.tick_count = 6000
        self.explosions = explosions
        self.bomb_tick = 16000
        self.hitler_plane = None
        self.hitler = False
        self.hitler_started = False
        self.hitler_beaten = False
        
    def reset(self, hitler=False):
        self.bullets.empty()
        self.planes.empty()
        self.ais.empty()
        self.bombs.empty()
        self.tick_count = 6000
        self.bomb_tick = 16000
        self.hitler = hitler
        
    def update(self, tick):
        for bomb in self.bombs:
            if bomb.explode:
                bomb.kill()
                self.explosions.add(sprites.Explosion((bomb.rect.centerx, bomb.rect.centery)))
                v = pygame.math.Vector2(0, 1)
                for i in range(0, 8):
                    v = v.rotate(45)
                    d = sprites.Debris(v, (bomb.rect.centerx, bomb.rect.centery))
                    self.bullets.add(d)
        
        self.ais.update(tick)
        self.bullets.update(tick)
        self.planes.update(tick)
        
        self.tick_count -= tick
        if self.hitler and self.hitler_started:
            if len(self.planes) == 0:
                self.hitler_beaten = True
                
        elif self.hitler and not self.hitler_started and self.tick_count <= 0:
            self.hitler_started = True
            plane = sprites.Aircraft01()
            plane.life = HITLER_LIFE
            self.hitler_plane = plane
            
            v = pygame.math.Vector2(1, 0)
            ss = sprites.SkullShield(plane, v)
            self.planes.add(ss)
            ai = SkullGrenade(ss, self.bullets)
            self.ais.add(ai)

            v = v.rotate(120)
            ss = sprites.SkullShield(plane, v)
            self.planes.add(ss)
            ai = SkullGrenade(ss, self.bullets)
            self.ais.add(ai)

            v = v.rotate(120)
            ss = sprites.SkullShield(plane, v)
            self.planes.add(ss)
            ai = SkullGrenade(ss, self.bullets)
            self.ais.add(ai)

            ai = Hitler(plane, self.bullets, self.explosions)
            self.ais.add(ai)
            self.planes.add(plane)
        else:
            if self.tick_count <= 0 and len(self.planes) <= 5:
                self.tick_count = random.randint(10, 3000)
                if random.randint(1, 10) == 1:
                    plane = sprites.Aircraft06()
                    ai = AircraftAIBack(plane, self.bullets, self.explosions)
                else:
                    plane = sprites.Aircraft05()
                    ai = AircraftAIFront(plane, self.bullets, self.explosions)
                self.ais.add(ai)
                self.planes.add(plane)

        self.bomb_tick -= tick
        if self.bomb_tick <= 0:
            self.bomb_tick = random.randint(1000, 5000)
            bomb = sprites.Bomb()
            self.planes.add(bomb)
            self.bullets.add(bomb)
            self.bombs.add(bomb)
            
class Player(pygame.sprite.Sprite):

    def __init__(self, statusbar, powerupbar):
        pygame.sprite.Sprite.__init__(self)
        
        self.quit = False
        self.left_click = False
        self.space = False
        self.show_warp_zone = False
        self.gameover = False
        self.tick_count = 0
        self.tick_count_power = 0
        self.main_plane = sprites.Aircraft10()
        self.main_plane.rect.x = 500
        self.main_plane.rect.y = 800
        self.bullets = pygame.sprite.Group()
        self.rect = self.main_plane.rect
        self.gems = []
        self.powerup_counter = 0
        self.statusbar = statusbar
        self.powerupbar = powerupbar
        self.bulletv = pygame.math.Vector2()
        self.bulletv[1] = 1
        self.bulletvl1 = self.bulletv.rotate(15)
        self.bulletvr1 = self.bulletv.rotate(-15)
        self.bulletvl2 = self.bulletv.rotate(30)
        self.bulletvr2 = self.bulletv.rotate(-30)
        #self.gems.append("Hitler")
        
    def reset(self):
        self.main_plane.rect.x = 500
        self.main_plane.rect.y = 800
        self.gems = []
        self.tick_count = 0
        self.tick_count_power = 0
        self.bullets.empty()        
    
    def reset_hard(self):
        self.reset()
        self.powerup_counter = 0
        self.powerupbar.reset()
        self.main_plane.life = 10
        self.statusbar.set_current_life(10)
        
    def add_gem(self, gem):
        self.gems.append(gem.name)
        self.statusbar.set_collected(len(self.gems))
        self.powerup_counter += 1
        if self.powerup_counter >= 10:
            self.powerupbar.set_color(gem.color)
        
    def manage_key(self, e):
        if e.type == pygame.QUIT:
            self.quit = True
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                self.space = True
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_ESCAPE:
                self.show_warp_zone = not self.show_warp_zone
            elif e.key == pygame.K_SPACE:
                self.space = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                self.left_click = True
            if e.button == 3:
                if self.powerup_counter >= 10:
                    if self.powerupbar.color == "orange":
                        self.main_plane.life += 3
                        if self.main_plane.life > 10:
                            self.main_plane.life = 10
                        self.statusbar.set_current_life(self.main_plane.life)
                    self.powerupbar.activate_powerup()
                    self.powerup_counter = 0
            
        elif e.type == pygame.MOUSEBUTTONUP:
            buttons = pygame.mouse.get_pressed()
            if buttons[0] == 0:
                self.left_click = False
                        
    def shoot_bullet(self, tick):
        if self.tick_count <= 0:
            self.tick_count = 60
            self.bullets.add(sprites.BlueBullet(self.bulletv, (self.main_plane.rect.centerx - 8, self.main_plane.rect.y - 30)))
            if self.powerupbar.blue_active > 0 and self.tick_count_power <= 0:
                self.bullets.add(sprites.BlueBullet(self.bulletvl1, (self.main_plane.rect.x + 10, self.main_plane.rect.y - 30)))
                self.bullets.add(sprites.BlueBullet(self.bulletvr1, (self.main_plane.rect.x + self.main_plane.rect.w - 40, self.main_plane.rect.y - 30)))
                self.bullets.add(sprites.BlueBullet(self.bulletvl2, (self.main_plane.rect.x - 20, self.main_plane.rect.y - 30)))
                self.bullets.add(sprites.BlueBullet(self.bulletvr2, (self.main_plane.rect.x + self.main_plane.rect.w - 20, self.main_plane.rect.y - 30)))
                self.tick_count_power = 180
    
    def move_main_plane_mouse(self, tick):
        if self.gameover:
            return
        
        if self.powerupbar.yellow_active:
            move = 50000 / tick
        else:
            move = 750 / tick 
        x, y = pygame.mouse.get_pos()
        x -= self.main_plane.rect.w / 2
        y -= self.main_plane.rect.h / 2
        
        if self.main_plane.rect.x > x:
            if self.main_plane.rect.x - move <= x:
                self.main_plane.set_drawing_position_x(x)
            else:
                self.main_plane.move_x(-move)
        elif self.main_plane.rect.x < x:
            if self.main_plane.rect.x + move >= x:
                self.main_plane.set_drawing_position_x(x)
            else:
                self.main_plane.move_x(move)
                
        if self.main_plane.rect.y > y:
            if self.main_plane.rect.y - move <= y:
                self.main_plane.set_drawing_position_y(y)
            else:
                self.main_plane.move_y(-move)
        elif self.main_plane.rect.y < y:
            if self.main_plane.rect.y + move >= y:
                self.main_plane.set_drawing_position_y(y)
            else:
                self.main_plane.move_y(move)
        
    def update(self, tick):
        self.bullets.update(tick)
        self.move_main_plane_mouse(tick)
        if (self.left_click or self.space) and not self.show_warp_zone and not self.gameover:
            self.shoot_bullet(tick)
        self.tick_count -= tick
        self.tick_count_power -= tick
        self.main_plane.update(tick)
        