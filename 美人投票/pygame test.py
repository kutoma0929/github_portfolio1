import pygame
import sys

WHITE=(255,255,0)
BLACK=(0,0,0)

def main():
    pygame.init()
    pygame.display.set_caption("初めてのPygame")
    screen=pygame.display.set_mode((1100,800))
    clock=pygame.time.Clock()
    img_bg=pygame.image.load("ゲーム背景.jpg")
    font=pygame.font.Font(None,80)
    tmr=0
    
    while True:
        tmr = tmr+1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(img_bg,[0,0])
        
        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    main()