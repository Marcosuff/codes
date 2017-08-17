# Import modules
import pandas as pd

##### This script filters a similarity searching  according to leads similarities to known FDA approved drugs deposited on DrugBank #####

# Open similarity results as a dataframe
df = pd.read_csv('lead_similarity_summary.csv') # Open the summary filedf.

# Filter
#identicals = df.Tanimoto_score >= 1.00
identicals = (df[df['Tanimoto_score'] >= 1.00]).drop_duplicates(subset='Similar')

print len(identicals['Similar'])

# Save drugs/leads pairs to file
#identicals.to_csv('leads_drugs.csv', index=False, columns=['Compound_ID', 'Compound_smiles', 'Similar', 'Tanimoto_score'])


