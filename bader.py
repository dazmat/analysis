import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import argparse

from mpl_toolkits.mplot3d import Axes3D

def calculate_charge_differences(ref_file, def_file):
    # Load data for reference and defective structures
    data_ref = pd.read_csv(ref_file, delim_whitespace=True)
    data_def = pd.read_csv(def_file, delim_whitespace=True)
    
    # Extract and convert coordinates from Bohr to Angstrom
    xyz_ref = data_ref.iloc[:, [1, 2, 3]].apply(pd.to_numeric, errors='coerce').values * 0.529177
    xyz_def = data_def.iloc[:, [1, 2, 3]].apply(pd.to_numeric, errors='coerce').values * 0.529177

    # Extract Bader charges
    charge_ref = data_ref.iloc[:, 4].values
    charge_def = data_def.iloc[:, 4].values

    # Initialize list to hold charge differences for defective atoms
    charge_differences = np.full(len(xyz_def), np.nan)

    # Calculate charge differences for atoms in the defective structure
    for j, (x2, y2, z2) in enumerate(xyz_def):
        min_displacement = float('inf')
        closest_charge = np.nan
        
        for i, (x1, y1, z1) in enumerate(xyz_ref):
            displacement = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            
            if displacement < min_displacement:
                min_displacement = displacement
                closest_charge = charge_ref[i]
        
        if not np.isnan(closest_charge):
            charge_differences[j] = charge_def[j] - closest_charge

    print(f"Charge differences for defective atoms: {charge_differences}")

    # 3D Plot with heatmap for charge differences
    plot_charge_differences(xyz_def, charge_differences)

def plot_charge_differences(positions, charge_differences):
    # Extract x, y, z coordinates
    x = positions[:, 0]
    y = positions[:, 1]
    z = positions[:, 2]

    # Create 3D plot
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(x, y, z, c=charge_differences, cmap='coolwarm', s=50, edgecolor='k')

    # Add color bar
    cbar = plt.colorbar(sc, fraction=0.03, pad=0.06)
    cbar.set_label('Charge Difference (e)', rotation=270, labelpad=15)
    
    ax.grid(False)
    ax.set_facecolor('white')
    
    # Labels and title
    ax.set_xlabel('X (Å)')
    ax.set_ylabel('Y (Å)')
    ax.set_zlabel('Z (Å)')
    ax.view_init(elev=90, azim=-90)
    plt.tight_layout()

    plt.show()

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Script usage: python bader.py ref.dat def.dat, will output effective charges.')
    parser.add_argument('ref_file', type=str, help='Reference Bader file (e.g., ref.dat)')
    parser.add_argument('def_file', type=str, help='Defective Bader file (e.g., def.dat)')
    
    # Get arguments
    args = parser.parse_args()
    
    # Call the calculation function
    calculate_charge_differences(args.ref_file, args.def_file)

if __name__ == '__main__':
    main()

