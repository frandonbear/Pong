import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1280, 960
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (0, 255, 0)
BLACK = (0, 0, 0)

# Constants
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 150
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Paddles
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

# Score
player_score = 0
ai_score = 0
font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()

def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def move_paddle(paddle, direction):
    if direction == "up" and paddle.top > 0:
        paddle.y -= PADDLE_SPEED
    elif direction == "down" and paddle.bottom < HEIGHT:
        paddle.y += PADDLE_SPEED

def move_ball():
    global ball_speed_x, ball_speed_y, player_score, ai_score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    if ball.left <= 0:
        ai_score += 1
        ball_restart()
    if ball.right >= WIDTH:
        player_score += 1
        ball_restart()

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
        ball_speed_x *= -1

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        move_paddle(player_paddle, "up")
    if keys[pygame.K_s]:
        move_paddle(player_paddle, "down")

    # AI Paddle movement
    if ball.y < ai_paddle.y + ai_paddle.height // 2:
        move_paddle(ai_paddle, "up")
    elif ball.y > ai_paddle.y + ai_paddle.height // 2:
        move_paddle(ai_paddle, "down")

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, ai_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Move ball
    move_ball()

    # Draw scores
    draw_text(str(player_score), font, WHITE, WIDTH // 4, 20)
    draw_text(str(ai_score), font, WHITE, WIDTH * 3 // 4, 20)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
