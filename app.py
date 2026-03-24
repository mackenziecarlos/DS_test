import streamlit as st
import numpy as np
import joblib
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tabbed Bar Chart Dashboard", layout="wide")
st.title("Carlos Mackenzie - Principales Insights")

df = pd.read_csv("PruebaDS.xlsx - Sheet1.csv",dtype=str)

df[['anho', 'mes_anho']] = df['mes'].str.split('-', expand=True)

# 2.1.2 Se convierten las columnas tipo numero y fecha
num_cols = ['saldo_capital', 'dias_mora','meses_desde_ultimo_pago','duracion_llamadas_ultimos_6meses','anho', 'mes_anho']
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')

sum1 = df.groupby(['pago']).agg(registros=('mes_anho', 'count')).reset_index()
colores = {'0': 'gray','1': 'steelblue'}
fig1 = px.bar(sum1, x='pago', y='registros', color='pago', color_discrete_map=colores, title='Registros Pagados y No Pagados', text_auto=True)
fig1.update_xaxes(tickmode='linear')
#fig1.show()

sum2 = df.groupby(['mes_anho','pago']).agg(registros=('mes_anho', 'count')).reset_index()
fig2 = px.bar(sum2, x='mes_anho', y='registros', color='pago', color_discrete_map=colores, title='Numero de Pagos por Mes', text_auto=True)

fig3 = px.histogram(df, x= "duracion_llamadas_ultimos_6meses",title='Distribución Duración Llamadas Ultimos 6 Meses',range_x=[0, 200])
fig4 = px.box(df, x="pago", y="duracion_llamadas_ultimos_6meses",title='Box Plot Pagos vs Duración Llamadas Ultimos 6 Meses')

sum5 = df.groupby(['pago_mes_anterior','pago']).agg(registros=('mes_anho', 'count')).reset_index()
fig5 = px.bar(sum5, x='pago_mes_anterior', y='registros', color='pago', color_discrete_map=colores,title='Numero de Pagos Realizados por Pago Mes Anterior',text_auto=True)

sum6 = df.groupby(['pago_mes_anterior']).agg(registros_totales=('mes_anho', 'count')).reset_index()
sum7 = pd.merge(sum5, sum6, on='pago_mes_anterior')
sum7['part_reg']=sum7['registros']/sum7['registros_totales']*100
sum7g = sum7[sum7['pago']=='1']
colores_pago = {'0':'steelblue', '1':'#17BECF'} 
fig6 = px.bar(sum7g, x='pago_mes_anterior', y='part_reg', title='Porcentaje de Pagos Mes Anterior',color='pago_mes_anterior',color_discrete_map=colores_pago,
              labels={"part_reg": "Participación % Pagos"},text_auto=True)
fig6.update_yaxes(tickformat=".2s")

#   2.2.13 Contacto Mes Anterior
sum8 = df.groupby(['contacto_mes_anterior','pago']).agg(registros=('mes_anho', 'count')).reset_index()
fig7 = px.bar(sum8, x='contacto_mes_anterior', y='registros', color='pago', color_discrete_map=colores,title='Numero de Pagos Realizados vs Contacto Mes Anterior',text_auto=True)
sum9 = df.groupby(['contacto_mes_anterior']).agg(registros_totales=('mes_anho', 'count')).reset_index()
sum10 = pd.merge(sum8, sum9, on='contacto_mes_anterior')
sum10['part_reg']=sum10['registros']/sum10['registros_totales']*100
sum10g = sum10[sum10['pago']=='1']
colores_pago = {'0':'steelblue', '1':'#17BECF'} 
fig8 = px.bar(sum10g, x='contacto_mes_anterior', y='part_reg', title='Porcentaje de Pagos Realizados vs Contacto Mes Anterior',color='contacto_mes_anterior',color_discrete_map=colores_pago,
              labels={"part_reg": "Participación % Pagos"},text_auto=True)
fig8.update_yaxes(tickformat=".2s")

sum11 = df.groupby(['sin_pago_previo','pago']).agg(registros=('mes_anho', 'count')).reset_index()
fig9 = px.bar(sum11, x='sin_pago_previo', y='registros', color='pago', color_discrete_map=colores,title='Numero de Pagos Realizados vs Sin Pago Previo',text_auto=True)

sum12 = df.groupby(['sin_pago_previo']).agg(registros_totales=('mes_anho', 'count')).reset_index()
sum13 = pd.merge(sum11, sum12, on='sin_pago_previo')
sum13['part_reg']=sum13['registros']/sum13['registros_totales']*100
sum13g = sum13[sum13['pago']=='1']
colores_pago_s = {'1':'steelblue', '0':'#17BECF'} 
fig10 = px.bar(sum13g, x='sin_pago_previo', y='part_reg', title='Porcentaje de Pagos Realizados por Banco',color='sin_pago_previo',color_discrete_map=colores_pago_s,
              labels={"part_reg": "Participación % Pagos"},text_auto=True)
fig10.update_yaxes(tickformat=".2s")

# --- Tab Setup ---
tab1, tab2, tab3, tab4,tab5,tab6 = st.tabs(["Distribución Pagos", "Pagos por Mes","Duración Llamadas","Pago Mes Anterior",
                                                 "Contacto Mes Anterior","Sin Pago Previo"])

# --- Tab 1: Product Performance ---
with tab1:
   
    st.header("Distribución General de Pagos")
    st.plotly_chart(fig1, use_container_width=True)
    
# --- Tab 2: Regional Sales ---
with tab2:
    st.header("Pagos por Mes")
    
    # Bar Chart 2
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.header("Duración Llamadas Ultimos 6 meses")
    st.plotly_chart(fig3, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)

with tab4:
    st.header("Pagos Mes anterior")
    st.plotly_chart(fig5, use_container_width=True)
    st.plotly_chart(fig6, use_container_width=True)

with tab5:
    st.header("Contacto Mes Anterior")
    st.plotly_chart(fig7, use_container_width=True)
    st.plotly_chart(fig8, use_container_width=True)

with tab6:
    st.header("Sin Pago Previo")
    st.plotly_chart(fig9, use_container_width=True)
    st.plotly_chart(fig10, use_container_width=True)
