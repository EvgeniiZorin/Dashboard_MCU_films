import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.config['suppress_callback_exceptions'] = True
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
df1['Worldwide box office (mln)'] = df1['Worldwide box office'] / 1000000
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


# df1_display is the version for displaying in the dashboard
df1_display = df1.copy()
df1_display['Date_pretty'] = df1_display['Date'].dt.strftime('%d %b %Y')
df1_display['Date_string'] = df1_display['Date'].astype(str)
print(df1_display.columns)
print(df1_display)

# ------------------------------------------------------------------------------
# --- Define some static figures -----------------------------------------------
# ------------------------------------------------------------------------------

def director_scatter_vertical():
	df2 = df1.copy()
	df2['Worldwide box office (bln)'] = df2['Worldwide box office (bln)'].round(2)
	fig = px.scatter(
		df2, x='Worldwide box office (bln)', y='Director(s)', color='Worldwide box office (bln)', color_continuous_scale='OrRd', range_color=[0.2, 1],
		title='Graph 1: box office per movies of each director', 
		# width=900, height=600, 
		size='Worldwide box office (bln)')
	fig.update_traces(textposition='middle right')
	# Disable zoom into graph
	fig.update_xaxes(fixedrange=True)
	fig.update_yaxes(fixedrange=True)
	return fig

def profit():
	df2 = df1.copy()
	df2['Phase'] = df2['Phase'].astype(str)
	df2['Box office / budget'] = df2['Worldwide box office'] / df2['Production budget']
	df2.sort_values(by='Box office / budget', ascending=True, inplace=True)
	fig = px.bar(
		df2, x='Box office / budget', y='Film', 
		# color='Phase',
		title='Graph 2: Most profitable movies (by box office / budget ratio) sorted in decreasing order',
		# width=900, height=600
	)
	# Disable zoom into graph
	fig.update_xaxes(fixedrange=True)
	fig.update_yaxes(fixedrange=True)
	return fig


# ------------------------------------------------------------------------------
# --- App Layout ---------------------------------------------------------------
# ------------------------------------------------------------------------------


SIDEBAR_STYLE = {
	"position": "fixed", 
	"top": 0, 
	"left": 0, 
	"bottom": 0, 
	"width": "16rem", 
	"padding": "2rem 1rem", 
	"background-color": "#f8f9fa"
}

CONTENT_STYLE = {
	"margin-left": "18rem", 
	"margin-right": "2rem", 
	"padding": "2rem 1rem",
}

sidebar = html.Div(
	[
		html.H2("Sidebar", className="display-4"),
		html.Hr(),
		html.P(
			"Statistics and Data Visualisations on the major superhero movie franchises ", className="lead"
		),
		dbc.Nav(
			[
				dbc.NavLink("Home", href="/", active="exact"),
				dbc.NavLink("MCU", href="/MCU-page", active="exact"),
				dbc.NavLink("DC", href="/DC-page", active="exact"),
			],
			vertical=True,
			pills=True,
		),
	],
	style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
	dcc.Location(id="url"),
	sidebar,
	content
])

# PAGES

Home_page = [
	html.P(
		"I love superhero movies and statistics. In this project, I use dashboard to investigate the former with the latter, and have fun in the process!",
		style={'text-align':'center', 'font-size':'30px'}),
	html.P(
		"I will compare and contrast budgets and profits of movies in the two biggest superhero franchises - Marvel Cinematic Universe (MCU) and DC.",
		style={'text-align':'center', 'font-size':'30px'}),
	html.Div(
		'Created by: Evgenii Zorin', 
		style={'text-align':'center', 'font-size':'20px'}
	),
	html.Div([
		html.A(
		'Link to the source code', href='https://github.com/EvgeniiZorin/MCU_films_dashboard', 
		target="_blank", # Open link in a new tab
		# style={'textAlign':'center', 'font-size':'20px'}, 
	),
	], style={'font-size':'20px', "display": "flex", "justifyContent": "center"}),
	# html.A(
	# 	'Link to the source code', href='https://github.com/EvgeniiZorin/MCU_films_dashboard', 
	# 	target="_blank", # Open link in a new tab
	# 	style={'textAlign':'center', 'font-size':'20px'}, 
	# ),
]

