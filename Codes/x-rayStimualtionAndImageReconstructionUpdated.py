import tkinter as tk
from tkinter import Tk, Toplevel, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.ndimage import rotate  # For smooth angle rotation


# Function from X-ray Simulation File
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


# GUI for parameter adjustment
class XRaySimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("X-Ray Simulator - Leg Phantom")

        self.beam_energy = tk.DoubleVar(value=50.0)
        self.source_distance = tk.DoubleVar(value=100.0)
        self.phantom = generate_leg_phantom()
        self.setup_gui()

    def setup_gui(self):
        ttk.Label(self.root, text="Beam Energy (keV)").grid(row=0, column=0, padx=10, pady=5)
        self.beam_energy_slider = ttk.Scale(
            self.root, from_=30, to=100, variable=self.beam_energy, command=self.update_preview)
        self.beam_energy_slider.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Source Distance (cm)").grid(row=1, column=0, padx=10, pady=5)
        self.source_distance_slider = ttk.Scale(
            self.root, from_=50, to=200, variable=self.source_distance, command=self.update_preview)
        self.source_distance_slider.grid(row=1, column=1, padx=10, pady=5)

        self.fig, self.ax = plt.subplots(figsize=(4, 4))
        self.ax.axis('off')
        self.image_canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.image_canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.visualize_button = ttk.Button(
            self.root, text="Visualize Full Phantom Slice", command=self.open_visualization_window)
        self.visualize_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.update_preview()

    def update_preview(self, event=None):
        reconstructed_image = simulate_xray_image(
            self.phantom,
            self.beam_energy.get(),
            self.source_distance.get()
        )

        self.ax.clear()
        self.ax.imshow(reconstructed_image, cmap="gray", origin="lower")
        self.ax.set_title(
            f"Beam Energy={self.beam_energy.get():.1f} keV, "
            f"Source Distance={self.source_distance.get():.1f} cm"
        )
        self.ax.axis('off')
        self.image_canvas.draw()

    def open_visualization_window(self):
        """Open a new window to display the full visualization with details."""
        slice_index = self.phantom.shape[0] // 2
        slice_image = self.phantom[slice_index]

        # Apply transformations based on user inputs
        adjusted_image = simulate_xray_image(
            self.phantom,
            self.beam_energy.get(),
            self.source_distance.get()
        )

        # Create a new window
        new_window = tk.Toplevel(self.root)
        new_window.title("Full X-Ray Image Visualization")

        # Create the figure
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(adjusted_image, cmap="gray", origin="lower")
        ax.set_title("Full X-Ray Image")
        ax.axis("off")

        # Display beam energy, intensity, and angle
        beam_energy = self.beam_energy.get()
        source_distance = self.source_distance.get()

        # Add annotations to the plot (with black text color)
        ax.text(
            0.05, 0.95,
            f"Beam Energy: {beam_energy:.1f} keV",
            transform=ax.transAxes,
            fontsize=12,
            color="black",
            verticalalignment="top"
        )
        ax.text(
            0.05, 0.90,
            f"Source Distance: {source_distance:.1f} cm",
            transform=ax.transAxes,
            fontsize=12,
            color="black",
            verticalalignment="top"
        )

        # Embed the figure into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.get_tk_widget().pack()
        canvas.draw()


# Run the application
root = Tk()
app = XRaySimulatorApp(root)
root.mainloop()

