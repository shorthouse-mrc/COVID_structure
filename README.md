# COVID_structure
Files pertaining to Shorthouse et al 2021, COVID manuscript

Scripts for reproducing mutant calcualtions in SARS-CoV-2. Minimal workflow involves: 

1) Energy Minimize the WT structure using the "RepairPDB" command
2) Mutate the WT structure at every position using the "PositionScan" command
3) Perform the analysis

The WT structure file is provided (6vxx.pd)

To energy minimize the structure:

$python Foldx_repair6.py 6vxx.pdb

Output: "6vxx_preRepair_Repair.pdb" an energy minimized structure

To calculate the mutational DG:

$python Foldx_positionscanall.py 6vxx_preRepair_Repair.pdb A

Where A represents the chain ID that you want to calculate.


Output: "PS_6vxx_preRepair_Repair_scanning_output.txt"

Calculations for the whole structure will take ~1 week on a 3 Ghz compute node.
