# Import modules
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Open csv files
df1 = pd.read_csv('averages.csv')
df2 = pd.read_csv('chembionet_averages.csv')
df3 = pd.read_csv('enamine_averages.csv')
df4 = pd.read_csv('Enamineessential_corrected_averages.csv')
df5 = pd.read_csv('Enaminegold_averages.csv')
df6 = pd.read_csv('Deubiquitinasefocused_averages.csv')
df7 = pd.read_csv('AuroraA_averages.csv')
df8 = pd.read_csv('fxa_chembl_c_averages.csv')
df9 = pd.read_csv('Selcia_averages.csv')


# x, y and labels
coords = [
[df1['Percentage'],df1['Averages'], 'Fragment library'], 
[df2['Percentage'],df2['Averages'],'ChemBionet'],
[df3['Percentage'],df3['Averages'],'Enamine general'], 
[df4['Percentage'],df4['Averages'],'Enamine essential'], 
[df5['Percentage'],df5['Averages'],'Enamine gold']
]

# Fragment library
#x1 = df1['Percentage'] # blue
#y1 = df1['Averages']
# ChemBioNet
#x2 = df2['Percentage'] # green
#y2 = df2['Averages']
# Enamine general
#x3 = df3['Percentage'] # black
#y3 = df3['Averages']
# Enamine essential
#x4 = df4['Percentage'] # red
#y4 = df4['Averages']
# Enamine gold
#x5 = df5['Percentage'] # yellow
#y5 = df5['Averages']

# axis limits
ax = plt.gca()
ax.set_xlim(0,100)
ax.set_ylim(0.00,1.00)
ax.tick_params(labelsize=11)

# Plot Tanimoto scores
for i in coords:
	# Plot averages
	plt.plot(i[0],i[1],label=i[2], linewidth=3, linestyle='solid')

	# Set axis labels
	plt.xlabel('Dataset screened %', fontsize=11)
	plt.ylabel('Average Tanimoto score', fontsize=11)

	# Plot title
	plt.title('Average Tanimoto score')

	# Add legend
	plt.legend(loc='best', fontsize=12)

	# Show plot

plt.show()


