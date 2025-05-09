import pygame
import pytmx

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
        # Load map dimensions immediately
        tmx_data = pytmx.load_pygame("test.tmx")
        self.map_width = tmx_data.width * tmx_data.tilewidth
        self.map_height = tmx_data.height * tmx_data.tileheight

    def load_map(self, screen, filename, character):
        screen.fill((0, 0, 0))

        # Calculate camera offset to center the character
        self.offset_x = self.WIDTH // 2 - character.Character_rect.centerx
        self.offset_y = self.HEIGHT // 2 - character.Character_rect.centery

        # Load the Tiled map
        tmx_data = pytmx.load_pygame(filename)
        self.map_width = tmx_data.width * tmx_data.tilewidth  # Total lebar peta
        self.map_height = tmx_data.height * tmx_data.tileheight  # Total tinggi peta

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
                    if obj.type == "House":
                        # Store objects in world coordinates (without offset for collision)
                        obj_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.objects.append(obj_rect)

        self.frame_index += 1
    
    def load_char(self, screen, char):
        self.check_zombie_collision(char)
        # Render character at screen center (adjusted by offset in load_map)
        screen.blit(char.player, (self.WIDTH // 2 - char.player.get_width() // 2, self.HEIGHT // 2 - char.player.get_height() // 2))
        screen.blit(char.player_moustache, (self.WIDTH // 2 - char.player.get_width() // 2, self.HEIGHT // 2 - char.player.get_height() // 2))
        screen.blit(char.player_shirt, (self.WIDTH // 2 - char.player.get_width() // 2, self.HEIGHT // 2 - char.player.get_height() // 2))
        screen.blit(char.weapon, (self.WIDTH // 2 - char.weapon.get_width() // 2 + 6, self.HEIGHT // 2 - char.weapon.get_height() // 2 + 10))
        self.draw_health_bar(char.hp, char.max_hp, char)

    def load_zombies(self, character):
        for zombie in self.zombies:
            zombie.idling(self.frame_index)  # Update animation
            zombie.move_towards_player(self, character.Character_rect, self.frame_index)  # Move towards player
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
        
    def check_house_collision(self, character, tmp):
        for obj_rect in self.objects:
            if character.Character_rect.colliderect(obj_rect):
                character.Character_rect = tmp
                character.acceleration = 0
                return
        character.acceleration = 5

    def check_zombie_collision(self, character):
        for zombie in self.zombies:
            if character.Character_rect.colliderect(zombie.rect):
                character.hp -= zombie.dmg

    def draw_health_bar(self, hp, max_hp, char, width=30, height=6):
        health_ratio = hp / max_hp  # hp/maxhp
        
        # Posisi kiri atas kotak health bar
        x = (self.WIDTH // 2) - width // 2
        y = (self.HEIGHT // 2) + char.player.get_height() // 2 + 3

        # Gambar background (merah)
        pygame.draw.rect(self.screen, (200, 0, 0), (x, y, width, height))
        # Gambar foreground (hijau) sesuai rasio
        pygame.draw.rect(self.screen, (0, 200, 0), (x, y, int(width * health_ratio), height))
        # (Opsional) bingkai tipis
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height), 1)
