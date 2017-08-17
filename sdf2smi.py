# Import modules
import os
import re
import sys
from subprocess import call, check_output

########################################################################################################################################
# This script was originally created for DrugBank SDF files. Other databases (PubChem, CheMBL) might have different fields to describe
# molecules names. Users should check if correct_name() applies to specific cases.
########################################################################################################################################

# This script has two functions that:
# 1) sdf2smi() converts an SDF file to SMI using OpenBabel
# 2) correct_names() corrects the names on the SMI file (GENERIC NAMES field of DrugBank files). 
## It replaces spaces with '_', removes digits and [NO_NAME] entries.

### Usage: python sdf2smi.py 'sdf_file.sdf' 'smi_file.smi' 'corrected_smi_file.smi'


def sdf2smi(sdf):
	"""Converts SDF to SMI using OpenBabel"""

	call('(obabel "%s" -O "%s" -r --append "DATABASE_ID")' % (sdf_file, smi_file), shell=True) # Calls OpenBabel to convert sdf to smi


def correct_names(smi, correct):
	with open(smi) as f: # Input Drugbank molecules. 
                                    # Some structures on the .sdf file didn't have SMILES representations.
				    # Openbabel was used to convert sdf to smiles
		with open(correct, 'w') as g: # Corrected output (Smiles names - All spaces on names were replaced by underscores)
			smiles = []
			generic_names = []

			for line in f:
				s = line.split()[0]
				n = '_'.join(line.split()[1:])

				generic_names.append(re.sub(r'((\d+)|(NO_NAME])|(\D))*_', '', n)) # Correct generic names
				smiles.append(s)
			zipped = zip(smiles,generic_names)
			g.write('\n'.join('%s %s' % x for x in zipped)) # Write results to file


if __name__ == '__main__':
	sdf_file = sys.argv[1]
	smi_file = sys.argv[2]
	corrected_file = sys.argv[3]

sdf2smi(sdf_file)
correct_names(smi_file, corrected_file)
os.remove(smi_file)
