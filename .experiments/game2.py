import pygame
import math
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
BALL_COLOR = (0, 0, 255)
SPLINE_COLOR = (0, 255, 0)
FPS = 60
SPLINE_WIDTH = 5
BALL_RADIUS = 15
SPLINE_CHANGE_INTERVAL = 10 * FPS  # Change the splines every 10 seconds
BALL_SPEED = 5  # Adjust the ball's speed
MIN_SPLINE_DISTANCE = BALL_RADIUS * 10  # Minimum space between splines

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spline Ball Game")

# Clock to control frame rate
clock = pygame.time.Clock()

# Spline properties
spline_offset = 0
spline_amplitude = 150  # Increased the amplitude for larger spacing
spline_frequency = 0.1

# Calculate initial ball position between the splines
initial_ball_x = WIDTH // 2
initial_ball_y = HEIGHT // 2

# Ball properties
ball_x = initial_ball_x
ball_y = initial_ball_y
ball_speed_x = 0

# Game start time
start_time = time.time()
game_started = False

# Game loop
running = True
frame_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_speed_x = -BALL_SPEED
    elif keys[pygame.K_RIGHT]:
        ball_speed_x = BALL_SPEED
    else:
        ball_speed_x = 0

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Calculate spline position
    spline_offset = math.sin(frame_count * spline_frequency) * spline_amplitude

    # Draw splines
    pygame.draw.line(screen, SPLINE_COLOR, (WIDTH // 2 + spline_offset, 0), (WIDTH // 2 + spline_offset, HEIGHT), SPLINE_WIDTH)
    pygame.draw.line(screen, (255, 255, 0), (WIDTH // 2 - spline_offset, 0), (WIDTH // 2 - spline_offset, HEIGHT), SPLINE_WIDTH)

    # Update ball position
    ball_x += ball_speed_x
    ball_y = HEIGHT // 2  # Keep the ball's vertical position in the center

    # Draw the ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_x), int(ball_y)), BALL_RADIUS)

    # Check for collision with splines
    # if abs(ball_x - WIDTH // 2 - spline_offset) > MIN_SPLINE_DISTANCE:
    #     running = False  # Game over if ball goes out of bounds

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

    # Increment frame count and update splines periodically
    frame_count += 1
    if frame_count % SPLINE_CHANGE_INTERVAL == 0:
        frame_count = 0

    # Start the game after 3 seconds
    if not game_started and time.time() - start_time >= 3:
        game_started = True

# Quit pygame
pygame.quit()
