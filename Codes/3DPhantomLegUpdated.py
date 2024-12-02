import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define dimensions and properties of the phantom
leg_radius = 50     # Radius of the leg (soft tissue) in arbitrary units
bone_radius = 20    # Radius of the bone (inner cylinder) in arbitrary units
height = 100        # Height of the leg phantom in arbitrary units

# Create an empty 3D matrix (phantom) filled with zeros
phantom = np.zeros((height, 2 * leg_radius, 2 * leg_radius))

# Populate the phantom with soft tissue and bone based on distance from center
for z in range(height):
    for x in range(2 * leg_radius):
        for y in range(2 * leg_radius):
            # Calculate the distance from the center of the cylinder
            distance = np.sqrt((x - leg_radius) ** 2 + (y - leg_radius) ** 2)
            if distance <= bone_radius:
                # Bone region
                phantom[z, x, y] = 2  # Higher attenuation value for bone
            elif distance <= leg_radius:
                # Soft tissue region
                phantom[z, x, y] = 1  # Lower attenuation value for soft tissue

# Function to simulate an orthogonal split
def add_orthogonal_split(phantom, split_z_start, split_z_end):
    """
    Simulate an orthogonal split in the phantom by setting attenuation values to zero
    in the specified z-range.
    """
    phantom[split_z_start:split_z_end, :, :] = 0

# Function to simulate an angled split
def add_angled_split(phantom, m, n, x0, y0, z0):
    """
    Simulate an angled split in the phantom by setting attenuation values to zero
    where z >= m*(x - x0) + n*(y - y0) + z0
    """
    height, width_x, width_y = phantom.shape

    # Generate coordinate grids
    z_indices = np.arange(height)[:, np.newaxis, np.newaxis]
    x_indices = np.arange(width_x)[np.newaxis, :, np.newaxis]
    y_indices = np.arange(width_y)[np.newaxis, np.newaxis, :]

    # Calculate the plane equation
    plane = m * (x_indices - x0) + n * (y_indices - y0) + z0

    # Create a mask where the attenuation values will be set to zero
    mask = z_indices >= plane

    # Apply the mask to the phantom
    phantom[mask] = 0

# Function to visualize a cross-section of the phantom
def visualize_phantom(phantom, slice_index):
    plt.figure(figsize=(8, 8))
    plt.imshow(phantom[slice_index], cmap="gray", origin='lower')
    plt.title(f"Cross-section of the Leg Phantom at Slice {slice_index}")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.colorbar(label="Attenuation Value")
    plt.show()

# Visualize the middle cross-section of the phantom before adding splits
visualize_phantom(phantom, height // 2)

# Save a copy of the original phantom for later comparison
phantom_original = phantom.copy()

# Add an orthogonal split
split_z_start = height // 2 + 5   # Adjusted to avoid zeroing out the middle slice
split_z_end = height // 2 + 15
add_orthogonal_split(phantom, split_z_start, split_z_end)

# Visualize a slice just before the split to observe the effect
visualize_phantom(phantom, height // 2 + 5)

# Reset the phantom to the original before adding the angled split
phantom = phantom_original.copy()

# Add an angled split
# Parameters for the angled plane
m = -0.5  # Negative slope to affect the upper part of the phantom
n = 0     # Slope in y-direction
x0 = leg_radius   # Center x-coordinate
y0 = leg_radius   # Center y-coordinate
z0 = height // 2  # The plane passes through the middle of the phantom

add_angled_split(phantom, m, n, x0, y0, z0)

# Visualize a slice affected by the angled split
visualize_phantom(phantom, height // 2 + 10)

# Function to plot attenuation profile along a line
def plot_attenuation_profile(phantom, z_slice, y_coord):
    attenuation_profile = phantom[z_slice, :, y_coord]
    plt.figure(figsize=(8, 4))
    plt.plot(attenuation_profile)
    plt.title(f"Attenuation Profile at Z={z_slice}, Y={y_coord}")
    plt.xlabel("X-axis")
    plt.ylabel("Attenuation Value")
    plt.show()

# Plot attenuation profiles before and after splits
# Before splits
phantom = phantom_original.copy()
plot_attenuation_profile(phantom, height // 2, leg_radius)

# After orthogonal split
phantom_with_orthogonal_split = phantom_original.copy()
add_orthogonal_split(phantom_with_orthogonal_split, split_z_start, split_z_end)
plot_attenuation_profile(phantom_with_orthogonal_split, height // 2 + 5, leg_radius)

# After angled split
phantom_with_angled_split = phantom_original.copy()
add_angled_split(phantom_with_angled_split, m, n, x0, y0, z0)
plot_attenuation_profile(phantom_with_angled_split, height // 2 + 10, leg_radius)

# 3D Visualization (optional)
def visualize_3d_phantom(phantom):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Get coordinates where the phantom has bone (attenuation value 2) and soft tissue (attenuation value 1)
    bone_coords = np.where(phantom == 2)
    soft_tissue_coords = np.where(phantom == 1)

    # Plot the bone in red
    ax.scatter(bone_coords[1], bone_coords[2], bone_coords[0], color="red", alpha=0.3, s=1, label="Bone")

    # Plot the soft tissue in blue
    ax.scatter(soft_tissue_coords[1], soft_tissue_coords[2], soft_tissue_coords[0], color="blue", alpha=0.1, s=1, label="Soft Tissue")

    ax.set_title("3D Visualization of the Leg Phantom with Splits")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Height (Z-axis)")
    ax.legend()
    plt.show()


