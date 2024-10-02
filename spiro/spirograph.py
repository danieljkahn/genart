import pygame
import pygame_gui
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Spirograph")

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

# Labels for sliders
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 10), (100, 20)),
    text="R (Fixed circle)",
    manager=manager
)
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 40), (100, 20)),
    text="r (Moving circle)",
    manager=manager
)
pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 70), (100, 20)),
    text="d (Pen distance)",
    manager=manager
)

# Function to draw the spirograph
def draw_spirograph(R, r, d):
    points = []
    t = 0
    while t < 200 * math.pi:  # Adjust for more or fewer rotations
        x = (R - r) * math.cos(t) + d * math.cos((R - r) * t / r)
        y = (R - r) * math.sin(t) - d * math.sin((R - r) * t / r)
        points.append((x + WIDTH // 2, y + HEIGHT // 2))
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

    # Draw the spirograph
    draw_spirograph(R, r, d)

    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()