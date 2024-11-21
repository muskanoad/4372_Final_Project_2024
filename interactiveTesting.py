import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt

# Function to simulate X-ray image
def generate_xray_image(energy_level, mu_value, angle):
    x = np.linspace(0, 10, 100)
    y = np.sin(x + np.radians(angle)) * energy_level / 100 * mu_value
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f'Energy: {energy_level} kVp, μ-value: {mu_value}, Angle: {angle}°')
    plt.title(f'X-ray Simulation\nEnergy: {energy_level} kVp, Angle: {angle}°')
    plt.xlabel('Position')
    plt.ylabel('X-ray Intensity')
    plt.legend()
    plt.grid(True)
    plt.show()

# Create a window using Tkinter
window = tk.Tk()
window.title("X-ray Machine Interactive Testing")

# Add a label
label = tk.Label(window, text="Select Energy Level (kVp), μ-value, and Angle for X-ray Simulation")
label.pack(pady=10)

# Energy Level Dropdown
energy_label = tk.Label(window, text="Energy Level (kVp):")
energy_label.pack(pady=5)

energy_levels = [50, 75, 100, 125, 150]
energy_dropdown = ttk.Combobox(window, values=energy_levels)
energy_dropdown.set(100)  # Default value
energy_dropdown.pack(pady=5)

# Mu Value Dropdown
mu_label = tk.Label(window, text="μ-value:")
mu_label.pack(pady=5)

mu_values = [0.1, 0.5, 1.0, 1.5, 2.0]
mu_dropdown = ttk.Combobox(window, values=mu_values)
mu_dropdown.set(1.0)  # Default value
mu_dropdown.pack(pady=5)

# Angle Dropdown
angle_label = tk.Label(window, text="Angle (°):")
angle_label.pack(pady=5)

angles = [0, 15, 30, 45, 60]
angle_dropdown = ttk.Combobox(window, values=angles)
angle_dropdown.set(0)  # Default value
angle_dropdown.pack(pady=5)

# Function to update plot based on selected values
def on_button_click():
    energy_level = int(energy_dropdown.get())
    mu_value = float(mu_dropdown.get())
    angle = int(angle_dropdown.get())
    generate_xray_image(energy_level, mu_value, angle)

# Add a button to generate the X-ray image
button = tk.Button(window, text="Generate X-ray Image", command=on_button_click)
button.pack(pady=20)

# Run the Tkinter event loop
window.mainloop()
