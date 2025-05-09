import pygame
from Game import *
from Character import *
from Zombies import *
from MainMenu import *

WIDTH, HEIGHT = 50*16, 16*30
pygame.init()

pygame.display.set_caption("Zombie Shooter")
menu = MainMenu(WIDTH, HEIGHT)
game_running = False
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        action = menu.handle_event(event)
        if action == "start":
            game_running = True
        elif action == "exit":
            run = False

    if game_running:
        character = Character()
        game = Game(WIDTH, HEIGHT)
        for _ in range(50):
            zombie = Zombie(game.map_width, game.map_height)
            game.zombies.append(zombie)

        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_running = False
                        run = False
            
            keys = pygame.key.get_pressed()
            game.movement(character, keys)
            game.load_map(game.screen, "test.tmx", character)
            game.animation(character)
            game.load_char(game.screen, character)
            game.load_zombies(character)
            
            game.clock.tick(60)
            pygame.display.flip()
    else:
        menu.draw()

pygame.quit()
