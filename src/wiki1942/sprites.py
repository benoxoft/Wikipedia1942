import pygame
import media
import random
import math

#http://opengameart.org/content/rotating-crystal-animation-8-step
#http://opengameart.org/content/aircrafts
#http://opengameart.org/content/orthographic-outdoor-tiles
#http://opengameart.org/content/fluffy-clouds
#http://opengameart.org/content/10-basic-message-boxes
#http://opengameart.org/content/explosion-animated
#http://opengameart.org/content/skull
#http://opengameart.org/content/lava-background-6-screen-resolutions

GEM_FRAMES = 8
GEM_ROTATE_TICK = 150
GEM_FONT_SIZE = 8
TOOLTIP_WIDTH = 400
GEM_COLORS = ("blue", "green", "orange", "grey", "yellow")
GEM_FONT_COLOR = (255, 255, 160)

ROTOR_ROTATE_TICK = 30

BULLET_COLORS = ("blue", "purple", "orange")
BULLET_SPEED = 2000

class Gem(pygame.sprite.Sprite):
    
    def __init__(self, name, size=32):
        pygame.sprite.Sprite.__init__(self)
        self.color = random.randint(0, len(GEM_COLORS) -1)
        self.name = name
        self.base_image = getattr(media, "gem" + str(size) + GEM_COLORS[self.color])
        self.next_rotate = GEM_ROTATE_TICK
        self.image_cursor = 1
        self.size = size
        self.frames = self.create_frames()
        self.image = self.frames[0]
        self.speed = random.randint(100, 200)
        self.rect = pygame.Rect((random.randint(100, 900), -60, 32, 32))
        
    def create_frames(self):
        return [self.create_gem_frame(i) for i in range(0, GEM_FRAMES)]
        
    def create_gem_frame(self, position):
        rect = pygame.Rect(self.size * position, 0, self.size, self.size)
        image = pygame.Surface((self.size, self.size)).convert()
        image.blit(self.base_image, (0, 0), rect)
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
        self.image = self.frames[self.image_cursor]
        self.rect.y += self.speed / tick

        if self.rect.y > 720:
            self.kill()
            
class GemTooltip(pygame.sprite.Sprite):
    
    def __init__(self, gem):
        pygame.sprite.Sprite.__init__(self)
        font = media.get_font(GEM_FONT_SIZE)
        self.image = font.render(gem.name, True, GEM_FONT_COLOR)
        self.rect = pygame.Rect((gem.rect.x - self.image.get_rect().w / 2, gem.rect.y + gem.size, self.image.get_rect().w, self.image.get_rect().h))
        self.speed = gem.speed
        self.gem = gem
        
    def update(self, tick):
        self.rect.y += self.speed / tick
        if not self.gem.alive():
            self.kill()
        
class Bomb(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale2x(media.rocket_purple)
        self.rect = pygame.Rect((random.randint(120, 660), -60, self.image.get_rect().w, self.image.get_rect().h))
        self.speed = random.randint(200, 300)
        self.tick_count = 0
        self.explode = False
        
    def set_collide(self):
        pass
    
    def set_drawing(self):
        pass
    
    def update(self, tick):
        move = self.speed /tick    
        self.rect.y += move
        self.tick_count += tick
        if self.tick_count > 100 and self.rect.y > 0:
            self.explode = random.randint(1, 50)  == 15 or self.explode
        if self.rect.y > 720:
            self.kill()
            
class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, initpos):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = media.explosionframes
        self.frames = [self.create_frame(i) for i in range(0, 16)]# if i % 2 == 1]
        self.index = 0
        self.image = self.frames[0]
        self.rect = pygame.Rect((initpos[0], initpos[1], self.image.get_rect().w, self.image.get_rect().h))
        media.explode.play()
        
    def create_frame(self, position):
        image = pygame.Surface((128, 128))
        if position < 8:
            rect = pygame.Rect(position * 128, 0, 128, 128)
        else:
            rect = pygame.Rect((position - 8) * 128, 128, 128, 128)
            
        image.blit(self.base_image, (0, 0), rect)
        colorkey = self.base_image.get_at((0,0))        
        image.set_colorkey(colorkey, pygame.RLEACCEL)
            
        return image
    
    def update(self, tick):
        self.index += 1
        if self.index == len(self.frames):
            self.kill()
            return 
        self.image = self.frames[self.index]
    
