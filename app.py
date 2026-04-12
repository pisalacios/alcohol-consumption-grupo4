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

st.divider()

    # Filtro de busqueda

st.sidebar.header("Opciones de Visualización")
        # Países
paises_disponibles = sorted(alcohol['pais'].unique())
paises_seleccionados = st.sidebar.multiselect(
    "Selecciona los países:",
    options=paises_disponibles,
    default=paises_disponibles
)
df_filtrado = alcohol[alcohol['pais'].isin(paises_seleccionados)]

        # Años
años_disponibles = sorted(alcohol['año'].unique())
rango_años = st.sidebar.select_slider(
    "Selecciona el rango de años:",
    options=años_disponibles,
    value=(años_disponibles[0], años_disponibles[-1])
)

        # Combinando el filtro
df_filtrado = alcohol[
    (alcohol['pais'].isin(paises_seleccionados)) & 
    (alcohol['año'] >= rango_años[0]) & 
    (alcohol['año'] <= rango_años[1])
]

    # Recuadros de información descriptiva básica

st.subheader("📈 Resumen de la BBDD")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🍺Total Consumido")
    sumatoria_total = df_filtrado['litros_por_persona'].sum() 
    st.metric("Suma de litros de alcohol p/p", f"{sumatoria_total:.2f}")

with col2:
    st.markdown("#### 🚨Máximo Registrado")
    max_alto = df_filtrado['limite_sup'].max()
    st.metric("Límite superior más alto de un país", f"{max_alto:.2f}")

with col3:
    st.markdown("#### 📊Promedio Global")
    promedio_consumo = df_filtrado['litros_por_persona'].mean()
    st.metric("Promedio de litros de alcohol consumimos", f"{promedio_consumo:.2f}")

st.divider()

