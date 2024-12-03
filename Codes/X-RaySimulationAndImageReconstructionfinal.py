import numpy as np
import matplotlib.pyplot as plt


def calculate_contrast(phantom_slice):
    """
    Calculate the contrast between bone and soft tissue regions in a given slice.
    Contrast is defined as the difference in average pixel intensity.
    """
    bone_pixels = phantom_slice[phantom_slice == 2]
    soft_tissue_pixels = phantom_slice[phantom_slice == 1]

    if bone_pixels.size > 0 and soft_tissue_pixels.size > 0:
        contrast = np.abs(np.mean(bone_pixels) - np.mean(soft_tissue_pixels))
    else:
        contrast = 0

    return contrast


def generate_angle_projection(phantom, angle):
    """
    Simulate a 2D X-ray projection at a given angle by summing along the rotated axis.
    """
    # Rotate the phantom in the plane perpendicular to the height axis
    rotated_phantom = np.rot90(phantom, k=int(angle // 90), axes=(1, 2))
    # Sum along the rotated height axis to simulate projection
    projection = np.sum(rotated_phantom, axis=0)

    return projection


def analyze_contrast_and_angle(phantom, slice_index, angles):
    """
    Perform contrast calculation for a specific slice and angle-based analysis for the whole phantom.
    """
    # Extract the specific slice for contrast calculation
    phantom_slice = phantom[slice_index]
    contrast = calculate_contrast(phantom_slice)

    print(f"Contrast for slice {slice_index}: {contrast}")

    # Generate and visualize projections for specified angles
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
if __name__ == "__main__":
    # Assuming the phantom is already generated in `phantom` from your other scripts
    slice_index = phantom.shape[0] // 2  # Middle slice for contrast analysis
    angles = [0, 45, 90, 135]  # Angles for projection analysis

    analyze_contrast_and_angle(phantom, slice_index, angles)
