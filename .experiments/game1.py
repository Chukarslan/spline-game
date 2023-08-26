import pygame
import numpy as np

pygame.init()

# Initialize screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Bending Lines")

clock = pygame.time.Clock()

# Initialize ball position
ball_radius = 20
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_speed = 5

# Line parameters
line_color = (255, 0, 0)
line_x_offset = 8 * ball_radius
line_width = 2

# Moving line parameters
moving_line_y = 0
moving_line_speed = 2

# Dashed line parameters
dash_length = 10
dash_spacing = 10
dash_offset = 0  # Initialize the offset for the dashed line

# Pre-render the dashed line onto a surface
dashed_line_surface = pygame.Surface((line_width, dash_length), pygame.SRCALPHA)
pygame.draw.line(dashed_line_surface, line_color, (line_width // 2, 0), (line_width // 2, dash_length), line_width)

# Initialize bending lines as splines
num_points = 100
spline_points = np.array([[screen_width // 2 + np.random.randint(-line_x_offset, line_x_offset + 1), y] for y in np.linspace(0, screen_height, num=num_points)])
spline = np.zeros((num_points, 2))

# Initialize bend angle
bend_angle = 0
target_bend_angle = 0
angle_change_rate = 0.001  # Adjust the rate of angle change

game_over = False

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

        # Update moving line position
        moving_line_y -= moving_line_speed
        if moving_line_y < -line_x_offset:
            moving_line_y = 0

        # Gradually change bend angle towards the target angle
        if abs(bend_angle - target_bend_angle) > 0.1:
            if bend_angle < target_bend_angle:
                bend_angle += angle_change_rate
            else:
                bend_angle -= angle_change_rate

        # Update and draw bending lines
        for i, point in enumerate(spline_points):
            rotation_matrix = np.array([[np.cos(bend_angle), -np.sin(bend_angle)], [np.sin(bend_angle), np.cos(bend_angle)]])
            rotated_point = np.dot(rotation_matrix, point - [screen_width // 2, moving_line_y]) + [screen_width // 2, moving_line_y]
            spline[i] = rotated_point

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the red lines
        pygame.draw.line(screen, (0, 0, 0), (screen_width // 2, 0), (screen_width // 2, screen_height), line_width)
        pygame.draw.line(screen, line_color, (screen_width // 2 - line_x_offset, 0), (screen_width // 2 - line_x_offset, screen_height), line_width)
        pygame.draw.line(screen, line_color, (screen_width // 2 + line_x_offset, 0), (screen_width // 2 + line_x_offset, screen_height), line_width)

        # Update and draw dashed center line
        dash_offset += moving_line_speed  # Adjust the offset based on the moving line speed
        if dash_offset >= dash_spacing:
            dash_offset = 0  # Reset the offset when it exceeds the spacing

        for y in range(dash_offset, screen_height, dash_length + dash_spacing):
            screen.blit(dashed_line_surface, (screen_width // 2 - line_width // 2, y - moving_line_y))

        # Draw the ball
        pygame.draw.circle(screen, (0, 255, 0), (ball_x, ball_y), ball_radius)

        # Draw the bending lines
        # pygame.draw.lines(screen, line_color, False, spline, line_width)

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
