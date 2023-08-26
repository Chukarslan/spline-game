import pygame
import numpy as np
import random

pygame.init()

# Simulation parameters
initial_frequency = 0.0003
initial_amplitude = 100
frequency_range = [0.0006, 0.0004, 0.00001]
amplitude_range = [100, 200]
transition_duration = 30000  # 10 seconds in milliseconds

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
line_thickness = 10 * ball_radius  # Thicker line width

# Initial curvature parameters
curvature_frequency = initial_frequency
curvature_amplitude = initial_amplitude

# Variables for dynamic changes
next_change_time = pygame.time.get_ticks() + transition_duration  # Initial change after 10 seconds

game_over = False
reset_button_rect = pygame.Rect(screen_width - 100, 10, 90, 30)  # Button to reset the game

transition_start_time = 0  # Initialize transition start time
start_frequency = initial_frequency
start_amplitude = initial_amplitude

def interpolate(a, b, t):
    return a + (b - a) * t

out_of_bounds = False  # To track if the ball is out of bounds

crash_sound = pygame.mixer.Sound("alarm.wav") # Crash sound

out_of_bounds_sound_playing = False  # To track if the out of bounds sound is playing

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if reset_button_rect.collidepoint(event.pos):
                # Reset the game
                curvature_frequency = initial_frequency
                curvature_amplitude = initial_amplitude
                next_change_time = pygame.time.get_ticks() + transition_duration
                ball_x = screen_width // 2
                ball_y = screen_height // 2

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

        # Ensure the ball stays within the screen bounds
        ball_x = np.clip(ball_x, ball_radius, screen_width - ball_radius)
        ball_y = np.clip(ball_y, ball_radius, screen_height - ball_radius)

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

        # Create a pixel array to manipulate
        pixel_array = pygame.surfarray.pixels3d(screen)

        # Draw the moving sine curved line
        y_range = np.arange(screen_height)
        phase = current_time * interpolated_frequency
        x_offset = interpolated_amplitude * np.sin(interpolated_frequency * y_range - phase)
        x_center = screen_width // 2 + x_offset.astype(int)
        x_indices = np.clip(x_center + np.arange(-line_thickness // 2, line_thickness // 2 + 1)[:, np.newaxis], 0, screen_width - 1)
        pixel_array[x_indices, y_range] = line_color

        # Release the pixel array
        del pixel_array

        # Draw the ball
        pygame.draw.circle(screen, (255, 255, 255), (ball_x, ball_y), ball_radius)

        # Check if the ball is within the red path
        ball_offset = np.abs(ball_x - x_center[ball_y])
        out_of_bounds = ball_offset > 4 * ball_radius

        # Display frequency and amplitude
        text = f"Frequency: {interpolated_frequency:.6f}   Amplitude: {interpolated_amplitude:.2f}"
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        # Draw reset button
        pygame.draw.rect(screen, (0, 0, 255), reset_button_rect)
        reset_text = font.render("Reset", True, (255, 255, 255))
        screen.blit(reset_text, (reset_button_rect.x + 10, reset_button_rect.y + 5))
        
        if out_of_bounds:
            if not out_of_bounds_sound_playing:
                # Start playing the crash sound
                pygame.mixer.Sound.play(crash_sound)
                out_of_bounds_sound_playing = True
        else:
            if out_of_bounds_sound_playing:
                # Stop playing the crash sound
                pygame.mixer.Sound.stop(crash_sound)
                out_of_bounds_sound_playing = False


        pygame.display.flip()
        clock.tick(60)

pygame.quit()
