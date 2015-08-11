import pygame
import os

import wiki1942
import wiki1942.controls
import wiki1942.sprites

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1024,720), pygame.HWSURFACE)
pygame.display.set_caption("Wiki 1942")

def main():
    
    
    
    gc = wiki1942.controls.GameControl(screen)
    while not gc.player.quit:
        for e in pygame.event.get():
            gc.player.manage_key(e)
        gc.update()
                
if __name__ == '__main__':
    main()
    