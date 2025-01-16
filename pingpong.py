import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
PASTEL_PINK = (255, 192, 203)
PASTEL_YELLOW = (255, 239, 150)
PASTEL_BLUE = (135, 206, 250)
WHITE = (255, 255, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cute Pong Game')

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load images
ball_img = pygame.image.load('ball.jpg')  # Add a cute ball image (e.g., ball with a smiley face)
player_img = pygame.image.load('cat.jpg')  # Add a paddle image (e.g., a cat)
ai_img = pygame.image.load('dog.jpg')  # Add another paddle image (e.g., a dog)

# Resize images
ball_img = pygame.transform.scale(ball_img, (30, 30))
player_img = pygame.transform.scale(player_img, (30, 100))
ai_img = pygame.transform.scale(ai_img, (30, 100))

# Ball setup
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = random.choice([-4, 4]), random.choice([-4, 4])
ball_size = 30

# Paddle setup
paddle_width, paddle_height = 30, 100
player_x, player_y = 10, HEIGHT // 2 - paddle_height // 2
ai_x, ai_y = WIDTH - 40, HEIGHT // 2 - paddle_height // 2
player_speed = 0
ai_speed = 4

# Scores
player_score = 0
ai_score = 0

# Fonts
font = pygame.font.Font(pygame.font.match_font("comicsansms"), 35)

def display_score(player, ai):
    score_text = font.render(f"Cat: {player}   Dog: {ai}", True, WHITE)
    screen.blit(score_text, (WIDTH // 3, 20))

# Game loop
def pong_game():
    global ball_x, ball_y, ball_dx, ball_dy, player_y, ai_y, player_score, ai_score, player_speed

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_speed = -5
                elif event.key == pygame.K_DOWN:
                    player_speed = 5
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    player_speed = 0

        # Update player paddle
        player_y += player_speed
        player_y = max(0, min(HEIGHT - paddle_height, player_y))  # Prevent going out of bounds

        # Update AI paddle
        if ball_y < ai_y + paddle_height // 2:
            ai_y -= ai_speed
        elif ball_y > ai_y + paddle_height // 2:
            ai_y += ai_speed
        ai_y = max(0, min(HEIGHT - paddle_height, ai_y))  # Prevent going out of bounds

        # Update ball position
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with top and bottom
        if ball_y - ball_size // 2 <= 0 or ball_y + ball_size // 2 >= HEIGHT:
            ball_dy = -ball_dy

        # Ball collision with paddles (rectangles)
        player_rect = pygame.Rect(player_x, player_y, paddle_width, paddle_height)
        ai_rect = pygame.Rect(ai_x, ai_y, paddle_width, paddle_height)

        if player_rect.collidepoint(ball_x - ball_size // 2, ball_y):
            ball_dx = -ball_dx

        if ai_rect.collidepoint(ball_x + ball_size // 2, ball_y):
            ball_dx = -ball_dx

        # Ball out of bounds
        if ball_x - ball_size // 2 <= 0:
            ai_score += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = random.choice([-4, 4])
            ball_dy = random.choice([-4, 4])

        if ball_x + ball_size // 2 >= WIDTH:
            player_score += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = random.choice([-4, 4])
            ball_dy = random.choice([-4, 4])

        # Draw everything
        screen.fill(PASTEL_BLUE)  # Set a pastel background color
        screen.blit(ball_img, (ball_x - ball_size // 2, ball_y - ball_size // 2))  # Ball image
        screen.blit(player_img, (player_x, player_y))  # Player paddle image
        screen.blit(ai_img, (ai_x, ai_y))  # AI paddle image

        # Draw invisible paddles for collision
        pygame.draw.rect(screen, WHITE, player_rect, 1)  # Optional: Outline for debugging
        pygame.draw.rect(screen, WHITE, ai_rect, 1)  # Optional: Outline for debugging

        display_score(player_score, ai_score)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

pong_game()
