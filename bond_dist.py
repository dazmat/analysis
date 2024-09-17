import numpy as np
from ase.io import read

# Load the XYZ file, change the name for file you want to calculate
try:
    atoms = read('SURFACE992-pos-1.xyz')
except Exception as e:
    print(f"Error reading file: {e}")
    exit()

# Check if atoms were loaded successfully
if not atoms:
    print("No atoms were loaded from the file.")
    exit()

# Define atomic symbols for Mo and S
symbol_Mo = 'W'
symbol_S = 'S'

# Extract positions and symbols of atoms
positions = atoms.get_positions()
symbols = atoms.get_chemical_symbols()

# Print loaded atoms and their symbols
#print("Loaded atoms and their symbols:")
#for symbol, pos in zip(symbols, positions):
#    print(f"{symbol}: {pos}")

# Initialize an empty list to store the nearest Mo-S bond distances
nearest_mo_s_distances = []

# Loop through all Mo atoms to find the nearest S atom for each Mo
for i, symbol_i in enumerate(symbols):
    if symbol_i == symbol_Mo:
        # Initialise nearest distance to infinity to ensure any other values found will be smaller than this in order to append to final list
        nearest_distance = float('inf')
        for j, symbol_j in enumerate(symbols):
            if symbol_j == symbol_S:
                # Calculate the distance between atom i (Mo) and atom j (S)
                dist = np.linalg.norm(positions[i] - positions[j])
                if dist < nearest_distance:
                    nearest_distance = dist
        nearest_mo_s_distances.append(nearest_distance)

# Print the nearest Mo-S distances
print("Nearest Mo-S bond distances (in Å):")
if nearest_mo_s_distances:
    for dist in nearest_mo_s_distances:
        print(dist)
else:
    print("No Mo-S bonds found.")
