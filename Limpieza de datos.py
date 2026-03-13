import pandas as pd

csv = ('https://raw.githubusercontent.com/pisalacios/alcohol-consumption-grupo4/refs/heads/main/15.%20Alcohol%20consumption.csv')

df = pd.read_csv(csv)
df = df.drop(columns=['sex','IndicatorCode','iso3'])
df = df.rename(columns={'country':'Pais',
                        'alcohol_liters_per_capita':'Litros de alcohol per capita',
                        'year':'año',
                        'lower_ci':'limite inferior',
                        'upper_ci':'limite superior',
                        'ci_width':'rango'}
)
paises_europeos = [
'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 
    'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 'Finland', 
    'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 
    'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova, Republic of', 
    'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 
    'Portugal', 'Romania', 'Russian Federation', 'Serbia', 'Slovakia', 
    'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom'
]
df_euro_ordenado = df.sort_values(by=['Pais', 'año'])

df_filtrado = df_euro_ordenado[df_euro_ordenado['Pais'].isin(paises_europeos)]


print(df_filtrado)

