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

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self, screen, offset_x=0, offset_y=0):
        pygame.draw.circle(screen, self.color, (int(self.x + offset_x), int(self.y + offset_y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
