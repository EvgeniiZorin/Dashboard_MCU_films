import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px

import fetch_dataset

df1, df1_display = fetch_dataset.main()

def director_scatter_vertical():
	df2 = df1.copy()
	df2['Worldwide box office (bln)'] = df2['Worldwide box office (bln)'].round(2)
	fig = px.scatter(
		df2, x='Worldwide box office (bln)', y='Director(s)', 
		color='Worldwide box office (bln)', color_continuous_scale='OrRd', 
		range_color=[0.2, 1],
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


Home_page = [
	dbc.Container([
		html.H1("Home Page", style={'text-align':'center'}),
		html.Br(),
		dcc.Markdown("""
		The two things that are among my favourites are Statistics and Superhero movies. 
		
		In this Interactive Dashboard, I will analyse the data about the superhero movies using my best Statistical knowledge!
		
		I will compare and contrast budgets and profits of movies in the two biggest superhero franchises - Marvel Cinematic Universe (MCU) and DC.


		""", style={'font-size':'30px'}),
		html.Br(),
		html.Div("Created by Evgenii Zorin", style={'text-align':'center', 'font-size':'20px'}),
		html.Div([
			html.A(
			'Link to the source code', href='https://github.com/EvgeniiZorin/MCU_films_dashboard', 
			target="_blank", # Open link in a new tab
			# style={'textAlign':'center', 'font-size':'20px'}, 
		),
		], style={'font-size':'20px', "display": "flex", "justifyContent": "center"}),
	])
]

MCU_page = [
	dbc.Container([
		html.H1("Marvel Cinematic Universe (MCU) movies", style={
		'color':'white', 'background-color':'darkred',
		'text-align': 'center'
		}), 
		html.Button('create pdf', id='run'),
		dcc.Graph(
			id='static_1', figure=director_scatter_vertical()
		)
	])
]

# MCU_page = [
# 	# html.H1('MCU page', style={'textAlign':'center'}),
# 	html.H1("Marvel Cinematic Universe (MCU) movies", style={
# 	'color':'white', 'background-color':'darkred',
# 	'text-align': 'center'
# 	}), 
# 	dcc.Graph(
# 		id='static_1', figure=director_scatter_vertical()
# 	),
# 	# html.Br(),
# 	# dcc.Graph(
# 	# 	id='static_1', figure=director_scatter_vertical(), 
# 	# 	style={'display':'inline-block', 'width':'50%', 'height': '68vh'}
# 	# 	),
# 	# dcc.Graph(
# 	# 	id='static_2', figure=profit(), 
# 	# 	style={'display':'inline-block', 'width':'50%', 'height': '68vh'}
# 	# 	),
# 	# html.Br(),
# 	# html.P('Graph 3: box office for each movie per phase', style={'text-align':'center', 'font-size':'25px'}), 
# 	# html.Div([
# 	# 	dcc.Checklist(
# 	# 		id='selectPhase', 
# 	# 		options=[
# 	# 			{'label': ' Phase 1', 'value': 1}, 
# 	# 			{'label': ' Phase 2', 'value': 2}, 
# 	# 			{'label': ' Phase 3', 'value': 3}, 
# 	# 			{'label': ' Phase 4', 'value': 4}], 
# 	# 		value=[1, 2, 3, 4], 
# 	# 		style={"display":"block"}
# 	# 		# style={'text-align':'center', 'display':'inline-block', 'width':'30%'}
# 	# 	),
# 	# 	], style={'width':'5%'}),
# 	# html.Br(),
# 	# dcc.Graph(id='selectPhase_lineplot', figure={}),

# 	# # html.Div('', style={'display':'inline-block', 'width':'10%'}),
# 	# #
# 	# # html.Div(id='')
# 	# html.Br(), 
# 	# html.Div('Below you can see the full data table', style={'text-align':'center', 'font-size':'30px'}),
# 	# html.Br()
# 	# # dash_table.DataTable(
# 	# # 	data=df1_display.to_dict('records'),
# 	# # 	# columns=[{'name':i, 'id':i} for i in df1.columns()],
# 	# # 	sort_action='native',
# 	# # 	columns=[
# 	# # 		{'name':'Date', 'id':'Date_string', 'type':'datetime'}, 
# 	# # 		{'name':'Film', 'id':'Film'},
# 	# # 		{'name':'Phase', 'id':'Phase'}, 
# 	# # 		{'name':'Saga', 'id':'Saga'}, 
# 	# # 		{'name':'Director(s)', 'id':'Director(s)'}, 
# 	# # 		{'name':'Producer(s)', 'id': 'Producer(s)'},
# 	# # 		{'name':'Production budget (mln)', 'id':'Production budget (mln)'}, 
# 	# # 		{'name':'Worldwide box office (mln)', 'id':'Worldwide box office (mln)'}
# 	# # 	],
# 	# # 	# style_header={'backgroundColor':'rgb(30,30,30)', 'color':'white'},
# 	# # 	# style_data={'backgroundColor':'rgb(50,50,50)', 'color':'white'}
# 	# # 	style_header={'backgroundColor':'rgb(192,192,192)', 'text-align':'center'},
# 	# # 	style_data={'backgroundColor':'rgb(224,224,224)', 'text-align':'center'}, 
# 	# # )
# ]

DC_page = [
	html.P('This section is under development', style={'text-align':'center', 'font-size':'25px'})
]

Data_tables = [
	html.H1("Data table for the MCU dataset", style={
	'color':'white', 'background-color':'darkred',
	'text-align': 'center'
	}), 
	dbc.Table.from_dataframe(df1_display, striped=True, bordered=True, hover=True, responsive='sm', size='sm')
]