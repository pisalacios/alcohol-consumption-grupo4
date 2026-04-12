# Bliblioteca de paquetes
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página

st.set_page_config(
    page_title="Alcolismo Europa Dashboard Interactivo", 
    layout="wide",
)

st.write("## Análisis del Consumo de Alcohol en Europa 🍷")
st.markdown("""
#### Impacto antes, durante y después de la pandemia del COVID-19
---
""")

st.markdown("""
En este dashboard interactivo podrás visualizar como fué el consumo anual de litros de 
licor en diferentes paises de Europa por persona habitada
""")

# Carga de la BBDD
df = pd.read_excel("alcohol_filtrado.xlsx")
