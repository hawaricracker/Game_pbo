import pygame

class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)
        self.buttons = []
        self.volume = 100
        self.music = 100
        self.show_settings = False
        self.setup_menu()

    def setup_menu(self):
        # Judul
        title_text = self.font.render("Gen-Z Slayer: Z is for Zombies!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 4))

        # Tombol Start
        start_text = self.small_font.render("Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(self.width // 2, self.height // 2))
        start_button = {"text": start_text, "rect": start_rect, "action": "start"}

        # Tombol Setting
        settings_text = self.small_font.render("Settings", True, (255, 255, 255))
        settings_rect = settings_text.get_rect(center=(self.width // 2, self.height // 2 + 80))
        settings_button = {"text": settings_text, "rect": settings_rect, "action": "settings"}

        # Tombol Exit
        exit_text = self.small_font.render("Exit", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=(self.width // 2, self.height // 2 + 160))
        exit_button = {"text": exit_text, "rect": exit_rect, "action": "exit"}

        self.buttons = [start_button, settings_button, exit_button]
        self.title = {"text": title_text, "rect": title_rect}

    def draw_settings(self):
        # Latar Belakang Hitam
        self.screen.fill((0, 0, 0))
        # Gambar Judul
        title = self.font.render("Settings", True, (255, 255, 255))
        # Gambar Tombol
        self.screen.blit(title, title.get_rect(center=(self.width//2, 100)))

        # Tombol Volume
        vol_text = self.small_font.render(f"Sound Volume: {self.volume}% (Left/Right)", True, (255, 255, 255))
        music_text = self.small_font.render(f"Music Volume: {self.music}% (A/D)", True, (255, 255, 255))
        back_text = self.small_font.render("Back (ESC or Click)", True, (255, 255, 255))

        # Menghitung dan Menyimpan Rect dari teks 
        self.vol_rect = vol_text.get_rect(center=(self.width//2, 200))
        self.music_rect = music_text.get_rect(center=(self.width//2, 280))
        self.back_rect = back_text.get_rect(center=(self.width//2, 400))

        # Menampilkan Teks Berdasarkan Rect
        self.screen.blit(vol_text, self.vol_rect)
        self.screen.blit(music_text, self.music_rect)
        self.screen.blit(back_text, self.back_rect)
        pygame.display.flip()

    def draw(self):
        # Tamppilan menu utama atau menu pengaturan saat ini
        if self.show_settings:
            self.draw_settings()
        else:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.title["text"], self.title["rect"])
            for button in self.buttons:
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
