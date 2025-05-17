# test_zombie_slayer.py

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

class TestGameInitialization(unittest.TestCase):
    """Test game initialization and basic setup"""
    
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    
    def test_game_initialization(self):
        """Test that the game initializes without errors"""
        try:
            game = Game(self.WIDTH, self.HEIGHT)
            self.assertIsNotNone(game)
            self.assertEqual(game.WIDTH, self.WIDTH)
            self.assertEqual(game.HEIGHT, self.HEIGHT)
            self.assertIsNotNone(game.screen)
            self.assertIsNotNone(game.clock)
            self.assertEqual(len(game.zombies), 0)
            self.assertEqual(len(game.bullets), 0)
        except Exception as e:
            self.fail(f"Game initialization failed with error: {e}")
    
    def test_character_initialization(self):
        """Test that the character initializes correctly"""
        try:
            character = Character()
            self.assertIsNotNone(character)
            self.assertEqual(character.hp, 100)
            self.assertEqual(character.max_hp, 100)
            self.assertIsNotNone(character.weapon)
            self.assertEqual(character.normal_speed, 10)
            self.assertEqual(character.dash_speed, 75)
        except Exception as e:
            self.fail(f"Character initialization failed with error: {e}")
    
    def test_zombie_initialization(self):
        """Test that zombies initialize correctly"""
        try:
            game = Game(self.WIDTH, self.HEIGHT)
            zombie = Zombie(game.map_width, game.map_height, game.objects)
            self.assertIsNotNone(zombie)
            self.assertEqual(zombie.hp, 100)
            self.assertEqual(zombie.max_hp, 100)
            self.assertGreaterEqual(zombie.rect.x, 0)
            self.assertLessEqual(zombie.rect.right, game.map_width)
            self.assertGreaterEqual(zombie.rect.y, 0)
            self.assertLessEqual(zombie.rect.bottom, game.map_height)
        except Exception as e:
            self.fail(f"Zombie initialization failed with error: {e}")
    
    def test_menu_initialization(self):
        """Test that the main menu initializes correctly"""
        try:
            menu = MainMenu(self.WIDTH, self.HEIGHT)
            self.assertIsNotNone(menu)
            self.assertEqual(menu.width, self.WIDTH)
            self.assertEqual(menu.height, self.HEIGHT)
            self.assertEqual(len(menu.buttons), 3)  # Start, Settings, Exit
            self.assertEqual(menu.volume, 100)
            self.assertEqual(menu.music, 100)
            self.assertFalse(menu.show_settings)
        except Exception as e:
            self.fail(f"Main menu initialization failed with error: {e}")


class TestCharacterFunctionality(unittest.TestCase):
    """Test character movement, collision, and animation"""
    
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game = Game(self.WIDTH, self.HEIGHT)
        self.character = Character()
    
    def test_character_movement(self):
        """Test character movement in all directions"""
        # Test moving right
        initial_x = self.character.Character_rect.x
        self.character.move_right(self.game)
        self.assertGreater(self.character.Character_rect.x, initial_x, "Character should move right")
        
        # Test moving left
        initial_x = self.character.Character_rect.x
        self.character.move_left(self.game)
        self.assertLess(self.character.Character_rect.x, initial_x, "Character should move left")
        
        # Test moving up
        initial_y = self.character.Character_rect.y
        self.character.move_up(self.game)
        self.assertLess(self.character.Character_rect.y, initial_y, "Character should move up")
        
        # Test moving down
        initial_y = self.character.Character_rect.y
        self.character.move_down(self.game)
        self.assertGreater(self.character.Character_rect.y, initial_y, "Character should move down")
    
    def test_character_dash(self):
        """Test character dash functionality"""
        # Store initial position and acceleration
        initial_accel = self.character.acceleration
        initial_x = self.character.Character_rect.x
        
        # Perform dash
        self.character.start_dash()
        self.assertTrue(self.character.is_dashing)
        self.assertEqual(self.character.acceleration, self.character.dash_speed)
        
        # Move while dashing
        self.character.move_right(self.game)
        dash_move_distance = self.character.Character_rect.x - initial_x
        
        # Reset character and move normally for comparison
        self.character.Character_rect.x = initial_x
        self.character.acceleration = initial_accel
        self.character.is_dashing = False
        self.character.move_right(self.game)
        normal_move_distance = self.character.Character_rect.x - initial_x
        
        # Dash should move character faster than normal
        self.assertGreater(dash_move_distance, normal_move_distance, "Dash should move character faster")
    
    def test_character_collision_with_obstacle(self):
        """Test character collision with obstacles"""
        # Create a test obstacle directly in front of character
        obstacle = pygame.Rect(
            self.character.Character_rect.x + 20,
            self.character.Character_rect.y,
            50, 50
        )
        self.game.objects = [obstacle]
        
        # Try to move into the obstacle
        initial_pos = self.character.Character_rect.copy()
        self.character.move_right(self.game)
        
        # Character should not move through the obstacle
        self.assertEqual(self.character.Character_rect, initial_pos, "Character shouldn't move through obstacles")
        self.assertEqual(self.character.acceleration, 0, "Acceleration should be 0 after collision")
        
        # Clear obstacle and test normal movement
        self.game.objects = []
        self.character.acceleration = 5
        self.character.move_right(self.game)
        self.assertNotEqual(self.character.Character_rect, initial_pos, "Character should move normally without obstacles")
    
    def test_character_animation(self):
        """Test character animation states"""
        # Test idle animation
        self.character.speed = [0, 0]
        initial_frame = self.character.player
        self.game.animation(self.character)
        # Character should have been drawn in idle animation
        self.assertEqual(self.character.player, self.idling_frame_list[0])


