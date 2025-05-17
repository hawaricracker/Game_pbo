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

        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.type == "Obstacle":
                        obj_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.objects.append(obj_rect)

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
            self.draw_health_bar(zombie.hp, zombie.max_hp, zombie)

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
                character.hp = max(0, character.hp)  # Pastikan HP tidak negatif

    def draw_health_bar(self, hp, max_hp, entity, width=30, height=6):
        health_ratio = hp / max_hp
        
        # Tentukan posisi health bar berdasarkan jenis entitas
        if hasattr(entity, 'Character_rect'):  # Untuk karakter
            x = (self.WIDTH // 2) - width // 2
            y = (self.HEIGHT // 2) + entity.player.get_height() // 2 + 3
        else:  # Untuk zombie
            x = 8 + entity.rect.centerx + self.offset_x - width // 2
            y = entity.rect.bottom + self.offset_y + 15
        
        # Gambar health bar
        pygame.draw.rect(self.screen, (200, 0, 0), (x, y, width, height))
        pygame.draw.rect(self.screen, (0, 200, 0), (x, y, int(width * health_ratio), height))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height), 1)

    def update_bullets(self):
        for bullet in self.bullets:
            if not bullet.collided:
                bullet.update_pos()  # Update posisi jika belum menabrak
            bullet.update_frame()  # Update frame animasi

        # Menghapus peluru yang keluar dari jangkauan bullet
        self.bullets = [
            b for b in self.bullets
            if 0 <= b.x <= self.map_width and 0 <= b.y <= self.map_height and not b.has_exceeded_range()
        ]

    def draw_bullets(self):
        bullets_to_remove = []
        zombies_to_remove = []  # Daftar untuk zombie yang HP-nya <= 0
        
        for bullet in self.bullets:
            bullet_rect = bullet.get_rect()
            
            # Jika peluru belum menabrak, periksa kolisi
            if not bullet.collided:
                obj_list = self.objects.copy() + [z.rect for z in self.zombies]
                for i, obj_rect in enumerate(obj_list):
                    if self.check_collision(bullet_rect, obj_rect):
                        bullet.collided = True  # Tandai sebagai menabrak
                        bullet.frame_index = 0  # Reset animasi saat pertama kali menabrak
                        
                        # Jika menabrak zombie, kurangi HP
                        if i >= len(self.objects):  # Artinya menabrak zombie
                            zombie_index = i - len(self.objects)
                            zombie = self.zombies[zombie_index]
                            zombie.hp -= bullet.damage  # Kurangi HP zombie
                            if zombie.hp <= 0:
                                zombies_to_remove.append(zombie)  # Tandai untuk dihapus
                        break
            
            # Gambar peluru berdasarkan status collided
            if bullet.collided:
                bullet.draw_collision(self.screen, self.offset_x, self.offset_y)
                bullet.update_frame()
                # Tandai peluru untuk dihapus setelah animasi selesai
                if bullet.frame_index >= len(bullet.bullet_frame_list) - 1:
                    bullets_to_remove.append(bullet)
            else:
                bullet.draw_normal(self.screen, self.offset_x, self.offset_y)
        
        # Hapus peluru yang sudah selesai animasi
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)
        
        # Hapus zombie yang HP-nya <= 0
        for zombie in zombies_to_remove[:]:  # Iterate over a copy to avoid modification during iteration
            if zombie in self.zombies:  # Ensure the zombie is still in the list
                self.zombies.remove(zombie)

    def show_game_over(self):
        # Menampilkan layar game over
        self.screen.fill((0, 0, 0))  # Background hitam
        
        # Teks game over
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
        
        # Instruksi keluar
        small_font = pygame.font.Font(None, 36)
        exit_text = small_font.render("Press ESC to return to main menu", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 50))
        
        # Tampilkan teks
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(exit_text, exit_rect)
        pygame.display.flip()

    def show_victory(self):
        # Menampilkan layar kemenangan
        self.screen.fill((0, 0, 0))  # Background hitam
        
        # Teks kemenangan
        font = pygame.font.Font(None, 74)
        victory_text = font.render("YOU WIN!", True, (0, 255, 0))
        victory_rect = victory_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
        
        # Instruksi keluar
        small_font = pygame.font.Font(None, 36)
        exit_text = small_font.render("Press ESC to return to main menu", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 50))
        
        # Tampilkan teks
        self.screen.blit(victory_text, victory_rect)
        self.screen.blit(exit_text, exit_rect)
        pygame.display.flip()