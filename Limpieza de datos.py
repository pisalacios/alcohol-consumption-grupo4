import pandas as pd

csv = ('C:\\Users\\USER\\Desktop\\alcohol-consumption-grupo4\\15. Alcohol consumption.csv')

df = pd.read_csv(csv)
df = df.drop(columns=['sex','IndicatorCode','iso3'])
df = df.rename(columns={'country':'Pais',
                        'alcohol_liters_per_capita':'Litros de alcohol per capita',
                        'year':'año',
                        'lower_ci':'limite inferior',
                        'upper_ci':'limite superior',
                        'ci_width':'rango'}
)
paises_arabes = [
    'Saudi Arabia', 'Lebanon', 'Egypt', 'Morocco', 'Tunisia', 
    'Qatar', 'Jordan', 'Kuwait', 'Bahrain', 'Algeria', 
    'Oman', 'Syrian Arab Republic', 'Iraq', 'Libya', 
    'State of Palestine', 'Sudan', 'Yemen', 'Mauritania', 
    'Somalia', 'Djibouti', 'Comoros'
]

# Filtrar el dataframe
df_filtrado = df[df['Pais'].isin(paises_arabes)]

# Mostrar los primeros resultados para verificar
print(df_filtrado.head(50))

