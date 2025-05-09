# test_main.py

import unittest
import pygame
from Character import Character
from Weapon import Weapon
from Bullet import Bullet
from Zombies import Zombie
from Game import Game
from MainMenu import MainMenu

pygame.init()
WIDTH, HEIGHT = 800, 600  # ukuran default untuk pengujian

class TestZombieShooter(unittest.TestCase):

    def test_character_initialization(self):
        character = Character()
        self.assertIsNotNone(character.Character_rect)
        self.assertIsInstance(character.weapon, Weapon)

    def test_weapon_fire_rate(self):
        weapon = Weapon()
        bullet1 = weapon.fire((0, 0), (100, 100))
        self.assertIsInstance(bullet1, Bullet)
        bullet2 = weapon.fire((0, 0), (100, 100))
        self.assertIsNone(bullet2)  # terlalu cepat menembak lagi

    def test_bullet_movement(self):
        bullet = Bullet((0, 0), (100, 0), 10)
        initial_pos = bullet.pos[:]
        bullet.move()
        self.assertNotEqual(initial_pos, bullet.pos)

    def test_zombie_spawn(self):
        zombie = Zombie(1000, 1000)
        self.assertGreaterEqual(zombie.rect.x, 0)
        self.assertLessEqual(zombie.rect.x, 1000)

    def test_main_menu_click_exit(self):
        menu = MainMenu(WIDTH, HEIGHT)
        fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
        result = menu.handle_event(fake_event)
        self.assertEqual(result, "exit")

    def test_game_initialization(self):
        game = Game(WIDTH, HEIGHT)
        self.assertEqual(game.map_width, 1000)  # nilai default dari Game.py
        self.assertEqual(game.map_height, 1000)

if __name__ == "__main__":
    unittest.main()
