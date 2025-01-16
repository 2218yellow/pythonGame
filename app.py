import pygame
import time
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock and font
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Sounds
#eat_sound = pygame.mixer.Sound('eat.wav')  # Add your sound file here
#game_over_sound = pygame.mixer.Sound('game_over.wav')

# Snake and food setup
def display_score(score):
    value = score_font.render(f"Your Score: {score}", True, WHITE)
    screen.blit(value, [10, 10])

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], CELL_SIZE, CELL_SIZE], border_radius=5)

def message(msg, color, size):
    font = pygame.font.SysFont("bahnschrift", size)
    mesg = font.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

def draw_gradient():
    for i in range(HEIGHT):
        r = min(255, i // 2)  # Clamp to 255
        g = min(255, i // 3)  # Clamp to 255
        b = 153  # Constant blue value
        color = (r, g, b)
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))


# Game menu
def main_menu():
    menu = True
    while menu:
        screen.fill(BLACK)
        message("Press SPACE to Start or Q to Quit", WHITE, 30)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Game loop
def game_loop():
    game_over = False
    game_close = False

    x1 = WIDTH // 2
    y1 = HEIGHT // 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    food_x = round(random.randrange(0, WIDTH - CELL_SIZE) / 20.0) * 20.0
    food_y = round(random.randrange(0, HEIGHT - CELL_SIZE) / 20.0) * 20.0

    speed = 15

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("You lost! Press C-Play Again or Q-Quit", RED, 30)
            display_score(length_of_snake - 1)
            pygame.display.update()
           # pygame.mixer.Sound.play(game_over_sound)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -CELL_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = CELL_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -CELL_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = CELL_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        # Draw background and borders
        draw_gradient()
        pygame.draw.rect(screen, WHITE, [0, 0, WIDTH, HEIGHT], 10)

        # Draw food with animation
        pygame.draw.rect(screen, RED, [food_x, food_y, CELL_SIZE, CELL_SIZE], border_radius=5)
        
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_list)
        display_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, WIDTH - CELL_SIZE) / 20.0) * 20.0
            food_y = round(random.randrange(0, HEIGHT - CELL_SIZE) / 20.0) * 20.0
            length_of_snake += 1
           # pygame.mixer.Sound.play(eat_sound)

        # Increase speed dynamically
        speed = 15 + (length_of_snake // 5)
        clock.tick(speed)

    pygame.quit()
    quit()

main_menu()
game_loop()
