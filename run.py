import pygame

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((1600, 1000))
    from main_menu.main_menu import MainMenu
    mainMenu = MainMenu()
    mainMenu.run()