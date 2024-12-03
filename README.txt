Requirements

numpy==1.24.3
matplotlib==3.7.1
scipy==1.11.2
tk==0.1.0


Prerequisites, Packages, and Libraries
Libraries:
	numpy: For numerical operations.
	matplotlib: For visualizing cross-sections, projections, and attenuation profiles.
	scipy: For advanced mathematical operations like rotations.
	tkinter: For creating the graphical user interface (GUI).
Installation:
	All libraries can be installed via pip:
	pip install numpy matplotlib scipy tk

Install Python:
Install Python version 3.11.5 or newer from python.org.
Verify the installation by running:
	python --version
or, if python points to Python 2 on your system:
	python3 --version
Set Up a Virtual Environment:
Open a terminal or command prompt and run:
	python -m venv venv
If that doesn't work, try:
	python3 -m venv venv
Activate the Virtual Environment:
Windows:
	venv\Scripts\activate
macOS/Linux:
	source venv/bin/activate
Install Required Libraries:
Once the virtual environment is activated, install the required dependencies:
	pip install numpy matplotlib scipy tk
Run the Program:
Navigate to the folder containing your Python scripts:
	cd <path_to_your_code>
Run the main script to execute the program:
	python <main_script_filename>.py


Downloading and Using with a Dataset

Dataset:
	The phantom generation is simulated within the code, so no external dataset is required.

Optional Dataset Usage:
	If you plan to replace the phantom with real imaging data:
	Ensure the data is stored in a compatible format (e.g., .npy for NumPy arrays).
	Modify the generate_leg_phantom function to load the dataset instead of generating 	synthetic data.
	example: phantom = np.load('path_to_dataset.npy')

How to Replicate Results in the Report

Contrast Analysis:
	Use the function calculate_contrast to compute the contrast for specific slices of the phantom.

X-ray Projections:
	Run the analyze_contrast_and_angle function to generate projections at 0°, 45°, 90°, and 135°.

Splits (Orthogonal and Angled):
	Simulate splits using add_orthogonal_split and add_angled_split and visualize the results with visualize_phantom.

GUI Interaction:
	Open the GUI to explore how beam energy, X-ray angle, and source distance affect the phantom image.