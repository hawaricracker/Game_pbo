import pygame
import math

class Bullet:
    def __init__(self, start_pos, target_pos, speed):
        self.x, self.y = start_pos
        dx, dy = target_pos[0] - self.x, target_pos[1] - self.y
        distance = math.hypot(dx, dy)
        self.vel_x = speed * dx / distance
        self.vel_y = speed * dy / distance
        self.damage = 10
        self.radius = 5
        self.color = (255, 255, 0)
        self.bullet = pygame.image.load("Asset/PNG/Bullet.png")
        self.bullet_frame_list = []
        self.frame_index = 0
        self.animation_speed = 1.2
        self.collided = False
        # Hitung sudut arah peluru (dalam derajat)
        self.angle = math.degrees(math.atan2(-dy, dx))  # Negatif dy untuk orientasi Pygame

        for y in range(self.bullet.get_height() // 16):
            for x in range(self.bullet.get_width() // 16):
                frame = self.bullet.subsurface((x * 16, y * 16, 16, 16))
                self.bullet_frame_list.append(frame)

    def update_pos(self):
        if not self.collided:  # Hanya update posisi jika belum menabrak
            self.x += self.vel_x
            self.y += self.vel_y
    
    def update_frame(self):
        if self.collided and self.frame_index == 0:  # Pastikan reset hanya sekali saat kolisi
            self.frame_index = 0
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.bullet_frame_list):
            self.frame_index = len(self.bullet_frame_list) - 1

    def draw_collision(self, screen, offset_x=0, offset_y=0):
        # Ambil frame saat ini
        current_frame = self.bullet_frame_list[int(self.frame_index)]
        current_frame = pygame.transform.scale(current_frame, (25, 25))
        # Rotasi frame sesuai sudut
        rotated_frame = pygame.transform.rotate(current_frame, self.angle)
        # Hitung posisi untuk memusatkan frame yang telah dirotasi
        rotated_rect = rotated_frame.get_rect(center=(self.x + offset_x, self.y + offset_y))
        # Gambar frame yang dirotasi
        screen.blit(rotated_frame, rotated_rect.topleft)
        
    def draw_normal(self, screen, offset_x=0, offset_y=0):
        # Ambil frame pertama
        current_frame = self.bullet_frame_list[0]
        # Skala frame
        current_frame = pygame.transform.scale(current_frame, (25, 25))
        # Rotasi frame sesuai sudut
        rotated_frame = pygame.transform.rotate(current_frame, self.angle)
        # Hitung posisi untuk memusatkan frame yang telah dirotasi
        rotated_rect = rotated_frame.get_rect(center=(self.x + offset_x, self.y + offset_y))
        # Gambar frame yang dirotasi
        screen.blit(rotated_frame, rotated_rect.topleft)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
