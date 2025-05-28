import streamlit as st
import codigo
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Escolar", layout="wide")
st.title("📚 Dashboard de Análise de Notas dos Alunos")

st.subheader("📊 Estatísticas Gerais das Notas")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Média Matemática", round(codigo.estatisticas['Média']['nota_matematica'], 2))
    st.metric("Moda Matemática", codigo.estatisticas['Moda']['nota_matematica'])
with col2:
    st.metric("Média Português", round(codigo.estatisticas['Média']['nota_portugues'], 2))
    st.metric("Moda Português", codigo.estatisticas['Moda']['nota_portugues'])
with col3:
    st.metric("Média Ciências", round(codigo.estatisticas['Média']['nota_ciencias'], 2))
    st.metric("Moda Ciências", codigo.estatisticas['Moda']['nota_ciencias'])

st.markdown("---")
st.subheader("📈 Frequência Média por Série")
frequencia_media = codigo.data_frame.groupby('serie')['frequencia_%'].mean()
st.write(frequencia_media)

st.markdown("---")
col4, col5 = st.columns(2)
with col4:
    st.subheader("🏙️ Melhor Nota Média por Cidade")
    st.dataframe(codigo.melhor_nota_cidade)

with col5:
    st.subheader("🏙️ Pior Nota Média por Cidade")
    st.dataframe(codigo.pior_nota_cidade)

st.markdown("---")
st.subheader("🔍 Alunos por Faixa de Nota Média")
col6, col7, col8, col9, col10 = st.columns(5)
col6.metric("Notas menores que 3.0", len(codigo.media_menor_3))
col7.metric("Notas menores que 5.0", len(codigo.media_menor_5))
col8.metric("Notas menores que 7.0", len(codigo.media_menor_7))
col9.metric("Notas menores que 9.0", len(codigo.media_menor_9))
col10.metric("Notas 10", len(codigo.media_10))

st.markdown("---")
st.subheader("📊 Histogramas de Notas por Disciplina")
col11, col12, col13 = st.columns(3)

for coluna, container in zip(["nota_matematica", "nota_portugues", "nota_ciencias"], [col11, col12, col13]):
    with container:
        fig, ax = plt.subplots(figsize=(3.5, 2.5))
        sns.histplot(codigo.data_frame[coluna], kde=True, bins=10, ax=ax)
        ax.set_title(f"{coluna.replace('nota_', '').capitalize()}", fontsize=9)
        ax.set_xlabel("Nota", fontsize=8)
        ax.set_ylabel("Frequência", fontsize=8)
        ax.tick_params(axis='both', labelsize=7)
        st.pyplot(fig)

st.markdown("---")
st.subheader("📦 Boxplot - Notas de matérias por Série")

col1, col2, col3 = st.columns([1, 1, 1])

fig, ax = plt.subplots(figsize=(6, 4))
sns.boxplot(data=codigo.data_frame, x='serie', y='nota_portugues', ax=ax, color='green')
ax.set_title("Notas de Português por Série", fontsize=11)
ax.set_xlabel("Série", fontsize=9)
ax.set_ylabel("Nota de Português", fontsize=9)
ax.tick_params(axis='both', labelsize=8)

fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.boxplot(data=codigo.data_frame, x='serie', y='nota_matematica', ax=ax2, color='blue')
ax2.set_title("Notas de Matematica por Série", fontsize=11)
ax2.set_xlabel("Série", fontsize=9)
ax2.set_ylabel("Nota de Matematica", fontsize=9)
ax2.tick_params(axis='both', labelsize=8)

fig3, ax3 = plt.subplots(figsize=(6, 4))
sns.boxplot(data=codigo.data_frame, x='serie', y='nota_ciencias', ax=ax3, color='purple')
ax3.set_title("Notas de Ciencias por Série", fontsize=11)
ax3.set_xlabel("Série", fontsize=9)
ax3.set_ylabel("Nota de Ciencias", fontsize=9)
ax3.tick_params(axis='both', labelsize=8)


with col1:
    st.pyplot(fig)
with col2:
    st.pyplot(fig2)
with col3:
    st.pyplot(fig3)


st.subheader("📊 Gráfico de barra - Qunatidade de alunos por cidade")
fig4, ax4 = plt.subplots(figsize=(8, 5))
sns.barplot(x=codigo.quant_alunos_por_cidade.index, y=codigo.quant_alunos_por_cidade.values, ax=ax4, palette="viridis")
ax4.set_title("Quantidade de Alunos por Cidade", fontsize=12)
ax4.set_xlabel("Cidade", fontsize=10)
ax4.set_ylabel("Número de Alunos", fontsize=10)
ax4.tick_params(axis='x', rotation=45, labelsize=9)

col1, col_central, col3 = st.columns([1, 2, 1])

with col_central:
    st.pyplot(fig4)


st.subheader("📊 Gráfico de barra - Dispersão Frequencia x Nota por Matéria")
fig5, ax5 = plt.subplots()
sns.scatterplot(data=codigo.data_frame, x="frequencia_%", y="Nota_Media", hue="Nota_Media", ax=ax5)
ax5.set_title("Dispersão: Frequência vs Nota por Matéria")
ax5.set_xlabel("Frequência (%)")
ax5.set_ylabel("Nota")

col1, col_central, col3 = st.columns([1, 2, 1])

with col_central:
    st.pyplot(fig5)






