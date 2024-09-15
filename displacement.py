import math
import numpy as np
import matplotlib.pyplot as plt
from ase import Atoms
from ase.io import write, read
from ase.neighborlist import NeighborList
from mpl_toolkits.mplot3d import Axes3D
import argparse
import sys

#this script takes a reference and defect .xyz files, reads them with ase, identifys matching items (if no of atoms is not equal as in vacancy systems), calculates their (min) displacement. Bcos of course if you take two far away atoms their disps will be very high. Then plots it into a 3D graph. you can really change these settings if you want

#normalize in this function is for user to identify, to normalise heat map
def displacement(reference_file, defective_file, normalize=False):
    # Read the structures using ase
    pristine_atoms = read(reference_file, format='xyz')
    defective_atoms = read(defective_file, format='xyz')

    # Extract the atomic positions
    pristine_positions = pristine_atoms.get_positions()
    defective_positions = defective_atoms.get_positions()

    # Initialize list to hold displacements for defective atoms, initial values are set to NaN, hence np.nan, the shape of array is same as def pos
    displacements = np.full(len(defective_positions), np.nan)

    # Create a neighbor list to detect close atomswith cutoff radii for atoms, this 1.5 can be changed but should be okay for most systems unless you have really big displacements
    cutoffs = [1.5] * len(pristine_atoms)  # Example cutoff for neighbor search
    nl = NeighborList(cutoffs, self_interaction=False, bothways=True)
    nl.update(pristine_atoms)

    # Calculate displacements for atoms in the defective structure
    for j, (x2, y2, z2) in enumerate(defective_positions):#iterates through atom j for a;; its positions in def structure
        min_displacement = float('inf')#initialised to infinitely large val
        
        for i, (x1, y1, z1) in enumerate(pristine_positions): #loop through pris atoms the same
            displacement = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) #calulctaes disps using formula
            
            if displacement < min_displacement:
                min_displacement = displacement #find min disp
        
        displacements[j] = min_displacement

    print(f"Displacements for defective atoms: {displacements}")

    # Normalize displacements if requested
    if normalize:
        displacements = (displacements - np.min(displacements)) / (np.max(displacements) - np.min(displacements))

    # 3D Plot with heatmap for displacement
    plot_displacements(defective_positions, displacements, normalize)

def plot_displacements(defective_positions, displacements, normalize):
    # Extract x, y, z coordinates from defective structure
    x = defective_positions[:, 0]
    y = defective_positions[:, 1]
    z = defective_positions[:, 2]

    # Create 3D plot with color based on displacements (heatmap)
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot using displacements as color
    sc = ax.scatter(x, y, z, c=displacements, cmap='hot', s=50, edgecolor='k')

    # Add color bar to represent the heatmap scale
    if normalize:
        cbar = plt.colorbar(sc, fraction=0.03, pad=0.06)#change fraction to change size of the bar
        cbar.set_label('Normalized Displacement', rotation=270, labelpad=15)
    else:
        cbar = plt.colorbar(sc, fraction=0.03, pad=0.06)
        cbar.set_label('Displacement (Å)', rotation=270, labelpad=15)
    
    ax.grid(False)
    ax.set_facecolor('white')
    
    # Labels and title
    ax.set_xlabel('X (Å)')
    ax.set_ylabel('Y (Å)')
    ax.set_zlabel('Z (Å)')
    ax.view_init(elev=90, azim=-90)#change rotation of the lattice depending on how the plot is to be viewed
    plt.tight_layout()
    
    plt.savefig('displacement.png', transparent=True, dpi=200)

    plt.show()

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Usage ./displacement.py [--normalize] pristine.xyz defect.xyz')
    parser.add_argument('files', nargs=2, help='The reference and defective .xyz files')
    parser.add_argument('--normalize', action='store_true', help='Normalize the displacement values between 0 and 1')
    args = parser.parse_args()

    reference_file, defective_file = args.files
    normalize = args.normalize

    # Call the function to plot the displacement from the xyz files
    displacement(reference_file, defective_file, normalize)
