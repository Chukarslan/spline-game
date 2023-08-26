import pygame
import numpy as np
import random

pygame.init()

# Simulation parameters
initial_frequency = 0.0003
initial_amplitude = 100
frequency_range = [0.0007, 0.0003, 0.00001]
amplitude_range = [100, 200]
transition_duration = 10000  # 10 seconds in milliseconds

# Initialize screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dynamic Curvature Thick Sine Curved Line")

font = pygame.font.Font(None, 36)  # Font for displaying text

clock = pygame.time.Clock()

# Initialize ball position
ball_radius = 20
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_speed = 5

# Line parameters
line_color = (255, 0, 0)
line_width = 2
line_thickness = 10 * ball_radius  # Thicker line width

# Initial curvature parameters
curvature_frequency = initial_frequency
curvature_amplitude = initial_amplitude

# Variables for dynamic changes
next_change_time = pygame.time.get_ticks() + transition_duration  # Initial change after 10 seconds

game_over = False

transition_start_time = 0  # Initialize transition start time
start_frequency = initial_frequency
start_amplitude = initial_amplitude

def interpolate(a, b, t):
    return a + (b - a) * t

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    if not game_over:
        # Handle keyboard arrow key input for ball movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ball_x -= ball_speed
        if keys[pygame.K_RIGHT]:
            ball_x += ball_speed
        if keys[pygame.K_UP]:
            ball_y -= ball_speed
        if keys[pygame.K_DOWN]:
            ball_y += ball_speed

        current_time = pygame.time.get_ticks()

        if current_time >= next_change_time:
            # Update curvature parameters smoothly every 10 seconds
            start_frequency = curvature_frequency
            start_amplitude = curvature_amplitude

            curvature_frequency += random.choice([-0.0001, 0.0001])
            curvature_frequency = np.clip(curvature_frequency, min(frequency_range), max(frequency_range))

            curvature_amplitude += random.choice([-100, 100])
            curvature_amplitude = np.clip(curvature_amplitude, min(amplitude_range), max(amplitude_range))

            transition_start_time = current_time
            next_change_time = current_time + transition_duration

        # Calculate the transition progress (0 to 1)
        transition_progress = (current_time - transition_start_time) / transition_duration
        transition_progress = np.clip(transition_progress, 0, 1)

        # Smoothly interpolate curvature parameters
        interpolated_frequency = interpolate(start_frequency, curvature_frequency, transition_progress)
        interpolated_amplitude = interpolate(start_amplitude, curvature_amplitude, transition_progress)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the moving sine curved lines
        phase = current_time * interpolated_frequency
        for y in range(0, screen_height):
            x_offset = interpolated_amplitude * np.sin(interpolated_frequency * y - phase)
            x_center = screen_width // 2 + int(x_offset)
            x_range = range(x_center - line_thickness // 2, x_center + line_thickness // 2 + 1)
            for x in x_range:
                pygame.draw.line(screen, line_color, (x, y), (x, y), line_width)

        # Draw the ball
        pygame.draw.circle(screen, (0, 255, 0), (ball_x, ball_y), ball_radius)

        # Display frequency and amplitude
        text = f"Frequency: {interpolated_frequency:.6f}   Amplitude: {interpolated_amplitude:.2f}"
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
