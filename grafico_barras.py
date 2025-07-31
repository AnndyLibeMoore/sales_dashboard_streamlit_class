import pandas as pd
import plotly.express as px 

def crear_grafico(df):
	revenues_category = df.groupby('product_category_name')[['valor_total']].sum().sort_values('valor_total', ascending=True).reset_index()

	fig = px.bar(revenues_category.tail(10),
		x = 'valor_total',
		y = 'product_category_name',
		text = 'valor_total',
		title = 'Top Ingresos por Categoría ($)'
	)
	fig.update_layout(yaxis_title = 'Categoría', xaxis_title= 'Ingresos ($)', showlegend=False)
	fig.update_traces(texttemplate = '%{text:.3s}')
		
	return fig	




