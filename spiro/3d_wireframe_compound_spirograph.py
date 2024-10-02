import pygame
import pygame_gui
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Compound Spirograph Wire-frame")

# Set up the UI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Create sliders for parameters
R1_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 10), (200, 20)),
    start_value=250, value_range=(100, 350),
    manager=manager
)
R2_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 40), (200, 20)),
    start_value=150, value_range=(50, 200),
    manager=manager
)
r_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 70), (200, 20)),
    start_value=50, value_range=(10, 100),
    manager=manager
)
d_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 100), (200, 20)),
    start_value=30, value_range=(5, 100),
    manager=manager
)

# Labels for sliders
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 10), (150, 20)),
    text="R1 (Outermost circle)",
    manager=manager
)
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 40), (150, 20)),
    text="R2 (Middle circle)",
    manager=manager
)
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 70), (150, 20)),
    text="r (Inner circle)",
    manager=manager
)
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 100), (150, 20)),
    text="d (Pen distance)",
    manager=manager
)

def rotate_x(theta):
    return np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)]
    ])

def rotate_y(theta):
    return np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

def rotate_z(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])

def project(point):
    z = 0.5
    return [
        point[0] * z / (z - point[2]) * 100 + WIDTH / 2,
        point[1] * z / (z - point[2]) * 100 + HEIGHT / 2
    ]

def draw_3d_compound_spirograph(R1, R2, r, d):
    points = []
    t = np.linspace(0, 2 * np.pi, 1000)
    
    # Calculate spirograph points
    x1 = (R1 - R2) * np.cos(t)
    y1 = (R1 - R2) * np.sin(t)
    x = x1 + (R2 - r) * np.cos((R1 - R2) * t / R2) + d * np.cos(((R1 - R2) * t / R2) + ((R2 - r) * t / r))
    y = y1 + (R2 - r) * np.sin((R1 - R2) * t / R2) - d * np.sin(((R1 - R2) * t / R2) + ((R2 - r) * t / r))
    z = np.zeros_like(x)

    # Create 3D points
    points = np.column_stack((x, y, z))

    # Create rotation matrices
    rotation = rotate_x(0.5) @ rotate_y(0.5) @ rotate_z(pygame.time.get_ticks() * 0.001)

    # Apply rotation
    rotated_points = points @ rotation

    # Project 3D points to 2D
    projected_points = [project(point) for point in rotated_points]

    # Draw the spirograph
    pygame.draw.lines(screen, (255, 255, 255), False, projected_points, 1)

    # Draw connecting lines to create a wire-frame effect
    num_connections = 50
    for i in range(0, len(projected_points), len(projected_points) // num_connections):
        pygame.draw.line(screen, (100, 100, 255), projected_points[i], (WIDTH/2, HEIGHT/2), 1)

# Main game loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Get current parameter values
    R1 = R1_slider.get_current_value()
    R2 = R2_slider.get_current_value()
    r = r_slider.get_current_value()
    d = d_slider.get_current_value()

    # Draw the 3D compound spirograph
    draw_3d_compound_spirograph(R1, R2, r, d)

    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()