import json
import pygame
from pygame.locals import *
import time

KEY_REPEAT_DELAY = 0.1

def display_pokedex():
    pygame.init()

    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 1024
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("POKEDEX")

    with open("pokedex_data.json", "r") as json_file:
        pokemon_data = json.load(json_file)

    pokemon_sprites = [pygame.image.load(pokemon["sprite"]) for pokemon in pokemon_data]
    pokemon_sprites_back = [pygame.image.load(pokemon["back"]) for pokemon in pokemon_data]
    pokemon_sprites_footprint = [pygame.image.load(pokemon["footprint"]) for pokemon in pokemon_data]

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    font_big = pygame.font.Font("assets/font/Kenzo.otf", 48)
    font_small = pygame.font.Font("assets/font/Kenzo.otf", 36)
    font_extra = pygame.font.Font("assets/font/Kenzo.otf", 668)

    running = True
    selected_index = 0
    key_repeat_time = 0

    while running:
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    selected_index = max(0, selected_index - 1)
                    key_repeat_time = current_time + KEY_REPEAT_DELAY
                elif event.key == K_DOWN:
                    selected_index = min(len(pokemon_data) - 1, selected_index + 1)
                    key_repeat_time = current_time + KEY_REPEAT_DELAY
                elif event.key == K_ESCAPE:
                    return True

        keys = pygame.key.get_pressed()

        if keys[K_UP] and current_time > key_repeat_time:
            selected_index = max(0, selected_index - 1)
            key_repeat_time = current_time + KEY_REPEAT_DELAY
        elif keys[K_DOWN] and current_time > key_repeat_time:
            selected_index = min(len(pokemon_data) - 1, selected_index + 1)
            key_repeat_time = current_time + KEY_REPEAT_DELAY

        window.fill(WHITE)

        arriere_plan = pygame.image.load('assets/image/background/bg2.jpg').convert()
        arriere_plan = pygame.transform.scale(arriere_plan, (WINDOW_WIDTH, WINDOW_HEIGHT))
        arriere_plan.set_alpha(180)
        window.blit(arriere_plan, (0,0))

        if 0 <= selected_index < len(pokemon_data):
            selected_pokemon = pokemon_data[selected_index]
            name = selected_pokemon["name"]
            type = selected_pokemon["type"]
            defense = selected_pokemon["defense"]
            attack = selected_pokemon["attack"]
            hp = selected_pokemon["hp"]
            att_spe = selected_pokemon["special_attack"]
            def_spe = selected_pokemon["special_defense"]
            speed = selected_pokemon["speed"]

            text = font_extra.render(f"#{selected_pokemon['id']}", True, BLACK)
            text.set_alpha(80)
            window.blit(text, (0,  WINDOW_HEIGHT/4))

            window.blit(pokemon_sprites[selected_index], (50, 50))
            window.blit(pokemon_sprites_footprint[selected_index], (38, 140))
            window.blit(pokemon_sprites_back[selected_index], (WINDOW_WIDTH/2.5, WINDOW_HEIGHT/2.5))
            text = font_big.render(f"{name}", True, BLACK)
            window.blit(text, (180, 50))


            text = font_small.render(f"Type: {type}", True, BLACK)
            window.blit(text, (180, 120))

            text = font_small.render(f"Taille: {selected_pokemon.get('height', 'N/A')/10}M", True, BLACK)
            window.blit(text, (180, 160))

            text = font_small.render(f"Poids: {selected_pokemon.get('weight', 'N/A')/10}KG", True, BLACK)
            window.blit(text, (180, 200))

            text = font_small.render(f"Talents: {', '.join(selected_pokemon.get('abilities', ['N/A']))}", True, BLACK)
            window.blit(text, (180, 240))

            additional_info = [
                f"HP: {hp}",
                f"Attaque: {attack}",
                f"Defense: {defense}",
                f"Attaque Speciale: {att_spe}",
                f"Defense Speciale: {def_spe}",
                f"Vitesse: {speed}"
            ]

            for i, info in enumerate(additional_info):
                text = font_small.render(info, True, BLACK)
                window.blit(text, (180, WINDOW_HEIGHT/1.35 + i * 40))

            text = font_big.render("STATS", True, BLACK)
            window.blit(text, (50,WINDOW_HEIGHT/1.35))

        pygame.display.flip()
    pygame.quit()
    return False