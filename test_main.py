# test_game.py

import unittest
import pygame
import time
from unittest.mock import patch, Mock
from Character import Character
from Weapon import Weapon
from Bullet import Bullet
from Game import Game
from MainMenu import MainMenu
from Zombies import Zombie

pygame.init()

class TestGameComponents(unittest.TestCase):
    def setUp(self):
        self.screen_width = 800
        self.screen_height = 600
        self.game = Game(self.screen_width, self.screen_height)

    def test_bullet_trajectory_and_update(self):
        bullet = Bullet((0, 0), (100, 0), 10)
        initial_x = bullet.x
        bullet.update()
        self.assertGreater(bullet.x, initial_x, "Bullet should move to the right.")

    def test_weapon_fire_cooldown(self):
        weapon = Weapon()
        bullet = weapon.fire((0, 0), (100, 100))
        self.assertIsInstance(bullet, Bullet)
        bullet2 = weapon.fire((0, 0), (100, 100))
        self.assertIsNone(bullet2, "Weapon should respect fire_rate cooldown.")

    def test_character_initial_hp_and_movement(self):
        character = Character()
        old_pos = character.Character_rect.copy()
        character.move_right(self.game)
        self.assertGreater(character.Character_rect.x, old_pos.x, "Character should move right.")
        self.assertEqual(character.hp, 100)
        self.assertEqual(character.max_hp, 100)

    def test_game_offset_calculation(self):
        character = Character()
        self.game.load_map(self.game.screen, "test.tmx", character)
        offset_expected = self.screen_width // 2 - character.Character_rect.centerx
        self.assertEqual(self.game.offset_x, offset_expected)

    def test_zombie_moves_towards_player(self):
        character = Character()
        zombie = Zombie(1000, 1000)
        old_pos = zombie.rect.copy()
        zombie.move_towards_player(self.game, character.Character_rect, 0)
        self.assertNotEqual((old_pos.x, old_pos.y), (zombie.rect.x, zombie.rect.y))

    def test_main_menu_exit_event(self):
        menu = MainMenu(self.screen_width, self.screen_height)
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
        result = menu.handle_event(event)
        self.assertEqual(result, "exit")

    def test_draw_health_bar_values(self):
        character = Character()
        try:
            self.game.draw_health_bar(character.hp, character.max_hp, character)
        except Exception as e:
            self.fail(f"draw_health_bar() raised Exception unexpectedly: {e}")

    def test_update_bullets_removal_out_of_bounds(self):
        bullet = Bullet((self.game.map_width + 100, self.game.map_height + 100), (0, 0), 10)
        self.game.bullets.append(bullet)
        self.game.update_bullets()
        self.assertEqual(len(self.game.bullets), 0, "Out-of-bounds bullets should be removed")

if __name__ == "__main__":
    unittest.main()
