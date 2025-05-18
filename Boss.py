import pygame
import random

class Boss(pygame.sprite.Sprite):
    def __init__(self, map_width, map_height, objects):
        super().__init__()
        self.boss_frame_list = []

        # Load sprite sheet boss
        sprite_sheet = pygame.image.load("zombie/ZombieShooter/Sprites/Zombie/Zombie_Boss.png").convert_alpha()
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
        self.damage = 25 / 60
        self.is_dead = False

        self.attack_range = 80
        self.attack_cooldown = 1000
        self.last_attack_time = 0

    def idling(self, frame_index):
        frame = self.boss_frame_list[(frame_index // 7) % 4]
        self.image = pygame.transform.scale(frame, (self.scale, self.scale))

    def move_towards_player(self, game, player_rect, frame_index):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = max(1, (dx**2 + dy**2)**0.5)

        move_x = int((dx / distance) * self.speed)
        move_y = int((dy / distance) * self.speed)

        tmp = self.rect.copy()
        self.rect.x += move_x
        self.rect.y += move_y

        # Batas peta
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(game.map_width, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(game.map_height, self.rect.bottom)

        # Cek tabrakan objek
        for obj_rect in game.objects:
            if self.rect.colliderect(obj_rect):
                self.rect = tmp
                break
                


        # Animasi berjalan (frame 0-? sesuai sprite)
        frame_num = (frame_index // 7) % len(self.boss_frame_list)
        frame = self.boss_frame_list[frame_num]
        self.image = pygame.transform.scale(frame, (self.scale, self.scale))

    def attack_player(self, player, current_time):
        distance = ((player.rect.centerx - self.rect.centerx) ** 2 +
                    (player.rect.centery - self.rect.centery) ** 2) ** 0.5
        if distance <= self.attack_range:
            if current_time - self.last_attack_time >= self.attack_cooldown:
                player.hp -= 10
                self.last_attack_time = current_time

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.is_dead = True

    def update(self, game, player, frame_index):
        self.move_towards_player(game, player.rect, frame_index)
        current_time = pygame.time.get_ticks()
        self.attack_player(player, current_time)

        for bullet in game.bullets[:]:
            if self.rect.colliderect(bullet.get_rect()):
                self.take_damage(bullet.damage)
                game.bullets.remove(bullet)

        if self.is_dead:
            # Bisa tambahkan animasi mati
            pass
