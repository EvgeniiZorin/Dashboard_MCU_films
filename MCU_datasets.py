import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc

import styles
import fetch_dataset
import pages

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config['suppress_callback_exceptions'] = True

# ------------------------------------------------------------------------------
# --- Import and clean data (importing csv into pandas) ------------------------
# ------------------------------------------------------------------------------
df1, df1_display = fetch_dataset.main()


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


app.layout = html.Div([
	html.H1(
		children='Dashboard for the Superhero Movie Universes - MCU and DCEU'
	),
	dbc.Tabs(
		[
			dbc.Tab(label="Home", tab_id="home"),
			dbc.Tab(label="MCU", tab_id="MCU-page"),
			dbc.Tab(label="DC", tab_id="DC-page")
		],
		id="tabs",
		active_tab="home"
	),
	html.Div(id="tab-content", className="p-4"),
])

# content = html.Div(id="page-content", children=[], style=styles.CONTENT_STYLE)


# PAGES

# Home_page = [
# 	dbc.Container([
# 		html.H1("Home Page", style={'text-align':'center'}),
# 		html.Br(),
# 		dcc.Markdown("""
# 		The two things that are among my favourites are Statistics and Superhero movies. 
		
# 		In this Interactive Dashboard, I will analyse the data about the superhero movies using my best Statistical knowledge!
		
# 		I will compare and contrast budgets and profits of movies in the two biggest superhero franchises - Marvel Cinematic Universe (MCU) and DC.


# 		""", style={'font-size':'30px'}),
# 		html.Br(),
# 		html.Div("Created by Evgenii Zorin", style={'text-align':'center', 'font-size':'20px'}),
# 		html.Div([
# 			html.A(
# 			'Link to the source code', href='https://github.com/EvgeniiZorin/MCU_films_dashboard', 
# 			target="_blank", # Open link in a new tab
# 			# style={'textAlign':'center', 'font-size':'20px'}, 
# 		),
# 		], style={'font-size':'20px', "display": "flex", "justifyContent": "center"}),
# 	])
# ]

# # Home_page = [
# # 	html.P(
# # 		"I love superhero movies and statistics. In this project, I use dashboard to investigate the former with the latter, and have fun in the process!",
# # 		style={'text-align':'center', 'font-size':'30px'}),
# # 	html.P(
# # 		"I will compare and contrast budgets and profits of movies in the two biggest superhero franchises - Marvel Cinematic Universe (MCU) and DC.",
# # 		style={'text-align':'center', 'font-size':'30px'}),
# # 	html.Div(
# # 		'Created by: Evgenii Zorin', 
# # 		style={'text-align':'center', 'font-size':'20px'}
# # 	),
# 	# html.Div([
# 	# 	html.A(
# 	# 	'Link to the source code', href='https://github.com/EvgeniiZorin/MCU_films_dashboard', 
# 	# 	target="_blank", # Open link in a new tab
# 	# 	# style={'textAlign':'center', 'font-size':'20px'}, 
# 	# ),
# 	# ], style={'font-size':'20px', "display": "flex", "justifyContent": "center"}),
# 	# # html.A(
# 	# # 	'Link to the source code', href='https://github.com/EvgeniiZorin/MCU_films_dashboard', 
# 	# # 	target="_blank", # Open link in a new tab
# 	# # 	style={'textAlign':'center', 'font-size':'20px'}, 
# 	# # ),
# # ]

