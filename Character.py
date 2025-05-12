import pygame
from Weapon import Weapon
#class player
class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.idling_frame_list = []
        self.moustache_frame_list = []
        self.shirt_frame_list = []
        
        self.player = pygame.image.load("zombie/ZombieShooter/Sprites/Character/Body/Body.png")
        self.player_moustache = pygame.image.load("zombie/ZombieShooter/Sprites/Character/Moustach/Moustach1.png")
        self.player_shirt = pygame.image.load("zombie/ZombieShooter/Sprites/Character/Shirt/Shirt1.png")
        self.weapon_img = pygame.image.load("zombie/ZombieShooter/Sprites/Objects&Tiles/Weapons.png")

        for y in range(self.player.get_height() // 32):
            for x in range(self.player.get_width() // 32):
                frame = self.player.subsurface((x * 32, y * 32, 32, 32))
                frame1 = self.player_moustache.subsurface((x * 32, y * 32, 32, 32))
                frame2 = self.player_shirt.subsurface((x * 32, y * 32, 32, 32))
                self.idling_frame_list.append(frame)
                self.moustache_frame_list.append(frame1)
                self.shirt_frame_list.append(frame2)

        for y in range(self.weapon_img.get_height() // 32):
            for x in range(self.weapon_img.get_width() // 32):
                wp_frame = self.weapon_img.subsurface(x * 32, y * (32 // 3), 32, (32 // 3))
                self.weapon_img = wp_frame

        self.player = self.idling_frame_list[0]
        self.player_moustache = self.moustache_frame_list[0]
        self.player_shirt = self.shirt_frame_list[0]
        # Set initial spawn position in world coordinates
        self.Character_rect = self.player.get_rect(topleft=(100, 100))  # Adjust to avoid house collision
        self.speed = [0, 0]
        self.acceleration = 4
        self.scale = 50
        self.hp = 100
        self.max_hp = 100
        self.weapon = Weapon() 
    
    def idling(self, frame_index):
        self.player = self.idling_frame_list[(frame_index // 7) % 4]
        self.player_moustache = self.moustache_frame_list[(frame_index // 7) % 4]
        self.player_shirt = self.shirt_frame_list[(frame_index // 7) % 4]
        self.player = pygame.transform.scale(self.player, (self.scale, self.scale))
        self.player_moustache = pygame.transform.scale(self.player_moustache, (self.scale, self.scale))
        self.player_shirt = pygame.transform.scale(self.player_shirt, (self.scale, self.scale))
        self.weapon_img = pygame.transform.scale(self.weapon_img, (self.scale // 2, self.scale // 3))

    def run(self, frame_index):
        self.player = self.idling_frame_list[((frame_index // 7) % 6) + 4]
        self.player_moustache = self.moustache_frame_list[((frame_index // 7) % 6) + 4]
        self.player_shirt = self.shirt_frame_list[((frame_index // 7) % 6) + 4]
        self.player = pygame.transform.scale(self.player, (self.scale, self.scale))
        self.player_moustache = pygame.transform.scale(self.player_moustache, (self.scale, self.scale))
        self.player_shirt = pygame.transform.scale(self.player_shirt, (self.scale, self.scale))
        self.weapon_img = pygame.transform.scale(self.weapon_img, (self.scale // 2, self.scale // 3))

    def move_right(self, game):
        tmp = self.Character_rect.copy()
        self.Character_rect.x += self.acceleration
        self.restrict_to_map_bounds(game)
        self.speed[0] = 1
        game.char_check_house_collision(self, tmp)

    def move_left(self, game):
        tmp = self.Character_rect.copy()
        self.Character_rect.x -= self.acceleration
        self.restrict_to_map_bounds(game)
        self.speed[0] = 1
        game.char_check_house_collision(self, tmp)

    def move_up(self, game):
        tmp = self.Character_rect.copy()
        self.Character_rect.y -= self.acceleration
        self.restrict_to_map_bounds(game)
        self.speed[1] = 1
        game.char_check_house_collision(self, tmp)

    def move_down(self, game):
        tmp = self.Character_rect.copy()
        self.Character_rect.y += self.acceleration
        self.restrict_to_map_bounds(game)
        self.speed[1] = 1
        game.char_check_house_collision(self, tmp)
    
    def restrict_to_map_bounds(self, game):
        # Batasi posisi karakter agar tetap dalam peta
        self.Character_rect.left = max(0, self.Character_rect.left)
        self.Character_rect.right = min(game.map_width, self.Character_rect.right)
        self.Character_rect.top = max(0, self.Character_rect.top)
        self.Character_rect.bottom = min(game.map_height, self.Character_rect.bottom)
