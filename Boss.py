import pygame
import random
from Entity import Entity

class Boss(Entity):
    def __init__(self, map_width, map_height, objects):
        super().__init__()
        self.boss_frame_list = []

        # Load sprite sheet boss
        try:
            sprite_sheet = pygame.image.load("zombie/ZombieShooter/Sprites/Zombie/Zombie_Boss.png").convert_alpha()
        except FileNotFoundError:
            print("Gambar Boss tidak ditemukan, pakai gambar default!")
            sprite_sheet = pygame.Surface((64, 64))  # Ganti dengan surface kosong kalau gagal
        frame_width, frame_height = 64, 64

        # Potong frame
        for y in range(sprite_sheet.get_height() // frame_height):
            for x in range(sprite_sheet.get_width() // frame_width):
                frame = sprite_sheet.subsurface((x * frame_width, y * frame_height, frame_width, frame_height))
                self.boss_frame_list.append(frame)

        self.scale = 128
        self.image = pygame.transform.scale(self.boss_frame_list[0], (self.scale, self.scale))

        # Spawn random posisi valid tanpa tabrakan sama objek
        valid_position = False
        while not valid_position:
            self.rect = self.image.get_rect(center=(
                random.randint(0, map_width - self.scale),
                random.randint(0, map_height - self.scale)
            ))
            valid_position = True
            for obj_rect in objects:
                if self.rect.colliderect(obj_rect):
                    valid_position = False
                    break

        self.speed = 2
        self.hp = 5000
        self.max_hp = 5000
        self.damage = 2500 / 60
        self.is_dead = False
        self.attack_range = 80
        self.attack_cooldown = 1000
        self.last_attack_time = 0

    def idling(self, frame_index):
        frame = self.boss_frame_list[(frame_index // 7) % 4]
        self.image = pygame.transform.scale(frame, (self.scale, self.scale))

    def move_towards_player(self, game, player_rect, frame_index):
        if not isinstance(player_rect, pygame.Rect):
            raise ValueError("player_rect must be a pygame.Rect object")
        
        # Calculate direction vector to player
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = max(1, (dx**2 + dy**2)**0.5)
        move_x = (dx / distance) * self.speed
        move_y = (dy / distance) * self.speed
        
        # Store previous position
        tmp = self.rect.copy()
        
        # Try moving in both directions
        self.rect.x += move_x
        self.rect.y += move_y
        collided = False
        blocking_obj = None
        if hasattr(game, 'objects'):
            for obj_rect in game.objects:
                if self.rect.colliderect(obj_rect):
                    collided = True
                    blocking_obj = obj_rect
                    break
        else:
            raise AttributeError("game must have an 'objects' attribute")
        
        if collided:
            self.rect = tmp  # Revert to original position
            # Determine if obstacle is primarily above, below, left, or right
            obj_center_x, obj_center_y = blocking_obj.center
            relative_x = obj_center_x - self.rect.centerx
            relative_y = obj_center_y - self.rect.centery
            
            # Prioritize movement based on player position and obstacle location
            if abs(relative_x) > abs(relative_y):  # Obstacle is more left/right
                # Prefer y movement (up/down)
                preferred_y = self.speed if dy > 0 else -self.speed  # Move toward player
                self.rect.y += preferred_y
                for obj_rect in game.objects:
                    if self.rect.colliderect(obj_rect):
                        self.rect.y = tmp.y
                        # Try opposite y direction
                        self.rect.y += -preferred_y
                        for obj_rect in game.objects:
                            if self.rect.colliderect(obj_rect):
                                self.rect.y = tmp.y
                                break
                self.rect.x = tmp.x  # Keep x unchanged
            else:  # Obstacle is more above/below
                # Prefer x movement (left/right)
                preferred_x = self.speed if dx > 0 else -self.speed  # Move toward player
                self.rect.x += preferred_x
                for obj_rect in game.objects:
                    if self.rect.colliderect(obj_rect):
                        self.rect.x = tmp.x
                        # Try opposite x direction
                        self.rect.x += -preferred_x
                        for obj_rect in game.objects:
                            if self.rect.colliderect(obj_rect):
                                self.rect.x = tmp.x
                                break
                self.rect.y = tmp.y  # Keep y unchanged
        
        # Restrict to map bounds
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(game.map_width, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(game.map_height, self.rect.bottom)
        
        # Update animation
        if self.rect.x != tmp.x or self.rect.y != tmp.y:
            frame_num = (frame_index // 7) % len(self.boss_frame_list)
            frame = self.boss_frame_list[frame_num]
            self.image = pygame.transform.scale(frame, (self.scale, self.scale))

    def attack_player(self, player, current_time):
        # Use getter method for player's rect to support encapsulation
        player_rect = player.get_rect()
        distance = ((player_rect.centerx - self.rect.centerx) ** 2 +
                    (player_rect.centery - self.rect.centery) ** 2) ** 0.5
        if distance <= self.attack_range:
            if current_time - self.last_attack_time >= self.attack_cooldown:
                player.set_hp(player.get_hp() - self.damage)  # Use setter for HP
                self.last_attack_time = current_time

    def take_damage(self, amount, game=None, player=None, current_time=None):
        self.hp -= amount
        if self.hp <= 0:
            self.is_dead = True

    #Enkapsulasi
    def get_hp(self):
        return self.hp

    def set_hp(self, value):
        self.hp = max(0, min(value, self.max_hp))

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect

    def move_towards(self, game, player_rect, frame_index):
        self.move_towards_player(game, player_rect, frame_index)