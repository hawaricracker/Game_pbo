# Inisialisasi senjata
weapon = Weapon(fire_rate=200, bullet_speed=10, ammo_count=30)
bullets = pygame.sprite.Group()  # Grup untuk menyimpan bullet

# Dalam loop game
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Jika LMB ditekan
                mouse_pos = pygame.mouse.get_pos()  # Mendapatkan posisi mouse
                angle = math.atan2(mouse_pos[1] - character.Character_rect.centery, 
                                   mouse_pos[0] - character.Character_rect.centerx)  # Menghitung sudut
                bullet = weapon.shoot(character.Character_rect.center, angle)  # Menembak
                if bullet:
                    bullets.add(bullet)  # Menambahkan bullet ke grup

    # Memperbarui dan menggambar bullet
    bullets.update()  # Memperbarui posisi bullet
    for bullet in bullets:
        screen.blit(bullet.image, bullet.rect)  # Menggambar bullet
