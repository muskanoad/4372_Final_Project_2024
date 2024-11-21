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

# Function to visualize a cross-section of the phantom
def visualize_phantom(phantom, slice_index):
    plt.figure(figsize=(8, 8))
    plt.imshow(phantom[slice_index], cmap="gray")
    plt.title(f"Cross-section of the Leg Phantom at Slice {slice_index}")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.colorbar(label="Attenuation Value")
    plt.show()

# Visualize the middle cross-section of the phantom
visualize_phantom(phantom, height // 2)

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

    ax.set_title("3D Visualization of the Leg Phantom")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Height (Z-axis)")
    ax.legend()
    plt.show()

# Uncomment the line below to visualize the 3D structure (optional, may take time for large arrays)
# visualize_3d_phantom(phantom)
