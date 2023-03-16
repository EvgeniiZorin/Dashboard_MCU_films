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
			dbc.Tab(label="DC", tab_id="DC-page"),
			dbc.Tab(label="Data tables", tab_id="Data-tables")
		],
		id="tabs",
		active_tab="home"
	),
	html.Div(id="tab-content", className="p-4"),
])




@app.callback(
	Output("tab-content", "children"),
	Input("tabs", "active_tab")
)
def render_page_content(active_tab):
	if active_tab == "home":
		return pages.Home_page
		# return [
		#         html.H1('Home page',
		#                 style={'textAlign':'center'}),
		#         # dcc.Graph(id='bargraph',
		#         #          figure=px.bar(df, barmode='group', x='Years',
		#         #          y=['Girls Kindergarten', 'Boys Kindergarten']))
		#         ]
	elif active_tab == "MCU-page":
		return pages.MCU_page
	elif active_tab == "DC-page":
		return pages.DC_page
	elif active_tab == "Data-tables":
		return pages.Data_tables



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
	df1, df1_display = fetch_dataset.main()
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