import pygame
import time
from Weapon import Weapon
from Entity import Entity
#class player
class Character(Entity):
    def __init__(self):
        super().__init__()
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
        
        self.acceleration = 10
        self.normal_speed = self.acceleration   # Simpan kecepatan normal
        self.dash_speed = 15                    # Kecepatan saat dash
        self.is_dashing = False                 # Status dash sedang aktif atau tidak
        self.dash_just_started = False          # Menandai bahwa dash baru saja dimulai
        self.dash_duration = 0.2                # Lama dash dalam detik
        self.dash_cooldown = 5.0                # Delay cooldown dalam detik
        self.dash_time = 0                      # Waktu terakhir dash aktif (timestamp)
        self.last_dash_time = -999              # Waktu terakhir dash dipakai (timestamp)

        self.scale = 50
        self.hp = 100
        self.max_hp = 100
        self.weapon = Weapon() 

        self.last_damage_time = time.time()    # Waktu terakhir terkena damage
        self.regen_delay = 3.0                 # Waktu tunda sebelum mulai regen
        self.regen_rate = 2.5                  # Jumlah HP yang ditambah per interval
        self.regen_interval = 1.0              # Frekuensi penambahan (per detik)
        self.last_regen_time = time.time()     # Waktu terakhir penambahan HP   

    def start_dash(self):
        current_time = time.time()
        if current_time - self.last_dash_time >= self.dash_cooldown:
            self.is_dashing = True
            self.dash_just_started = True
            self.dash_time = current_time
            self.last_dash_time = current_time
            self.acceleration = self.dash_speed

    def update_dash(self):
        if self.is_dashing:
            current_time = time.time()
            if current_time - self.dash_time >= self.dash_duration:
                self.is_dashing = False
                self.acceleration = self.normal_speed

    def update_health_regen(self):
        current_time = time.time()

    # Hanya regen jika HP belum penuh dan sudah lewat delay sejak terakhir kena damage
        if self.hp < self.max_hp and current_time - self.last_damage_time >= self.regen_delay:
            if current_time - self.last_regen_time >= self.regen_interval:
                self.hp += self.regen_rate
                self.hp = min(self.hp, self.max_hp)  # Jangan melebihi max
                self.last_regen_time = current_time            
    
    
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

    #Enkapsulasi
    def get_hp(self):
        return self.hp

    def set_hp(self, value):
        self.hp = max(0, min(value, self.max_hp))  # Pastikan HP tetap dalam batas

    def get_rect(self):
        return self.Character_rect

    def set_rect(self, rect):
        self.Character_rect = rect

    def move_towards(self):
        pass

    def take_damage(self, amount):
        self.hp -= amount
        self.hp = max(0, self.hp)
        self.last_damage_time = time.time()