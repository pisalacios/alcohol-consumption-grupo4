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
