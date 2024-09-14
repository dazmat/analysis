import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def plot_dat_files(file_list):
    """
    Reads all .dat files passed as command-line arguments and plots their data.
    Files with 'BETA' in the filename will have their DOS values multiplied by -1.

    Args:
    file_list (list of str): List of .dat file paths passed as arguments.

    Returns:
    None
    """
    
    # Check if any .dat files are passed
    if not file_list:
        print("No .dat files provided.")
        return
    
    plt.figure(figsize=(5, 5), dpi=400)
    plt.xlabel('Energy (eV)', fontsize=16)

    # Color palette for multiple files
    colors = ['tab:blue', 'tab:blue', 'tab:red', 'tab:red', 'tab:purple', 'tab:purple']
    color_index = 0  # To loop over colors for each file

    # Plot data from each .dat file
    for idx, file in enumerate(file_list):
        if not file.endswith('.dat'):
            print(f"Skipping non-dat file: {file}")
            continue
        
        # Check if file exists
        if not os.path.exists(file):
            print(f"File not found: {file}")
            continue

        # Read the data from the .dat file
        data = np.loadtxt(file)
        x = data[:, 0]  # First column is energy (x-axis)
        y = data[:, 1]  # Second column is DOS (y-axis)
        
        # Check if 'BETA' is in the filename and multiply y by -1 if true
        if 'BETA' in os.path.basename(file).upper():
            y = -y  # Multiply DOS values by -1 for BETA files
            print(f"Multiplying values of {file} by -1.")

        # Plot the data with customized settings
        plt.plot(x, y, '-', alpha=1, color=colors[color_index % len(colors)], linewidth=2, label=os.path.basename(file).split('.')[0])
        color_index += 1

    # Set x and y limits
    plt.xlim(-3, 4)
    plt.ylim(-70, 70)

    # Set x-axis ticks
    plt.xticks(np.arange(-3, 5, 1), fontsize=15)
    plt.gca().xaxis.set_minor_locator(MultipleLocator(0.2))  # Minor ticks

    # Add legend at the lower center
    plt.legend(fontsize=8, loc='lower center', ncol=3)

    # Adjust layout for better spacing
    plt.tight_layout()
    plt.savefig('pdos_plot.png', transparent=True, dpi=200)

    # Display the plot
    plt.show()


if __name__ == "__main__":
    # Get the list of .dat files from command line arguments
    dat_files = sys.argv[1:]
    
    # Call the function to plot the .dat files
    plot_dat_files(dat_files)
