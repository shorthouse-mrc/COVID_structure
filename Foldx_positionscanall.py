import sys, os

## Set up an amino acid conversion dictionary
aminoacid_dict = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}

def aaconvert(x):
    if len(x) % 3 != 0: 
        raise ValueError('Input length should be a multiple of three')

    y = ''
    for i in range(len(x)//3):
            y += aminoacid_dict[x[3*i:3*i+3]]
    return y

## Pdbfile is the first input, second input is the chain to run positionscan on

pdbfile = sys.argv[1]

chainid = sys.argv[2]

## Open the pdb file
with open(pdbfile) as f:
    pdbcontent = f.readlines()
 
## Go through each line and get the WT residue, then construct the foldx string to mutate it to everything, add to a list
mutation_list = []   
for line in pdbcontent:
    line = line.strip()
    if line.startswith("ATOM"):
        linecontents = [line[:6], line[6:11], line[12:16], line[17:20], line[21], line[22:26], line[30:38], line[38:46], line[46:54]]
        atomtype = linecontents[2].strip()
        if atomtype == "CA":
            if linecontents[4].strip() == chainid:
                mutationcode = aaconvert(linecontents[3].strip()) + linecontents[4].strip() + linecontents[5].strip() + "a"
                mutation_list.append(mutationcode)

## Join the foldx list to have one huge input command
mutationstring = ",".join(mutation_list)


## Construct and run the foldx command
foldxcommand = "foldx --command=PositionScan --pdb={0} --ionStrength=0.05 --pH=7 --water=CRYSTAL --vdwDesign=2 --positions={1} --pdbHydrogens=false"\
.format(sys.argv[1], mutationstring)

os.system(foldxcommand)
