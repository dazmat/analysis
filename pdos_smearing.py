import os
import numpy as np
import sys

class pdos:
    """
    Modified from the CP2K website get_smearing_pdos.py
    Projected electronic density of states from CP2K output files.

    Attributes:
    -----------
    atom: str
        the name of the atom where the DoS is projected
    iterstep: int
        the iteration step from the CP2K job
    efermi: float
        the energy of the Fermi level [a.u]
    e: float
        (eigenvalue - efermi) in eV
    occupation: list of int
        1 for occupied state or 0 for unoccupied
    pdos: nested list of float
        projected density of states on each orbital for each eigenvalue
    tpdos: list of float
        sum of all the orbitals PDOS
    """

    def __init__(self, infilename):
        """Read a CP2K .pdos file and build a pdos instance."""
        input_file = open(infilename, 'r')

        # The first and second lines in the pdos files are headers
        firstline = input_file.readline().strip().split()
        secondline = input_file.readline().strip().split()

        # Use self. so the variables are attributes of the pdos class and can be accessed below
        self.atom = firstline[6]
        self.iterstep = int(firstline[12][:-1])  # Remove trailing comma
        self.efermi = float(firstline[15])

        # Get orbital names
        secondline[0:5] = []  # Remove non-orbital columns
        self.orbitals = secondline

        lines = input_file.readlines()
        eigenvalue = []
        self.occupation = []
        self.pdos = []
        
        # Creates a list of eigenvalues, occupation and pdos for each orbital
        for line in lines:
            data = line.split()[1:]
            eigenvalue.append(float(data.pop(0)))
            self.occupation.append(int(float(data.pop(0))))
            self.pdos.append([float(i) for i in data])

        self.e = [(x - self.efermi) * 27.2114 for x in eigenvalue]  # Convert to eV and shift to fermi energy=0
        self.tpdos = [sum(i) for i in self.pdos] # Make a total pdos by adding all orbital contributions
    # Generates npts evently spaced between min and max energy, this grid can be modfied in the main function and centres the function on energy

    def delta(self, emin, emax, npts, energy, width):
        """Return a Gaussian-like delta-function centered at energy used for smearing."""
        energies = np.linspace(emin, emax, npts)
        x = -((energies - energy) / width) ** 2
        return np.exp(x) / (np.sqrt(np.pi) * width)

    # Compute a Gaussian like delta function centered at e scaled by pdos value at e 

    def smearing(self, npts, width):
        """Return a Gaussian smeared DOS."""
        d = np.zeros(npts)
        emin = min(self.e)
        emax = max(self.e)
        for e, pd in zip(self.e, self.tpdos):
            d += pd * self.delta(emin, emax, npts, e, width)
        return d

def sum_tpdos(tpdos1, tpdos2):
    """Return the sum of two smeared PDOS."""
    return [i + j for i, j in zip(tpdos1, tpdos2)]


# Main script to handle multiple input files and apply smearing
if __name__ == "__main__":
    if len(sys.argv) >= 2:  # Handle multiple files
        smearing_width = 0.10  # Define smearing width (can be made user-configurable)

        for infilename in sys.argv[1:]:
            # Ensure the file has the correct .pdos extension
            if not infilename.endswith(".pdos"):
                print(f"Skipping {infilename}: not a .pdos file")
                continue

            try:
                # Process the PDOS file
                alpha = pdos(infilename)
                npts = len(alpha.e) * 4  # Adjust number of points for smearing
                alpha_smeared = alpha.smearing(npts, smearing_width)
                eigenvalues = np.linspace(min(alpha.e), max(alpha.e), npts)

                # Create the output filename by replacing .pdos with .dat
                base_name = os.path.splitext(infilename)[0]  # Extract base name
                output_filename = base_name + '.dat'

                # Write smeared data to .dat file
                with open(output_filename, 'w') as g:
                    for e_val, smeared_val in zip(eigenvalues, alpha_smeared):
                        g.write(f"{e_val:.6f}     {smeared_val:.6f}\n")

                print(f"Smearing applied to {infilename}, output saved to {output_filename}")

            except Exception as e:
                print(f"Error processing {infilename}: {e}")

    else:
        print("Wrong number of arguments!")
        print("Usage:")
        print("./get-smearing-pdos.py FILE1.pdos [FILE2.pdos ...]")

