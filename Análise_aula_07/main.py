#1. Os vários fatores de previsão inicialmente escolhidos realmente afetam a expectativa de
#vida? Quais são as variáveis de previsão que realmente afetam a expectativa de vida?
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_frame = pd.read_csv('Life_Expectancy_Data.csv', delimiter=',', encoding='utf-8')

filtered_df = data_frame[['Life expectancy', 'Income composition of resources', 'Adult Mortality', 'BMI', 'Schooling']].dropna()

print(filtered_df)