import pygame
import random

class Zombie(pygame.sprite.Sprite):
    def __init__(self, map_width, map_height):
        pygame.sprite.Sprite.__init__(self)
        self.zombie_frame_list = []
        
        self.image = pygame.image.load("zombie/ZombieShooter/Sprites/Zombie/Zombie.png")
        for y in range(self.image.get_height() // 32):
            for x in range(self.image.get_width() // 32):
                frame = self.image.subsurface((x * 32, y * 32, 32, 32))
                self.zombie_frame_list.append(frame)

        self.image = self.zombie_frame_list[0]
        # Set random spawn position in world coordinates
        self.rect = self.image.get_rect(topleft=(
            random.randint(0, map_width - self.image.get_width()),
            random.randint(0, map_height - self.image.get_height())
        ))
        self.speed = [0, 0]
        self.acceleration = 0.75
        self.scale = 50
        self.idling(0)  # Initialize with idle animation
        self.dmg = 5 / 60
        self.speed = 3

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

        if move_x != 0 and move_y != 0:
            self.image = self.zombie_frame_list[((frame_index // 7) % 6) + 4]
            self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
