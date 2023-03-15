import os
import pandas as pd

def main():
	"""
	Returns [df1, df1_display]"""
	# df = pd.read_csv('https://raw.githubusercontent.com/EvgeniiZorin/MCU_films_dashboard/main/MCU_dataset.tsv', sep='\t', skiprows=2)
	# file_path = os.path.join( os.getcwd(), 'Datasets', 'MCU_dataset.tsv' )
	file_path = os.path.join( os.path.abspath( os.path.dirname( __file__ ) ), 'Datasets', 'MCU_dataset.tsv' )
	df = pd.read_csv(file_path, sep='\t', skiprows=2)
	df1 = df.copy()
	# Replace all "and" and "&" with a comma, 
	# except for in the case of "Anthony and Joe Russo", because in the MCU they are called by everyone as "the Russo brothers" as they work on everything together
	df1['Director(s)'] = df1['Director(s)'].str.replace("&| &| ," , ",")
	df1['Producer(s)'] = df1['Producer(s)'].str.replace(", and| and", ",")
	# Next, let's change datatype of "Date" column into Datetime:
	df1['Date'] = pd.to_datetime(df1['Date'])
	df1['Year'] = df1['Date'].dt.strftime('%Y')
	# Next, let's convert columns "Production budget" and "Worldwide box office" into datatype "Int":
	df1['Production budget'] = df1['Production budget'].str.replace(',', '') # remove commas
	df1['Production budget'] = df1['Production budget'].astype(int)
	df1['Production budget (mln)'] = df1['Production budget'] / 1000000
	df1['Worldwide box office'] = df1['Worldwide box office'].str.replace(',', '') 
	df1['Worldwide box office'] = df1['Worldwide box office'].astype(float)
	df1['Worldwide box office (bln)'] = df1['Worldwide box office'] / 1000000000
	df1['Worldwide box office (mln)'] = df1['Worldwide box office'] / 1000000
	# Let's create a new column with names of movies which have more than 1 bln box officce
	# df1['Film bln'] = df1['Worldwide box office'] > 1000000000
	df1['Film bln'] = ''
	for index, row in df1.iterrows():
		if row['Worldwide box office'] >= 1000000000:
			df1['Film bln'].iloc[index] = row['Film']
		# else:
		# 	df1['Film bln'].iloc[index] = ''

	# Also, let's separate the column "Phase (Saga)" into two columns - "Phase" and "Saga"
	df1['Phase'] = df1['Phase'].astype(int)
	# df1_display is the version for displaying in the dashboard
	df1_display = df1.copy()
	df1_display['Date_pretty'] = df1_display['Date'].dt.strftime('%d %b %Y')
	df1_display['Date_string'] = df1_display['Date'].astype(str)
	# print(df1_display.columns)
	# print(df1_display)
	return df1, df1_display
