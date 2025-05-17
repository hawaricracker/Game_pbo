# Fixed test_main.py
import unittest
import pygame
import os
import time
from Game import Game
from Character import Character
from Zombies import Zombie
from MainMenu import MainMenu
from Weapon import Weapon
from Bullet import Bullet

# Setup dummy video driver for headless testing
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((800, 600))

class TestCharacterFunctionality(unittest.TestCase):
    def setUp(self):
        self.game = Game(800, 600)
        self.character = Character()

    def test_character_movement(self):
        pos = self.character.Character_rect.x
        self.character.move_right(self.game)
        self.assertGreater(self.character.Character_rect.x, pos)

    def test_character_dash(self):
        self.character.start_dash()
        self.assertTrue(self.character.is_dashing)

    def test_character_collision_with_obstacle(self):
        obstacle = pygame.Rect(self.character.Character_rect.x + 20, self.character.Character_rect.y, 50, 50)
        self.game.objects = [obstacle]
        old_rect = self.character.Character_rect.copy()
        self.character.move_right(self.game)
        self.assertEqual(self.character.Character_rect, old_rect)

    def test_character_animation(self):
        self.character.idling(0)
        self.assertIsNotNone(self.character.player)


class TestZombieFunctionality(unittest.TestCase):
    def setUp(self):
        self.game = Game(800, 600)
        self.character = Character()
        self.zombie = Zombie(self.game.map_width, self.game.map_height, self.game.objects)
        self.game.zombies = [self.zombie]

    def test_zombie_collision_with_obstacle(self):
        obstacle = pygame.Rect(self.zombie.rect.x - 5, self.zombie.rect.y, 10, 100)
        self.game.objects = [obstacle]
        self.character.Character_rect.x = self.zombie.rect.x - 50
        old_pos = self.zombie.rect.copy()
        self.zombie.move_towards_player(self.game, self.character.Character_rect, 0)
        self.assertEqual(self.zombie.rect, old_pos)

    def test_zombie_damage_player(self):
        self.zombie.rect = self.character.Character_rect.copy()
        old_hp = self.character.hp
        self.game.char_check_zombie_collision(self.character)
        self.assertLess(self.character.hp, old_hp)


class TestWeaponAndBulletFunctionality(unittest.TestCase):
    def setUp(self):
        self.game = Game(800, 600)
        self.weapon = Weapon()
        self.character = Character()

    def test_bullet_collision_detection(self):
        bullet = Bullet((100, 100), (200, 100), 10)
        self.game.bullets = [bullet]
        self.game.objects = [pygame.Rect(150, 95, 20, 10)]
        bullet.update_pos()
        rect = bullet.get_rect()
        collided = rect.colliderect(self.game.objects[0])
        self.assertTrue(collided)

    def test_bullet_damage_zombie(self):
        bullet = Bullet((100, 100), (200, 100), 10)
        self.game.bullets = [bullet]
        zombie = Zombie(self.game.map_width, self.game.map_height, [])
        zombie.rect.x = 150
        zombie.rect.y = 95
        self.game.zombies = [zombie]
        bullet.update_pos()
        if bullet.get_rect().colliderect(zombie.rect):
            zombie.hp -= bullet.damage
        self.assertLess(zombie.hp, 100)


class TestMenuFunctionality(unittest.TestCase):
    def setUp(self):
        self.menu = MainMenu(800, 600)

    def test_menu_button_actions(self):
        start_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.menu.buttons[0]['rect'].center})
        self.assertEqual(self.menu.handle_event(start_event), 'start')


if __name__ == '__main__':
    unittest.main()
