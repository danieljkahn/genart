import pygame
import pygame_gui
import math
import colorsys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive 3D Compound Spirograph with Color")

# Set up the UI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Create sliders for parameters (same as before)
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
tilt_x_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 130), (200, 20)),
    start_value=30, value_range=(0, 90),
    manager=manager
)
tilt_y_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 160), (200, 20)),
    start_value=30, value_range=(0, 90),
    manager=manager
)

# Labels for sliders (same as before)
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
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 130), (150, 20)),
    text="Tilt X (degrees)",
    manager=manager
)
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 160), (150, 20)),
    text="Tilt Y (degrees)",
    manager=manager
)

def rotate_point(x, y, z, angle_x, angle_y, angle_z):
    # Rotate around X axis
    new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
    new_z = y * math.sin(angle_x) + z * math.cos(angle_x)
    y, z = new_y, new_z

    # Rotate around Y axis
    new_x = x * math.cos(angle_y) + z * math.sin(angle_y)
    new_z = -x * math.sin(angle_y) + z * math.cos(angle_y)
    x, z = new_x, new_z

    # Rotate around Z axis
    new_x = x * math.cos(angle_z) - y * math.sin(angle_z)
    new_y = x * math.sin(angle_z) + y * math.cos(angle_z)
    x, y = new_x, new_y

    return x, y, z

def project_point(x, y, z):
    # Simple perspective projection
    factor = 300 / (z + 300)
    x_proj = x * factor
    y_proj = y * factor
    return x_proj, y_proj

def get_color(x, y, z, t, max_distance):
    # Normalize x, y, z to [0, 1] range
    x_norm = (x + max_distance) / (2 * max_distance)
    y_norm = (y + max_distance) / (2 * max_distance)
    z_norm = (z + max_distance) / (2 * max_distance)

    # Use x, y, z for Hue, Saturation, Value respectively
    h = (x_norm + y_norm + t / (math.pi * 200)) % 1  # Hue cycles through colors and changes with time
    s = 0.7 + (0.3 * z_norm)  # Saturation varies with z
    v = 0.5 + (0.5 * y_norm)  # Value (brightness) varies with y

    # Convert HSV to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)

def draw_3d_compound_spirograph(R1, R2, r, d, tilt_x, tilt_y):
    points = []
    colors = []
    t = 0
    max_distance = max(R1, R2, r, d)  # Used for color normalization
    
    while t < 200 * math.pi:  # Adjust for more or fewer rotations
        # Position of the center of the middle circle
        x1 = (R1 - R2) * math.cos(t)
        y1 = (R1 - R2) * math.sin(t)
        
        # Position of the pen point
        x = x1 + (R2 - r) * math.cos((R1 - R2) * t / R2) + d * math.cos(((R1 - R2) * t / R2) + ((R2 - r) * t / r))
        y = y1 + (R2 - r) * math.sin((R1 - R2) * t / R2) - d * math.sin(((R1 - R2) * t / R2) + ((R2 - r) * t / r))
        z = 0

        # Apply 3D rotation
        angle_x = math.radians(tilt_x)
        angle_y = math.radians(tilt_y)
        angle_z = t * 0.01  # This creates a rotation around the Z-axis as the spirograph is drawn
        x, y, z = rotate_point(x, y, z, angle_x, angle_y, angle_z)

        # Get color based on 3D position and time
        color = get_color(x, y, z, t, max_distance)

        # Project 3D point to 2D
        x_proj, y_proj = project_point(x, y, z)
        
        points.append((int(x_proj + WIDTH // 2), int(y_proj + HEIGHT // 2)))
        colors.append(color)
        t += 0.01
    
    # Draw the spirograph with color gradients
    if len(points) > 1:
        for i in range(1, len(points)):
            pygame.draw.line(screen, colors[i], points[i-1], points[i], 2)

# Main game loop (same as before)
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
    tilt_x = tilt_x_slider.get_current_value()
    tilt_y = tilt_y_slider.get_current_value()

    # Draw the 3D compound spirograph
    draw_3d_compound_spirograph(R1, R2, r, d, tilt_x, tilt_y)

    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()