import pandas as pd
import seaborn as sns
import matplotlib as plot

#1. Calcule a média, mediana, moda, variância, amplitude e desvio padrão das notas de
#matemática, português e ciências.

def classificar_nota(nota):
    if nota < 3.0:
        return 'Reprovado'
    elif nota < 6.0:
        return 'Exame'
    else:
        return 'Aprovado'


data_frame = pd.read_csv('dados_alunos_escola.csv', delimiter=',', encoding='utf-8')

estatisticas = {
    "Média": data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].mean(),
    "Mediana": data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].median(),
    "Moda": data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].mode().iloc[0],
    "Variância": data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].var(),
    "Amplitude": data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].max() - data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].min(),
    "Desvio Padrão": data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].std(),
}


#2. Qual é a frequência média dos alunos por série?

frequencia = data_frame.groupby('serie')['frequencia_%'].mean()
#print(round(frequencia, 2))

#3. Filtre os alunos com frequência abaixo de 75% e calcule a média geral deles.

frequencia_75 = data_frame[data_frame['frequencia_%'] < 75]
frequencia_75['Nota_Media'] = round(frequencia_75[['nota_portugues', 'nota_matematica', 'nota_ciencias']].mean(axis=1), 1)
#print(frequencia_75)

#4. Use groupby para obter a nota média por cidade e matéria.

nota_media_por_cidade = data_frame.groupby('cidade')[['nota_matematica', 'nota_portugues', 'nota_ciencias']].mean()

# 5. Crie a seguinte classificação:
#a. Nota menor que 3,0 = reprovado
#b. Nota menor que 6,0 = exame
#c. Nota acima de 6,0 = aprovado

data_frame['Classificação'] = frequencia_75['Nota_Media'].apply(classificar_nota)
print(data_frame)

# 6. Quantos alunos possuem a nota menor que 3,0?

data_frame['Nota_Media'] = round(data_frame[['nota_portugues', 'nota_matematica', 'nota_ciencias']])