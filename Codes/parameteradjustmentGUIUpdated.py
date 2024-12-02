import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.ndimage import rotate

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

# Apply transformations for angle, beam energy, and distance
def adjust_phantom_slice(slice_image, angle, beam_energy, source_distance):
    # Determine the padding size to avoid cropping during rotation
    pad_x = slice_image.shape[0] // 2
    pad_y = slice_image.shape[1] // 2

    # Pad the slice symmetrically
    padded_slice = np.pad(slice_image, ((pad_x, pad_x), (pad_y, pad_y)), mode='constant', constant_values=0)

    # Rotate the padded slice
    rotated_slice = rotate(padded_slice, angle, reshape=False, mode='nearest')

    # Crop back to the original size
    start_x = (rotated_slice.shape[0] - slice_image.shape[0]) // 2
    start_y = (rotated_slice.shape[1] - slice_image.shape[1]) // 2
    cropped_slice = rotated_slice[start_x:start_x + slice_image.shape[0], start_y:start_y + slice_image.shape[1]]

    # Adjust intensity based on beam energy and source distance
    attenuation_factor = (beam_energy / 100) * (200 / source_distance)
    adjusted_slice = cropped_slice * attenuation_factor

    # Normalize the values for display (to avoid clipping or too dark visuals)
    adjusted_slice = np.clip(adjusted_slice / adjusted_slice.max(), 0, 1)
    return adjusted_slice



# GUI for parameter adjustment
class XRaySimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("X-Ray Simulator - Leg Phantom")

        self.beam_energy = tk.DoubleVar(value=50.0)
        self.xray_angle = tk.DoubleVar(value=0.0)
        self.source_distance = tk.DoubleVar(value=100.0)

        self.phantom = generate_leg_phantom()
        self.setup_gui()

    def setup_gui(self):
        ttk.Label(self.root, text="Beam Energy (keV)").grid(row=0, column=0, padx=10, pady=5)
        self.beam_energy_slider = ttk.Scale(
            self.root, from_=30, to=100, variable=self.beam_energy, command=self.update_preview)
        self.beam_energy_slider.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="X-Ray Angle (degrees)").grid(row=1, column=0, padx=10, pady=5)
        self.xray_angle_slider = ttk.Scale(
            self.root, from_=0, to=180, variable=self.xray_angle, command=self.update_preview)
        self.xray_angle_slider.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Source Distance (cm)").grid(row=2, column=0, padx=10, pady=5)
        self.source_distance_slider = ttk.Scale(
            self.root, from_=50, to=200, variable=self.source_distance, command=self.update_preview)
        self.source_distance_slider.grid(row=2, column=1, padx=10, pady=5)

        self.fig, self.ax = plt.subplots(figsize=(4, 4))
        self.ax.axis('off')
        self.image_canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.image_canvas.get_tk_widget().grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.visualize_button = ttk.Button(
            self.root, text="Visualize Full Phantom Slice", command=self.open_visualization_window)
        self.visualize_button.grid(row=4, column=0, columnspan=3, pady=10)

        self.update_preview()

    def update_preview(self, event=None):
        slice_index = self.phantom.shape[0] // 2
        slice_image = self.phantom[slice_index]

        adjusted_image = adjust_phantom_slice(
            slice_image,
            angle=self.xray_angle.get(),
            beam_energy=self.beam_energy.get(),
            source_distance=self.source_distance.get()
        )

        self.ax.clear()
        self.ax.imshow(adjusted_image, cmap="gray", origin="lower")
        self.ax.set_title(
            f"Beam Energy={self.beam_energy.get():.1f} keV, "
            f"Angle={self.xray_angle.get():.1f}°, Distance={self.source_distance.get():.1f} cm"
        )
        self.ax.axis('off')
        self.image_canvas.draw()

    def open_visualization_window(self):
        """Open a new window to display the full visualization with details."""
        slice_index = self.phantom.shape[0] // 2
        slice_image = self.phantom[slice_index]

        # Apply transformations based on user inputs
        adjusted_image = adjust_phantom_slice(
            slice_image,
            angle=self.xray_angle.get(),
            beam_energy=self.beam_energy.get(),
            source_distance=self.source_distance.get()
        )

        # Create a new window
        new_window = tk.Toplevel(self.root)
        new_window.title("Phantom Slice Visualization")

        # Create the figure
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(adjusted_image, cmap="gray", origin="lower")
        ax.set_title("Full Phantom Slice Visualization")
        ax.axis("off")

        # Display beam energy, intensity, and angle
        beam_energy = self.beam_energy.get()
        xray_angle = self.xray_angle.get()
        source_distance = self.source_distance.get()

        # Add annotations to the plot
        ax.text(
            0.05, 0.95,
            f"Beam Energy: {beam_energy:.1f} keV",
            transform=ax.transAxes,
            fontsize=12,
            color="white",
            verticalalignment="top"
        )
        ax.text(
            0.05, 0.90,
            f"Angle: {xray_angle:.1f}°",
            transform=ax.transAxes,
            fontsize=12,
            color="white",
            verticalalignment="top"
        )
        ax.text(
            0.05, 0.85,
            f"Source Distance: {source_distance:.1f} cm",
            transform=ax.transAxes,
            fontsize=12,
            color="white",
            verticalalignment="top"
        )

        # Embed the figure into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.get_tk_widget().pack()
        canvas.draw()


# Run the application
root = tk.Tk()
app = XRaySimulatorApp(root)
root.mainloop()


