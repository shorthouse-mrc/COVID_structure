import os, sys, glob
import statistics
### Summarize the energies of every combination of variant mutations

## Output file name
mutfilename = "Variant_mutational_energy_Foldx_summary.txt"
mutationfile = open(mutfilename, "w")
mutationfile.write("Mutation\tddG\n")
mutationfile.close()

## Find each output energy file from the nested folders and get the DDG
mutationfile = open(mutfilename, "a+")
for filename in sorted(glob.glob("./*/Dif*.fxout")):
    energy_list = []
    mutationname = filename.split("/")[1]
    f = open(filename)
    lines = f.readlines()
    f.close()
    for line in lines:
        linecontents = line.split("\t")
        if linecontents[0].endswith(".pdb"):
            energy = linecontents[1]
            energy_list.append(float(energy))
    DDG = statistics.mean(energy_list)
## Write the DDG + mutation to the outputfile
    mutationfile.write(mutationname + "\t" + str(DDG) + "\n")
mutationfile.close()
