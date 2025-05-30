import pygame
import os

class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        
        # Font setup - menggunakan font yang lebih bold untuk judul
        self.title_font = pygame.font.Font(None, 96)  # Font untuk judul
        self.button_font = pygame.font.Font(None, 72)  # Font untuk tombol
        self.small_font = pygame.font.Font(None, 64)   # Font untuk settings
        
        self.buttons = []
        self.volume = 100
        self.music = 100
        self.show_settings = False
        
        # Load background image
        self.load_background()
        self.setup_menu()

    def load_background(self):
        """Load dan resize background image"""
        try:
            # Ganti 'background.png' dengan nama file gambar Anda
            self.background = pygame.image.load('Asset/PNG/Apocalypse.png')
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except:
            # Jika gambar tidak ditemukan, buat background gradient sederhana
            self.background = self.create_gradient_background()

    def create_gradient_background(self):
        """Membuat background gradient jika gambar tidak tersedia"""
        background = pygame.Surface((self.width, self.height))
        
        # Gradient dari hijau gelap ke abu-abu
        for y in range(self.height):
            ratio = y / self.height
            r = int(40 + (100 - 40) * ratio)
            g = int(60 + (120 - 60) * ratio)
            b = int(40 + (80 - 40) * ratio)
            pygame.draw.line(background, (r, g, b), (0, y), (self.width, y))
        
        return background

    def setup_menu(self):
        # Judul dengan shadow effect
        title_text = "GEN-Z SLAYER: Z IS FOR ZOMBIES!"
        
        # Main title
        self.title_shadow = self.title_font.render(title_text, True, (0, 0, 0))
        self.title_main = self.title_font.render(title_text, True, (255, 255, 255))
        self.title_rect = self.title_main.get_rect(center=(self.width // 2, self.height // 4 - 20))
        self.title_shadow_rect = self.title_rect.copy()
        self.title_shadow_rect.x += 3
        self.title_shadow_rect.y += 3

        # Setup buttons dengan styling yang lebih menarik
        button_y_start = self.height // 2 + 50
        button_spacing = 70
        
        buttons_data = [
            ("START", "start"),
            ("SETTINGS", "settings"),
            ("EXIT", "exit")
        ]
        
        self.buttons = []
        for i, (text, action) in enumerate(buttons_data):
            y_pos = button_y_start + (i * button_spacing)
            
            # Create button dengan shadow
            button_shadow = self.button_font.render(text, True, (0, 0, 0))
            button_main = self.button_font.render(text, True, (255, 255, 255))
            button_rect = button_main.get_rect(center=(self.width // 2, y_pos))
            button_shadow_rect = button_rect.copy()
            button_shadow_rect.x += 2
            button_shadow_rect.y += 2
            
            button = {
                "text": button_main,
                "shadow": button_shadow,
                "rect": button_rect,
                "shadow_rect": button_shadow_rect,
                "action": action,
                "hover": False
            }
            self.buttons.append(button)

    def draw_settings(self):
        # Background untuk settings
        self.screen.blit(self.background, (0, 0))
        
        # Overlay gelap untuk settings
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Settings title
        title_shadow = self.title_font.render("SETTINGS", True, (0, 0, 0))
        title_main = self.title_font.render("SETTINGS", True, (255, 255, 255))
        title_rect = title_main.get_rect(center=(self.width//2, 100))
        title_shadow_rect = title_rect.copy()
        title_shadow_rect.x += 2
        title_shadow_rect.y += 2
        
        self.screen.blit(title_shadow, title_shadow_rect)
        self.screen.blit(title_main, title_rect)

        # Settings options dengan shadow
        vol_text = f"SOUND VOLUME: {self.volume}% (LEFT/RIGHT)"
        music_text = f"MUSIC VOLUME: {self.music}% (A/D)"
        back_text = "BACK (ESC OR CLICK)"

        # Volume setting
        vol_shadow = self.small_font.render(vol_text, True, (0, 0, 0))
        vol_main = self.small_font.render(vol_text, True, (255, 255, 255))
        self.vol_rect = vol_main.get_rect(center=(self.width//2, 200))
        vol_shadow_rect = self.vol_rect.copy()
        vol_shadow_rect.x += 1
        vol_shadow_rect.y += 1
        
        # Music setting
        music_shadow = self.small_font.render(music_text, True, (0, 0, 0))
        music_main = self.small_font.render(music_text, True, (255, 255, 255))
        self.music_rect = music_main.get_rect(center=(self.width//2, 280))
        music_shadow_rect = self.music_rect.copy()
        music_shadow_rect.x += 1
        music_shadow_rect.y += 1
        
        # Back button
        back_shadow = self.small_font.render(back_text, True, (0, 0, 0))
        back_main = self.small_font.render(back_text, True, (255, 255, 255))
        self.back_rect = back_main.get_rect(center=(self.width//2, 400))
        back_shadow_rect = self.back_rect.copy()
        back_shadow_rect.x += 1
        back_shadow_rect.y += 1

        # Draw all shadows first, then main text
        self.screen.blit(vol_shadow, vol_shadow_rect)
        self.screen.blit(vol_main, self.vol_rect)
        self.screen.blit(music_shadow, music_shadow_rect)
        self.screen.blit(music_main, self.music_rect)
        self.screen.blit(back_shadow, back_shadow_rect)
        self.screen.blit(back_main, self.back_rect)
        
        pygame.display.flip()

    def update_button_hover(self, mouse_pos):
        """Update hover state untuk buttons"""
        for button in self.buttons:
            button["hover"] = button["rect"].collidepoint(mouse_pos)

    def draw(self):
        # Update hover state
        mouse_pos = pygame.mouse.get_pos()
        self.update_button_hover(mouse_pos)
        
        if self.show_settings:
            self.draw_settings()
        else:
            # Draw background
            self.screen.blit(self.background, (0, 0))
            
            # Draw title with shadow
            self.screen.blit(self.title_shadow, self.title_shadow_rect)
            self.screen.blit(self.title_main, self.title_rect)
            

            
            # Draw buttons dengan hover effect
            for button in self.buttons:
                # Draw shadow
                self.screen.blit(button["shadow"], button["shadow_rect"])
                
                # Draw main text dengan warna berbeda jika hover
                if button["hover"]:
                    # Warna kuning untuk hover
                    hover_text = self.button_font.render(button["text"].get_at((0,0)) and "START" or 
                                                       button["action"].upper(), True, (255, 255, 0))
                    # Re-render text untuk hover effect
                    if button["action"] == "start":
                        hover_text = self.button_font.render("START", True, (255, 255, 0))
                    elif button["action"] == "settings":
                        hover_text = self.button_font.render("SETTINGS", True, (255, 255, 0))
                    elif button["action"] == "exit":
                        hover_text = self.button_font.render("EXIT", True, (255, 255, 0))
                    self.screen.blit(hover_text, button["rect"])
                else:
                    self.screen.blit(button["text"], button["rect"])
            
            pygame.display.flip()

    def handle_event(self, event):
        if self.show_settings:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_rect.collidepoint(event.pos):
                    self.show_settings = False
                    return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_settings = False
                elif event.key == pygame.K_LEFT:
                    self.volume = max(0, self.volume - 5)
                elif event.key == pygame.K_RIGHT:
                    self.volume = min(100, self.volume + 5)
                elif event.key == pygame.K_a:
                    self.music = max(0, self.music - 5)
                elif event.key == pygame.K_d:
                    self.music = min(100, self.music + 5)
            return None
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        if button["action"] == "settings":
                            self.show_settings = True
                            return None
                        return button["action"]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "exit"
        return None
