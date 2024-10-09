import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Create figure
fig, ax = plt.subplots(figsize=(12, 6))
# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Set circle sizes (not to scale, just visually proportional)
earth_radius = 0.5  # Earth size (arbitrary units)
TNO_radius = 0.2  # TNO size (smaller than Earth)
star_radius = 2.0  # Star size (larger than Earth)

# Define positions (not to scale, just visually clear)
earth_position = (2, 0)
TNO_initial_position = (8, 2)  # Start TNO below the screen
star_position = (30, 0)

# Plot the Earth (blue circle)
earth = plt.Circle(earth_position, earth_radius, color='blue', label='Earth')
# Plot the star (yellow circle)
star = plt.Circle(star_position, star_radius, color='orange', label='Star')
# Add Earth and Star to the plot
ax.add_artist(earth)
ax.add_artist(star)

# Add labels for the objects
ax.text(earth_position[0], 4, 'Earth', color='blue', fontsize=12, ha='center')
ax.text(TNO_initial_position[0], 4, 'TNO', color='black', fontsize=12, ha='center')
ax.text(star_position[0], 4, 'Star', color='orange', fontsize=12, ha='center')

# Draw lines to show the angle subtended by the star from Earth's point of view
ax.plot([earth_position[0] + earth_radius, star_position[0]], [earth_position[1], star_radius], color='orange', linestyle='--')
ax.plot([earth_position[0] + earth_radius, star_position[0]], [earth_position[1], -star_radius], color='orange', linestyle='--')

# Add distance and TNO size labels
# Add lines to show the distance between the Earth and the TNO
ax.plot([earth_position[0] + earth_radius, TNO_initial_position[0]], [-3,-3], color='black')
# Vertical lines to make it look like a ruler
ax.plot([earth_position[0] + earth_radius, earth_position[0] + earth_radius], [-2.75, -3.25], color='black')
ax.plot([TNO_initial_position[0], TNO_initial_position[0]], [-2.75, -3.25], color='black')
ax.text((earth_position[0] + earth_radius + TNO_initial_position[0]) / 2, -2.5, r'$D$', color='black', fontsize=12, ha='center')

# Remove axes and grid for a cleaner visual
ax.set_xlim(0, 35)
ax.set_ylim(-6, 6)
ax.set_aspect('equal')
ax.axis('off')

# Initialize the TNO (black circle)
tno = plt.Circle(TNO_initial_position, TNO_radius, color='black', label='TNO')
ax.add_artist(tno)

# Make a horizontal slider to control the TNO x position
ax_x = fig.add_axes([0.25, 0.1, 0.65, 0.03])
x_slider = Slider(
    ax=ax_x,
    label='TNO x',
    valmin=earth_position[0] + earth_radius,
    valmax=25,
    valinit=TNO_initial_position[0],
)
# Make a vertical slider to control the TNO y position
ax_y = fig.add_axes([0.1, 0.25, 0.03, 0.65])
y_slider = Slider(
    ax=ax_y,
    label='TNO y',
    valmin=-2,
    valmax=2,
    valinit=TNO_initial_position[1],
    orientation='vertical'
)

# Lines representing the Fresnel scale
fresnel_scale = np.sqrt(x_slider.val - earth_position[0] - earth_radius) / 2
ax.plot([TNO_initial_position[0], TNO_initial_position[0]], [-fresnel_scale / 2 + y_slider.val, fresnel_scale / 2 + y_slider.val], color='black')
# Label the line
ax.text(TNO_initial_position[0], y_slider.val + fresnel_scale / 2 + 0.4, r'$F_s$', color='black', fontsize=12, ha='center', va='center')
# Create a shadow with height equal to the fresnel scale extending from the TNO to the left. Use a semi-transparent rectangle.
outer_shadow = plt.Rectangle((earth_position[0] + earth_radius, -fresnel_scale / 2 + TNO_initial_position[1]),
                       TNO_initial_position[0] - earth_position[0] - earth_radius, fresnel_scale, color='black', alpha=0.1)
