import pygame
import random
import sys

# --------------------------
# SETUP
# --------------------------
pygame.init()
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Car Racing 🚗")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Colors
ROAD_GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (200, 30, 30)
GREEN = (30, 200, 30)
YELLOW = (255, 220, 0)

# --------------------------
# PLAYER CLASS
# --------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 100))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 120))
        self.speed = 7

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Keep the car inside road boundaries
        if self.rect.left < 80:
            self.rect.left = 80
        if self.rect.right > WIDTH - 80:
            self.rect.right = WIDTH - 80

# --------------------------
# ENEMY CLASS
# --------------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((50, 100))
        self.image.fill(RED)
        self.rect = self.image.get_rect(
            center=(random.randint(120, WIDTH - 120), -100)
        )
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# --------------------------
# FUNCTIONS
# --------------------------
def draw_road():
    screen.fill((34, 139, 34))  # grass
    pygame.draw.rect(screen, ROAD_GRAY, (80, 0, WIDTH - 140, HEIGHT))  # road
    pygame.draw.rect(screen, WHITE, (80, 0, 9, HEIGHT))  # left border
    pygame.draw.rect(screen, WHITE, (WIDTH - 85, 0, 9, HEIGHT))  # right border

    # Center dashed line
    dash_height = 400
    gap = 200
    y = offset % (dash_height + gap)
    while y < HEIGHT:
        pygame.draw.rect(screen, YELLOW, (WIDTH // 2 - 5, y, 10, dash_height))
        y += dash_height + gap

def show_text(text, size, y, color=WHITE):
    font_obj = pygame.font.SysFont("Arial", size, True)
    label = font_obj.render(text, True, color)
    rect = label.get_rect(center=(WIDTH // 2, y))
    screen.blit(label, rect)

# --------------------------
# MAIN LOOP
# --------------------------
player = Player()
player_group = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()

SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 900)

speed = 6
score = 0
running = True
game_over = False
offset = 0

while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_ENEMY and not game_over:
            enemies.add(Enemy(speed))
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Restart
            enemies.empty()
            player.sqr.center = (WIDTH // 2, HEIGHT - 120)
            speed = 6
            score = 0
            game_over = False

    if not game_over:
        offset += speed / 2
        player.update(keys)
        enemies.update()

        # Collision detection
        if pygame.sprite.spritecollideany(player, enemies):
            game_over = True

        # Score update
        score += 0.05
        if int(score) % 15 == 0:
            speed = min(14, 6 + int(score) // 15)  # increase difficulty slowly

    # --------------------------
    # DRAWING
    # --------------------------
    draw_road()
    player_group.draw(screen)
    enemies.draw(screen)
    show_text(f"Score: {int(score)}", 28, 30)

    if game_over:
        show_text("GAME OVER", 70, HEIGHT // 2 - 60, RED)
        show_text(f"Final Score: {int(score)}", 40, HEIGHT // 2 + 10, WHITE)
        show_text("Press SPACE to Restart", 30, HEIGHT // 2 + 70, YELLOW)

    pygame.display.flip()
