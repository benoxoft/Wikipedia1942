import pygame
import media
import random

#http://opengameart.org/content/rotating-crystal-animation-8-step
#http://opengameart.org/content/aircrafts
#http://opengameart.org/content/orthographic-outdoor-tiles
#http://opengameart.org/content/fluffy-clouds
#http://opengameart.org/content/10-basic-message-boxes

GEM_FRAMES = 8
GEM_ROTATE_TICK = 150
GEM_FONT_SIZE = 8
TOOLTIP_WIDTH = 400
GEM_COLORS = ("blue", "green", "grey", "orange", "pink", "yellow")
GEM_FONT_COLOR = (255, 255, 255)

ROTOR_ROTATE_TICK = 30

BULLET_COLORS = ("blue", "purple", "orange")
BULLET_SPEED = 2000

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
        self.speed = random.randint(100, 200)
        self.rect = pygame.Rect((random.randint(120, 660), -60, 32, 32))
            
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
            
class Aircraft(pygame.sprite.Sprite):
    
    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)
        number = str(number).zfill(2)
        self.base_image = getattr(media, "Aircraft_" + number)
        self.rotor_image = getattr(media, "rotor" + number)
        self.hit_image = getattr(media, "Aircraft_" + number + "_hit")
        self.frames = [self.create_image(True), self.create_image(False)]
        
        self.image = self.frames[0]
        self.show_rotor = True
        self.rotor_tick = ROTOR_ROTATE_TICK
        
        self.rect = pygame.Rect(5, 10, self.image.get_rect().w - 10, self.image.get_rect().h - 35)
        
    def create_image(self, show_rotor):
        image = pygame.Surface(self.base_image.get_size()).convert()
        image.blit(self.base_image, (0, 0), self.base_image.get_rect())
        
        if show_rotor:
            self.draw_rotor(image)
        
        colorkey = self.base_image.get_at((0,0))        
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return pygame.transform.rotate(image, 180)

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
        self.frames[0] = pygame.transform.rotate(self.frames[0], 180)
        self.frames[1] = pygame.transform.rotate(self.frames[1], 180)
        
    def draw_rotor(self, image):
        image.blit(self.rotor_image, (image.get_rect().w / 2 - self.rotor_image.get_rect().w / 2, 0), self.rotor_image.get_rect())    

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, color, direction, initpos):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.base_image = getattr(media, "bullet_2_" + color)
        self.frames_hit = (getattr(media, "bullet_" + color + str(i).zfill(4)) for i in range(0, 5))
        self.image = self.base_image
        self.rect = pygame.Rect(initpos[0], initpos[1], self.image.get_rect().w, self.image.get_rect().h)
        
    def update(self, tick):
        move = BULLET_SPEED / tick
        self.rect.y -= move
        if self.rect.y < 0 or self.rect.y > 720:
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
        
class Background(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = media.map1
        self.tick_count = 0
        self.rect = pygame.Rect((0, 2480, 1024, 720))
        
    def update(self, tick):
        self.tick_count += tick
        self.rect.y = 2480 - 2480 * self.tick_count / 600000.0

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
        self.rect = pygame.Rect(16, 16, self.base_image.get_rect().w, self.base_image.get_rect().h)
        self.current_page = ""
        self.links_left = 0
        self.total_links = 0
        self.updated = True
        self.update()
        
    def set_current_page(self, current_page):
        self.current_page = current_page
        self.updated = True
    
    def set_links_left(self, links_left):
        self.links_left = links_left
        self.updated = True
    
    def set_total_links(self, total_links):
        self.total_links = total_links
        self.updated = True
    
    def update(self, *args):
        if not self.updated:
            return
        self.image = pygame.Surface((self.base_image.get_rect().w, self.base_image.get_rect().h)).convert()
        self.image.blit(self.base_image, (0,0))
        font = media.get_font(GEM_FONT_SIZE)
        page = font.render("Page: " + self.current_page, True, GEM_FONT_COLOR)
        self.image.blit(page, (16,16))
        links = font.render("Links left: " + str(self.links_left) + " / " + str(self.total_links), True, GEM_FONT_COLOR)
        self.image.blit(links, (16, 32))
        colorkey = self.base_image.get_at((0,0))        
        self.image.set_colorkey(colorkey, pygame.RLEACCEL)
        
class WarpPage(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = media.page2
        self.image = self.base_image
        self.rect = pygame.Rect(((1024 - self.base_image.get_rect().w) / 2, (720 - self.base_image.get_rect().h) / 2, self.base_image.get_rect().w, self.base_image.get_rect().h))
        self.current_page = 0
        self.found_links = None
        self.on_item_clicked = []
        self.items_rect = []
        self.next_rect = None
        self.prev_rect = None
        
    def set_found_links(self, found_links):
        self.found_links = found_links
    
    def next_page(self):
        pass
    
    def previous_page(self):
        pass
    
    def click(self):
        if self.next_rect.collidepoint(pygame.mouse.get_pos()):
            self.next_page()
        elif self.prev_rect.collidepoint(pygame.mouse.get_pos()):
            self.previous_page()
        else:
            for word, item, ir in self.items_rect:
                if ir.collidepoint(pygame.mouse.get_pos()):
                    print "clicked ", ir

    def count_pages(self):
        return 0
    
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
        title = title_font.render("Warp zone", True, GEM_FONT_COLOR)
        return (title, ((self.base_image.get_rect().w - title.get_rect().w) / 2, 48))
    
    def render_page1(self):
        item_font = media.get_font(10)
        for i in range(0, 16):
            y = 140 + 24 * i
            item_rect = pygame.Rect((self.rect.x + 48, self.rect.y + y, 320, 24))
            item = item_font.render("test", True, GEM_FONT_COLOR)
            
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                selitem = pygame.Surface((item_rect.w, item_rect.h))
                selitem.fill((50, 155, 50))
                selitem.blit(item, (8, 8))
                self.image.blit(selitem, (48, y))
            else:
                self.image.blit(item, (56, y + 8))
            self.items_rect.append(("test", item, item_rect))
                        
    def render_page2(self):
        item_font = media.get_font(10)
        for i in range(0, 16):
            item = item_font.render("test", True, GEM_FONT_COLOR)
            self.image.blit(item , (432, 148 + 24 * i))
            
    def update(self, *args):
        self.image = pygame.Surface((self.base_image.get_rect().w, self.base_image.get_rect().h)).convert()
        self.image.blit(self.base_image, (0, 0))
        self.image.blit(*self.create_title())
        self.image.blit(*self.create_pages())
        self.image.blit(*self.create_next_button())
        self.image.blit(*self.create_previous_button())
        self.render_page1()
        self.render_page2()
        colorkey = self.base_image.get_at((0,0))        
        self.image.set_colorkey(colorkey, pygame.RLEACCEL)
