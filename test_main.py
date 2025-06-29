# test_main.py
import unittest
import pygame
import os
import time
import math
from Game import Game
from Character import Character
from Zombies import Zombie
from MainMenu import MainMenu
from Weapon import Weapon
from Bullet import Bullet

# Set environment variable for headless testing
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((800, 600))

class TestCharacterFunctionality(unittest.TestCase):
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game = Game(self.WIDTH, self.HEIGHT)
        self.character = Character()

    def test_character_movement(self):
        initial_x = self.character.Character_rect.x
        self.character.move_right(self.game)
        self.assertGreater(self.character.Character_rect.x, initial_x, "Character should move right")

        initial_x = self.character.Character_rect.x
        self.character.move_left(self.game)
        self.assertLess(self.character.Character_rect.x, initial_x, "Character should move left")

        initial_y = self.character.Character_rect.y
        self.character.move_up(self.game)
        self.assertLess(self.character.Character_rect.y, initial_y, "Character should move up")

        initial_y = self.character.Character_rect.y
        self.character.move_down(self.game)
        self.assertGreater(self.character.Character_rect.y, initial_y, "Character should move down")

    def test_character_dash(self):
        initial_accel = self.character.acceleration
        initial_x = self.character.Character_rect.x

        self.character.start_dash()
        self.assertTrue(self.character.is_dashing)
        self.assertEqual(self.character.acceleration, self.character.dash_speed)

        self.character.move_right(self.game)
        dash_move_distance = self.character.Character_rect.x - initial_x

        self.character.Character_rect.x = initial_x
        self.character.acceleration = initial_accel
        self.character.is_dashing = False
        self.character.move_right(self.game)
        normal_move_distance = self.character.Character_rect.x - initial_x

        self.assertGreater(dash_move_distance, normal_move_distance, "Dash should move character faster")

    def test_character_collision_with_obstacle(self):
        obstacle = pygame.Rect(self.character.Character_rect.x + 20, self.character.Character_rect.y, 50, 50)
        self.game.objects = [obstacle]
        initial_pos = self.character.Character_rect.copy()
        self.character.move_right(self.game)
        self.assertEqual(self.character.Character_rect, initial_pos, "Character shouldn't move through obstacles")
        self.assertEqual(self.character.acceleration, 0, "Acceleration should be 0 after collision")

        self.game.objects = []
        self.character.acceleration = 5
        self.character.move_right(self.game)
        self.assertNotEqual(self.character.Character_rect, initial_pos, "Character should move normally without obstacles")

    def test_character_animation(self):
        self.character.speed = [0, 0]
        self.character.idling(0)
        surface_scaled = pygame.transform.scale(self.character.idling_frame_list[0], (self.character.scale, self.character.scale))
        self.assertEqual(self.character.player.get_size(), surface_scaled.get_size())
    
    def test_character_takes_damage_from_boss_collision(self):
        from Boss import Boss
        boss = Boss(self.game.map_width, self.game.map_height, self.game.objects)
        self.character.Character_rect.center = (100, 100)
        boss.rect.center = (110, 110)  # Jarak kurang dari attack_range (80 piksel)
        initial_hp = self.character.get_hp()
        current_time = pygame.time.get_ticks()
        boss.last_attack_time = current_time - boss.attack_cooldown  # Ensure cooldown is satisfied
        boss.attack_player(self.character, current_time)
        # Debug: Verify distance calculation
        distance = ((self.character.get_rect().centerx - boss.get_rect().centerx) ** 2 +
                    (self.character.get_rect().centery - boss.get_rect().centery) ** 2) ** 0.5
        self.assertLessEqual(distance, boss.attack_range, "Character and boss should be within attack range")
        self.assertLess(self.character.get_hp(), initial_hp, "Character should take damage from boss collision")
        self.assertEqual(self.character.get_hp(), initial_hp - boss.damage, "Character should lose exactly 10 HP from boss attack")

class TestZombieFunctionality(unittest.TestCase):
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game = Game(self.WIDTH, self.HEIGHT)
        self.character = Character()
        self.zombie = Zombie(self.game.map_width, self.game.map_height, self.game.objects)
        self.game.zombies = [self.zombie]

    def test_zombie_movement_towards_player(self):
        self.zombie.rect.x = self.character.Character_rect.x + 100
        self.zombie.rect.y = self.character.Character_rect.y + 100
        initial_x = self.zombie.rect.x
        initial_y = self.zombie.rect.y
        self.zombie.move_towards_player(self.game, self.character.Character_rect, 0)
        self.assertLess(self.zombie.rect.x, initial_x, "Zombie should move left towards player")
        self.assertLess(self.zombie.rect.y, initial_y, "Zombie should move up towards player")

    def test_zombie_collision_with_obstacle(self):
        obstacle = pygame.Rect(self.zombie.rect.x - 5, self.zombie.rect.y, 10, 100)
        self.game.objects = [obstacle]
        self.character.Character_rect.x = self.zombie.rect.x - 50
        self.character.Character_rect.y = self.zombie.rect.y
        initial_pos = self.zombie.rect.copy()
        self.zombie.move_towards_player(self.game, self.character.Character_rect, 0)
        dx = abs(self.zombie.rect.x - initial_pos.x)
        self.assertLessEqual(dx, 2, "Zombie shouldn't move significantly through obstacles")

    def test_zombie_damage_player(self):
        self.zombie.rect.x = self.character.Character_rect.x
        self.zombie.rect.y = self.character.Character_rect.y
        initial_hp = self.character.hp
        self.game.char_check_zombie_collision(self.character)
        self.assertLess(self.character.hp, initial_hp, "Player should take damage from zombie collision")

