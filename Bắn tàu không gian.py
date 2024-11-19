import pygame
import random

# Khởi tạo pygame
pygame.init()

# Định nghĩa màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Kích thước cửa sổ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Tạo cửa sổ game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Tải hình ảnh
player_image = pygame.image.load('c:/Users/User/Pictures/Saved Pictures/tauchien.png')
player_image = pygame.transform.scale(player_image, (50, 50))  # Thay đổi kích thước tàu

enemy_image = pygame.image.load('c:/Users/User/Pictures/Saved Pictures/maybay.png')
enemy_image = pygame.transform.scale(enemy_image, (50, 50))  # Thay đổi kích thước kẻ địch về 50x50

bullet_image = pygame.image.load('c:/Users/User/Pictures/Saved Pictures/bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (15, 30))  # Thay đổi kích thước của tên lửa về 15x30

# Tốc độ khung hình
FPS = 60
clock = pygame.time.Clock()

# Lớp tàu không gian (Player)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image  # Sử dụng hình ảnh tàu người chơi
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)  # Căn giữa tàu
        self.speed_x = 0

    def update(self):
        # Di chuyển tàu
        self.rect.x += self.speed_x
        # Giới hạn di chuyển tàu không ra ngoài màn hình
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def move_left(self):
        self.speed_x = -5

    def move_right(self):
        self.speed_x = 5

    def stop(self):
        self.speed_x = 0

# Lớp tên lửa (Bullet)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image  # Sử dụng hình ảnh tên lửa
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = -7
        self.angle = random.uniform(-0.05, 0.05)  # Một chút lệch hướng

    def update(self):
        # Di chuyển tên lửa lên trên, đồng thời thay đổi vị trí theo chiều ngang một chút
        self.rect.y += self.speed_y
        self.rect.x += int(self.angle * 10)  # Chuyển động lệch theo chiều ngang
        # Xóa tên lửa khi ra ngoài màn hình
        if self.rect.bottom < 0:
            self.kill()

# Lớp kẻ địch (Enemy)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image  # Sử dụng hình ảnh kẻ địch
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - 50)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 5)

    def update(self):
        # Di chuyển kẻ địch xuống dưới
        self.rect.y += self.speed_y
        # Khi kẻ địch rơi khỏi màn hình, xóa kẻ địch
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Hàm tạo kẻ địch ban đầu (Giới hạn số lượng kẻ địch)
def create_initial_enemies(all_sprites, enemies, num_enemies=5):
    for _ in range(num_enemies):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

# Hàm tạo kẻ địch mới sau một khoảng thời gian
def spawn_enemy(all_sprites, enemies, last_spawn_time, spawn_interval=2000):
    current_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại tính bằng ms
    if current_time - last_spawn_time > spawn_interval:
        # Tạo kẻ địch mới nếu đến thời gian spawn
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        last_spawn_time = current_time  # Cập nhật thời gian spawn mới
    return last_spawn_time
# Lớp hiệu ứng nổ (Explosion)
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)  # Tạo nền trong suốt
        pygame.draw.circle(self.image, (255, 255, 0), (25, 25), 25)  # Tạo hình tròn màu vàng (nổ)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.max_frames = 5  # Số khung hình của hiệu ứng nổ

    def update(self):
        self.frame += 1
        if self.frame >= self.max_frames:
            self.kill()  # Sau khi hoàn thành, xóa hiệu ứng nổ
        else:
            self.image.set_alpha(255 - self.frame * 50)  # Dần mờ đi

# Hàm tạo kẻ địch ban đầu
def create_initial_enemies(all_sprites, enemies, num_enemies=5):
    for _ in range(num_enemies):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

# Hàm vẽ điểm số lên màn hình
def draw_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Hàm vẽ Game Over
def draw_game_over(score):
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))

    # Vẽ nút chơi lại
    restart_button = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 1.5, 280, 80)
    pygame.draw.rect(screen, GREEN, restart_button)
    restart_text = pygame.font.Font(None, 50).render("PLAY AGAIN", True, WHITE)
    screen.blit(restart_text, (SCREEN_WIDTH // 3 + 40, SCREEN_HEIGHT // 1.5 + 20))

    # Vẽ nút thoát
    quit_button = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 1.25, 280, 80)
    pygame.draw.rect(screen, RED, quit_button)
    quit_text = pygame.font.Font(None, 50).render("THOÁT", True, WHITE)
    screen.blit(quit_text, (SCREEN_WIDTH // 3 + 100, SCREEN_HEIGHT // 1.25 + 20))
    
    return restart_button, quit_button

# Hàm xử lý menu chính
def draw_main_menu():
    font = pygame.font.Font(None, 120)
    title_text = font.render("Space Shooter", True, RED)
    screen.blit(title_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 4 - 48))

    # Tạo nút Start
    start_button = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, 280, 80)
    pygame.draw.rect(screen, BLUE, start_button)
    start_text = pygame.font.Font(None, 70).render("START", True, WHITE)
    screen.blit(start_text, (SCREEN_WIDTH // 3 + 60, SCREEN_HEIGHT // 1.95 + 10))

    # Tạo nút Quit
    quit_button = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 1.5, 280, 80)
    pygame.draw.rect(screen, RED, quit_button)
    quit_text = pygame.font.Font(None, 70).render("THOÁT", True, WHITE)
    screen.blit(quit_text, (SCREEN_WIDTH // 3 + 60, SCREEN_HEIGHT // 1.55 + 20))
    
    return start_button, quit_button

# Hàm xử lý menu
def main_menu():
    menu_running = True
    
    while menu_running:
        screen.fill(BLACK)
        start_button, quit_button = draw_main_menu()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    menu_running = False
                    return 'start'
                elif quit_button.collidepoint(mouse_pos):
                    menu_running = False
                    return 'quit'

# Hàm xử lý game
def game_loop():
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)
    
    score = 0
    create_initial_enemies(all_sprites, enemies)
    
    last_spawn_time = pygame.time.get_ticks()  # Lưu thời gian spawn lần đầu
    max_enemies = 7 # Giới hạn số lượng kẻ địch trên màn hình
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_RETURN:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stop()
        
        all_sprites.update()

        # Kiểm tra va chạm giữa tên lửa và kẻ địch
        for bullet in bullets:
           enemy_hits = pygame.sprite.spritecollide(bullet, enemies, True)
           for enemy in enemy_hits:
               bullet.kill()
               score += 10
               explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
               all_sprites.add(explosion)

        # Giới hạn số lượng kẻ địch trên màn hình
        if len(enemies) < max_enemies:
            last_spawn_time = spawn_enemy(all_sprites, enemies, last_spawn_time, spawn_interval=500)  # 0.5 giây một lần

        # Kiểm tra va chạm giữa kẻ địch và tàu
        if pygame.sprite.spritecollide(player, enemies, False):
            game_running = False

        # Vẽ mọi thứ lên màn hình
        screen.fill(BLACK)
        draw_score(score)
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)
    
    return score

# Hàm chính
def main():
    game_running = True
    while game_running:
        game_result = main_menu()
        
        if game_result == 'start':
            score = game_loop()
            game_over = True
            while game_over:
                screen.fill(BLACK)
                restart_button, quit_button = draw_game_over(score)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_running = False
                        game_over = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if restart_button.collidepoint(mouse_pos):
                            game_over = False
                        elif quit_button.collidepoint(mouse_pos):
                            game_running = False
                            game_over = False
        elif game_result == 'quit':
            game_running = False

    pygame.quit()

if __name__ == "__main__":
    main()
