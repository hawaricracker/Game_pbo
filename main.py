import pygame
from Game import *
from Character import *
from Zombies import *

WIDTH, HEIGHT = 50*16, 16*30
pygame.init()

pygame.display.set_caption("Tiled Map Example")
character = Character()
game = Game(WIDTH, HEIGHT)
for _ in range(50):
    zombie = Zombie(game.map_width, game.map_height)
    game.zombies.append(zombie)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    
    keys = pygame.key.get_pressed()
    game.movement(character, keys)
    game.load_map(game.screen, "test.tmx", character)
    game.animation(character)
    game.load_char(game.screen, character)
    game.load_zombies(character)
    
    game.clock.tick(60)
    pygame.display.flip()

pygame.quit()