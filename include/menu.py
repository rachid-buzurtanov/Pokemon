import pygame, sys
from pygame.locals import *
from tkinter import Tk
from include.button import Button
from include.pokedex import display_pokedex
from include.combat import GameStarter

pygame.init()

FPS = 30


pygame.display.set_caption("Pokemon")

BG = pygame.image.load("assets/image/background/background.jpg")
LARGEUR, HAUTEUR = BG.get_size()
SCREEN = pygame.display.set_mode((LARGEUR, HAUTEUR))
WIDTH = BG.get_width()


def get_font(size):
    return pygame.font.Font("assets/font/font.ttf", size)

def play():
    while True:
        game = GameStarter()
        game.start_game_loop()
        pygame.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def pokedex():
    while True:

        if not display_pokedex():
            display_pokedex()
        else:
            main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("Black")

        OPTIONS_TEXT = get_font(30).render("This is the OPTIONS screen.", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(LARGEUR/2, HAUTEUR/2))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(LARGEUR/2, HAUTEUR/1.4),
                            text_input="BACK", font=get_font(45), base_color="White", hovering_color="#b68f40")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                    
        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))


        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("assets/image/background/Play Rect.png"), pos=(LARGEUR/2, HAUTEUR/2.4),
                            text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        POKEDEX_BUTTON = Button(image=pygame.image.load("assets/image/background/Pokedex.png"), pos=(LARGEUR/2, HAUTEUR/1.8),
                                text_input="POKEDEX", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/image/background/PLay Rect.png"), pos=(LARGEUR/2, HAUTEUR/1.45),
                            text_input="OPTIONS", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/image/background/Play Rect.png"), pos=(LARGEUR/2, HAUTEUR/1.2),
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, POKEDEX_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if POKEDEX_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pokedex()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()