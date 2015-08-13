
import pygame
import os
import sys

m = sys.modules[__name__]

def load_image(img):
    image = pygame.image.load(img)
    #colorkey = image.get_at((0,0))        
    #image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image

def load_all_images():
    for d in os.listdir(os.path.join('media', 'images')):
        if d == '.DS_Store':
            continue
        for f in os.listdir(os.path.join('media', 'images', d)):
            if f == '.DS_Store':
                continue
            filename, _ = os.path.splitext(f)
            fullf = os.path.abspath(os.path.join('media', 'images', d, f))
            if hasattr(m, filename):
                delattr(m, filename)
            setattr(m, filename, load_image(fullf))

def load_sound(snd):
    return pygame.mixer.Sound(snd)

def load_all_sounds():
    for f in os.listdir(os.path.join('media', 'sounds')):
        if f == '.DS_Store':
            continue
        filename, _ = os.path.splitext(f)
        fullf = os.path.abspath(os.path.join('media', 'sounds', f))
        setattr(m, filename, load_sound(fullf))
        setattr(m, filename + '_file', fullf)
        
def get_font(size):
    return pygame.font.Font(os.path.join('.', 'media', 'fonts', 'PressStart2P.ttf'), size)

def load_all_fonts():
    pass

load_all_images()
load_all_sounds()
load_all_fonts()