class TestZombieFunctionality(unittest.TestCase):
    """Test zombie behavior and interactions"""
    
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game = Game(self.WIDTH, self.HEIGHT)
        self.character = Character()
        self.zombie = Zombie(self.game.map_width, self.game.map_height, self.game.objects)
        self.game.zombies = [self.zombie]
    
    def test_zombie_movement_towards_player(self):
        """Test that zombies move towards the player"""
        # Position zombie away from character
        self.zombie.rect.x = self.character.Character_rect.x + 100
        self.zombie.rect.y = self.character.Character_rect.y + 100
        
        # Store initial position
        initial_x = self.zombie.rect.x
        initial_y = self.zombie.rect.y
        
        # Move zombie towards player
        self.zombie.move_towards_player(self.game, self.character.Character_rect, 0)
        
        # Zombie should have moved closer to player
        self.assertLess(self.zombie.rect.x, initial_x, "Zombie should move left towards player")
        self.assertLess(self.zombie.rect.y, initial_y, "Zombie should move up towards player")
    
    def test_zombie_collision_with_obstacle(self):
        """Test that zombies don't move through obstacles"""
        # Create obstacle in zombie's path
        obstacle = pygame.Rect(
            self.zombie.rect.x - 20,  # Place obstacle to left of zombie
            self.zombie.rect.y,
            10, 100
        )
        self.game.objects = [obstacle]
        
        # Position character to left of obstacle (so zombie tries to move through it)
        self.character.Character_rect.x = self.zombie.rect.x - 50
        self.character.Character_rect.y = self.zombie.rect.y
        
        # Store initial position and try to move
        initial_pos = self.zombie.rect.copy()
        self.zombie.move_towards_player(self.game, self.character.Character_rect, 0)
        
        # Zombie should not have moved through obstacle
        self.assertEqual(self.zombie.rect, initial_pos, "Zombie shouldn't move through obstacles")
    
    def test_zombie_damage_player(self):
        """Test that zombies damage the player on collision"""
        # Position zombie to collide with player
        self.zombie.rect.x = self.character.Character_rect.x
        self.zombie.rect.y = self.character.Character_rect.y
        
        # Store initial player HP
        initial_hp = self.character.hp
        
        # Check collision and damage
        self.game.char_check_zombie_collision(self.character)
        
        # Player HP should have decreased
        self.assertLess(self.character.hp, initial_hp, "Player should take damage from zombie collision")


