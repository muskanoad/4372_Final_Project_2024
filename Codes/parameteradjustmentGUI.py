import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

# Phantom generation function (from previous step)
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

# Visualization function for a specific slice
def visualize_phantom_slice(phantom, slice_index):
    plt.imshow(phantom[slice_index], cmap="gray")
    plt.title(f"Leg Phantom Slice at Z = {slice_index}")
    plt.colorbar(label="Attenuation Value")
    plt.show()

# GUI for parameter adjustment
class XRaySimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("X-Ray Simulator - Leg Phantom")

        # Default values for parameters
        self.beam_energy = tk.DoubleVar(value=50.0)
        self.xray_angle = tk.DoubleVar(value=0.0)
        self.source_distance = tk.DoubleVar(value=100.0)

        # GUI Layout
        # Beam energy adjustment
        ttk.Label(root, text="Beam Energy (keV)").grid(row=0, column=0, padx=10, pady=5)
        self.beam_energy_slider = ttk.Scale(root, from_=30, to=100, variable=self.beam_energy, command=self.update_simulation)
        self.beam_energy_slider.grid(row=0, column=1, padx=10, pady=5)

        # X-ray angle adjustment
        ttk.Label(root, text="X-Ray Angle (degrees)").grid(row=1, column=0, padx=10, pady=5)
        self.xray_angle_slider = ttk.Scale(root, from_=0, to=180, variable=self.xray_angle, command=self.update_simulation)
        self.xray_angle_slider.grid(row=1, column=1, padx=10, pady=5)

        # Source distance adjustment
        ttk.Label(root, text="Source Distance (cm)").grid(row=2, column=0, padx=10, pady=5)
        self.source_distance_slider = ttk.Scale(root, from_=50, to=200, variable=self.source_distance, command=self.update_simulation)
        self.source_distance_slider.grid(row=2, column=1, padx=10, pady=5)

        # Button to visualize the phantom with current settings
        self.visualize_button = ttk.Button(root, text="Visualize Phantom Slice", command=self.visualize_phantom)
        self.visualize_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Initial phantom generation
        self.phantom = generate_leg_phantom()

    def update_simulation(self, event=None):
        # Display current parameter values (for debugging)
        print(f"Beam Energy: {self.beam_energy.get()} keV")
        print(f"X-Ray Angle: {self.xray_angle.get()} degrees")
        print(f"Source Distance: {self.source_distance.get()} cm")
        # Additional simulation updates can be added here

    def visualize_phantom(self):
        # Visualize a middle slice of the phantom
        slice_index = self.phantom.shape[0] // 2
        visualize_phantom_slice(self.phantom, slice_index)

# Run the application
root = tk.Tk()
app = XRaySimulatorApp(root)
root.mainloop()