MCU_page = [
	# html.H1('MCU page', style={'textAlign':'center'}),
	html.H1("Marvel Cinematic Universe (MCU) movies", style={
	'color':'white', 'background-color':'darkred',
	'text-align': 'center'
	}), 
	dcc.Graph(
		id='static_1', figure=director_scatter_vertical()
	),
	html.Br(),
	dcc.Graph(
		id='static_1', figure=director_scatter_vertical(), 
		style={'display':'inline-block', 'width':'50%', 'height': '68vh'}
		),
	dcc.Graph(
		id='static_2', figure=profit(), 
		style={'display':'inline-block', 'width':'50%', 'height': '68vh'}
		),
	html.Br(),
	html.P('Graph 3: box office for each movie per phase', style={'text-align':'center', 'font-size':'25px'}), 
	html.Div([
		dcc.Checklist(
			id='selectPhase', 
			options=[
				{'label': ' Phase 1', 'value': 1}, 
				{'label': ' Phase 2', 'value': 2}, 
				{'label': ' Phase 3', 'value': 3}, 
				{'label': ' Phase 4', 'value': 4}], 
			value=[1, 2, 3, 4], 
			style={"display":"block"}
			# style={'text-align':'center', 'display':'inline-block', 'width':'30%'}
		),
		], style={'width':'5%'}),
	html.Br(),
	dcc.Graph(id='selectPhase_lineplot', figure={}),

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
	Output("tab-content", "children"),
	Input("tabs", "active_tab")
)
def render_page_content(active_tab):
	if active_tab == "home":
		# return Home_page
		return pages.Home_page
		# return [
		#         html.H1('Home page',
		#                 style={'textAlign':'center'}),
		#         # dcc.Graph(id='bargraph',
		#         #          figure=px.bar(df, barmode='group', x='Years',
		#         #          y=['Girls Kindergarten', 'Boys Kindergarten']))
		#         ]
	elif active_tab == "MCU-page":
		return MCU_page
		# return [
		# 		html.H1('Page 1',
		# 				style={'textAlign':'center'}),
		# 		# dcc.Graph(id='bargraph',
		# 		#          figure=px.bar(df, barmode='group', x='Years',
		# 		#          y=['Girls Grade School', 'Boys Grade School']))
		# 		]
	elif active_tab == "DC-page":
		return DC_page



# ------------------------------------------------------------------------------
# --- Connect the Plotly graphs with Dash Components ---------------------------
# ------------------------------------------------------------------------------
@app.callback(
	Output(component_id='selectPhase_lineplot', component_property='figure'), 
	# [
	# 	# Output(component_id='output_choiceStr', component_property='children'),
	# 	Output(component_id='selectPhase_lineplot', component_property='figure')], 
	[Input(component_id='selectPhase', component_property='value')]
)
def phase_lineplot(selectPhase):
	df2 = df1.copy()
	df2 = df2[df2['Phase'].isin(selectPhase)]
	fig = px.line(
		# df2, x='Date', y='Worldwide box office (bln)', color='Phase',
		df2, y='Worldwide box office (bln)', x='Date', color='Phase', 
		# text='Film', 
		hover_name='Film',
		title='',
	)
	fig.update_traces(mode="markers+lines")
	fig.update_layout(
		hoverlabel=dict(
			bgcolor="white",
			font_size=14,
			# font_family="Times New Roman"
		)
	)

	# fig.update_layout(
	# 	# height=1200, width=1000, 
	# 	# yaxis=dict(tickmode='linear', tick0=2008, dtick=1)
	# 	uniformtext_minsize=10, uniformtext_mode='hide'
	# )
	# fig.update_traces(textposition='middle right')
	fig.update_xaxes(dtick="M12", tickformat="%Y")
	fig.update_xaxes(fixedrange=True)
	fig.update_yaxes(fixedrange=True)
	return fig
# 	yearZero = df2['Date'].min().strftime('%Y')
# 	print(yearZero)
# 	output_choiceStr = f"You have chosen: {sorted(selectPhase)}"
# 	return output_choiceStr, fig
# def phase_barplot(selectPhase):
# 	df2 = df1.copy()
# 	df2 = df2[df2['Phase'].isin(selectPhase)]
# 	# print(df2.dtypes)
# 	df2['Phase'] = df2['Phase'].astype(str) 
# 	fig = px.bar(
# 		df2, x='Date', y='Worldwide box office (bln)', color='Phase',
# 		text='Film', 
# 		# text_auto='.2s',
# 		title='',
# 		# color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
# 	)
# 	fig.update_layout(
# 		# height=500, width=1900, 
# 		uniformtext_minsize=10, uniformtext_mode='hide' # uniformtext_mode = 'show', 'hide'
# 	)
# 	fig.update_traces(
# 		textposition='outside', 
# 		textangle=340
# 	)
# 	fig.update_xaxes(dtick="M12", tickformat="%Y")
# 	fig.update_xaxes(fixedrange=True)
# 	fig.update_yaxes(fixedrange=True)
# 	yearZero = df2['Date'].min().strftime('%Y')
# 	return fig


# ------------------------------------------------------------------------------
if __name__=='__main__':
	app.run_server(debug=True)