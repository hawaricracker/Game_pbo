# test_main_run.py

import unittest
import pygame
import os
from Game import Game
from Character import Character
from Zombies import Zombie
from MainMenu import MainMenu
from Weapon import Weapon
from Bullet import Bullet

# Agar pygame tidak membuka GUI di GitHub/Linux
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((800, 600))

class TestFullGameRun(unittest.TestCase):
    def test_run_main_loop_simulation(self):
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()

        game = Game(WIDTH, HEIGHT)
        character = Character()

        # Tambahkan 5 zombie (bukan 50, agar test lebih cepat)
        for _ in range(5):
            zombie = Zombie(game.map_width, game.map_height)
            game.zombies.append(zombie)

        # Simulasi input: gerak kanan dan tembak mouse
        keys = {
            pygame.K_d: True,  # tekan 'D'
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_a: False
        }

        # Simulasi mouse klik kiri ke arah kanan bawah
        mouse_pressed = True
        mouse_pos = (character.Character_rect.centerx + 100, character.Character_rect.centery + 100)
        player_pos = character.Character_rect.center
        target_pos = (mouse_pos[0] - game.offset_x, mouse_pos[1] - game.offset_y)

        # Gerakan karakter
        character.move_right(game)
        game.animation(character)

        # Fire
        bullet = character.weapon.fire(player_pos, target_pos)
        if bullet:
            game.bullets.append(bullet)

        # Update semua
        game.update_bullets()
        for z in game.zombies:
            z.move_towards_player(game, character.Character_rect, game.frame_index)

        # Simulasi draw tanpa benar-benar menggambar ke layar
        try:
            game.load_char(screen, character)
            game.draw_health_bar(character.hp, character.max_hp, character)
            game.draw_bullets()
        except Exception as e:
            self.fail(f"Rendering simulation failed: {e}")

        self.assertTrue(character.Character_rect.x > 100, "Karakter harus bergerak ke kanan")
        self.assertGreaterEqual(len(game.bullets), 0, "Bullet list tidak boleh error")
        self.assertEqual(len(game.zombies), 5, "Zombie harus terload semua")
        
    def test_character_collision_with_house(self):
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        game = Game(WIDTH, HEIGHT)
        character = Character()

        # Buat rumah dummy (objek persegi panjang)
        house_rect = pygame.Rect(character.Character_rect.x + 20, character.Character_rect.y, 50, 50)
        game.objects = [house_rect]

        # Simulasikan gerakan ke kanan — akan tabrak rumah
        old_rect = character.Character_rect.copy()
        character.move_right(game)  # ini akan trigger check_house_collision()

        # Harusnya posisi karakter dikembalikan ke old_rect
        self.assertEqual(character.Character_rect, old_rect, "Karakter seharusnya tidak bisa menembus rumah.")

        # Selain itu, akselerasi harus jadi 0 setelah tabrakan
        self.assertEqual(character.acceleration, 0, "Akselerasi harus nol jika karakter menabrak objek.")


if __name__ == "__main__":
    unittest.main()
