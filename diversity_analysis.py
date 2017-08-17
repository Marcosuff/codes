# Import modules
from subprocess import call, check_output
import re
import sys
import pandas as pd
import os

####################################################################################
#    This script finds the n most similar compounds to a query list of molecules   #
####################################################################################  

#query_file = None
#fs_file = None # FP2 fingerprints file
#num_of_similar_compounds = None # max number of similar compounds to find

with open('chembionet.smi') as x: # Query SMILE file (format: smiles compd_name)
	smiles = [line for line in x] 

def similarity_search(smi):
	""" This function calls openbabel similarity search on the list of SMILES submitted by the user"""

	fs_file = 'chembionet.fs' # FP2 fingerprints file
	max_similarity = '10' # max number of similar compounds to find
	
	
	output = 'chembionet_dissimilarity.out' # Output file for FDA approved drugs
	#pubchem_out = '.similar_pubchem.out' # Output file for PubChem similarity analysis

	with open(output, 'w') as y:
		for mol in smi:

			#### Similarity Search using DrugBank All/Approved Drugs (LOCALLY) ####

			output_message = 'Compound ' + str(mol)
			a = check_output('(obabel %s -otxt -S "%s" -at%s -aa)' % (fs_file, mol, max_similarity), shell=True)
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

##################################################################################################################
#        This code formats the similarity analysis scores (tanimoto_raw.out file) into a csv file       #
##################################################################################################################

dt = [] # Creates a list to store dictionariess

with open('chembionet_dissimilarity.out') as f: # Opens similarity output file

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
df.to_csv('chembionet_diversity_summary.csv')
print 'Your summary is ready!'
