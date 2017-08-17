import pandas as pd
import os
import re

df = pd.read_csv('enamine_averages.csv')
matches = r'.*averages.csv'
for f in os.listdir('.'):
	if re.search(matches, f):
		df = pd.read_csv(f)
		variance = df.var()
		std = df.std()
		print '%s var = %s' %(f, str(variance))
		print '%s std = %s' %(f, str(std))
