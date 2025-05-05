import pygame
import sys
import gameworld

def main():
    pygame.quit()  # Luk pygame helt, hvis det allerede kører
    pygame.init()  # Genstart pygame
    pygame.font.init()  # Sørg for at font-systemet også startes

    # Skærmopløsning
    res = (720, 720)
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("Whack-a-Mole")

    # Font
    font = pygame.font.SysFont("corbel", 35)  # Opret skrifttype EFTER pygame er initialiseret

    menu(screen, font)

def menu(screen, font):
    color = (255, 255, 255)  
    color_light = (170, 170, 170)  
    color_dark = (100, 100, 100)  

    button_width = 200
    button_height = 50
    menu_running = True

    def draw_button(x, y, text):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x <= mouse[0] <= x + button_width and y <= mouse[1] <= y + button_height:
            pygame.draw.rect(screen, color_light, [x, y, button_width, button_height])
            if click[0]:  # Venstre klik
                return True
        else:
            pygame.draw.rect(screen, color_dark, [x, y, button_width, button_height])

        text_render = font.render(text, True, color)
        screen.blit(text_render, (x + 50, y + 10))
        return False

    while menu_running:
        screen.fill((60, 25, 60))

        start_clicked = draw_button(250, 300, "Start")
        quit_clicked = draw_button(250, 400, "Quit")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if start_clicked:
            pygame.mixer.music.load("background_music.wav")
            pygame.mixer.music.play(-1)
            gameworld.game_loop(screen, font)

        if quit_clicked:
            pygame.quit()
            sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main()
