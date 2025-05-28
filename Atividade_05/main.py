import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

def Faixa_Etaria(idade):
  if idade <= 25:
    return 'Jovem'
  elif idade <= 45:
    return 'Adulto'
  else:
    return 'Sênior'

def plot1():
    fig, ax = plt.subplots()
    sns.countplot(x='estado', data=data_frame, ax=ax)
    return fig

def plot2():
  fig2, ax2 = plt.subplots()
  sns.boxplot(x='departamento', y='salario', data=data_frame, ax=ax2)
  return fig2

def plot3():
  fig3, ax3 = plt.subplots()
  plt.title("Idade x Salário por Departamento")
  sns.scatterplot(x='idade', y='salario', hue='departamento', data=data_frame, ax=ax3)
  return fig3

data_frame = pd.read_csv('dados_estatistica_visualizacao.csv', sep=',', encoding='utf-8')

print(data_frame.head(10))

media_idade = data_frame['idade'].mean()
media_salario = data_frame['salario'].mean()
print('-----------------------------------------------------')
print("\nA média da idade é:",media_idade)
print("A média do salario é:",media_salario)

moda_idade = data_frame['idade'].mode()
moda_salario = data_frame['salario'].mode()
print('-----------------------------------------------------')
print("\nA moda da idade é:",moda_idade)
print("A moda do salario é:",moda_salario)
print('-----------------------------------------------------')

mediana_idade = data_frame['idade'].median()
mediana_salario = data_frame['salario'].median()

print("\nA mediana da idade é:",mediana_idade, '\n')
print("A mediana do salario é:",mediana_salario)
print('-----------------------------------------------------')
var_idade = data_frame['idade'].var()
var_salario = data_frame['salario'].var()

print("\nA variancia da idade é:",var_idade, '\n')
print("A variancia do salario é:",var_salario)
print('-----------------------------------------------------')

data_frame['idade'].max() - data_frame['idade'].min()
print('\nAmplitude da idade:', data_frame['idade'].max() - data_frame['idade'].min())
data_frame['salario'].max() - data_frame['salario'].min()
print('Amplitude do salario:', data_frame['salario'].max() - data_frame['salario'].min())


data_frame['Faixa_Etaria'] = data_frame['idade'].apply(Faixa_Etaria)
print(data_frame)
