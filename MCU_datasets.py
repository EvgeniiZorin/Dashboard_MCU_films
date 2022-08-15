import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
server = app.server


# ------------------------------------------------------------------------------
# --- Import and clean data (importing csv into pandas) ------------------------
# ------------------------------------------------------------------------------
df = pd.read_csv('https://raw.githubusercontent.com/EvgeniiZorin/MCU_films_dashboard/main/MCU_dataset.tsv', sep='\t', skiprows=2)


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
# Let's create a new column with names of movies which have more than 1 bln box officce
# df1['Film bln'] = df1['Worldwide box office'] > 1000000000
df1['Film bln'] = ''
for index, row in df1.iterrows():
	if row['Worldwide box office'] >= 1000000000:
		# df['Film bln'].iloc[index] = row['Film']
		print(row['Film'])
		df1['Film bln'].iloc[index] = row['Film']
	# else:
	# 	df1['Film bln'].iloc[index] = ''

# Also, let's separate the column "Phase (Saga)" into two columns - "Phase" and "Saga"
df1[['Phase', 'Saga']] = df1['Phase (Saga)'].str.split('(', expand=True)
df1['Phase'] = df1['Phase'].str.replace(' ', '')
df1['Phase'] = df1['Phase'].astype(int)
df1['Saga'] = df1['Saga'].str.replace(')', '')
print(df1.dtypes)
df1


# ------------------------------------------------------------------------------
# --- App Layout ---------------------------------------------------------------
# ------------------------------------------------------------------------------



# --- Static figure ------------------------------------------------------------
def director_scatter():
	df2 = df1.copy()
	df2['Worldwide box office (bln)'] = df2['Worldwide box office (bln)'].round(2)
	fig = px.scatter(
		# df2, x='Date', y='Worldwide box office (bln)', 
		df2, x='Director(s)', y='Worldwide box office (bln)', color='Worldwide box office (bln)', color_continuous_scale='OrRd', range_color=[0.2, 1],
		# color='Director(s)',
		text='Worldwide box office (bln)',
		title='Graph 2: box office per movies of each director')
	fig.update_traces(textposition='middle right')
	return fig
# ------------------------------------------------------------------------------



app.layout = html.Div([
	html.H1("Marvel Cinematic Universe movies", style={'text-align': 'center'}), 
	dcc.Checklist(
		id='selectPhase', 
		options=[
			{'label': 'Phase 1', 'value': 1}, 
			{'label': 'Phase 2', 'value': 2}, 
			{'label': 'Phase 3', 'value': 3}], 
		value=[1, 2, 3]
	), 
	html.Div(id='output_choiceStr', children=[]), # You have chosen: 
	html.Br(),
	dcc.Graph(id='selectPhase_barplot', figure={}), 
	#
	# html.Div(id='')
	html.Br(), 
	dcc.Graph(id='director_scatter', figure=director_scatter())
])

# ------------------------------------------------------------------------------
# --- Connect the Plotly graphs with Dash Components ---------------------------
# ------------------------------------------------------------------------------
@app.callback(
	[
		Output(component_id='output_choiceStr', component_property='children'),
		Output(component_id='selectPhase_barplot', component_property='figure')], 
	[Input(component_id='selectPhase', component_property='value')]
)
def phase_lineplot(selectPhase):
	df2 = df1.copy()
	df2 = df2[df2['Phase'].isin(selectPhase)]
	fig = px.line(
		# df2, x='Date', y='Worldwide box office (bln)', color='Phase',
		df2, x='Worldwide box office (bln)', y='Date', color='Phase', 
		text='Film', title='Graph 1: box office for each movie per phase',
	)
	fig.update_layout(
		height=1200, width=1000, 
		# yaxis=dict(tickmode='linear', tick0=2008, dtick=1)
	)
	# fig.update_traces(textposition='middle right')
	fig.update_yaxes(dtick="M12", tickformat="%Y")
	yearZero = df2['Date'].min().strftime('%Y')
	print(yearZero)
	output_choiceStr = f"You have chosen: {sorted(selectPhase)}"
	return output_choiceStr, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
	# Run the app on server (browser)
	app.run_server(debug=True)
