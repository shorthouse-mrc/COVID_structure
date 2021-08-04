import os
import sys
from shutil import copyfile
import shutil

##PDB file is the input file
pdbfile = sys.argv[1]

# repair the pdb file 6 times

pdbsplit = pdbfile.split(".")[0]
# Set up files (retain copy of original)

prerepairfile = pdbsplit + "_preRepair." + pdbfile.split(".")[1]
copyfile(pdbfile, prerepairfile)

# Run repair number one
repaircommand = "foldx --command=RepairPDB --pdb=%s --ionStrength=0.05 --pH=7 --vdwDesign=2 --pdbHydrogens=false > repair_1.txt" % (prerepairfile)
print(repaircommand)
os.system(repaircommand)

repairfile = prerepairfile.split(".")[0] + "_Repair." + prerepairfile.split(".")[1]
repairfile2 = repairfile.split(".")[0] + "_Repair." + repairfile.split(".")[1]


# Run loop of 5 further repair commands
repaircommand = "foldx --command=RepairPDB --pdb=%s --ionStrength=0.05 --pH=7 --vdwDesign=2 --pdbHydrogens=false" % (repairfile)
for repair in range(0,4):
    print(repaircommand + " > repair_%s.txt" % (str(int(repair)+2)))
    os.system(repaircommand + " > repair_%s.txt" % (str(int(repair)+2)))
    shutil.move(repairfile2, repairfile)

