import pygame
import random
import sys

WIDTH, HEIGHT = 480, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 2, HEIGHT - 10)
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self, bullets_group):
        bullet = Bullet(self.rect.midtop)
        bullets_group.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midbottom=position)
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 20))
        self.image.fill(RED)
        x = random.randint(0, WIDTH - self.image.get_width())
        self.rect = self.image.get_rect(topleft=(x, -20))
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Shooter")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    score = 0
    enemy_spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn_event, 1000)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(bullets)
            elif event.type == enemy_spawn_event:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)

        all_sprites.update()
        bullets.update()

        # Collision detection
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        score += len(hits)

        if pygame.sprite.spritecollideany(player, enemies):
            running = False

        screen.fill(BLACK)
        all_sprites.draw(screen)
        bullets.draw(screen)
        pygame.display.flip()

    print("Final Score:", score)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
