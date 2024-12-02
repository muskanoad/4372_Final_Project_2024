import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate

# Define the function to generate the phantom
def generate_leg_phantom(leg_radius=50, bone_radius=20, height=100):
    phantom = np.zeros((height, 2 * leg_radius, 2 * leg_radius))
    for z in range(height):
        for x in range(2 * leg_radius):
            for y in range(2 * leg_radius):
                distance = np.sqrt((x - leg_radius) ** 2 + (y - leg_radius) ** 2)
                if distance <= bone_radius:
                    phantom[z, x, y] = 2  # Bone region
                elif distance <= leg_radius:
                    phantom[z, x, y] = 1  # Soft tissue region
    return phantom

# Generate the phantom
phantom = generate_leg_phantom()

# Add the functions for contrast and angle analysis (as previously provided)
def calculate_contrast(phantom_slice):
    bone_pixels = phantom_slice[phantom_slice == 2]
    soft_tissue_pixels = phantom_slice[phantom_slice == 1]
    if bone_pixels.size > 0 and soft_tissue_pixels.size > 0:
        contrast = np.abs(np.mean(bone_pixels) - np.mean(soft_tissue_pixels))
    else:
        contrast = 0
    return contrast

def generate_angle_projection(phantom, angle):
    rotated_phantom = rotate(phantom, angle, axes=(1, 2), reshape=False, mode='constant', cval=0)
    projection = np.sum(rotated_phantom, axis=0)
    return projection

def analyze_contrast_and_angle(phantom, slice_index, angles):
    phantom_slice = phantom[slice_index]
    contrast = calculate_contrast(phantom_slice)
    print(f"Contrast for slice {slice_index}: {contrast}")
    for angle in angles:
        projection = generate_angle_projection(phantom, angle)
        plt.figure(figsize=(8, 8))
        plt.imshow(projection, cmap="gray")
        plt.title(f"X-Ray Projection at {angle}°")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.colorbar(label="Intensity Sum")
        plt.show()

# Example usage
slice_index = phantom.shape[0] // 2
angles = [0, 45, 90, 135]
analyze_contrast_and_angle(phantom, slice_index, angles)
