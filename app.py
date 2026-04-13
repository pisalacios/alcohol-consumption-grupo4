    # Bliblioteca de paquetes y BBDD
import streamlit as st
import pandas as pd
import plotly.express as px

alcohol = pd.read_excel("alcohol_filtrado.xlsx")

    # Configuración de la página

st.set_page_config(
    page_title="Alcoholismo Europa Dashboard Interactivo", 
    layout="wide",
    page_icon="Logo de la Web.png"
)

    # Titulo, subtitulo y descripción

st.write("## Análisis del Consumo de Alcohol en Europa 🍷")
st.markdown("""
#### Impacto Antes, Durante y Después de la Pandemia del COVID-19
---
""")

st.markdown("""
En este dashboard interactivo podrás visualizar y comprender el consumo de alcohol
en los paises de la región de europa
""")

    # Filtro de busqueda

st.sidebar.header("Opciones de Visualización")
        # Países
paises_disponibles = sorted(alcohol['pais'].unique())
paises_seleccionados = st.sidebar.multiselect(
    "Selecciona los países:",
    options=paises_disponibles,
    default=paises_disponibles
)

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

    # Separando por pestañas los resultados y gráficos
tab1, tab2 = st.tabs(
    [
        "**Métricas Principales**", 
        "**Evolución Anula**"
    ]
)

with tab1:
    st.subheader("📈 Resumen de los Indicadores del Consumo de Alcohol")      # titulo
    
    with st.container(border=True):                                            # distribucion
        col1, col2, col3 = st.columns(3)

            # Recuadros de información descriptiva básica

        with col1:
            st.markdown("#### 🍺Consumo Total en Europa")
            sumatoria_total = df_filtrado['litros_por_persona'].sum() 
            st.metric("Suma de litros p/p acumulados", f"{sumatoria_total:.2f}")

        with col2:
            st.markdown("#### 🌍Países Seleccionados")
            cantidad_paises = df_filtrado['pais'].nunique()
            st.metric("Total de países en la vista", f"{cantidad_paises}")

        with col3:
            st.markdown("#### 📊Promedio de Litros por Persona")
            promedio_consumo = df_filtrado['litros_por_persona'].mean()
            st.metric("Promedio de litros de alcohol anuales consumidos", f"{promedio_consumo:.2f}")

with tab2:
    st.subheader("🔍 Evolución del Consumo de Alcohol de los Países")       # titulo

    col_izq, col_der = st.columns([3, 1])                                   # distribucion

    # Gráfico 1 IZQUIERDA - Gráficos de lineas
    
    with col_izq:
        st.markdown("##### Promedio General de los Países")
        
        df_promedio = df_filtrado.groupby('año')['litros_por_persona'].mean().reset_index()

        fig_1=px.line(
            df_promedio, 
            x="año", 
            y="litros_por_persona",
            markers=True,
            line_shape="linear",
            template="plotly_white",
            color_discrete_sequence=["#045dc2"], 
            labels={"litros_por_persona": "Promedio de Litros (p/p)", "año": "Año"},
            )

        st.plotly_chart(fig_1, use_container_width=True)

    # Tabla DERECHA - Promedios de temporadas 

    with col_der:
        st.markdown("##### Promedios por Temporada")
        
        promedio_antes = df_filtrado[df_filtrado['temporada'] == 'Antes']['litros_por_persona'].mean()
        promedio_durante = df_filtrado[df_filtrado['temporada'] == 'Durante']['litros_por_persona'].mean()
        promedio_despues = df_filtrado[df_filtrado['temporada'] == 'Después']['litros_por_persona'].mean()

        st.metric("Antes (2016-2019)", f"{promedio_antes:.2f} L")
        st.metric("Durante (2020)", f"{promedio_durante:.2f} L")
        st.metric("Después (2022)", f"{promedio_despues:.2f} L")

