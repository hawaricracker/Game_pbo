import pygame
import pytmx
import time
from Bullet import *  # ⬅ Tambahan: import Bullet untuk sistem peluru
from Zombies import Zombie

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
        self.bullets = []
        self.boss = None
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
        self.zombies = [z for z in self.zombies if isinstance(z, Zombie)]  # Ensure no Boss in zombies

    def load_map(self, screen, filename, character):
        screen.fill((0, 0, 0))

        # Calculate camera offset to center the character
        self.offset_x = self.WIDTH // 2 - character.Character_rect.centerx
        self.offset_y = self.HEIGHT // 2 - character.Character_rect.centery

        # Load the Tiled map
        try:
            tmx_data = pytmx.load_pygame(filename)
        except Exception as e:
            print(f"Error memuat peta: {e}, pakai peta kosong!")
            tmx_data = None  # Lanjut dengan peta kosong kalau gagal
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
    
    def load_entities(self, entities, player):
        for entity in entities:
            entity.idling(self.frame_index)
            entity.move_towards(self, player.Character_rect, self.frame_index)
            self.screen.blit(entity.image, (
                entity.rect.x + self.offset_x,
                entity.rect.y + self.offset_y
            ))
            self.draw_health_bar(entity.get_hp(), entity.max_hp, entity)

    def load_char(self, screen, char):
        self.char_check_zombie_collision(char)
        screen.blit(char.player, (self.WIDTH // 2 - char.player.get_width() // 2, self.HEIGHT // 2 - char.player.get_height() // 2))
        screen.blit(char.player_moustache, (self.WIDTH // 2 - char.player.get_width() // 2, self.HEIGHT // 2 - char.player.get_height() // 2))
        screen.blit(char.player_shirt, (self.WIDTH // 2 - char.player.get_width() // 2, self.HEIGHT // 2 - char.player.get_height() // 2))
        screen.blit(char.weapon_img, (self.WIDTH // 2 - char.weapon_img.get_width() // 2 + 6, self.HEIGHT // 2 - char.weapon_img.get_height() // 2 + 10))  # ⬅ Ganti dari weapon ke weapon_img
        self.draw_health_bar(char.hp, char.max_hp, char)

    def load_zombies(self, character):
        self.load_entities(self.zombies, character)

    def load_boss(self, boss, player):
        if boss and not boss.is_dead:
            self.load_entities([boss], player)

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

    #Implementasi Enkapsulasi
    def char_check_zombie_collision(self, character):
        for zombie in self.zombies:
            if character.get_rect().colliderect(zombie.rect):
                character.set_hp(character.get_hp() - zombie.dmg)  # Gunakan getter dan setter
                character.last_damage_time = time.time() # Reset timer regen saat terkena damage
                  

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
        zombies_to_remove = []
        
        for bullet in self.bullets:
            bullet_rect = bullet.get_rect()
            
            # Jika peluru belum menabrak, periksa kolisi
            if not bullet.collided:
                obj_list = self.objects.copy() + [z.rect for z in self.zombies]
                # Tambah bos ke daftar kalau ada dan belum mati
                if hasattr(self, 'boss') and self.boss and not self.boss.is_dead:
                    obj_list.append(self.boss.get_rect())
                
                for i, obj_rect in enumerate(obj_list):
                    if self.check_collision(bullet_rect, obj_rect):
                        bullet.collided = True
                        bullet.frame_index = 0
                        
                        # Jika menabrak zombie
                        if i >= len(self.objects) and i < len(self.objects) + len(self.zombies):
                            zombie_index = i - len(self.objects)
                            zombie = self.zombies[zombie_index]
                            zombie.hp -= bullet.damage
                            if zombie.hp <= 0:
                                zombies_to_remove.append(zombie)
                        # Jika menabrak bos
                        elif i >= len(self.objects) + len(self.zombies):
                            self.boss.take_damage(bullet.damage)
                        break
            
            # Gambar peluru berdasarkan status collided
            if bullet.collided:
                bullet.draw_collision(self.screen, self.offset_x, self.offset_y)
                bullet.update_frame()
                if bullet.frame_index >= len(bullet.bullet_frame_list) - 1:
                    bullets_to_remove.append(bullet)
            else:
                bullet.draw_normal(self.screen, self.offset_x, self.offset_y)
        
        # Hapus peluru yang sudah selesai animasi
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)
        
        # Hapus zombie yang HP-nya <= 0
        for zombie in zombies_to_remove[:]:
            if zombie in self.zombies:
                self.zombies.remove(zombie)

    
    def check_dash_collision_with_zombies(self, character):
        if not character.is_dashing or not character.dash_just_started:
            return


        for zombie in self.zombies:
            if character.Character_rect.colliderect(zombie.rect):
            # Hitung arah dorongan
                dx = zombie.rect.centerx - character.Character_rect.centerx
                dy = zombie.rect.centery - character.Character_rect.centery
                distance = math.hypot(dx, dy)
                if distance == 0:
                    continue

                push_strength = 30 # Jarak dorongan
                dx /= distance
                dy /= distance

                # Dorong zombie menjauh dari player
                zombie.rect.x += int(dx * push_strength)
                zombie.rect.y += int(dy * push_strength)

                # (Opsional) Kurangi HP zombie
                zombie.hp -= 5  # Bisa disesuaikan
        
        character.dash_just_started = False        



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
    
    def char_check_boss_collision(self, character, boss, current_time):
        if boss and not boss.is_dead:
            boss.attack_player(character, current_time)