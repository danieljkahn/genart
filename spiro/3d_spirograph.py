import pygame
import pygame_gui
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive 3D Spirograph")

# Set up the UI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Create sliders for parameters
R_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 10), (200, 20)),
    start_value=200, value_range=(50, 300),
    manager=manager
)
r_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 40), (200, 20)),
    start_value=50, value_range=(10, 100),
    manager=manager
)
d_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 70), (200, 20)),
    start_value=80, value_range=(10, 100),
    manager=manager
)
angle_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 100), (200, 20)),
    start_value=45, value_range=(0, 90),
    manager=manager
)

# Labels for sliders
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 10), (150, 20)),
    text="R (Fixed circle)",
    manager=manager
)
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 40), (150, 20)),
    text="r (Moving circle)",
    manager=manager
)
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 70), (150, 20)),
    text="d (Pen distance)",
    manager=manager
)
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 100), (150, 20)),
    text="Tilt angle (degrees)",
    manager=manager
)

def rotate_point(x, y, z, angle_x, angle_y):
    # Rotate around X axis
    new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
    new_z = y * math.sin(angle_x) + z * math.cos(angle_x)
    y, z = new_y, new_z

    # Rotate around Y axis
    new_x = x * math.cos(angle_y) + z * math.sin(angle_y)
    new_z = -x * math.sin(angle_y) + z * math.cos(angle_y)
    x, z = new_x, new_z

    return x, y, z

def project_point(x, y, z):
    # Simple perspective projection
    factor = 200 / (z + 200)
    x_proj = x * factor
    y_proj = y * factor
    return x_proj, y_proj

def draw_3d_spirograph(R, r, d, tilt_angle):
    points = []
    t = 0
    while t < 200 * math.pi:  # Adjust for more or fewer rotations
        x = (R - r) * math.cos(t) + d * math.cos((R - r) * t / r)
        y = (R - r) * math.sin(t) - d * math.sin((R - r) * t / r)
        z = 0

        # Apply 3D rotation
        angle_x = math.radians(tilt_angle)
        angle_y = t * 0.01  # This creates the rotation around the Y-axis as the spirograph is drawn
        x, y, z = rotate_point(x, y, z, angle_x, angle_y)

        # Project 3D point to 2D
        x_proj, y_proj = project_point(x, y, z)
        
        points.append((x_proj + WIDTH // 2, y_proj + HEIGHT // 2))
        t += 0.01
    
    if len(points) > 1:
        pygame.draw.lines(screen, (255, 255, 255), False, points, 1)

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
    R = R_slider.get_current_value()
    r = r_slider.get_current_value()
    d = d_slider.get_current_value()
    tilt_angle = angle_slider.get_current_value()

    # Draw the 3D spirograph
    draw_3d_spirograph(R, r, d, tilt_angle)

    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()