MCU_page = [
	# html.H1('MCU page', style={'textAlign':'center'}),
	html.H1("Marvel Cinematic Universe (MCU) movies", style={
	'color':'white', 'background-color':'darkred',
	'text-align': 'center'
	}), 
	dcc.Graph(
		id='static_1', figure=director_scatter_vertical(), 
		style={'display':'inline-block', 'width':'50%'}
		),
	dcc.Graph(
		id='static_2', figure=profit(), 
		style={'display':'inline-block', 'width':'50%'}
		),
	html.Br(),
	html.P('Graph 3: box office for each movie per phase', style={'text-align':'center', 'font-size':'25px'}), 
	dcc.Checklist(
		id='selectPhase', 
		options=[
			{'label': 'Phase 1', 'value': 1}, 
			{'label': 'Phase 2', 'value': 2}, 
			{'label': 'Phase 3', 'value': 3}], 
		value=[1, 2, 3], 
		style={'text-align':'center', 'display':'inline-block', 'width':'30%'}
	), 
	# html.P('asdf', style={'display':'inline-block', 'width':'70%'}), 
	html.Div(id='output_choiceStr', children=[], style={'display':'inline-block', 'width':'70%'}), # You have chosen: 
	html.Br(),
	dcc.Graph(id='selectPhase_barplot', figure={}),

	# html.Div('', style={'display':'inline-block', 'width':'10%'}),
	#
	# html.Div(id='')
	html.Br(), 
	html.Div('Below you can see the full data table', style={'text-align':'center', 'font-size':'30px'}),
	html.Br(),
	dash_table.DataTable(
		data=df1_display.to_dict('records'),
		# columns=[{'name':i, 'id':i} for i in df1.columns()],
		sort_action='native',
		columns=[
			{'name':'Date', 'id':'Date_string', 'type':'datetime'}, 
			{'name':'Film', 'id':'Film'},
			{'name':'Phase', 'id':'Phase'}, 
			{'name':'Saga', 'id':'Saga'}, 
			{'name':'Director(s)', 'id':'Director(s)'}, 
			{'name':'Producer(s)', 'id': 'Producer(s)'},
			{'name':'Production budget (mln)', 'id':'Production budget (mln)'}, 
			{'name':'Worldwide box office (mln)', 'id':'Worldwide box office (mln)'}
		],
		# style_header={'backgroundColor':'rgb(30,30,30)', 'color':'white'},
		# style_data={'backgroundColor':'rgb(50,50,50)', 'color':'white'}
		style_header={'backgroundColor':'rgb(192,192,192)', 'text-align':'center'},
		style_data={'backgroundColor':'rgb(224,224,224)', 'text-align':'center'}, 
	)
]

DC_page = [
	html.P('This section is under development', style={'text-align':'center', 'font-size':'25px'})
]

@app.callback(
	Output("page-content", "children"),
	[Input("url", "pathname")]
)
def render_page_content(pathname):
	if pathname == "/":
		# return MCU_page
		return Home_page
		# return [
		#         html.H1('Home page',
		#                 style={'textAlign':'center'}),
		#         # dcc.Graph(id='bargraph',
		#         #          figure=px.bar(df, barmode='group', x='Years',
		#         #          y=['Girls Kindergarten', 'Boys Kindergarten']))
		#         ]
	elif pathname == "/MCU-page":
		return MCU_page
		# return [
		# 		html.H1('Page 1',
		# 				style={'textAlign':'center'}),
		# 		# dcc.Graph(id='bargraph',
		# 		#          figure=px.bar(df, barmode='group', x='Years',
		# 		#          y=['Girls Grade School', 'Boys Grade School']))
		# 		]
	elif pathname == "/DC-page":
		return DC_page
	# If the user tries to reach a different page, return a 404 message
	return dbc.Jumbotron(
		[
			html.H1("404: Not found", className="text-danger"),
			html.Hr(),
			html.P(f"The pathname {pathname} was not recognised..."),
		]
	)


# ------------------------------------------------------------------------------
# --- Connect the Plotly graphs with Dash Components ---------------------------
# ------------------------------------------------------------------------------
@app.callback(
	[
		Output(component_id='output_choiceStr', component_property='children'),
		Output(component_id='selectPhase_barplot', component_property='figure')], 
	[Input(component_id='selectPhase', component_property='value')]
)
# def phase_lineplot(selectPhase):
# 	df2 = df1.copy()
# 	df2 = df2[df2['Phase'].isin(selectPhase)]
# 	fig = px.line(
# 		# df2, x='Date', y='Worldwide box office (bln)', color='Phase',
# 		df2, x='Worldwide box office (bln)', y='Date', color='Phase', 
# 		text='Film', title='Graph 3: box office for each movie per phase',
# 	)
# 	fig.update_layout(
# 		height=1200, width=1000, 
# 		# yaxis=dict(tickmode='linear', tick0=2008, dtick=1)
# 	)
# 	# fig.update_traces(textposition='middle right')
# 	fig.update_yaxes(dtick="M12", tickformat="%Y")
# 	yearZero = df2['Date'].min().strftime('%Y')
# 	print(yearZero)
# 	output_choiceStr = f"You have chosen: {sorted(selectPhase)}"
# 	return output_choiceStr, fig
def phase_barplot(selectPhase):
	df2 = df1.copy()
	df2 = df2[df2['Phase'].isin(selectPhase)]
	# print(df2.dtypes)
	df2['Phase'] = df2['Phase'].astype(str) 
	fig = px.bar(
		df2, x='Date', y='Worldwide box office (bln)', color='Phase',
		text='Film', 
		# text_auto='.2s',
		title='',
		# color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
	)
	fig.update_layout(
		# height=500, width=1900, 
		uniformtext_minsize=10, uniformtext_mode='hide' # uniformtext_mode = 'show', 'hide'
	)
	fig.update_traces(
		textposition='outside', 
		# textangle=270
		textangle=340
	)
	fig.update_xaxes(dtick="M12", tickformat="%Y")
	fig.update_xaxes(fixedrange=True)
	fig.update_yaxes(fixedrange=True)
	yearZero = df2['Date'].min().strftime('%Y')
	print(yearZero)
	output_choiceStr = f"You have chosen: {sorted(selectPhase)}"
	return output_choiceStr, fig


# ------------------------------------------------------------------------------
if __name__=='__main__':
	app.run_server(debug=True)