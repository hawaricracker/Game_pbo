import pygame
import os

class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        
        # Font setup - menggunakan font yang lebih bold untuk judul
        self.title_font = pygame.font.Font(None, 128)  # Font untuk judul
        self.button_font = pygame.font.Font(None, 72)  # Font untuk tombol
        self.small_font = pygame.font.Font(None, 64)   # Font untuk settings
        
        self.buttons = []
        self.volume = 100
        self.music = 100
        self.show_settings = False
        
        # Slider dragging states
        self.dragging_sound = False
        self.dragging_music = False
        
        # Bar rectangles (akan diset dalam draw_settings)
        self.sound_bar_rect = None
        self.music_bar_rect = None
        
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

    def draw_volume_bar(self, x, y, width, height, volume, label):
        """Menggambar volume bar dengan label"""
        # Label text
        label_shadow = self.small_font.render(label, True, (0, 0, 0))
        label_main = self.small_font.render(label, True, (255, 255, 255))
        label_rect = label_main.get_rect(center=(self.width//2, y - 30))
        label_shadow_rect = label_rect.copy()
        label_shadow_rect.x += 1
        label_shadow_rect.y += 1
        
        self.screen.blit(label_shadow, label_shadow_rect)
        self.screen.blit(label_main, label_rect)
        
        # Volume percentage text
        vol_text = f"{volume}%"
        vol_shadow = self.small_font.render(vol_text, True, (0, 0, 0))
        vol_main = self.small_font.render(vol_text, True, (255, 255, 255))
        vol_text_rect = vol_main.get_rect(center=(self.width//2, y + height + 20))
        vol_shadow_rect = vol_text_rect.copy()
        vol_shadow_rect.x += 1
        vol_shadow_rect.y += 1
        
        self.screen.blit(vol_shadow, vol_shadow_rect)
        self.screen.blit(vol_main, vol_text_rect)
        
        # Bar background (dark gray with border)
        bar_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (30, 30, 30), bar_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), bar_rect, 2)
        
        # Bar fill (green gradient)
        fill_width = int((volume / 100) * width)
        if fill_width > 0:
            fill_rect = pygame.Rect(x, y, fill_width, height)
            # Gradient effect for the fill
            for i in range(fill_width):
                color_intensity = 100 + int(100 * (i / width))
                color = (color_intensity, 200, 50)  # Green color
                pygame.draw.line(self.screen, color, (x + i, y), (x + i, y + height))
        
        # Bar slider handle
        handle_x = x + fill_width - 5
        handle_rect = pygame.Rect(handle_x, y - 5, 10, height + 10)
        pygame.draw.rect(self.screen, (255, 255, 255), handle_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), handle_rect, 2)
        
        return bar_rect

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
        title_rect = title_main.get_rect(center=(self.width//2, 80))
        title_shadow_rect = title_rect.copy()
        title_shadow_rect.x += 2
        title_shadow_rect.y += 2
        
        self.screen.blit(title_shadow, title_shadow_rect)
        self.screen.blit(title_main, title_rect)

        # Volume bars setup
        bar_width = 300
        bar_height = 30
        bar_x = (self.width - bar_width) // 2
        
        # Sound volume bar
        self.sound_bar_rect = self.draw_volume_bar(
            bar_x, 180, bar_width, bar_height, self.volume, "SOUND VOLUME"
        )
        
        # Music volume bar
        self.music_bar_rect = self.draw_volume_bar(
            bar_x, 360, bar_width, bar_height, self.music, "MUSIC VOLUME"
        )
        
        # Instructions text
        instruction_text = "Atur suara dengan geser atau keypad Atas-Bawah (SOUND) / A-D (MUSIC)"
        instr_shadow = pygame.font.Font(None, 24).render(instruction_text, True, (0, 0, 0))
        instr_main = pygame.font.Font(None, 24).render(instruction_text, True, (200, 200, 200))
        instr_rect = instr_main.get_rect(center=(self.width//2, 500))
        instr_shadow_rect = instr_rect.copy()
        instr_shadow_rect.x += 1
        instr_shadow_rect.y += 1
        
        self.screen.blit(instr_shadow, instr_shadow_rect)
        self.screen.blit(instr_main, instr_rect)
        
        # Back button
        back_text = "BACK (ESC OR CLICK)"
        back_shadow = self.small_font.render(back_text, True, (0, 0, 0))
        back_main = self.small_font.render(back_text, True, (255, 255, 255))
        self.back_rect = back_main.get_rect(center=(self.width//2, 900))
        back_shadow_rect = self.back_rect.copy()
        back_shadow_rect.x += 1
        back_shadow_rect.y += 1

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

    def handle_bar_interaction(self, mouse_pos, bar_rect, volume_type):
        """Handle mouse interaction with volume bars"""
        if bar_rect and bar_rect.collidepoint(mouse_pos):
            # Calculate new volume based on mouse position
            relative_x = mouse_pos[0] - bar_rect.x
            new_volume = int((relative_x / bar_rect.width) * 100)
            new_volume = max(0, min(100, new_volume))  # Clamp between 0-100
            
            if volume_type == "sound":
                self.volume = new_volume
            elif volume_type == "music":
                self.music = new_volume
            
            return True
        return False

    def handle_event(self, event):
        if self.show_settings:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos
                    
                    # Check if clicking on back button
                    if self.back_rect and self.back_rect.collidepoint(mouse_pos):
                        self.show_settings = False
                        return None
                    
                    # Check if clicking on volume bars
                    if self.handle_bar_interaction(mouse_pos, self.sound_bar_rect, "sound"):
                        self.dragging_sound = True
                    elif self.handle_bar_interaction(mouse_pos, self.music_bar_rect, "music"):
                        self.dragging_music = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.dragging_sound = False
                    self.dragging_music = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_sound:
                    self.handle_bar_interaction(event.pos, self.sound_bar_rect, "sound")
                elif self.dragging_music:
                    self.handle_bar_interaction(event.pos, self.music_bar_rect, "music")
            
            elif event.type == pygame.KEYDOWN:
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