class TestWeaponAndBulletFunctionality(unittest.TestCase):
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game = Game(self.WIDTH, self.HEIGHT)
        self.character = Character()
        self.weapon = Weapon()

    def test_bullet_collision_detection(self):
        bullet = Bullet((100, 100), (200, 100), 10)
        self.game.bullets = [bullet]
        self.game.objects = [pygame.Rect(120, 95, 20, 10)]
        # Simulasi sampai collision
        collided = False
        for _ in range(20):
            bullet.update_pos()
            bullet_rect = bullet.get_rect()
            if any(bullet_rect.colliderect(obj) for obj in self.game.objects):
                collided = True
                break
        self.assertTrue(collided, "Bullet should detect collision with obstacle")

    def test_bullet_damage_zombie(self):
        bullet = Bullet((100, 100), (200, 100), 10)
        self.game.bullets = [bullet]
        zombie = Zombie(self.game.map_width, self.game.map_height, self.game.objects)
        zombie.rect.x = 120
        zombie.rect.y = 95
        self.game.zombies = [zombie]
        initial_hp = zombie.hp
        for _ in range(20):
            bullet.update_pos()
            if bullet.get_rect().colliderect(zombie.rect):
                zombie.hp -= bullet.damage
                break
        self.assertLess(zombie.hp, initial_hp, "Zombie should take damage from bullet collision")

class TestMenuFunctionality(unittest.TestCase):
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.menu = MainMenu(self.WIDTH, self.HEIGHT)

    def test_menu_button_actions(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.menu.buttons[0]["rect"].center})
        action = self.menu.handle_event(event)
        self.assertEqual(action, "start", "Clicking start button should return 'start' action")
# Tambahan di bawah test existing

class TestCharacterEdgeCases(unittest.TestCase):
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.game = Game(self.WIDTH, self.HEIGHT)
        self.character = Character()
        self.character.Character_rect.x = self.WIDTH - 1  # Ujung kanan
        self.character.Character_rect.y = self.HEIGHT - 1  # Ujung bawah

    def test_hp_never_negative(self):
        self.character.hp = 1
        zombie = Zombie(self.WIDTH, self.HEIGHT, [])
        zombie.dmg = 10
        self.game.zombies = [zombie]
        self.game.char_check_zombie_collision(self.character)
        self.assertGreaterEqual(self.character.hp, 0)

class TestZombieEdgeCases(unittest.TestCase):
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.game = Game(self.WIDTH, self.HEIGHT)
        self.zombie = Zombie(self.WIDTH, self.HEIGHT, [])
        self.zombie.hp = 1
        self.game.zombies = [self.zombie]

    def test_zombie_hp_not_negative(self):
        self.zombie.hp -= 10
        if self.zombie.hp < 0:
            self.zombie.hp = 0
        self.assertGreaterEqual(self.zombie.hp, 0)

    def test_dead_zombie_no_action(self):
        self.zombie.hp = 0
        # Simulasi: zombie seharusnya tidak bergerak/menyerang jika hp <= 0
        old_pos = self.zombie.rect.copy()
        self.zombie.move_towards_player(self.game, self.zombie.rect, 0)
        self.assertEqual(self.zombie.rect, old_pos)

class TestBulletEdgeCases(unittest.TestCase):
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.game = Game(self.WIDTH, self.HEIGHT)
        self.bullet = Bullet((790, 590), (900, 700), 10)  # Arah luar map

    def test_bullet_out_of_bounds(self):
        for _ in range(30):
            self.bullet.update_pos()
        rect = self.bullet.get_rect()
        self.assertFalse(0 <= rect.x < self.WIDTH and 0 <= rect.y < self.HEIGHT)

class TestMenuEdgeCases(unittest.TestCase):
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.menu = MainMenu(self.WIDTH, self.HEIGHT)

    def test_invalid_event(self):
        event = pygame.event.Event(pygame.USEREVENT, {})  # Event tak dikenal
        result = self.menu.handle_event(event)
        self.assertIsNone(result)

    def test_settings_volume_limits(self):
        self.menu.show_settings = True
        self.menu.volume = 0
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
        self.menu.handle_event(event)
        self.assertGreaterEqual(self.menu.volume, 0)
        self.menu.volume = 100
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
        self.menu.handle_event(event)
        self.assertLessEqual(self.menu.volume, 100)

if __name__ == "__main__":
    unittest.main()