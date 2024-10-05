import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons

def chladni_pattern(x, y, a, b, m, n):
    return np.sin(m * np.pi * x / a) * np.sin(n * np.pi * y / b)

def update(val):
    patterns = []
    for i in range(4):
        m, n = int(m_sliders[i].val), int(n_sliders[i].val)
        pattern = chladni_pattern(X, Y, a, b, m, n)
        patterns.append(pattern)
    
    combined_pattern = np.zeros_like(X)
    for i, pattern in enumerate(patterns):
        if freq_checkboxes[i].get_status()[0]:
            combined_pattern += pattern
    
    im.set_array(combined_pattern)
    fig.canvas.draw_idle()

# Initial parameters
a, b = 1.0, 1.0  # Plate dimensions
resolution = 500

# Create meshgrid
x = np.linspace(0, a, resolution)
y = np.linspace(0, b, resolution)
X, Y = np.meshgrid(x, y)

# Set up the figure and initial plot
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.35)

initial_pattern = chladni_pattern(X, Y, a, b, 2, 3)
im = ax.imshow(initial_pattern, cmap='RdBu', interpolation='nearest', aspect='equal')
plt.colorbar(im)

# Create sliders for m and n values (up to 4 frequencies)
m_sliders = []
n_sliders = []
freq_checkboxes = []

for i in range(4):
    ax_m = plt.axes([0.1, 0.25 - i*0.05, 0.65, 0.03])
    ax_n = plt.axes([0.1, 0.20 - i*0.05, 0.65, 0.03])
    ax_checkbox = plt.axes([0.85, 0.225 - i*0.05, 0.05, 0.05])
    
    m_slider = Slider(ax_m, f'm{i+1}', 0, 10, valinit=2, valstep=1)
    n_slider = Slider(ax_n, f'n{i+1}', 0, 10, valinit=3, valstep=1)
    checkbox = CheckButtons(ax_checkbox, [f'F{i+1}'], [True])
    
    m_sliders.append(m_slider)
    n_sliders.append(n_slider)
    freq_checkboxes.append(checkbox)
    
    m_slider.on_changed(update)
    n_slider.on_changed(update)
    checkbox.on_clicked(update)

# Create sliders for plate dimensions
ax_a = plt.axes([0.1, 0.05, 0.65, 0.03])
ax_b = plt.axes([0.1, 0.1, 0.65, 0.03])
a_slider = Slider(ax_a, 'a', 0.1, 2.0, valinit=1.0)
b_slider = Slider(ax_b, 'b', 0.1, 2.0, valinit=1.0)

def update_dimensions(val):
    global a, b, X, Y
    a, b = a_slider.val, b_slider.val
    x = np.linspace(0, a, resolution)
    y = np.linspace(0, b, resolution)
    X, Y = np.meshgrid(x, y)
    update(val)

a_slider.on_changed(update_dimensions)
b_slider.on_changed(update_dimensions)

# Add a reset button
reset_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(reset_ax, 'Reset')

def reset(event):
    for slider in m_sliders + n_sliders + [a_slider, b_slider]:
        slider.reset()
    for checkbox in freq_checkboxes:
        checkbox.set_active(0)
    update(None)

reset_button.on_clicked(reset)

plt.show()