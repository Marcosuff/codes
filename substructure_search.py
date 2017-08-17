# Import modules
from subprocess import call, check_output
import re
import sys
import pandas as pd
import os

with open('fragment_library.smi') as x: # Query SMILE file (format: smiles compd_name)
	smiles = [line for line in x] 

def similarity_search(smi):
	""" This function calls openbabel similarity search on the list of SMILES submitted by the user"""

	fs_file = 'drugbank_approved.fs' # FP2 fingerprints file
	#max_similarity = '10' # max number of similar compounds to find
	
	
	output = 'known_drugs_substructure.smi' # Output file for FDA approved drugs
	#pubchem_out = '.similar_pubchem.out' # Output file for PubChem similarity analysis

	with open(output, 'w') as y:
		for mol in smi:

			#### Similarity Search using DrugBank All/Approved Drugs (LOCALLY) ####

			output_message = str(mol)
			#babel mymols.fs -ifs -sN#Cc1ccccc1C#N results.smi
			a = check_output('(obabel %s -ifs -s "%s" -O %s -xt)' % (fs_file, mol, output), shell=True)
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
similarity_search(smiles)
