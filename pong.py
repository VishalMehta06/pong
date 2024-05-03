import pygame
import random
import math
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 3

player_paddle = pygame.Rect(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
cpu_paddle = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

BALL_SIZE = 20
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed = 5
ball_speed_x = ball_speed
ball_speed_y = ball_speed

player_score = 0
cpu_score = 0

cpu_reaction_delay = 1  # Adjusted CPU skill level

# Store initial ball speed components
def move_cpu_paddle():
    global cpu_reaction_delay
    # Introduce a delay in CPU reaction time
    if pygame.time.get_ticks() % cpu_reaction_delay == 0:
        # Adjust CPU paddle towards the ball's y-position smoothly
        if ball.centery < cpu_paddle.centery:
            cpu_paddle.y -= min(PADDLE_SPEED, abs(ball.centery - cpu_paddle.centery))
        elif ball.centery > cpu_paddle.centery:
            cpu_paddle.y += min(PADDLE_SPEED, abs(ball.centery - cpu_paddle.centery))

        # Ensure the paddle stays within the screen boundaries
        cpu_paddle.y = max(0, min(cpu_paddle.y, SCREEN_HEIGHT - PADDLE_HEIGHT))

def reset_ball():
    global ball_speed_x, ball_speed_y
    # Reset ball position
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    # Ensure ball moves in a random direction
    angle = random.uniform(-math.pi / 4, math.pi / 4)  # Recalculate angle
    ball_speed_x = ball_speed * math.cos(angle)
    ball_speed_y = ball_speed * math.sin(angle)

def update_score(player):
    global player_score, cpu_score
    if player == "player":
        player_score += 1
    elif player == "cpu":
        cpu_score += 1

font = pygame.font.Font(None, 36)

count = 3
while count > 0:
    screen.fill(GREEN)
    count_text = font.render(str(count), True, WHITE)
    screen.blit(count_text, (SCREEN_WIDTH // 2 - count_text.get_width() // 2, SCREEN_HEIGHT // 2 - count_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)
    count -= 1

screen.fill(GREEN)
start_text = font.render("Start!", True, WHITE)
screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
pygame.display.flip()
time.sleep(1)

# Draw lines to resemble a tennis court
def draw_court_lines():
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT // 4), (SCREEN_WIDTH, SCREEN_HEIGHT // 4), 5)
    pygame.draw.line(screen, WHITE, (0, 3 * SCREEN_HEIGHT // 4), (SCREEN_WIDTH, 3 * SCREEN_HEIGHT // 4), 5)

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player_paddle.bottom < SCREEN_HEIGHT:
        player_paddle.y += PADDLE_SPEED

    move_cpu_paddle()  # Update CPU paddle movement

    if not game_over:
        ball.x += int(ball_speed_x)  # Adjusted to convert to integer
        ball.y += int(ball_speed_y)  # Adjusted to convert to integer

        # Ball collision with top and bottom walls
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1  # Reverse the y component of velocity upon collision

        # Ball collision with paddles
        if ball.colliderect(player_paddle):
            # Adjust ball_speed_y based on paddle's vertical movement speed
            ball_speed_y += random.uniform(-5, 5)
            ball_speed_x *= -1
            ball_speed_y = max(-ball_speed, min(ball_speed, ball_speed_y))  # Limit y speed to avoid excessive bouncing

        elif ball.colliderect(cpu_paddle):
            # Adjust ball_speed_y based on paddle's vertical movement speed
            ball_speed_y += random.uniform(-5, 5)
            ball_speed_x *= -1
            ball_speed_y = max(-ball_speed, min(ball_speed, ball_speed_y))  # Limit y speed to avoid excessive bouncing

        # Check for scoring
        if ball.left <= 0:
            update_score("cpu")
            reset_ball()
        elif ball.right >= SCREEN_WIDTH:
            update_score("player")
            reset_ball()

    screen.fill(GREEN)
    draw_court_lines()  # Draw tennis court lines
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, cpu_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    if not game_over:
        player_text = font.render("Player: " + str(player_score), True, WHITE)
        cpu_text = font.render("CPU: " + str(cpu_score), True, WHITE)
        screen.blit(player_text, (50, 20))
        screen.blit(cpu_text, (SCREEN_WIDTH - 150 - cpu_text.get_width(), 20))
    else:
        # Display "Game Over" message at the top of the screen
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 50))

    if player_score == 20 or cpu_score == 20:
        game_over = True

    pygame.display.flip()

pygame.quit()