class Aircraft(pygame.sprite.Sprite):
    
    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)
        number = str(number).zfill(2)
        self.base_image = getattr(media, "Aircraft_" + number)
        self.rotor_image = getattr(media, "rotor" + number)
        self.hit_image = pygame.transform.rotate(getattr(media, "Aircraft_" + number + "_hit"), 180)
        self.frames = [self.create_image(True), self.create_image(False)]
        
        self.image = self.frames[0]
        self.show_rotor = True
        self.rotor_tick = ROTOR_ROTATE_TICK
        self.drawing_rect = pygame.Rect(random.randint(50, 950), -300, self.image.get_rect().w, self.image.get_rect().h)

        self.collide_rect_diff_x = 5
        self.collide_rect_diff_y = 20
        self.collide_rect = pygame.Rect(self.drawing_rect.x + self.collide_rect_diff_x,
                                        self.drawing_rect.y + self.collide_rect_diff_y,
                                        self.drawing_rect.w - 10, self.drawing_rect.h - 44)
        
        self.rect = self.drawing_rect
        
        #r = pygame.Surface((self.collide_rect.w, self.collide_rect.h))
        #r.fill(GEM_FONT_COLOR)
        #self.frames[0].blit(r, (self.collide_rect.x - self.drawing_rect.x, self.collide_rect.y - self.drawing_rect.y))
        #self.frames[1].blit(r, (self.collide_rect.x - self.drawing_rect.x, self.collide_rect.y - self.drawing_rect.y))
                
        self.life = 5
        
    def set_drawing(self):
        self.rect = self.drawing_rect
        
    def set_collide(self):
        self.rect = self.collide_rect
        
    def move(self, mx, my):
        self.move_x(mx)
        self.move_y(my)
        
    def move_x(self, mx):
        self.drawing_rect.x += mx
        self.collide_rect.x += mx
        
    def move_y(self, my):
        self.drawing_rect.y += my
        self.collide_rect.y += my
        
    def set_drawing_position_x(self, x):
        self.drawing_rect.x = x
        self.collide_rect.x = x + self.collide_rect_diff_x
        
    def set_drawing_position_y(self, y):
        self.drawing_rect.y = y
        self.collide_rect.y = y + self.collide_rect_diff_y
        
    def hit(self):
        self.image = self.hit_image
        self.life -= 1
        media.hit.play()
        if self.life == 0:
            self.kill()
            
    def create_image(self, show_rotor):
        image = pygame.Surface(self.base_image.get_size())#.convert()
        image.blit(self.base_image, (0, 0), self.base_image.get_rect())
        
        if show_rotor:
            self.draw_rotor(image)
        
        image = pygame.transform.rotate(image, 180).convert()
        colorkey = image.get_at((0,0))        
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def draw_rotor(self, image):
        pass
    
    def update(self, tick):
        self.rotor_tick -= tick

        if self.rotor_tick <= 0:
            self.rotor_tick = ROTOR_ROTATE_TICK
            self.show_rotor = not self.show_rotor
        if self.show_rotor:
            self.image = self.frames[0]
        else:
            self.image = self.frames[1]

    
class Aircraft01(Aircraft):
    
    def __init__(self):
        Aircraft.__init__(self, 1)
        
    def hit(self):
        self.image = self.hit_image
        if self.life > 0:
            self.life -= 1
        media.hit.play()

    def draw_rotor(self, image):
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 - 18, 10), self.rotor_image.get_rect())
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 4, 0), self.rotor_image.get_rect())
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 24, 10), self.rotor_image.get_rect())

            
class Aircraft02(Aircraft):
    
    def __init__(self):
        Aircraft.__init__(self, 2)
        
    def draw_rotor(self, image):
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 - 26, 10), self.rotor_image.get_rect())
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 2, 0), self.rotor_image.get_rect())
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 32, 10), self.rotor_image.get_rect())
            
class Aircraft03(Aircraft):
    
    def __init__(self):
        Aircraft.__init__(self, 3)
        
    def draw_rotor(self, image):
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 2, 0), self.rotor_image.get_rect())
    
class Aircraft04(Aircraft):
    
    def __init__(self):
        Aircraft.__init__(self, 4)
        
    def draw_rotor(self, image):
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 2, 0), self.rotor_image.get_rect())

class Aircraft05(Aircraft):
    
    def __init__(self):
        Aircraft.__init__(self, 5)
        
    def draw_rotor(self, image):
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 - 26, 10), self.rotor_image.get_rect())
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 2, 0), self.rotor_image.get_rect())
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 32, 10), self.rotor_image.get_rect())

class Aircraft06(Aircraft):
    
    def __init__(self):
        Aircraft.__init__(self, 6)
        
    def draw_rotor(self, image):
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 2, 0), self.rotor_image.get_rect())

class Aircraft07(Aircraft):
    
    def __init__(self):
        Aircraft.__init__(self, 7)
        
    def draw_rotor(self, image):
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 - 26, 10), self.rotor_image.get_rect())
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 2, 0), self.rotor_image.get_rect())
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 32, 10), self.rotor_image.get_rect())

class Aircraft08(Aircraft):
    
    def __init__(self):
        Aircraft.__init__(self, 8)
        
    def draw_rotor(self, image):
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2, 0), self.rotor_image.get_rect())

class Aircraft09(Aircraft):
    
    def __init__(self):
        Aircraft.__init__(self, 9)
        
    def draw_rotor(self, image):
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 - 40, 24), self.rotor_image.get_rect())
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2 + 40, 24), self.rotor_image.get_rect())

