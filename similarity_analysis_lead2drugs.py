# Import modules
from subprocess import call, check_output
import re
import sys
import pandas as pd
import os
#from pubchempy import * For PubChem similarity analysis

# Things to check later
# 1) Update the summary.csv on the fly without creating a raw_score file
# 2) How can I use this for diverse analysis? The filtering to csv might be useful to visualize the results
# 3) Users MUST generate FINGERPRINTS (.fs file) BEFORE running this script. Automatic fingerprinting will be added in the future
# 4) Most of the arguments and variables are still hardcoded. More flexibility must be implemented.

# USAGE: python similarity_analysis.py 'sdf_file.sdf' 'smi_file.smi' 'corrected_smi_file.smi'

########################################################################################################################################
# This script was originally created for DrugBank SDF files. Other databases (PubChem, CheMBL) might have different fields to describe
# molecules names. Users should check if correct_name() applies to specific cases.
########################################################################################################################################

# This script has two functions that:
# 1) sdf2smi() converts an SDF file to SMI using OpenBabel
# 2) correct_names() corrects the names on the SMI file (GENERIC NAMES field of DrugBank files). 
## It replaces spaces with '_', removes digits and [NO_NAME] entries.


def sdf2smi(sdf):
	"""Converts SDF to SMI using OpenBabel"""

	call('(obabel "%s" -O "%s" --append "GENERIC_NAME")' % (sdf_file, smi_file), shell=True) # Calls OpenBabel to convert sdf to smi


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

				generic_names.append(re.sub(r'((\d+)|(NO_NAME]))_', '', n)) # Correct generic names
				smiles.append(s)
			zipped = zip(smiles,generic_names)
			g.write('\n'.join('%s %s' % x for x in zipped)) # Write results to file

if __name__ == '__main__':
	sdf_file = sys.argv[1]
	smi_file = sys.argv[2]
	corrected_file = sys.argv[3]

####################################################################################
#    This script finds the 5 most similar compounds to a query list of molecules   #
####################################################################################  

#query_file = None
#fs_file = None # FP2 fingerprints file
#num_of_similar_compounds = None # max number of similar compounds to find

with open('small_sample_20.smi') as x: # Query SMILE file (format: smiles compd_name)
	smiles = [line for line in x] 

def similarity_search(smi):
	""" This function calls openbabel similarity search on the list of SMILES submitted by the user"""

	fs_file = 'fda_corrected.fs' # FP2 fingerprints file
	num_of_similar_compounds = '5' # max number of similar compounds to find
	
	
	fda_out = 'tanimoto_raw.out' # Output file for FDA approved drugs
	#pubchem_out = '.similar_pubchem.out' # Output file for PubChem similarity analysis

	with open(fda_out, 'w') as y:
		for mol in smi:

			#### Similarity Search using DrugBank All/Approved Drugs (LOCALLY) ####

			output_message = 'Compound ' + str(mol)
			a = check_output('(obabel %s -otxt -S "%s" -at%s -aa)' % (fs_file, mol, num_of_similar_compounds), shell=True)
			y.write(('%s%s') % (output_message, a)) # Output format: query_SMILES;similar_compounds;tanimoto_score


	print ('Similarity against FDA dataset complete. Our gremlins are working on the output file. Please wait...')
		
			#### Similarity Search on PubChem server (NOT IMPLEMENTED YET) ####

	#with open(pubchem_out, 'w') as g:
		#for mol in smi:

			#output_message = 'Calculating similars to ' + str(mol) + '\n'
			#a = get_compounds(mol, 'smiles', searchtype='similarity', listkey_count=10, Threshold=80)
			#g.write(('%s%s%s') % (output_message, a, '\n')) # Output format: query_SMILES;similar_compounds;tanimoto_score

	#print ('PubChem analysis complete. The results were store in %s') % (pubchem_out)

# Call function
sdf2smi(sdf_file)
correct_names(smi_file, corrected_file)
os.remove(smi_file)
similarity_search(smiles)

##################################################################################################################
#        This code formats the similarity analysis scores (tanimoto_raw.out file) into a csv file       #
##################################################################################################################

dt = [] # Creates a list to store dictionariess

with open('tanimoto_raw.out') as f: # Opens similarity output file

	compound = None
	smiles = None

	for line in f:
		if line.startswith('Compound'):
			ZINC_id = line.split()[2]
			smi = line.split()[1]
			compound = ZINC_id
			smiles = smi			
		else:
			similar,score = line.split()
			dt.append({'Tanimoto_score': format(float(score), '.2f'), 'Similar': similar, })
			dt[-1]['Compound_ID'] = compound
			dt[-1]['Compound_smiles'] = smiles

# Create dataframe
df = pd.DataFrame(dt)

# Save to csv file
#os.remove('tanimoto_raw.out')
df.to_csv('similarity_summary.csv')
print 'Your summary is ready!'
