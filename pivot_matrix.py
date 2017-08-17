import pandas as pd
import numpy as np

# This code creates a pivot matrix of the similarity summary file to calculate average Tanimoto scores ##

# Format dataframe floats
pd.options.display.float_format = '{:,.2f}'.format

# Create a matrix
df = pd.read_csv('fxa_chembl_c_diversity_summary.csv') # Open the summary file
matrix = df.pivot(index='Compound_ID', columns='Similar', values='Tanimoto_score') # Pivoting to create matrix

# Calculate means
matrix['Averages'] = matrix.mean(axis=1)

# Sort CID
a = matrix.sort_values('Averages', ascending=False)

# Calculate % of databased screened
length = len(a['Averages'])
a['Index'] = range(1,length + 1)
a['Percentage'] = (a['Index'] / length) * 100

# Define columns to save
co = ['Averages', 'Percentage']

#Save averages to csv_file
a.to_csv('fxa_chembl_c_averages.csv', columns=co)