class Aircraft10(Aircraft):
    
    def __init__(self):
        Aircraft.__init__(self, 10)
        self.frames[0] = pygame.transform.rotate(self.frames[0], 180).convert()
        colorkey = self.frames[0].get_at((0,0))        
        self.frames[0].set_colorkey(colorkey, pygame.RLEACCEL)
        self.frames[1] = pygame.transform.rotate(self.frames[1], 180).convert()
        colorkey = self.frames[1].get_at((0,0))        
        self.frames[1].set_colorkey(colorkey, pygame.RLEACCEL)
        
        self.hit_image = pygame.transform.rotate(self.hit_image, 180)
        self.life = 10

        self.collide_rect_diff_x = 5
        self.collide_rect_diff_y = 20
        self.collide_rect = pygame.Rect(self.drawing_rect.x + self.collide_rect_diff_x,
                                        self.drawing_rect.y + self.collide_rect_diff_y,
                                        self.drawing_rect.w - 10, self.drawing_rect.h - 44)

    def draw_rotor(self, image):
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2, 0), self.rotor_image.get_rect())    

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, color, direction, initpos):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.base_image = pygame.transform.scale2x(getattr(media, "bullet_2_" + color))
        self.image = pygame.transform.rotate(self.base_image, pygame.math.Vector2(0, -1).as_polar()[1])
        self.image = pygame.transform.rotate(self.image, self.direction.as_polar()[1])
        
        self.rect = pygame.Rect(initpos[0], initpos[1], self.image.get_rect().w, self.image.get_rect().h)
        self.hit_frame = -1
        self.bullet_speed = BULLET_SPEED
                
    def update(self, tick):
        move = self.bullet_speed / tick
        self.rect.x += move * self.direction[0]
        self.rect.y -= move * self.direction[1]
        if self.rect.y < 0 or self.rect.y > 720:
            self.kill()
        if self.rect.x < 0 or self.rect.x > 1024:
            self.kill()
            
class BlueBullet(Bullet):
    
    def __init__(self, direction, initpos):
        Bullet.__init__(self, "blue", direction, initpos)

class PurpleBullet(Bullet):
    
    def __init__(self, direction, initpos):
        Bullet.__init__(self, "purple", direction, initpos)
        
class OrangeBullet(Bullet):
    
    def __init__(self, direction, initpos):
        Bullet.__init__(self, "orange", direction, initpos)
        
class Debris(pygame.sprite.Sprite):
    
    def __init__(self, direction, initpos):
        pygame.sprite.Sprite.__init__(self)
        self.frames = [media.bullet_orange0003, media.bullet_blue0003, media.bullet_purple0003]
        self.frames = [pygame.transform.scale2x(frame) for frame in self.frames]
        self.image = self.frames[0]
        self.rect = pygame.Rect((initpos[0], initpos[1], self.image.get_rect().w, self.image.get_rect().h))
        self.index = 0
        self.speed = 500
        self.direction = direction
        
    def update(self, tick):
        self.index += 1
        if self.index == len(self.frames):
            self.index = 0
        self.image = self.frames[self.index]
        self.rect.x += self.speed / tick * self.direction.x
        self.rect.y += self.speed / tick * self.direction.y
        
        if self.rect.x < 0 or self.rect.x > 1024:
            self.kill()
        if self.rect.y < 0 or self.rect.y > 720:
            self.kill()
        
