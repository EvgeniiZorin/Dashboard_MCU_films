import dash_bootstrap_components as dbc
from dash import dcc, html

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

