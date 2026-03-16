import pygame
import random
import sys

# 게임 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("간단한 슈팅 게임 (갤러그 스타일)")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 0)

# FPS 설정
FPS = 60
clock = pygame.time.Clock()

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 8
        self.shoot_delay = 200 # 연사 속도 (밀리초)
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

# 적 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speedy
        # 화면 아래로 벗어나면 위에서 다시 생성
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(2, 6)

# 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # 화면 밖으로 나가면 삭제
        if self.rect.bottom < 0:
            self.kill()

# 텍스트 출력 함수
def draw_text(surf, text, size, x, y, color=WHITE):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# 스프라이트 그룹 설정
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# 초기 적 생성
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

score = 0
running = True
game_over = False

# 게임 루프
while running:
    clock.tick(FPS)
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    
    # 스페이스바로 총알 발사
    if keys[pygame.K_SPACE] and not game_over:
        player.shoot()
        
    if not game_over:
        # 상태 업데이트
        all_sprites.update()
        
        # 충돌 검사 1: 총알과 적 (True, True는 둘 다 삭제함을 의미)
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10 # 10점 획득
            # 파괴된 만큼 새로운 적 생성
            e = Enemy()
            all_sprites.add(e)
            enemies.add(e)
            
        # 충돌 검사 2: 플레이어와 적
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            game_over = True
            
    # 화면 그리기
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, f"Score: {score}", 30, WIDTH // 2, 10)
    
    # 게임 오버 화면
    if game_over:
        draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 2 - 50, RED)
        draw_text(screen, "Press R to Restart or Q to Quit", 30, WIDTH // 2, HEIGHT // 2 + 30)
        
        if keys[pygame.K_r]:
            game_over = False
            score = 0
            # 모든 스프라이트 초기화
            all_sprites.empty()
            enemies.empty()
            bullets.empty()
            # 플레이어 및 적 재생성
            player = Player()
            all_sprites.add(player)
            for i in range(8):
                e = Enemy()
                all_sprites.add(e)
                enemies.add(e)
        elif keys[pygame.K_q]:
            running = False
            
    # 화면 업데이트
    pygame.display.flip()

pygame.quit()
sys.exit()
