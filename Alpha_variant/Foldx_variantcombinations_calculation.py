import os, sys, shutil
import itertools
from Bio.PDB.PDBParser import PDBParser
import multiprocessing




## Get files
variantfile = sys.argv[1]
pdbfile = sys.argv[2]

## Open variants and get each individual variant
with open(variantfile) as f:
    variants = f.readlines()
variants = [x.strip() for x in variants] 

variants_nocomments = []
for variant in variants:
    if variant.startswith("#"):
        continue
    else:
        variants_nocomments.append(variant)

variants = variants_nocomments
for variant in variants:
    variant_index = int(variant[1:-1])

## Read in the pdb file
p = PDBParser()
pdbstructure = p.get_structure("pdbstructure", pdbfile)

## Generate each combination of variants
variants_combinations = []
for L in range(0, len(variants)+1):
    for subset in itertools.combinations(variants, L):
        variants_combinations.append(subset)

## Define a function for calculating the mutational energy of a combination of mutations
def mutatecombination(combinationtuple):
    logfile = "LOG_MUT_" + str(len(combinationtuple)) + "_" + "_".join(combinationtuple) + ".log"
    mutationfile = "individual_list_" + str(len(combinationtuple)) + "_" +  "_".join(combinationtuple) + ".txt"
    os.makedirs(str(len(combinationtuple)) + "_" + "_".join(combinationtuple))#, exist_ok = True)
    os.chdir(str(len(combinationtuple)) + "_" + "_".join(combinationtuple))
    shutil.copyfile("../"+pdbfile, "./"+pdbfile)
    mutationstrings  = []
    for item in combinationtuple:
        AAfrom = item[0]
        AAto = item[-1]
        residue = item[1:-1]
        mutationstrings.append("{0}A{1}{2}".format(AAfrom, residue, AAto))
    mutationcombine = ",".join(mutationstrings)
#### Make the mutationtuple here from http://foldxsuite.crg.eu/parameter/mutant-file ####
    
    mutwrite = open(mutationfile, "w+")
    mutwrite.write(("""{0};""").format(mutationcombine))
    mutwrite.close()
    
    
    foldxcommand = (("foldx --command=BuildModel --pdb=../{0} --mutant-file={1} --ionStrength=0.05 --pH=7 --vdwDesign=2 --pdbHydrogens=false --numberOfRuns=15 > {2}").format(pdbfile, mutationfile, logfile))
    os.system(foldxcommand)
    os.chdir("../")
  
## Make a list of all the cominbations that exist in the structure
variant_list = []
for item in variants_combinations:
    if len(item) != 0:
        variant_list.append(item)	

## Run the function on every variants combination of mutations
def pool_handler():
    p = multiprocessing.Pool(32)
    p.map(mutatecombination, variant_list)
    
if __name__ == '__main__':
    pool_handler()   




