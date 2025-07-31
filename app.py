import streamlit as st
import pandas as pd
import grafico_mapa as graf1
import grafico_lineas as graf2
import grafico_barras as graf3
import grafico_pizza as graf4

st.set_page_config(layout = 'wide')

st.title('Dashboard de Ventas 🛒 ')

def formato_numero(valor, prefijo = ''):
  for unidad in ['', 'k']:
    if valor < 1000:
      return f'{prefijo} {valor:.2f} {unidad}'
    valor /= 1000
  return f'{prefijo} {valor:.2f} M'

#Abrimos las bases de datos
df_ventas = pd.read_csv('https://raw.githubusercontent.com/AnndyLibeMoore/sales_dashboard_streamlit_class/main/base_ventas.csv')
#Total de ingresos
df_ventas['valor_total'] = (df_ventas.cantidad_itens * df_ventas.price) + (df_ventas.cantidad_itens * df_ventas.freight_value)
df_ventas['order_purchase_timestamp'] = pd.to_datetime(df_ventas['order_purchase_timestamp'])
df_ventas['tipo_productos'] = df_ventas['product_category_name'].str.split('_').str[0]

#configuración de filtros
st.sidebar.image('https://raw.githubusercontent.com/AnndyLibeMoore/sales_dashboard_streamlit_class/main/estadistica.png')
st.sidebar.title('Filtros')

estados = sorted(list(df_ventas['geolocation_state'].unique()))
ciudades = st.sidebar.multiselect('Estados', estados)

productos = sorted(list(df_ventas['tipo_productos'].dropna().unique()))
productos.insert(0, 'Todos')
producto = st.sidebar.selectbox('Productos', productos)

años = st.sidebar.checkbox('Todo el periodo', value=True)
if not años:
  año = st.sidebar.slider('Año',df_ventas['order_purchase_timestamp'].dt.year.min(), df_ventas['order_purchase_timestamp'].dt.year.max())



#filtrando los datos

if ciudades:
  df_ventas = df_ventas[df_ventas['geolocation_state'].isin(ciudades)]

if producto != 'Todos':
    df_ventas = df_ventas[df_ventas['tipo_productos'] == producto]
 
if not años:
    df_ventas = df_ventas[df_ventas['order_purchase_timestamp'].dt.year == año]




#Llamamos a los gráficos
graf_mapa = graf1.crear_mapa(df_ventas) 
graf_lineas = graf2.crear_grafico(df_ventas) 
graf_barras = graf3.crear_grafico(df_ventas)
graf_pizza = graf4.crear_grafico(df_ventas) 




col1, col2 = st.columns(2)
#Métrica 1 ingresos.
with col1:
  st.metric('**Total de Ingresos', formato_numero(df_ventas['valor_total'].sum(),'$'))
  st.plotly_chart(graf_mapa, use_container_width=True)
  st.plotly_chart(graf_barras, use_container_width=True)

  
#Métrica de cantidad de productos vendidos osea ventas realizadas si cada producto vendido se cuenta ocmo una venta
with col2:
  st.metric('**Total de Ventas', formato_numero(df_ventas['cantidad_itens'].sum()))
  st.plotly_chart(graf_lineas, use_container_width=True)
  st.plotly_chart(graf_pizza, use_container_width=True)


#st.dataframe(df_ventas)