import pygame
from win32api import GetSystemMetrics
from Game import *
from Character import *
from Zombies import *
from MainMenu import *
from Boss import *

WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
pygame.init()

pygame.display.set_caption("Gen-Z Slayer")
menu = MainMenu(WIDTH, HEIGHT)
game_running = False
run = True
num_zombies = 1
game_over = False
victory = False

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
        try:
            character = Character()
            game = Game(WIDTH, HEIGHT)
        except MemoryError:
            print("Kesalahan memori, coba ulang!")
            run = False
        game_over = False
        victory = False
        boss_spawned = False
        boss = None

        for _ in range(num_zombies):
            new_zombie = Zombie(game.map_width, game.map_height, game.objects)
            game.zombies.append(new_zombie)

        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if game_over or victory:
                            game_running = False
                        else:
                            game_running = False
                            run = False
                    elif event.key == pygame.K_LSHIFT and not game_over and not victory:
                        character.start_dash()
            
            # Periksa kondisi menang (semua zombie dan boss sudah dikalahkan)
            if len(game.zombies) == 0 and not boss_spawned and not game_over:
                boss = Boss(game.map_width, game.map_height, game.objects)
                boss_spawned = True
                print("Boss spawned")  # Debug: Confirm single boss spawn
            
            # Periksa jika karakter masih hidup
            if character.get_hp() <= 0:
                game_over = True
            
            if game_over:
                game.show_game_over()
            elif victory:
                game.show_victory()
            else:
                # Gerakan keyboard (hanya untuk karakter)
                keys = pygame.key.get_pressed()
                game.movement(character, keys)
                character.update_dash()
                game.check_dash_collision_with_zombies(character)
                character.update_health_regen()
                
                # Sistem Tembak dengan LMB
                mouse_pressed = pygame.mouse.get_pressed()[0]
                mouse_pos = pygame.mouse.get_pos()
                
                player_world_pos = character.get_rect().center
                target_world_pos = (
                    mouse_pos[0] - game.offset_x,
                    mouse_pos[1] - game.offset_y
                )
                
                if mouse_pressed:
                    bullet = character.weapon.fire(player_world_pos, target_world_pos)
                    if bullet:
                        game.bullets.append(bullet)
                
                # Rendering dan update semua objek
                game.load_map(game.screen, "Asset/MAP/map1.tmx", character)
                game.animation(character)
                game.load_char(game.screen, character)
                game.load_zombies(character)
                if boss_spawned and boss and not boss.is_dead:
                    game.load_boss(boss, character)
                    for bullet in game.bullets[:]:
                        if boss.get_rect().colliderect(bullet.get_rect()):
                            boss.take_damage(bullet.damage)
                            game.bullets.remove(bullet)
                    game.char_check_boss_collision(character, boss, pygame.time.get_ticks())
                
                game.update_bullets()
                game.draw_bullets()
            
            game.clock.tick(60)
            pygame.display.flip()
    else:
        menu.draw()

pygame.quit()