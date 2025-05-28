from abc import ABC, abstractmethod
import pygame

class Entity(ABC, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def move_towards(self, game, target_rect, frame_index):
        pass

    @abstractmethod
    def take_damage(self, amount):
        pass

    @abstractmethod
    def idling(self, frame_index):
        pass