# Analysis
These scripts help to analyse data obtained from calculations.

The displacement.py script takes .xyz files and calculates displacements between reference and defect structure. Usage ./displacement.py [--normalize] -ref.xyz -def.xyz

The bader.py script takes .dat files resulting from Bader charge analysis using the Henkleman code and calculates effective charge differences between reference and defect. Usage ./bader.py -ref.dat -def.dat

The pdos_smearing.py script was modified using scripts from the CP2K website for outputting the smeared pdos files (in .dat) format. Implemented for up to 3 elements, can be easily modified for more. Takes in .pdos files in CP2K format, outputs .dat smeared files with same filename as .pdos files. The smearing parameter is defauly 0.1, which can be changed, as well as, the size of the sampling grid. Usage: ./pdos_smearing.py -file1.pdos -file2.pdos -... Output file1.dat file2.dat

The pdos_plot.py script takes .dat smeared pdos files and plots them. Usage ./pdos_plot.py -file1.dat -file2.dat ...

The bond_dist.py script calculates bond distances in your structure between nearest neighbours, I havent yet implemented usage with command line parsing so have to change the name of .xyz file in script to calculate for desired structure
