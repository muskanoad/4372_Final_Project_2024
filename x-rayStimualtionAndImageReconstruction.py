import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

# Phantom generation function
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

# X-ray simulation and image reconstruction
def simulate_xray_image(phantom, beam_energy, source_distance):
    height, width, depth = phantom.shape
    reconstructed_image = np.zeros((width, depth))

    # Attenuation factors based on beam energy and tissue type
    bone_attenuation = 0.5 + (beam_energy / 100) * 0.5  # Adjustable factor for bone
    tissue_attenuation = 0.2 + (beam_energy / 100) * 0.3  # Adjustable factor for tissue

    # Calculate the X-ray intensity at each point by summing attenuations through the depth
    for x in range(width):
        for y in range(depth):
            attenuation_sum = 0
            for z in range(height):
                if phantom[z, x, y] == 2:  # Bone region
                    attenuation_sum += bone_attenuation
                elif phantom[z, x, y] == 1:  # Soft tissue region
                    attenuation_sum += tissue_attenuation
            # Calculate intensity based on attenuation and distance
            reconstructed_image[x, y] = np.exp(-attenuation_sum / source_distance)
    
    return reconstructed_image

# Visualization function for reconstructed image
def visualize_reconstructed_image(image):
    plt.figure(figsize=(6, 6))
    plt.imshow(image, cmap="gray", origin="lower")
    plt.title("Reconstructed X-Ray Image")
    plt.colorbar(label="Intensity")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()

# GUI for parameter adjustment
class XRaySimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("X-Ray Simulator - Leg Phantom")

        # Default values for parameters
        self.beam_energy = tk.DoubleVar(value=50.0)
        self.source_distance = tk.DoubleVar(value=100.0)

        # GUI Layout
        # Beam energy adjustment
        ttk.Label(root, text="Beam Energy (keV)").grid(row=0, column=0, padx=10, pady=5)
        self.beam_energy_slider = ttk.Scale(root, from_=30, to=100, variable=self.beam_energy, command=self.update_simulation)
        self.beam_energy_slider.grid(row=0, column=1, padx=10, pady=5)

        # Source distance adjustment
        ttk.Label(root, text="Source Distance (cm)").grid(row=1, column=0, padx=10, pady=5)
        self.source_distance_slider = ttk.Scale(root, from_=50, to=200, variable=self.source_distance, command=self.update_simulation)
        self.source_distance_slider.grid(row=1, column=1, padx=10, pady=5)

        # Button to simulate and visualize the X-ray image with current settings
        self.simulate_button = ttk.Button(root, text="Simulate X-Ray Image", command=self.simulate_xray)
        self.simulate_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Initial phantom generation
        self.phantom = generate_leg_phantom()

    def update_simulation(self, event=None):
        # Display current parameter values for debugging
        print(f"Beam Energy: {self.beam_energy.get()} keV")
        print(f"Source Distance: {self.source_distance.get()} cm")
    
    def simulate_xray(self):
        # Run the X-ray simulation with current settings
        reconstructed_image = simulate_xray_image(
            self.phantom,
            self.beam_energy.get(),
            self.source_distance.get()
        )
        # Visualize the reconstructed X-ray image
        visualize_reconstructed_image(reconstructed_image)

# Run the application
root = tk.Tk()
app = XRaySimulatorApp(root)
root.mainloop()
