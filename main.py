import pygame
from win32api import GetSystemMetrics #Install pip win32api agar game berjalan pada fullscreen
from Game import *
from Character import *
from Zombies import *
from MainMenu import *

WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
pygame.init()

pygame.display.set_caption("Zombie Shooter")
menu = MainMenu(WIDTH, HEIGHT)
game_running = False
run = True
zombie = 50

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
        for _ in range(zombie):
            zombie = Zombie(game.map_width, game.map_height, game.objects)
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

            # Gerakan keyboard
            keys = pygame.key.get_pressed()
            game.movement(character, keys)

            # ⬇️⬇️⬇️ BAGIAN BARU: Sistem Tembak dengan LMB ⬇️⬇️⬇️
            mouse_pressed = pygame.mouse.get_pressed()[0]  # LMB ditekan
            mouse_pos = pygame.mouse.get_pos()

            # Posisi karakter di dunia (real coordinates)
            player_world_pos = character.Character_rect.center
            target_world_pos = (
                mouse_pos[0] - game.offset_x,
                mouse_pos[1] - game.offset_y
            )

            if mouse_pressed:
                bullet = character.weapon.fire(player_world_pos, target_world_pos)
                if bullet:
                    game.bullets.append(bullet)
            # ⬆️⬆️⬆️ AKHIR BAGIAN BARU ⬆️⬆️⬆️

            # Rendering dan update semua objek
            game.load_map(game.screen, "Asset/MAP/map1.tmx", character)
            game.animation(character)
            game.load_char(game.screen, character)
            game.load_zombies(character)
            game.update_bullets()  # Update posisi peluru
            game.draw_bullets()    # Gambar peluru ke layar

            game.clock.tick(60)
            pygame.display.flip()
    else:
        menu.draw()

pygame.quit()