class Background(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = media.map1
        self.tick_count = 0
        self.rect = pygame.Rect((0, 2480, 1024, 720))
        
    def reset(self):
        self.tick_count = 0
        
    def update(self, tick):
        return
        self.tick_count += tick
        self.rect.y = 2480 - 2480 * self.tick_count / 600000.0

class BackgroundLava(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = media.lava
        self.rect = self.image.get_rect()
        
    def update(self, *args):
        pass

class EndlessCloud(pygame.sprite.Sprite):
    
    def __init__(self, delay=0):
        pygame.sprite.Sprite.__init__(self)
        self.delay = delay
        self.reset()
        
    def reset(self):
        number = random.randint(1, 4)
        self.image = getattr(media, "cloud" + str(number))
        self.speed = random.randint(50, 80)
        self.rect = pygame.Rect((random.randint(0, 1000) - 500, -self.image.get_rect().h, self.image.get_rect().w, self.image.get_rect().h))
    
    def update(self, tick):
        if self.delay > 0:
            self.delay -= tick
            return
        self.rect.y += self.speed / tick
        if self.rect.y >= 720:
            self.reset()
        
class StatusBar(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = media.status_bar
        self.image = None
        self.rect = pygame.Rect(16, 16, 1000, self.base_image.get_rect().h)
        self.current_page = ""
        self.links_left = 0
        self.total_links = 0
        self.collected = 0
        self.current_life = 10
        self.updated = True
        self.update()
        
    def draw_life_bar(self):
        font = media.get_font(8)
        s = font.render("Life:", True, GEM_FONT_COLOR)
        self.image.blit(s, (812, 0))
        for i in range(0, self.current_life):
            bar = pygame.Surface((10, 38))
            bar.fill((200, 30, 30))
            self.image.blit(bar, (812 + 18 * i, 10))
        
    def set_current_page(self, current_page):
        self.current_page = current_page
        self.updated = True
    
    def set_links_left(self, links_left):
        self.links_left = links_left
        self.updated = True
    
    def set_total_links(self, total_links):
        self.total_links = total_links
        self.updated = True
    
    def set_collected(self, collected):
        self.collected = collected
        self.updated = True
    
    def set_current_life(self, life):
        self.current_life = life
        self.updated = True
        
    def update(self, *args):
        if not self.updated:
            return
        self.image = pygame.Surface((self.rect.w, self.rect.h)).convert()
        colorkey = self.base_image.get_at((0,0))        
        self.image.fill(colorkey)
        self.image.blit(self.base_image, (0,0))
        font = media.get_font(GEM_FONT_SIZE)
        page = font.render("Page: " + self.current_page, True, GEM_FONT_COLOR)
        self.image.blit(page, (16,14))
        links = font.render("Gems left: " + str(self.links_left) + " / " + str(self.total_links), True, GEM_FONT_COLOR)
        self.image.blit(links, (16, 28))
        collected = font.render("Collected: " + str(self.collected), True, GEM_FONT_COLOR)
        self.image.blit(collected, (220, 28))
        self.draw_life_bar()
        colorkey = self.base_image.get_at((0,0))        
        self.image.set_colorkey(colorkey, pygame.RLEACCEL)
        
class WarpPage(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = media.page3
        self.image = self.base_image
        self.rect = pygame.Rect(((1024 - self.base_image.get_rect().w) / 2, (780 - self.base_image.get_rect().h) / 2, self.base_image.get_rect().w, self.base_image.get_rect().h))
        self.current_page = 1
        self.found_links = None
        self.on_item_clicked = []
        self.items_rect = []
        self.next_rect = None
        self.prev_rect = None
        self.messagebox = None
        self.warp_to_word = None
        self.accept = False
        self.level_cleared = False
        
    def reset(self):
        self.current_page = 1
        self.messagebox = None
        self.warp_to_word = None
        self.accept = False
        
    def set_found_links(self, found_links):
        self.found_links = sorted(found_links)
    
    def next_page(self):
        if self.current_page < self.count_pages():
            media.beep.play()
            self.current_page += 1
            self.update()
            
    def previous_page(self):
        if self.current_page > 1:
            media.beep.play()
            self.current_page -= 1
            self.update()
            
    def click(self):
        if self.messagebox:
            self.messagebox.click()
        else:
            if self.next_rect.collidepoint(pygame.mouse.get_pos()):
                self.next_page()
            elif self.prev_rect.collidepoint(pygame.mouse.get_pos()):
                self.previous_page()
            else:
                for word, item, ir in self.items_rect:
                    if ir.collidepoint(pygame.mouse.get_pos()):
                        self.messagebox = MessageBox(word, self)
                        self.warp_to_word = word
                        #media.beep.play()
                        
    def count_pages(self):
        c = int(math.ceil(len(self.found_links) / 16.0))
        if c == 0:
            return 1
        else:
            return c
    
    def create_next_button(self):
        buttons_font = media.get_font(16)
        snext = buttons_font.render("Next", True, GEM_FONT_COLOR)
        self.next_rect = pygame.Rect((self.rect.x + 660, self.rect.y + 594, snext.get_rect().w, snext.get_rect().h))
        return (snext, (660, 594))
        
    def create_previous_button(self):
        buttons_font = media.get_font(16)
        sprevious = buttons_font.render("Previous", True, GEM_FONT_COLOR)
        self.prev_rect = pygame.Rect((self.rect.x + 430, self.rect.y + 594, sprevious.get_rect().w, sprevious.get_rect().h))
        return (sprevious, (430, 594))
    
    def create_pages(self):
        pages_font = media.get_font(20)
        pages = pages_font.render("Page: " + str(self.current_page) + " / " + str(self.count_pages()), True, GEM_FONT_COLOR)
        return (pages, (48, 592))
    
    def create_title(self):
        title_font = media.get_font(32)
        if self.level_cleared:
            title = title_font.render("Page cleared!", True, GEM_FONT_COLOR)
        else:
            title = title_font.render("Warp zone", True, GEM_FONT_COLOR)
        return (title, ((self.base_image.get_rect().w - title.get_rect().w) / 2, 48))
    
    def render_page(self):
        item_font = media.get_font(8)
        page_items = self.found_links[16 * (self.current_page - 1) : 16 * self.current_page]
            
        for i in range(0, len(page_items)):
            y = 140 + 24 * i
            item_rect = pygame.Rect((self.rect.x + 48, self.rect.y + y, 700, 24))
            item = item_font.render(page_items[i], True, GEM_FONT_COLOR)
            
            if not self.messagebox and item_rect.collidepoint(pygame.mouse.get_pos()):
                selitem = pygame.Surface((item_rect.w, item_rect.h))
                selitem.fill((50, 155, 50))
                selitem.blit(item, (8, 8))
                self.image.blit(selitem, (48, y))
            else:
                self.image.blit(item, (56, y + 8))
            self.items_rect.append((page_items[i], item, item_rect))
                                    
    def update(self, *args):
        self.image = pygame.Surface((self.base_image.get_rect().w, self.base_image.get_rect().h))
        self.image.blit(self.base_image, (0, 0))
        self.image.blit(*self.create_title())
        self.image.blit(*self.create_pages())
        self.image.blit(*self.create_next_button())
        self.image.blit(*self.create_previous_button())
        self.render_page()
        
        if self.messagebox:
            if self.messagebox.yes:
                self.messagebox = None
                self.accept = True
            elif self.messagebox.no:
                self.messagebox = None
            else:
                self.messagebox.update()
                self.image.blit(self.messagebox.image, (self.messagebox.rect.x, self.messagebox.rect.y))
            
        colorkey = self.base_image.get_at((0,0))        
        self.image.set_colorkey(colorkey, pygame.RLEACCEL)

class MessageBox(pygame.sprite.Sprite):
    
    def __init__(self, word, owner):
        pygame.sprite.Sprite.__init__(self)
        self.word = word
        self.owner = owner
        self.base_image = media.messagebox
        self.image = self.base_image
        self.rect = pygame.Rect(((self.owner.rect.w - self.base_image.get_rect().w) / 2, (self.owner.rect.h - self.base_image.get_rect().h) / 2, self.base_image.get_rect().w, self.base_image.get_rect().h))
        self.on_item_clicked = []
        self.ok_rect = None
        self.cancel_rect = None
        self.yes = False
        self.no = False
        
    def create_title(self):
        title_font = media.get_font(32)
        title = title_font.render("Warp to?", True, GEM_FONT_COLOR)
        return (title, (32, 48))
    
    def create_message(self):
        msg_font = media.get_font(8)
        msg = msg_font.render(self.word, True, GEM_FONT_COLOR)
        return (msg, (32, 148))
    
    def create_yes(self):
        buttons_font = media.get_font(16)
        ok = buttons_font.render("Yes", True, GEM_FONT_COLOR)
        self.ok_rect = pygame.Rect((self.owner.rect.x + self.rect.x + 328, self.owner.rect.y + self.rect.y + 256, ok.get_rect().w, ok.get_rect().h))
        return (ok, (328, 256))
    
    def create_no(self):
        buttons_font = media.get_font(16)
        cancel = buttons_font.render("No", True, GEM_FONT_COLOR)
        self.cancel_rect = pygame.Rect((self.owner.rect.x + self.rect.x + 116, self.owner.rect.y + self.rect.y + 256, cancel.get_rect().w, cancel.get_rect().h))
        return (cancel, (116, 256))
    
    def click(self):
        print pygame.mouse.get_pos()
        if self.ok_rect.collidepoint(pygame.mouse.get_pos()):
            self.yes = True
            media.beep.play()
        elif self.cancel_rect.collidepoint(pygame.mouse.get_pos()):
            self.no = True
            media.beep.play()
            
    def update(self, *args):
        self.image = pygame.Surface((self.base_image.get_rect().w, self.base_image.get_rect().h))
        self.image.blit(self.base_image, (0, 0))
        self.image.blit(*self.create_title())
        self.image.blit(*self.create_message())
        self.image.blit(*self.create_yes())
        self.image.blit(*self.create_no())

        colorkey = self.base_image.get_at((0,0))        
        self.image.set_colorkey(colorkey, pygame.RLEACCEL)
    
class PowerupBar(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = media.powerup_bar
        self.image = self.base_image
        self.rect = pygame.Rect((16, 640, 1000, self.base_image.get_rect().h))
        
        self.gem_green16 = pygame.Surface((16, 16))
        self.gem_green16.blit(media.gem16green, pygame.Rect(0, 0, 16, 16))
        colorkey = self.gem_green16.get_at((0,0))        
        self.gem_green16.set_colorkey(colorkey, pygame.RLEACCEL)
        self.gem_green32 = pygame.Surface((32, 32))
        self.gem_green32.blit(media.gem32green, pygame.Rect(0, 0, 32, 32))
        colorkey = self.gem_green32.get_at((0,0))        
        self.gem_green32.set_colorkey(colorkey, pygame.RLEACCEL)

        self.gem_blue16 = pygame.Surface((16, 16))
        self.gem_blue16.blit(media.gem16blue, pygame.Rect(0, 0, 16, 16))
        colorkey = self.gem_blue16.get_at((0,0))        
        self.gem_blue16.set_colorkey(colorkey, pygame.RLEACCEL)
        self.gem_blue32 = pygame.Surface((32, 32))
        self.gem_blue32.blit(media.gem32blue, pygame.Rect(0, 0, 32, 32))
        colorkey = self.gem_blue32.get_at((0,0))        
        self.gem_blue32.set_colorkey(colorkey, pygame.RLEACCEL)

        self.gem_yellow16 = pygame.Surface((16, 16))
        self.gem_yellow16.blit(media.gem16yellow, pygame.Rect(0, 0, 16, 16))
        colorkey = self.gem_yellow16.get_at((0,0))        
        self.gem_yellow16.set_colorkey(colorkey, pygame.RLEACCEL)
        self.gem_yellow32 = pygame.Surface((32, 32))
        self.gem_yellow32.blit(media.gem32yellow, pygame.Rect(0, 0, 32, 32))
        colorkey = self.gem_yellow32.get_at((0,0))        
        self.gem_yellow32.set_colorkey(colorkey, pygame.RLEACCEL)
        
        self.gem_orange16 = pygame.Surface((16, 16))
        self.gem_orange16.blit(media.gem16orange, pygame.Rect(0, 0, 16, 16))
        colorkey = self.gem_orange16.get_at((0,0))        
        self.gem_orange16.set_colorkey(colorkey, pygame.RLEACCEL)
        self.gem_orange32 = pygame.Surface((32, 32))
        self.gem_orange32.blit(media.gem32orange, pygame.Rect(0, 0, 32, 32))
        colorkey = self.gem_orange32.get_at((0,0))        
        self.gem_orange32.set_colorkey(colorkey, pygame.RLEACCEL)
        
        self.gem_grey16 = pygame.Surface((16, 16))
        self.gem_grey16.blit(media.gem16grey, pygame.Rect(0, 0, 16, 16))
        colorkey = self.gem_grey16.get_at((0,0))        
        self.gem_grey16.set_colorkey(colorkey, pygame.RLEACCEL)
        self.gem_grey32 = pygame.Surface((32, 32))
        self.gem_grey32.blit(media.gem32grey, pygame.Rect(0, 0, 32, 32))
        colorkey = self.gem_grey32.get_at((0,0))        
        self.gem_grey32.set_colorkey(colorkey, pygame.RLEACCEL)
                
        self.green_active = 0
        self.blue_active = 0
        self.yellow_active = 0
        self.grey_active = 0
        self.color = ""
        
    def reset(self):
        self.green_active = 0
        self.blue_active = 0
        self.yellow_active = 0
        self.grey_active = 0
        self.color = ""
    
    def create_image(self):
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        colorkey = self.base_image.get_at((0,0))        
        self.image.set_colorkey(colorkey, pygame.RLEACCEL)
        self.image.fill(colorkey)
        self.image.blit(self.base_image, (0, 0))
        self.image.blit(self.gem_green16, (self.base_image.get_rect().w, 0))
        self.image.blit(self.gem_blue16, (self.base_image.get_rect().w, 16))
        self.image.blit(self.gem_yellow16, (self.base_image.get_rect().w, 32))
        self.image.blit(self.gem_grey16, (self.base_image.get_rect().w, 48))
        self.draw_powerup_gem()
        self.draw_progress_bars()
        
    def set_color(self, color):
        self.color = GEM_COLORS[color]

    def draw_powerup_gem(self):
        if self.color == "green":
            image = self.gem_green32
        elif self.color == "blue":
            image = self.gem_blue32
        elif self.color == "yellow":
            image = self.gem_yellow32
        elif self.color == "grey":
            image = self.gem_grey32
        elif self.color == "orange":
            image = self.gem_orange32
        else:
            return
        
        colorkey = image.get_at((0,0))        
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        self.image.blit(image, (16, 16))
    
    def activate_powerup(self):
        media.powerup.play()
        if self.color == "green":
            self.green_active = 180000
        elif self.color == "blue":
            self.blue_active = 30000
        elif self.color == "yellow":
            self.yellow_active = 60000
        elif self.color == "grey":
            self.grey_active = 60000
        self.color = ""
        
    def draw_progress_bars(self):
        if self.green_active > 0:
            bar = pygame.Surface((self.green_active / 180, 8))
            bar.fill((0, 200, 0))
            self.image.blit(bar, (self.base_image.get_rect().w + 32, 0))
        if self.blue_active > 0:
            bar = pygame.Surface((self.blue_active / 30, 8))
            bar.fill((0, 0, 200))
            self.image.blit(bar, (self.base_image.get_rect().w + 32, 16))
        if self.yellow_active > 0:
            bar = pygame.Surface((self.yellow_active / 60, 8))
            bar.fill((200, 200, 0))
            self.image.blit(bar, (self.base_image.get_rect().w + 32, 32))
        if self.grey_active > 0:
            bar = pygame.Surface((self.grey_active / 60, 8))
            bar.fill((180, 180, 180))
            self.image.blit(bar, (self.base_image.get_rect().w + 32, 48))
            
    def update(self, tick):
        self.green_active -= tick
        if self.green_active < 0:
            self.green_active = 0
        self.blue_active -= tick
        if self.blue_active < 0:
            self.blue_active = 0
        self.yellow_active -= tick
        if self.yellow_active < 0:
            self.yellow_active = 0
        self.grey_active -= tick
        if self.grey_active < 0:
            self.grey_active = 0
            
        self.create_image()
        
class Gameover(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = media.gameover
        self.image = self.base_image
        self.rect = pygame.Rect(((1024 - self.base_image.get_rect().w) / 2, (720 - self.base_image.get_rect().h) / 2, self.base_image.get_rect().w, self.base_image.get_rect().h))
        self.try_again_rect = None
        self.quit_rect = None
        self.create_image()
        self.try_again = False
        self.quit = False
        self.timing = 1000
        
    def create_image(self):
        self.image = pygame.Surface((self.base_image.get_rect().w, self.base_image.get_rect().h))
        self.image.blit(self.base_image, (0, 0))
        f = media.get_font(32)
        s = f.render("Game Over!!", True, GEM_FONT_COLOR)    
        self.image.blit(s, (150, 56))
        
        buttons = media.get_font(16)
        
        s = buttons.render("Try Again", True, GEM_FONT_COLOR)
        self.image.blit(s, (120, 312))
        self.try_again_rect = pygame.Rect((self.rect.x + 120, self.rect.y + +312, s.get_rect().w, s.get_rect().h))
        s = buttons.render("Quit", True, GEM_FONT_COLOR)
        self.image.blit(s, (464, 312))
        self.quit_rect = pygame.Rect((self.rect.x + 464, self.rect.y + 312, s.get_rect().w, s.get_rect().h))
        
        colorkey = self.image.get_at((0,0))        
        self.image.set_colorkey(colorkey, pygame.RLEACCEL)
        
    def click(self):
        if self.try_again_rect.collidepoint(pygame.mouse.get_pos()):
            self.try_again = True
            media.beep.play()
        elif self.quit_rect.collidepoint(pygame.mouse.get_pos()):
            self.quit = True
            media.beep.play()
    
    def update(self, *args):
        pass
    
class Gameplay(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = media.page3
        self.rect = pygame.Rect(((1024 - self.base_image.get_rect().w) / 2, (720 - self.base_image.get_rect().h) / 2, self.base_image.get_rect().w, self.base_image.get_rect().h))
        self.close = False
        self.current_page = 1
        
        self.pages = ["""
Hitler invaded Wikipedia!

You must defeat him and make Wikipedia free again!

This game is inspired by the Hitler Wikipedia game.
When the game start, a random page from Wikipedia will be generated.
All the links on this page will appear as gems in the game.
By collecting gems, you can warp to these pages.
You must collect gems and warp to other Wikipedia pages until you
reach the Hitler page.
This is where Hitler is hiding.  Find him and defeat him.
""",
"""
Hit space or left-click to shoot bullets.
Hit Esc. to make the Warp zone appear.

You start the game with 10 HP.
Everytime you take a hit, you lose 1 HP.
If you finish a level (no gems left), you will recover all your life.

You can warp to another page anytime during the game by pressing Esc.
However, if you do so you won't recover your life.
If you drop to 0 HP, it's Game Over.

Gathering gems will allow you to use power-ups.  
Right-click to activate the power-up shown in the lower-left corner.
""",
"""
You must collect 10 gems to get a power-up.
The power-up will appear in the lower-left corner.
Power-ups are associated with gem colors.
If you don't use your power and collect another gem,
the power-up will change to the last color you collected.


Green: Activate a shield that last for 3 minutes.
       If you take a hit, the shield will absorb it.
Blue: Increase the power of your gun for 30 seconds.
Yellow: Increase your agility for 60 seconds.
Grey:  Activate a gem magnet for 60 seconds.
       The gems will fly in your direction when you get close.
Red : Regenerate 3 HP.
"""]
        self.create_image()

    def next_page(self):
        if self.current_page < self.count_pages():
            media.beep.play()
            self.current_page += 1
            self.create_image()
        else:
            media.beep.play()
            self.close = True
            self.current_page = 1
            self.create_image()
            
    def previous_page(self):
        if self.current_page > 1:
            media.beep.play()
            self.current_page -= 1
            self.create_image()
            
    def manage_event(self, e):
        if e.type == pygame.MOUSEBUTTONUP:
            if self.next_rect.collidepoint(pygame.mouse.get_pos()):
                self.next_page()
            elif self.prev_rect.collidepoint(pygame.mouse.get_pos()):
                self.previous_page()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.close = True
                self.current_page = 1
                self.create_image()
                
    def count_pages(self):
        return len(self.pages)
    
    def create_next_button(self):
        buttons_font = media.get_font(16)
        if self.current_page == self.count_pages():
            snext = buttons_font.render("Close", True, GEM_FONT_COLOR)
            self.next_rect = pygame.Rect((self.rect.x + 648, self.rect.y + 594, snext.get_rect().w, snext.get_rect().h))
            return (snext, (648, 594))
        else:
            snext = buttons_font.render("Next", True, GEM_FONT_COLOR)
            self.next_rect = pygame.Rect((self.rect.x + 660, self.rect.y + 594, snext.get_rect().w, snext.get_rect().h))
            return (snext, (660, 594))
        
    def create_previous_button(self):
        buttons_font = media.get_font(16)
        sprevious = buttons_font.render("Previous", True, GEM_FONT_COLOR)
        self.prev_rect = pygame.Rect((self.rect.x + 430, self.rect.y + 594, sprevious.get_rect().w, sprevious.get_rect().h))
        return (sprevious, (430, 594))
    
    def create_pages(self):
        pages_font = media.get_font(20)
        pages = pages_font.render("Page: " + str(self.current_page) + " / " + str(self.count_pages()), True, GEM_FONT_COLOR)
        return (pages, (48, 592))
    
    def create_title(self):
        title_font = media.get_font(32)
        if self.current_page == 1:
            s = "Introduction"
        elif self.current_page == 2:
            s = "Gameplay"
        else:
            s = "Power-ups"
        title = title_font.render(s, True, GEM_FONT_COLOR)
        return (title, ((self.base_image.get_rect().w - title.get_rect().w) / 2, 48))
    
    def render_page(self):
        item_font = media.get_font(9)
        page_items = self.pages[self.current_page - 1].split("\n")
            
        for i in range(0, len(page_items)):
            y = 140 + 24 * i
            item_rect = pygame.Rect((self.rect.x + 48, self.rect.y + y, 700, 24))
            item = item_font.render(page_items[i], True, GEM_FONT_COLOR)
            self.image.blit(item, (56, y + 8))
                                    
    def create_image(self):
        self.image = pygame.Surface((self.base_image.get_rect().w, self.base_image.get_rect().h))
        self.image.blit(self.base_image, (0, 0))
        self.image.blit(*self.create_title())
        self.image.blit(*self.create_pages())
        self.image.blit(*self.create_next_button())
        self.image.blit(*self.create_previous_button())
        self.render_page()
                    
        colorkey = self.base_image.get_at((0,0))        
        self.image.set_colorkey(colorkey, pygame.RLEACCEL)

    def update(self, *args):
        pass
    
class Credits(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.close = False
        
    def manage_event(self):
        pass
    
class Gamestart(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.start_game_rect = None
        self.gameplay_rect = None
        self.quit_rect = None
        self.image = self.create_image()
        self.rect = pygame.Rect((0, 0, 1024, 720))
        self.position = 0
        self.cursor = media.Aircraft_10
        
        self.quit = False
        self.start_game = False
        self.show_gameplay = False
        
    def create_wikipedia(self):
        font = media.get_font(64)
        s = font.render("Wikipedia", True, GEM_FONT_COLOR)
        return (s, ((1024 - s.get_rect().w) / 2, 120))
    
    def create_1942(self):
        font = media.get_font(128)
        s = font.render("1942", True, GEM_FONT_COLOR)
        return (s, ((1024 - s.get_rect().w) / 2, 200))
    
    def create_start_game(self):
        font = media.get_font(32)
        s = font.render("Start Game", True, GEM_FONT_COLOR)
        rect = pygame.Rect((1024 - s.get_rect().w) / 2, 450, s.get_rect().w, s.get_rect().h)
        return (s, rect)
    
    def create_gameplay(self):
        font = media.get_font(32)
        s = font.render("Gameplay", True, GEM_FONT_COLOR)
        rect = pygame.Rect((1024 - s.get_rect().w) / 2, 500, s.get_rect().w, s.get_rect().h)
        return (s, rect)
    
    def create_quit(self):
        font = media.get_font(32)
        s = font.render("Quit", True, GEM_FONT_COLOR)
        rect = pygame.Rect((1024 - s.get_rect().w) / 2, 550, s.get_rect().w, s.get_rect().h)
        return (s, rect)
       
    def create_image(self):
        image = pygame.Surface((1024, 720))
        image.blit(*self.create_wikipedia())
        image.blit(*self.create_1942())
        
        s, self.start_game_rect = self.create_start_game()
        image.blit(s, self.start_game_rect)
        
        s, self.gameplay_rect = self.create_gameplay()
        image.blit(s, self.gameplay_rect)
                
        s, self.quit_rect = self.create_quit()
        image.blit(s, self.quit_rect)
        
        return image
    
    def manage_event(self, e):
        if e.type == pygame.QUIT:
            self.quit = True
            return        
        if e.type != pygame.MOUSEBUTTONUP:
            return
        
        pos = pygame.mouse.get_pos()
        if self.start_game_rect.collidepoint(pos):
            self.start_game = True
            media.beep.play()
        elif self.gameplay_rect.collidepoint(pos):
            self.show_gameplay = True
            media.beep.play()
        elif self.quit_rect.collidepoint(pos):
            self.quit = True
    
    def update(self):
        pass
    
class SkullShield(pygame.sprite.Sprite):
    
    def __init__(self, plane, initvector):
        pygame.sprite.Sprite.__init__(self)
        self.image = media.skull_copy
        self.rect = self.image.get_rect()
        self.plane = plane
        self.v = initvector
        self.life = 10
        self.tick_count = 0
        
    def hit(self):
        self.life -= 1
    
    def set_collide(self):
        pass
    
    def set_drawing(self):
        pass
    
    def update(self, tick):
        if self.life <= 0:
            self.life = 10
            self.rect = pygame.Rect((-1000, -1000, 0, 0))
            self.tick_count = 30000
            
        if not self.plane.alive():
            self.kill()
        self.tick_count -= tick
        self.v = self.v.rotate(800 / tick)
        if self.tick_count <= 0:
            self.rect.x = self.plane.rect.centerx + 80 * self.v.x - 10
            self.rect.y = self.plane.rect.centery + 80 * self.v.y
        
class HitlerLifebar(pygame.sprite.Sprite):
    
    def __init__(self, max_life):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 540))
        self.rect = pygame.Rect((16, 40, 16, 540))
        self.current_life = 0
        self.max_life = max_life
        
    def set_current_life(self, current_life):
        self.current_life = current_life
    
    def update(self, *args):
        self.image = pygame.Surface((16, 540 * self.current_life/ self.max_life))
        self.image.fill((160, 30, 230))
        self.rect.y = 80 + 540 - (540 * self.current_life/ self.max_life)
        self.rect.h = self.image.get_rect().h
                
class Ending(pygame.sprite.Sprite):
    
    def __init__(self):
        self.image = pygame.Surface((1024, 720))
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.alpha = 0
        self.show_credits = False

    def create_credits(self):
        self.image = pygame.Surface((1024, 720*2))
        self.rect = pygame.Rect((0, 0, 1024, 720))        
        font = media.get_font(32)
        s = font.render("Congratulations!", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 20+720))
        
        font = media.get_font(16)
        s = font.render("Hitler has been defeated!", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 120+720))
        s = font.render("Wikipedia is free again!", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 150+720))
        
        s = font.render("Entry for pyweek #20", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 220+720))
        s = font.render("https://github.com/benoxoft/Wikipedia1942", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 250+720))

        s = font.render("All art content from opengameart.org", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 350+720))

        s = font.render("opengameart.org/content/rotating-crystal-animation-8-step", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 380+720))

        s = font.render("opengameart.org/content/aircrafts", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 410+720))

        s = font.render("opengameart.org/content/orthographic-outdoor-tiles", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 440+720))

        s = font.render("opengameart.org/content/fluffy-clouds", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 470+720))

        s = font.render("opengameart.org/content/10-basic-message-boxes", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 500+720))

        s = font.render("opengameart.org/content/explosion-animated", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 530+720))

        s = font.render("opengameart.org/content/skull", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 560+720))

        s = font.render("opengameart.org/content/lava-background-6-screen-resolutions", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 590+720))

        s = font.render("opengameart.org/content/confrontation", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 620+720))

        s = font.render("Thank you for playing!", True, GEM_FONT_COLOR)
        self.image.blit(s, ((1024 - s.get_rect().w) / 2, 670+720))
        self.show_credits = True
        
    def update(self, tick):
        self.alpha += tick / 20
        if self.alpha >= 255 and not self.show_credits:
            self.alpha = 255
            self.create_credits()
        self.image.set_alpha(self.alpha)

        if self.show_credits:
            self.rect.y -= tick / 20
            if self.rect.y < -720:
                self.rect.y = -720
    