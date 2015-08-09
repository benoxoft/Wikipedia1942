
import pygame
import os
import sys

m = sys.modules[__name__]

def load_image(img):
    image = pygame.image.load(img)
    return image

def load_all_images():
    for f in os.listdir(os.path.join('media', 'images')):
        if f == '.DS_Store':
            continue
        filename, _ = os.path.splitext(f)
        fullf = os.path.abspath(os.path.join('media', 'images', f))
        if hasattr(m, filename):
            delattr(m, filename)
        setattr(m, filename, load_image(fullf))

def load_sound(snd):
    return pygame.mixer.Sound(snd)

def load_all_sounds():
    for f in os.listdir(os.path.join('media', 'sounds')):
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