import pygame
import json
import random

class GameStarter:
    def __init__(self):
        pygame.init()

        with open('pokedex_data.json', 'r') as file:
            self.pokemon_data = json.load(file)

        self.screen_width, self.screen_height = 1024, 1024
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pokemon")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.player_pokemon = None
        self.computer_pokemon = None
        self.selected_index = 0
        self.button_active = False
        self.hover = False
        self.button_rect = pygame.Rect(0, 0, 0, 0)

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def load_pokemon_images(self, pokemon, size=(400, 400)):
        sprite = pygame.image.load(pokemon['back']).convert_alpha()
        sprite = pygame.transform.scale(sprite, size)
        return sprite

    def show_chosen_pokemon(self, pokemon):
        font = pygame.font.Font("assets/font/Kenzo.otf", 50)
        self.screen.fill((255, 255, 255))
        sprite = self.load_pokemon_images(pokemon)
        x = (self.screen_width - 350) // 2
        y = (self.screen_height - 350) // 2
        self.screen.blit(sprite, (x, y))
        self.draw_text(f"Vous avez choisi le Pokémon {pokemon['name']}!",font, (0, 0, 0), 50, 50)
        pygame.display.flip()
        pygame.time.delay(2000)

    def show_computer_pokemon_transition(self, player_pokemon, computer_pokemon):
        font = pygame.font.Font("assets/font/Kenzo.otf", 50)
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.time.delay(200)

        self.screen.fill((255, 255, 255))
        self.draw_text("Le Pokémon adverse est...", font, (0, 0, 0), 50, 50)
        pygame.display.flip()
        pygame.time.delay(1000)

        self.screen.fill((255, 255, 255))
        sprite = self.load_pokemon_images(computer_pokemon)
        x = (self.screen_width - 400) // 2
        y = (self.screen_height - 400) // 2
        self.screen.blit(sprite, (x, y))
        self.draw_text(f"{computer_pokemon['name']}!", font, (0, 0, 0), 50, 250)
        pygame.display.flip()
        pygame.time.delay(2000)

    def show_battle_interface(self, player_pokemon, computer_pokemon):
        arriere_plan = pygame.image.load('assets/image/background/bg_combat.jpg').convert()
        arriere_plan = pygame.transform.scale(arriere_plan, (self.screen_width , self.screen_height))
        self.screen.blit(arriere_plan, (0,0))


        player_sprite = self.load_pokemon_images(player_pokemon, (400, 400))
        player_x = (self.screen_width - 400) // 13
        player_y = (self.screen_height - 400) // 2
        self.screen.blit(player_sprite, (player_x, player_y))

        computer_sprite = self.load_pokemon_images(computer_pokemon, (400, 400))
        computer_x = (self.screen_width - 400) // 1.08
        computer_y = (self.screen_height - 400) // 2
        self.screen.blit(computer_sprite, (computer_x, computer_y))

        font = pygame.font.Font("assets/font/Kenzo.otf", 160)
        self.draw_text("VS", font, (255, 255, 255), (self.screen_width - 120) // 2, (self.screen_height - 70) // 2)

        pygame.display.flip()
        pygame.time.delay(10000)

    def choose_random_pokemon(self):
        return random.choice(self.pokemon_data)

    def show_pokemon_carousel(self):
        font = pygame.font.Font("assets/font/Kenzo.otf", 40)

        current_pokemon = self.pokemon_data[self.selected_index]

        sprite = self.load_pokemon_images(current_pokemon)
        x = (self.screen_width - 400) // 2
        y = (self.screen_height - 400) // 2
        self.screen.blit(sprite, (x, y))

        self.draw_text(current_pokemon['name'], font,(0, 0, 0), x + 130, y + 410)

        button_rect = pygame.Rect(self.screen_width // 2 - 100, y + 470, 200, 60)
        pygame.draw.rect(self.screen, "#FFD689" if self.button_active else (100, 100, 100), button_rect)
        self.draw_text("Combattre", font,(0, 0, 0), self.screen_width // 2 - 75, y + 485)

        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, "#FFBC42", button_rect)

        pygame.display.flip()

        return button_rect

    def start_game_loop(self):
        running = True
        while running:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.pokemon_data)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.pokemon_data)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.button_active:
                    if self.button_rect.collidepoint(event.pos):
                        self.player_pokemon = self.pokemon_data[self.selected_index]
                        self.computer_pokemon = self.choose_random_pokemon()

                        self.show_chosen_pokemon(self.player_pokemon)
                        self.show_computer_pokemon_transition(self.player_pokemon, self.computer_pokemon)
                        self.show_battle_interface(self.player_pokemon, self.computer_pokemon)

                elif event.type == pygame.MOUSEMOTION:
                    self.hover = self.button_rect.collidepoint(event.pos)

            self.button_rect = self.show_pokemon_carousel()
            self.button_active = True if self.player_pokemon is None else False

            pygame.display.flip()
            self.clock.tick(30)