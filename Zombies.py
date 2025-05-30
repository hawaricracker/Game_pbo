import pygame
import random
from Entity import Entity

class Zombie(Entity):
    def __init__(self, map_width, map_height, objects):
        pygame.sprite.Sprite.__init__(self)
        self.zombie_frame_list = []
        
        self.image = pygame.image.load("zombie/ZombieShooter/Sprites/Zombie/Zombie.png")
        for y in range(self.image.get_height() // 32):
            for x in range(self.image.get_width() // 32):
                frame = self.image.subsurface((x * 32, y * 32, 32, 32))
                self.zombie_frame_list.append(frame)

        self.image = self.zombie_frame_list[0]
        
        # Set random spawn position with collision check
        valid_position = False
        while not valid_position:
            self.rect = self.image.get_rect(topleft=(
                random.randint(0, map_width - self.image.get_width()),
                random.randint(0, map_height - self.image.get_height())
            ))
            valid_position = True
            # Periksa apakah rect zombie bertabrakan dengan objects
            for obj_rect in objects:
                if self.rect.colliderect(obj_rect):
                    valid_position = False
                    break
        
        self.speed = [0, 0]
        self.acceleration = 0.75
        self.scale = 50
        self.idling(0)
        self.dmg = 10 / 60
        self.speed = 3
        self.hp = 100
        self.max_hp = 100

    def idling(self, frame_index):
        self.image = self.zombie_frame_list[(frame_index // 7) % 4]
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))

    def move_towards_player(self, game, player_rect, frame_index):
        # Calculate direction vector to player
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        # Calculate distance to avoid division by zero
        distance = max(1, (dx**2 + dy**2)**0.5)
        # Normalize direction and apply speed
        move_x = (dx / distance) * self.speed
        move_y = (dy / distance) * self.speed
        
        # Store previous position for collision handling
        tmp = self.rect.copy()
        # Update position
        self.rect.x += move_x
        self.rect.y += move_y
        
        # Restrict to map bounds
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(game.map_width, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(game.map_height, self.rect.bottom)
        
        # Check collision with houses
        for obj_rect in game.objects:
            if self.rect.colliderect(obj_rect):
                self.rect = tmp
                break
        
        # Check collision with other zombies
        self.check_zombie_collision(game, game.zombies)

        if move_x != 0 and move_y != 0:
            self.image = self.zombie_frame_list[((frame_index // 7) % 6) + 4]
            self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
    
    def move_towards(self, game, player_rect, frame_index):
        self.move_towards_player(game, player_rect, frame_index)
    
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
    
    def get_hp(self):
        return self.hp

    def set_hp(self, value):
        self.hp = max(0, min(value, self.max_hp))

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect

    def check_zombie_collision(self, game, zombies):
        for other_zombie in zombies:
            if other_zombie != self and self.rect.colliderect(other_zombie.rect):
                # Store current position before pushing
                tmp = self.rect.copy()
                # Calculate push direction
                dx = self.rect.centerx - other_zombie.rect.centerx
                dy = self.rect.centery - other_zombie.rect.centery
                distance = max(1, (dx**2 + dy**2)**0.5)
                # Normalize and apply reduced push strength
                push_x = (dx / distance) * 1
                push_y = (dy / distance) * 1
                # Move this zombie away from the other
                self.rect.x += push_x
                self.rect.y += push_y
                # Ensure zombie stays within map bounds
                self.rect.left = max(0, self.rect.left)
                self.rect.right = min(game.map_width, self.rect.right)
                self.rect.top = max(0, self.rect.top)
                self.rect.bottom = min(game.map_height, self.rect.bottom)
                # Check collision with map objects after pushing
                for obj_rect in game.objects:
                    if self.rect.colliderect(obj_rect):
                        self.rect = tmp  # Revert to original position if collision occurs
                        break