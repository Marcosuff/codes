# Import modules
import pandas as pd
import os
import re
import matplotlib.pyplot as plt

###########   This script plots calculated physicochemical properties using MatPlotLib #########

names = ['smiles', 'Compound_ID', 'Molecular_weight', 'TPSA', 'logP', 'HBD', 'rtb'] # Dataframe columns names

# For regex inside loop
matches1 = r'.*TESTE.smi$'
#matches2 = r'.*csv$'

# Define markers to plot
marker1 = "o"
marker2 = "v"
marker3 = "^"

# Open file and convert to dataframe
#with open('Enamine10240.smi') as f:
	#lines = [line.split() for line in f]
#frames = pd.DataFrame(lines, columns=names)
#frames.to_csv('Enamine10240.csv')

# This loop converts smi files into csv files (For later use with Pandas)
for f in os.listdir('.'): # Find all .smi files inside current directory
	if re.search(matches1,f):
		base = str(os.path.splitext(os.path.basename(f))[0]) # Get files names

		with open(f) as f: # Open files
			lines = [line.split() for line in f] # Create a list of all lines
		frames = pd.DataFrame(lines, columns=names) # output lines to Pandas dataframes
		frames.to_csv(('%s.csv') % (base)) # Save csv file

############# PLOTTING IS STILL HARDCODED AND VERY CRUDE #########################

# Plot dataframes with matplotlib 

df1 = pd.read_csv('chembionetTESTE.csv')
y1 = df1['logP']
x1 = df1['Molecular_weight']

df2 = pd.read_csv('Enamine10240TESTE.csv')
y2 = df2['logP']
x2 = df2['TPSA']

df3 = pd.read_csv('fragment_libraryTESTE.csv')
x3 = df3['logP']
y3 = df3['Molecular_weight']

########## Plot kinds (histogram or scatter plots) ###############################

# For hist
#mw_bin = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750] # MW
#logp_bin = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
#tpsa_bin = range(0,150)
#plt.hist(x1, y1, label='Chembionet', color='r', s=0.08) # Chembionet (red)
#plt.hist(x2, tpsa_bin, label='Enamine', color='b', rwidth=0.8) # Enamine (blue)
#plt.hist(x3, y3, label='Fragment library', color='k', s=0.08) # Fragment library (black)			
		

# For scatter plots
#plt.scatter(x1, y1, label='Chembionet', color='r', s=0.08) # Chembionet (red)
#plt.scatter(x2, tpsa_bin, label='Enamine', color='b', rwidth=0.8) # Enamine (blue)
#plt.scatter(x3, y3, label='Fragment library', color='k', s=0.08) # Fragment library (black)

# Axis and plot properties

# Axis labels
plt.xlabel('TPSA')
plt.ylabel('Frequency')
# Plot title
plt.title('TPSA distribution')
# Add legend
plt.legend()
# Show plot
plt.show()
