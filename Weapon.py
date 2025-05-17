import pygame
from Bullet import Bullet
import time

class Weapon:
    def __init__(self):
        self.fire_rate = 0.1  # detik antar tembakan (10 peluru per detik)
        self.bullet_speed = 10
        self.last_shot_time = 0

    def can_fire(self):
        return time.time() - self.last_shot_time >= self.fire_rate 

    def fire(self, pos, target_pos):
        if self.can_fire():
            self.last_shot_time = time.time()
            return Bullet(pos, target_pos, self.bullet_speed)
        return None
