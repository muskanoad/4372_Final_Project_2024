import numpy as np
import matplotlib.pyplot as plt

def generate_xray_image(energy_level, mu_value, angle=0, distance=1):
    x = np.linspace(0, 10, 100)
    y = np.sin(x + np.radians(angle)) * energy_level / 100 * mu_value / distance
    plt.plot(x, y)
    plt.title(f'X-ray Image\nEnergy Level: {energy_level} kVp, μ-Value: {mu_value}, Angle: {angle}, Distance: {distance}')
    plt.xlabel('X-axis')
    plt.ylabel('Intensity')
    plt.show()

def simulate_leg_fracture(angle):
    x = np.linspace(0, 10, 100)
    y = np.piecewise(x, [x < 5, x >= 5], [lambda x: np.sin(x), lambda x: np.sin(x + np.radians(angle))])
    plt.plot(x, y)
    plt.title(f'Leg Phantom with Fracture at Angle: {angle}°')
    plt.xlabel('X-axis')
    plt.ylabel('Intensity')
    plt.show()

def validate_acquisition_parameters(energy_levels, angles, distances):
    for energy in energy_levels:
        for angle in angles:
            for distance in distances:
                generate_xray_image(energy, mu_value=1.0, angle=angle, distance=distance)

def validate_leg_fractures(angles):
    for angle in angles:
        simulate_leg_fracture(angle)

# Example values for validation
energy_levels = [50, 100, 150]
angles = [0, 30, 60]
distances = [1, 1.5, 2]
fracture_angles = [15, 30, 45]

# Validate acquisition parameters
print("Validating acquisition parameters...")
validate_acquisition_parameters(energy_levels, angles, distances)

# Validate leg fractures
print("Validating leg fractures...")
validate_leg_fractures(fracture_angles)
