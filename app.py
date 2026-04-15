    # Bliblioteca de paquetes y BBDD
import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl as op

alcohol = pd.read_excel("Data/Clean/Alcohol_Filtrado.xlsx")

    # Configuración de la página

st.set_page_config(
    page_title="Alcoholismo Europa Dashboard Interactivo", 
    layout="wide",
    page_icon="Photos\\Logo de la Web.png"
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
tab1, tab4, tab2, tab3 = st.tabs(
    [
        "**Métricas Principales**",
        "**Ranking de la Pandemia**", 
        "**Evolución Anual**",
        "**Análisis de Dispersión**"
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
    
        # Para indicar los filtros aplicados en la vista
    st.info(f"**Filtros aplicados:** Datos desde el año **{rango_años[0]}** al **{rango_años[1]}**, "
            f"incluyendo **{cantidad_paises}** países seleccionados.")

with tab2:
    st.subheader("🔍 Evolución del Consumo de Alcohol de los Países")       # titulo

    col_izq, col_der = st.columns([3, 1])                                   # distribucion

    # Gráfico 1 IZQUIERDA - Gráficos de lineas

    with col_izq:
        st.markdown("##### Promedio General de los Países")         # titulo del gráfico
        
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

        # Para indicar los filtros aplicados en la vista
    st.info(f"**Filtros aplicados:** Datos desde el año **{rango_años[0]}** al **{rango_años[1]}**, "
            f"incluyendo **{cantidad_paises}** países seleccionados.")

    # Tabla DERECHA - Promedios de temporadas 

    with col_der:
        st.markdown("##### Promedios por Temporada")        # titulo de la tabla
        
        promedio_antes = df_filtrado[df_filtrado['temporada'] == 'Antes']['litros_por_persona'].mean()
        promedio_durante = df_filtrado[df_filtrado['temporada'] == 'Durante']['litros_por_persona'].mean()
        promedio_despues = df_filtrado[df_filtrado['temporada'] == 'Después']['litros_por_persona'].mean()

        st.metric("Antes (2016-2019)", f"{promedio_antes:.2f} L")
        st.metric("Durante (2020)", f"{promedio_durante:.2f} L")
        st.metric("Después (2022)", f"{promedio_despues:.2f} L")

with tab3:
    st.subheader("📦 Distribución del Consumo por temporada Pandémica")       # titulo

    st.markdown("##### Dispersión del Consumo de Alcohol en Europa")        # titulo del gráfico

        # Filtramos para al excluir 2021 y quedarnos con las temporadas de estudio
    df_box = df_filtrado[df_filtrado['temporada'].isin(['Antes', 'Durante', 'Después'])]

    # Gráfico 1 - Diagrama de caja

    fig_box = px.box(
        df_box,
        x="temporada",
        y="litros_por_persona",
        color="temporada",
        notched=True,
        template="plotly_dark",
        color_discrete_map={            # Tonos de azul para mantener la estética
            "Antes": "#045dc2",
            "Durante": "#50a1ff",
            "Después": "#022d5e"
        },
        category_orders={"temporada": ["Antes", "Durante", "Después"]},     # Forzamos el orden de la vista
        labels={"litros_por_persona": "Consumo (Litros por Persona)", "temporada": "Periodo de la Pandemia"},
    )

    st.plotly_chart(fig_box, use_container_width=True)

        # Para indicar los filtros aplicados en la vista
    st.info(f"**Filtros aplicados:** Datos desde el año **{rango_años[0]}** al **{rango_años[1]}**, "
            f"incluyendo **{cantidad_paises}** países seleccionados.")

with tab4:
    st.subheader("🔥Ranking de Países con Mayor Consumo de Litros de Alcohol (p/p)")

        # Añadiendo a los filtro un dezlizable para el ranking
    n_top = st.sidebar.slider("Número de países para el ranking:", 1, 20, 10)    # mostrará por defecto top 10
        # Añadiendo al filtro para seleccionar la temporada de la pandemia
    periodo_seleccionado = st.sidebar.radio(
        "Seleccionar periodo para el ranking:",
        options=["Antes", "Durante", "Después"],
        index=1     # mostrará por defecto "durante"
    )

        #  Mostrar solo la temporada durante (media de los distintos valores de los registros)
    df_periodo = df_filtrado[df_filtrado['temporada'] == periodo_seleccionado]
    df_ranking = df_periodo.groupby('pais')['litros_por_persona'].mean().reset_index()
        # Para que tome el top N que escojamos de los mayores
    df_ranking = df_ranking.sort_values(by='litros_por_persona', ascending=False).head(n_top)

        # Gráfico 1 - Barras desendentes (mayor a menor)

    fig_bar = px.bar(
        df_ranking,
        x='litros_por_persona',
        y='pais',
        orientation='h',                # Mostar en horizontal
        color='litros_por_persona',
        color_continuous_scale=['#ef5350', '#d32f2f', '#b30000'],
        template="plotly_dark",
        labels={'litros_por_persona': 'Promedio de Litros (p/p)', 'pais': 'País'},
        text_auto='.1f'                 # para redondear solo un decimal en los valores
    )

# Configuraciones extras del gráfico de la leyenda y ejes
    fig_bar.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        font=dict(color="black"),           # números de valores del gráfico en negro
        yaxis=dict(
            tickfont=dict(color="black")    # letras del eje Y negro
        ),
        xaxis=dict(
            tickfont=dict(color="black")    # letras del eje X negro
        )
    )
        # para poner los balores al lado de su respectiva barra
    fig_bar.update_traces(textposition='outside')   

        # Invirtiendo eje Y para que sea desendente 
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})

    st.plotly_chart(fig_bar, use_container_width=True)

#--------------------------------------------------------------------------------------------------------

    st.subheader("🧊Ranking de Países con Menor Consumo de Litros de Alcohol (p/p)")
    
        # Reobtener la lista de paises para que filtre de nuevo
    df_ranking_min = df_periodo.groupby('pais')['litros_por_persona'].mean().reset_index()

        # Para que tome el top N que escojamos de los menores
    df_min = df_ranking_min.sort_values(by='litros_por_persona', ascending=True).head(n_top)

        # Gráfico 2 - Barras esendentes (mayor a menor) para mantener estetica

    fig_min = px.bar(
            df_min, x='litros_por_persona',
            y='pais',
            orientation='h',                # Mostar en horizontal
            color='litros_por_persona',
            color_continuous_scale=['#003366', '#0059b3', '#3399ff'],
            template="plotly_dark",
            labels={'litros_por_persona': 'Promedio (p/p)', 'pais': 'País'},
            text_auto='.1f'                 # para redondear solo un decimal en los valores
    )

        # Configuraciones extras del gráfico de la leyenda y ejes
    fig_min.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            font=dict(color="black"),           # números de valores del gráfico en negro
            xaxis=dict(
                range=[0, 18],                  # escala hasta el valor 18 para mantener estetica
                tickfont=dict(color="black")    # letras del eje X negro
                ),
            yaxis=dict(
                tickfont=dict(color="black"),    # letras del eje Y negro
                )
    )

        # para poner los balores al lado de su respectiva barra
    fig_min.update_traces(textposition='outside')
       
        # Invertimos el orden para que el valor más bajo quede abajo
    fig_min.update_layout(yaxis={'categoryorder':'total descending'})

    st.plotly_chart(fig_min, use_container_width=True)

        # Para indicar los filtros aplicados en la vista
    st.info(f"**Filtros de Ranking:** Mostrando el Top **{n_top}** países "
            f"durante el periodo **{periodo_seleccionado}**.")



