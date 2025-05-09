import pygame

# Kelas Weapon untuk menangani senjata
class Weapon:
    def __init__(self, fire_rate, bullet_speed, ammo_count=60):
        # Menyimpan kecepatan tembak (delay antara tembakan dalam milidetik)
        self.fire_rate = fire_rate  
        # Menyimpan kecepatan peluru yang ditembakkan
        self.bullet_speed = bullet_speed  
        # Menyimpan jumlah peluru yang tersedia untuk senjata. Default adalah 60
        self.ammo_count = ammo_count  
        # Waktu tembakan terakhir
        self.last_shot_time = 0  

    def shoot(self, position, angle):
        # Memeriksa apakah ada peluru yang tersedia
        if self.ammo_count > 0:
            current_time = pygame.time.get_ticks()  # Mendapatkan waktu saat ini
            # Memeriksa apakah cukup waktu telah berlalu untuk menembak
            if current_time - self.last_shot_time >= self.fire_rate:
                bullet = Bullet(position, angle, self.bullet_speed, 10)  # Membuat bullet baru
                self.last_shot_time = current_time  # Memperbarui waktu tembakan terakhir
                self.ammo_count -= 1  # Mengurangi jumlah peluru
                return bullet  # Mengembalikan bullet yang baru dibuat
        return None  # Jika tidak bisa menembak, kembalikan None
