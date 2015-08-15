import pygame
pygame.init()
pygame.mixer.init()

import os

import wiki1942
import wiki1942.controls
import wiki1942.sprites

os.environ['SDL_VIDEO_CENTERED'] = '1'

screen = pygame.display.set_mode((1024,720), pygame.HWSURFACE)
pygame.display.set_caption("Wiki 1942")

def main():
    
    main_page = wiki1942.sprites.Gamestart()
    credits_page = wiki1942.sprites.Credits()
    gameplay_page = wiki1942.sprites.Gameplay()
    
    clock = pygame.time.Clock()
    while not main_page.quit and not main_page.start_game:
        for e in pygame.event.get():
            if main_page.show_gameplay:
                gameplay_page.manage_event(e)
            else:
                main_page.manage_event(e)
            
        tick = clock.tick(24)
        main_page.update()
        screen.blit(main_page.image, (0, 0))
        
        if main_page.show_gameplay:
            gameplay_page.update()
            screen.blit(gameplay_page.image, gameplay_page.rect)
            if gameplay_page.close:
                gameplay_page.close = False 
                main_page.show_gameplay = False
                
        pygame.display.update()
        
    if main_page.start_game:
        gc = wiki1942.controls.GameControl(screen)
        while not gc.player.quit:
            for e in pygame.event.get():
                gc.manage_event(e)
            gc.update()
    pygame.quit()
    
if __name__ == '__main__':
    main()
    