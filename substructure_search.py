# Import modules
from subprocess import check_output
import sys
import os
import pandas as pd

#### This script uses OpenBabel for substructure search

with open('pures.smi') as x: # Query SMILE file (format: smiles compd_name)
	smiles = [line for line in x]
dt = [] # Create a dict to store OpenBabel results

def similarity_search(smi):
	""" This function calls openbabel similarity search on the list of SMILES submitted by the user"""

	fs_file = 'drugbank_approved.fs' # FP2 fingerprints file

	for mol in smi:

		smiles,mol_name = str(mol.split()[0]),str(mol.split()[1])

		a = (check_output('(obabel %s -ifs -s "%s" -otxt -xt)' % (fs_file, mol), shell=True))
		supers = a.split() # Split a at '\n' to get the superstructures separated by a comma

		if len(supers) > 0: # Append only fragments match a drug
			dt.append({'Fragment': mol_name, 'Smiles' : smiles, 'Superstructures': (", ".join(supers))})

	print ('Similarity against FDA dataset complete. Our gremlins are working on the output file. Please wait...')

# Call function
similarity_search(smiles)

# Create dataframe
df = pd.DataFrame(dt)

new_df = (df['Superstructures'].str.split(',', expand=True)
.stack().reset_index(level=0).set_index('level_0')
.rename(columns={0:'Superstructures'})
.join(df.drop('Superstructures',1), how='left')
.sort_index(axis=1)
) # Split the values on Superstructures columms to different rows

# Save to csv file
new_df.to_csv('substructures.csv')
