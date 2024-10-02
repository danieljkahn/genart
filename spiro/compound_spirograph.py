import pygame
import pygame_gui
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Compound Spirograph")

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

# Function to draw the compound spirograph
def draw_compound_spirograph(R1, R2, r, d):
    points = []
    t = 0
    while t < 200 * math.pi:  # Adjust for more or fewer rotations
        # Position of the center of the middle circle
        x1 = (R1 - R2) * math.cos(t)
        y1 = (R1 - R2) * math.sin(t)
        
        # Position of the pen point
        x = x1 + (R2 - r) * math.cos((R1 - R2) * t / R2) + d * math.cos(((R1 - R2) * t / R2) + ((R2 - r) * t / r))
        y = y1 + (R2 - r) * math.sin((R1 - R2) * t / R2) - d * math.sin(((R1 - R2) * t / R2) + ((R2 - r) * t / r))
        
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
    R1 = R1_slider.get_current_value()
    R2 = R2_slider.get_current_value()
    r = r_slider.get_current_value()
    d = d_slider.get_current_value()

    # Draw the compound spirograph
    draw_compound_spirograph(R1, R2, r, d)

    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()