import pandas as pd 
import plotly.express as px 

def crear_grafico(df):
	df_review  = df.groupby('review_score').agg(
		total_ventas = ('cantidad_itens', 'sum')
		).reset_index()

	colors = ['#E6F3FF', '#99D1FF', '#4DAFFF', '#0082CC', '#005580']

	fig = px.pie(df_review,
		values = 'total_ventas',
		names = 'review_score',
		title = 'Calificación de las ventas',
		color_discrete_sequence = colors
		)

	fig.update_layout(yaxis_title = 'Calificación', xaxis_title = 'Ventas', showlegend=False)
	fig.update_traces(textposition = 'inside', textinfo = 'percent+label', insidetextfont=dict(size=16))

	return fig