import pygame
import sys

# Configurações do jogo
WIDTH, HEIGHT = 800, 600
BALL_SPEED = [4, 4]
PADDLE_SPEED = 6

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Classes dos objetos
def save_score(score1, score2):
    with open("scores.txt", "a") as file:
        file.write(f"Jogador 1: {score1} - Jogador 2: {score2}\n")

class Paddle(pygame.Rect):
    def __init__(self, x):
        super().__init__(x, HEIGHT // 2 - 60, 10, 120)

    def move(self, up, down):
        keys = pygame.key.get_pressed()
        if keys[up] and self.top > 0:
            self.y -= PADDLE_SPEED
        if keys[down] and self.bottom < HEIGHT:
            self.y += PADDLE_SPEED

class Ball(pygame.Rect):
    def __init__(self):
        super().__init__(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
        self.speed = BALL_SPEED.copy()
    
    def move(self, paddle1, paddle2, scores):
        self.x += self.speed[0]
        self.y += self.speed[1]
        
        if self.top <= 0 or self.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
        
        if self.colliderect(paddle1) or self.colliderect(paddle2):
            self.speed[0] = -self.speed[0]
        
        if self.left <= 0:
            scores[1] += 1
            save_score(scores[0], scores[1])
            self.reset()
        elif self.right >= WIDTH:
            scores[0] += 1
            save_score(scores[0], scores[1])
            self.reset()
    
    def reset(self):
        self.x, self.y = WIDTH // 2 - 10, HEIGHT // 2 - 10
        self.speed = BALL_SPEED.copy()

# Inicialização de objetos
paddle1 = Paddle(30)
paddle2 = Paddle(WIDTH - 40)
ball = Ball()
scores = [0, 0]

clock = pygame.time.Clock()

# Loop do jogo
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    paddle1.move(pygame.K_w, pygame.K_s)
    paddle2.move(pygame.K_UP, pygame.K_DOWN)
    ball.move(paddle1, paddle2, scores)
    
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"{scores[0]}  -  {scores[1]}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 30, 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
