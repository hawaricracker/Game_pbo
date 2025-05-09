import pygame

class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font(None, 74)  # Font bawaan Pygame, ukuran 74
        self.small_font = pygame.font.Font(None, 50)
        self.buttons = []
        self.setup_menu()

    def setup_menu(self):
        # Judul
        title_text = self.font.render("Zombie Shooter", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 4))

        # Tombol Start
        start_text = self.small_font.render("Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(self.width // 2, self.height // 2))
        start_button = {"text": start_text, "rect": start_rect, "action": "start"}

        # Tombol Exit
        exit_text = self.small_font.render("Exit", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=(self.width // 2, self.height // 2 + 80))
        exit_button = {"text": exit_text, "rect": exit_rect, "action": "exit"}

        self.buttons = [start_button, exit_button]
        self.title = {"text": title_text, "rect": title_rect}

    def draw(self):
        # Latar belakang hitam
        self.screen.fill((0, 0, 0))
        # Gambar judul
        self.screen.blit(self.title["text"], self.title["rect"])
        # Gambar tombol
        for button in self.buttons:
            self.screen.blit(button["text"], button["rect"])
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    return button["action"]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "exit"
        return None