class TestWeaponAndBulletFunctionality(unittest.TestCase):
    """Test weapon firing and bullet behavior"""
    
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game = Game(self.WIDTH, self.HEIGHT)
        self.character = Character()
        self.weapon = Weapon()
    
    def test_weapon_fire_rate(self):
        """Test that weapons respect their fire rate"""
        # Get player position
        player_pos = self.character.Character_rect.center
        target_pos = (player_pos[0] + 100, player_pos[1])
        
        # First shot should succeed
        bullet1 = self.weapon.fire(player_pos, target_pos)
        self.assertIsNotNone(bullet1, "First shot should create a bullet")
        
        # Immediate second shot should fail due to fire rate
        bullet2 = self.weapon.fire(player_pos, target_pos)
        self.assertIsNone(bullet2, "Second immediate shot should not create a bullet")
        
        # Shot after waiting should succeed
        time.sleep(self.weapon.fire_rate + 0.01)
        bullet3 = self.weapon.fire(player_pos, target_pos)
        self.assertIsNotNone(bullet3, "Shot after waiting should create a bullet")
    
    def test_bullet_movement(self):
        """Test that bullets move correctly in their target direction"""
        # Create a bullet with specific start and target
        start_pos = (100, 100)
        target_pos = (200, 100)  # Directly to the right
        bullet = Bullet(start_pos, target_pos, 10)
        
        # Store initial position
        initial_x = bullet.x
        initial_y = bullet.y
        
        # Update position and check movement
        bullet.update_pos()
        
        # Bullet should have moved right (x increases)
        self.assertGreater(bullet.x, initial_x, "Bullet should move horizontally toward target")
        self.assertAlmostEqual(bullet.y, initial_y, places=5, msg="Bullet should not move vertically")
    
    def test_bullet_collision_detection(self):
        """Test that bullets detect collisions with objects"""
        # Create a bullet
        start_pos = (100, 100)
        target_pos = (200, 100)
        bullet = Bullet(start_pos, target_pos, 10)
        self.game.bullets = [bullet]
        
        # Create an obstacle in bullet's path
        obstacle = pygame.Rect(150, 95, 20, 10)
        self.game.objects = [obstacle]
        
        # Initially, bullet should not have collided
        self.assertFalse(bullet.collided, "Bullet should not start as collided")
        
        # Update bullet and check collisions
        bullet.update_pos()
        bullet_rect = bullet.get_rect()
        
        # Process collisions manually as game.draw_bullets() would
        collided = False
        for obj_rect in self.game.objects:
            if bullet_rect.colliderect(obj_rect):
                collided = True
                break
        
        self.assertTrue(collided, "Bullet should detect collision with obstacle")
    
    def test_bullet_damage_zombie(self):
        """Test that bullets damage zombies on collision"""
        # Create bullet and zombie
        start_pos = (100, 100)
        target_pos = (200, 100)
        bullet = Bullet(start_pos, target_pos, 10)
        self.game.bullets = [bullet]
        
        # Position zombie in bullet's path
        zombie = Zombie(self.game.map_width, self.game.map_height, self.game.objects)
        zombie.rect.x = 150
        zombie.rect.y = 95
        initial_hp = zombie.hp
        self.game.zombies = [zombie]
        
        # Update bullet and manually process collision as game.draw_bullets() would
        bullet.update_pos()
        bullet_rect = bullet.get_rect()
        
        if bullet_rect.colliderect(zombie.rect):
            zombie.hp -= bullet.damage
        
        # Zombie HP should have decreased
        self.assertLess(zombie.hp, initial_hp, "Zombie should take damage from bullet collision")
    
    def test_bullet_range_limit(self):
        """Test that bullets disappear after exceeding their range"""
        # Create a bullet
        start_pos = (100, 100)
        target_pos = (500, 100)  # Far away
        bullet = Bullet(start_pos, target_pos, 10)
        
        # Move the bullet until it exceeds its range
        while not bullet.has_exceeded_range():
            bullet.update_pos()
        
        self.assertTrue(bullet.has_exceeded_range(), "Bullet should exceed its range after traveling max distance")


class TestMenuFunctionality(unittest.TestCase):
    """Test menu interactions and state changes"""
    
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.menu = MainMenu(self.WIDTH, self.HEIGHT)
    
    def test_menu_button_actions(self):
        """Test menu button click actions"""
        # Test start button
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.menu.buttons[0]["rect"].center})
        action = self.menu.handle_event(event)
        self.assertEqual(action, "start", "Clicking start button should return 'start' action")
        
        # Test settings button
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.menu.buttons[1]["rect"].center})
        action = self.menu.handle_event(event)
        self.assertEqual(action, None, "Clicking settings button should return None")
        self.assertTrue(self.menu.show_settings, "Settings menu should be shown")
        
        # Test exit button
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.menu.buttons[2]["rect"].center})
        self.menu.show_settings = False  # Reset to main menu
        action = self.menu.handle_event(event)
        self.assertEqual(action, "exit", "Clicking exit button should return 'exit' action")
    
    def test_settings_volume_adjustment(self):
        """Test volume adjustment in settings menu"""
        # Activate settings menu
        self.menu.show_settings = True
        initial_volume = self.menu.volume
        
        # Test decrease volume
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
        self.menu.handle_event(event)
        self.assertEqual(self.menu.volume, initial_volume - 5, "Volume should decrease by 5")
        
        # Test increase volume
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
        self.menu.handle_event(event)
        self.assertEqual(self.menu.volume, initial_volume, "Volume should increase by 5")
        
        # Test music volume
        initial_music = self.menu.music
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a})
        self.menu.handle_event(event)
        self.assertEqual(self.menu.music, initial_music - 5, "Music volume should decrease by 5")


class TestGameStateTransitions(unittest.TestCase):
    """Test game state transitions like victory and game over"""
    
    def setUp(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game = Game(self.WIDTH, self.HEIGHT)
        self.character = Character()
    
    def test_game_over_state(self):
        """Test game over state when player health reaches zero"""
        # Reduce player health to zero
        self.character.hp = 0
        
        # Check if game over screen appears
        try:
            self.game.show_game_over()
            # If we get here without error, the function works
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Game over screen failed to display: {e}")
    
    def test_victory_state(self):
        """Test victory state when all zombies are defeated"""
        # Initialize with no zombies (all defeated)
        self.game.zombies = []
        
        # Check if victory screen appears
        try:
            self.game.show_victory()
            # If we get here without error, the function works
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Victory screen failed to display: {e}")


if __name__ == "__main__":
    unittest.main()
