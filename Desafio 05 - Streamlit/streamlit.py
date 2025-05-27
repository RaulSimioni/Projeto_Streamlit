import streamlit as st
import codigo
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Escolar", layout="wide")
st.title("📚 Dashboard de Análise de Notas dos Alunos")

# Estatísticas sempre visíveis com layout compacto
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
col6.metric("< 3.0", len(codigo.media_menor_3))
col7.metric("< 5.0", len(codigo.media_menor_5))
col8.metric("< 7.0", len(codigo.media_menor_7))
col9.metric("< 9.0", len(codigo.media_menor_9))
col10.metric("= 10", len(codigo.media_10))

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
st.subheader("📦 Boxplot - Notas de Português por Série")
fig, ax = plt.subplots(figsize=(6, 4))
sns.boxplot(data=codigo.data_frame, x='serie', y='nota_portugues', ax=ax)
ax.set_title("Notas de Português por Série", fontsize=11)
ax.set_xlabel("Série", fontsize=9)
ax.set_ylabel("Nota de Português", fontsize=9)
ax.tick_params(axis='both', labelsize=8)
st.pyplot(fig)
