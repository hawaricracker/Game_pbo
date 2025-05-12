import pygame
import pytmx
from Bullet import *  # ⬅ Tambahan: import Bullet untuk sistem peluru

class Game:
    def __init__(self, width, height):
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.frame_index = 0
        self.clock = pygame.time.Clock()
        self.objects = []
        self.offset_x = 0
        self.offset_y = 0
        self.map_width = 0
        self.map_height = 0
        self.zombies = []
        self.bullets = []  # ⬅ Tambahan: menyimpan semua peluru aktif dalam game

        # Load map dimensions immediately
        tmx_data = pytmx.load_pygame("Asset/MAP/map1.tmx")
        self.map_width = tmx_data.width * tmx_data.tilewidth
        self.map_height = tmx_data.height * tmx_data.tileheight

    def load_map(self, screen, filename, character):
        screen.fill((0, 0, 0))

        # Calculate camera offset to center the character
        self.offset_x = self.WIDTH // 2 - character.Character_rect.centerx
        self.offset_y = self.HEIGHT // 2 - character.Character_rect.centery

        # Load the Tiled map
        tmx_data = pytmx.load_pygame(filename)
        self.map_width = tmx_data.width * tmx_data.tilewidth
        self.map_height = tmx_data.height * tmx_data.tileheight

        # Render the map
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (x * tmx_data.tilewidth + self.offset_x, y * tmx_data.tileheight + self.offset_y))
        
        # Clear previous objects to avoid duplicates
        self.objects.clear()
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.type == "Obstacle":
                        obj_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.objects.append(obj_rect)

        self.frame_index += 1

    def load_char(self, screen, char):
        self.char_check_zombie_collision(char)
        screen.blit(char.player, (self.WIDTH // 2 - char.player.get_width() // 2, self.HEIGHT // 2 - char.player.get_height() // 2))
        screen.blit(char.player_moustache, (self.WIDTH // 2 - char.player.get_width() // 2, self.HEIGHT // 2 - char.player.get_height() // 2))
        screen.blit(char.player_shirt, (self.WIDTH // 2 - char.player.get_width() // 2, self.HEIGHT // 2 - char.player.get_height() // 2))
        screen.blit(char.weapon_img, (self.WIDTH // 2 - char.weapon_img.get_width() // 2 + 6, self.HEIGHT // 2 - char.weapon_img.get_height() // 2 + 10))  # ⬅ Ganti dari weapon ke weapon_img
        self.draw_health_bar(char.hp, char.max_hp, char)

    def load_zombies(self, character):
        for zombie in self.zombies:
            zombie.idling(self.frame_index)
            zombie.move_towards_player(self, character.Character_rect, self.frame_index)
            self.screen.blit(zombie.image, (
                zombie.rect.x + self.offset_x,
                zombie.rect.y + self.offset_y
            ))

    def movement(self, character, keys):
        character.speed = [0, 0]
        if keys[pygame.K_d]:
            character.move_right(self)
        elif keys[pygame.K_a]:
            character.move_left(self)
        elif keys[pygame.K_w]:
            character.move_up(self)
        elif keys[pygame.K_s]:
            character.move_down(self)

    def animation(self, character):
        if character.speed[0] == 0 and character.speed[1] == 0:
            character.idling(self.frame_index)
        else:
            character.run(self.frame_index)

    def check_collision(self, obj, obstacle):
        if obj.colliderect(obstacle):
            return True
        return False
    
    def char_check_house_collision(self, character, tmp):
        for obj_rect in self.objects:
            if self.check_collision(character.Character_rect, obj_rect):
                character.Character_rect = tmp
                character.acceleration = 0
                return 1
        character.acceleration = 5
        return 0

    def char_check_zombie_collision(self, character):
        for zombie in self.zombies:
            if character.Character_rect.colliderect(zombie.rect):
                character.hp -= zombie.dmg

    def draw_health_bar(self, hp, max_hp, char, width=30, height=6):
        health_ratio = hp / max_hp
        x = (self.WIDTH // 2) - width // 2
        y = (self.HEIGHT // 2) + char.player.get_height() // 2 + 3
        pygame.draw.rect(self.screen, (200, 0, 0), (x, y, width, height))
        pygame.draw.rect(self.screen, (0, 200, 0), (x, y, int(width * health_ratio), height))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height), 1)

    def update_bullets(self):
        for bullet in self.bullets:
            if bullet.collided:
                bullet.update_frame()  # Hanya update animasi jika sudah menabrak
                continue
            bullet_rect = bullet.get_rect()
            for obj_rect in self.objects:
                if self.check_collision(bullet_rect, obj_rect):
                    bullet.collided = True  # Tandai sebagai menabrak
                    bullet.update_frame()
                    break
            else:
                bullet.update_pos()  # Update posisi jika tidak menabrak
                bullet.update_frame()

        # Menghapus peluru yang keluar dari batas peta
        self.bullets = [
            b for b in self.bullets
            if 0 <= b.x <= self.map_width and 0 <= b.y <= self.map_height
        ]

    def draw_bullets(self):
        bullets_to_remove = []
        for bullet in self.bullets:
            bullet_rect = bullet.get_rect()
            collided = False
            for obj_rect in self.objects:
                if self.check_collision(bullet_rect, obj_rect):
                    if not bullet.collided:  # Reset animasi saat pertama kali menabrak
                        bullet.frame_index = 0
                    bullet.collided = True  # Tandai sebagai menabrak
                    bullet.draw_collision(self.screen, self.offset_x, self.offset_y)
                    collided = True
                    # Tandai peluru untuk dihapus setelah animasi selesai
                    if bullet.frame_index >= len(bullet.bullet_frame_list) - 1:
                        bullets_to_remove.append(bullet)
                    break
            if not collided:
                bullet.draw_normal(self.screen, self.offset_x, self.offset_y)
        # Hapus peluru yang sudah selesai animasi
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)
