import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def classificar_nota(nota):
    if nota < 3.0:
        return 'Reprovado'
    elif nota < 6.0:
        return 'Exame'
    else:
        return 'Aprovado'


# Leitura do dataset
data_frame = pd.read_csv('dados_alunos_escola.csv', delimiter=',', encoding='utf-8')


estatisticas = {
    "Média": data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].mean(),
    "Mediana": data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].median(),
    "Moda": data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].mode().iloc[0],
    "Variância": data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].var(),
    "Amplitude": data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].max() - data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].min(),
    "Desvio Padrão": data_frame[['nota_matematica', 'nota_portugues', 'nota_ciencias']].std(),
}

# Frequência média por série
frequencia = data_frame.groupby('serie')['frequencia_%'].mean()

# Média de alunos com frequência abaixo de 75%
frequencia_75 = data_frame[data_frame['frequencia_%'] < 75].copy()
frequencia_75['Nota_Media'] = round(frequencia_75[['nota_portugues', 'nota_matematica', 'nota_ciencias']].mean(axis=1), 1)

# Nota média por cidade e disciplina
nota_media_por_cidade = data_frame.groupby('cidade')[['nota_matematica', 'nota_portugues', 'nota_ciencias']].mean()

# Cálculo da nota média geral e classificação
data_frame['Nota_Media'] = round(data_frame[['nota_portugues', 'nota_matematica', 'nota_ciencias']].mean(axis=1), 1)
data_frame['Classificacao'] = data_frame['Nota_Media'].apply(classificar_nota)

# Contagens de alunos por faixas de nota
media_menor_3 = data_frame[data_frame['Nota_Media'] < 3.0]
media_menor_5 = data_frame[data_frame['Nota_Media'] < 5.0]
media_menor_7 = data_frame[data_frame['Nota_Media'] < 7.0]
media_menor_9 = data_frame[data_frame['Nota_Media'] < 9.0]
media_10 = data_frame[data_frame['Nota_Media'] == 10.0]

# Melhor e pior nota média por cidade
melhor_nota_cidade = data_frame.groupby('cidade')['Nota_Media'].max()
pior_nota_cidade = data_frame.groupby('cidade')['Nota_Media'].min()

quant_alunos_por_cidade = data_frame.groupby('cidade')['nome'].count()

# Histogramas das notas
colunas_notas = ["nota_matematica", "nota_portugues", "nota_ciencias"]

for coluna in colunas_notas:
    fig, ax = plt.subplots()
    ax.hist(data_frame[coluna], bins=10, color='skyblue', edgecolor='black')
    ax.set_title(f"Histograma de {coluna}")
    ax.set_xlabel("Notas")
    ax.set_ylabel("Frequência")
    plt.show()
