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

# Tốc độ khung hình
FPS = 60
clock = pygame.time.Clock()

# Lớp tàu không gian (Player)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
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
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
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
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - 50)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 5)

    def update(self):
        # Di chuyển kẻ địch xuống dưới
        self.rect.y += self.speed_y
        # Reset kẻ địch khi ra ngoài màn hình
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(SCREEN_WIDTH - 50)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 5)

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
    font = pygame.font.Font(None, 36)  # Sử dụng font mặc định với kích thước 36
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))  # Hiển thị điểm ở góc trên bên trái

# Hàm vẽ thông báo "Game Over"
def draw_game_over(score):
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))

# Hàm chính của game
def main():
    # Khởi tạo đối tượng player, enemies, bullets
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    enemies = pygame.sprite.Group()

    # Khởi tạo kẻ địch ban đầu
    create_initial_enemies(all_sprites, enemies, num_enemies=5)

    # Biến kiểm tra trạng thái game
    running = True
    score = 0  # Khởi tạo điểm số
    game_over = False  # Biến kiểm tra trạng thái game over

    while running:
        # Kiểm tra các sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_RETURN:  # Bắn bằng phím Enter
                    # Tạo tên lửa
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)

            if event.type == pygame.KEYUP and not game_over:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stop()

        if not game_over:
            # Cập nhật tất cả sprite
            all_sprites.update()

            # Kiểm tra va chạm giữa tên lửa và kẻ địch
            for bullet in all_sprites:
                if isinstance(bullet, Bullet):  # Kiểm tra nếu đối tượng là tên lửa
                    enemies_hit = pygame.sprite.spritecollide(bullet, enemies, True)
                    for enemy in enemies_hit:
                        bullet.kill()  # Xóa tên lửa
                        score += 10  # Tăng điểm khi bắn trúng kẻ địch
                        # Tạo hiệu ứng nổ
                        explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                        all_sprites.add(explosion)
                        # Tạo thêm một kẻ địch mới
                        new_enemy = Enemy()
                        all_sprites.add(new_enemy)
                        enemies.add(new_enemy)

            # Kiểm tra nếu có kẻ địch nào ra ngoài màn hình và tạo lại
            for enemy in enemies:
                if enemy.rect.top > SCREEN_HEIGHT:
                    # Xóa kẻ địch cũ và tạo một kẻ địch mới
                    enemy.kill()
                    new_enemy = Enemy()
                    all_sprites.add(new_enemy)
                    enemies.add(new_enemy)

            # Kiểm tra va chạm giữa tàu không gian và kẻ địch
            if pygame.sprite.spritecollide(player, enemies, False):
                game_over = True  # Kết thúc game khi va chạm với kẻ địch

            # Vẽ tất cả đối tượng lên màn hình
            screen.fill(BLACK)
            all_sprites.draw(screen)

            # Vẽ điểm số lên màn hình
            draw_score(score)

        else:
            # Nếu game kết thúc, hiển thị thông báo "Game Over"
            draw_game_over(score)

        # Cập nhật màn hình
        pygame.display.flip()

        # Điều chỉnh tốc độ khung hình
        clock.tick(FPS)

    # Thoát game
    pygame.quit()

# Chạy game
if __name__ == "__main__":
    main()