# The geometric shadow
inner_shadow = plt.Rectangle((earth_position[0] + earth_radius, -TNO_radius + TNO_initial_position[1]),
                              TNO_initial_position[0] - earth_position[0] - earth_radius, TNO_radius * 2, color='black', alpha=0.2)
ax.add_artist(outer_shadow)
ax.add_artist(inner_shadow)

# Add lines to show the distance between the observer and the shadow center
ax.plot([earth_position[0] - earth_radius - 1, earth_position[0] - earth_radius - 1], [earth_position[1], TNO_initial_position[1]], color='black')
# Vertical lines to make it look like a ruler
ax.plot([earth_position[0] - earth_radius - 0.75, earth_position[0] - earth_radius - 1.25], [earth_position[1], earth_position[1]], color='black')
ax.plot([earth_position[0] - earth_radius - 0.75, earth_position[0] - earth_radius - 1.25], [TNO_initial_position[1], TNO_initial_position[1]], color='black')
ax.text(earth_position[0] - earth_radius - 1.5, (earth_position[1] + TNO_initial_position[1]) / 2, r'$r$', color='black', fontsize=12, ha='center', va='center')

# Add dashed vertical orange line at the projected stellar radius
projected_star_radius = star_radius * (TNO_initial_position[0] - earth_position[0]) / (star_position[0] - earth_position[0])
ax.plot([TNO_initial_position[0], TNO_initial_position[0]], [-projected_star_radius, projected_star_radius], color='orange', linestyle='--')
ax.text(TNO_initial_position[0], -projected_star_radius - 0.5, r'$2R_{star}$', color='orange', fontsize=12, ha='center', va='center')

# The function to be called anytime a slider's value changes
def update(val):
    tno.set_center((x_slider.val, y_slider.val))
    ax.texts[1].set_position((x_slider.val, 4))
    # Adjust line from earth to TNO
    ax.lines[2].set_xdata([earth_position[0] + earth_radius, x_slider.val])
    ax.lines[4].set_xdata([x_slider.val, x_slider.val])
    fresnel_scale = np.sqrt(x_slider.val - earth_position[0] - earth_radius) / 2
    ax.texts[3].set_position(((x_slider.val + earth_position[0] + earth_radius) / 2, -2.5))
    # Adjust line to shadow center
    ax.lines[6].set_ydata([y_slider.val, earth_position[1]])
    ax.lines[8].set_ydata([y_slider.val, y_slider.val])
    ax.texts[5].set_position((earth_position[0] - earth_radius - 1.5, (earth_position[1] + y_slider.val) / 2))
    # Adjust fresnel scale line
    ax.lines[5].set_xdata([x_slider.val, x_slider.val])
    ax.lines[5].set_ydata([-fresnel_scale / 2 + y_slider.val, fresnel_scale / 2 + y_slider.val])
    # Move the label
    ax.texts[4].set_position((x_slider.val, y_slider.val + 0.4 + fresnel_scale / 2))
    # Move the shadow
    ax.patches[3].set_width(x_slider.val - earth_position[0] - earth_radius)
    ax.patches[3].set_height(fresnel_scale)
    ax.patches[3].set_xy([earth_position[0] + earth_radius, -fresnel_scale / 2 + y_slider.val])
    # Move the geometric shadow
    ax.patches[4].set_width(x_slider.val - earth_position[0] - earth_radius)
    ax.patches[4].set_xy([earth_position[0] + earth_radius, -TNO_radius + y_slider.val])
    # Adjust projected stellar radius
    projected_star_radius = star_radius * (x_slider.val - earth_position[0]) / (star_position[0] - earth_position[0])
    ax.lines[9].set_xdata([x_slider.val, x_slider.val])
    ax.lines[9].set_ydata([-projected_star_radius, projected_star_radius])
    ax.texts[6].set_position((x_slider.val, -projected_star_radius - 0.5))
    fig.canvas.draw_idle()

x_slider.on_changed(update)
y_slider.on_changed(update)

plt.show()