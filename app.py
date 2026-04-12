    # Bliblioteca de paquetes y BBDD
import streamlit as st
import pandas as pd
import plotly.express as px

alcohol = pd.read_excel("alcohol_filtrado.xlsx")

    # Configuración de la página

st.set_page_config(
    page_title="Alcolismo Europa Dashboard Interactivo", 
    layout="wide",
    page_icon="Logo de la Web.png"
)

    # Titulo, subtitulo y descripción

st.write("## Análisis del Consumo de Alcohol en Europa 🍷")
st.markdown("""
#### Impacto antes, durante y después de la pandemia del COVID-19
---
""")

st.markdown("""
En este dashboard interactivo podrás visualizar como fué el consumo anual de litros de 
licor en diferentes paises de Europa por persona habitada
""")
    # Filtro de busqueda

st.sidebar.header("Opciones de Visualización")

paises_disponibles = sorted(alcohol['pais'].unique())
paises_seleccionados = st.sidebar.multiselect(
    "Selecciona los países:",
    options=paises_disponibles,
    default=paises_disponibles
)
df_filtrado = alcohol[alcohol['pais'].isin(paises_seleccionados)]

    # 1er cuadro de información

sumatoria_total = df_filtrado['litros_por_persona'].sum()
st.metric("Suma de litros p/p consumidos", f"{sumatoria_total:.2f}")
st.caption("Sumatoria de litros consumidos en la seleción de la bsuqueda")