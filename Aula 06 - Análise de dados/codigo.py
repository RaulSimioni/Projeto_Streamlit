import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Dashboard de Clientes", layout="wide")

data_frame = pd.read_csv('clientes.csv', delimiter=',', encoding='latin1')

cancelados = data_frame[data_frame['Categoria'] == 'Cancelado']
ativos = data_frame[data_frame['Categoria'] != 'Cancelado']

total_clientes = len(data_frame)
qnt_cancelados = len(cancelados)
qnt_ativos = len(ativos)

st.title("📊 Dashboard de Clientes")
st.markdown("Bem-vindo ao painel de clientes! Aqui você pode visualizar a distribuição das categorias e outras métricas importantes.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("📌 Estatísticas")
    st.metric(label="Total de Clientes", value=total_clientes)
    st.metric(label="Clientes Cancelados", value=qnt_cancelados)
    st.metric(label="Clientes Ativos", value=qnt_ativos)

with col2:
    st.subheader("Distribuição das Categorias")
    categoria_counts = data_frame['Categoria'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(categoria_counts, labels=categoria_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('Distribuição das Categorias')
    st.pyplot(fig)

with col3:
    st.subheader("Distribuição por Faixa Salarial Anual (Cancelados)")
    salario_cancelados = cancelados['Faixa Salarial Anual'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    salario_cancelados.plot(kind='bar', ax=ax)
    ax.set_ylabel('Quantidade')
    ax.set_title('Faixa Salarial Anual dos Cancelados')
    st.pyplot(fig)

with col4:
    st.subheader("Distribuição por Categoria do Cartão (Cancelados)")
    cartao_cancelados = cancelados['Categoria Cartão'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    cartao_cancelados.plot(kind='bar', ax=ax)
    ax.set_ylabel('Quantidade')
    ax.set_title('Categoria do Cartão dos Cancelados')
    st.pyplot(fig)

st.markdown("---")

st.subheader("Distribuição de Idade dos Clientes")
fig, ax = plt.subplots(figsize=(10, 5))

bins = range(data_frame['Idade'].min(), data_frame['Idade'].max() + 1, 1)

ax.hist(ativos['Idade'], bins=bins, alpha=0.5, label='Ativos', color='green', edgecolor='black')
ax.hist(cancelados['Idade'], bins=bins, alpha=0.7, label='Cancelados', color='red', edgecolor='black')

ax.set_title('Distribuição de Idade dos Clientes Cancelados e Ativos')
ax.set_xlabel('Idade')
ax.set_ylabel('Quantidade de Clientes')
ax.legend()

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

st.pyplot(fig)

st.subheader("Meses como Cliente dos Cancelados")
fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(cancelados['Meses como Cliente'], bins=20, color='skyblue', edgecolor='black')
ax.set_title('Meses como Cliente - Cancelados')
ax.set_xlabel('Meses')
ax.set_ylabel('Quantidade de Clientes')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

st.subheader("Taxa de Utilização do Cartão")
fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(ativos['Taxa de Utilização Cartão'], bins=30, alpha=0.5, label='Ativos', color='green', edgecolor='black')
ax.hist(cancelados['Taxa de Utilização Cartão'], bins=30, alpha=0.7, label='Cancelados', color='red', edgecolor='black')
ax.set_title('Taxa de Utilização do Cartão - Cancelados vs Ativos')
ax.set_xlabel('Taxa de Utilização')
ax.set_ylabel('Quantidade de Clientes')
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

st.markdown("---")
st.subheader("Conclusões e Recomendações")
st.markdown(
    "\n- Percebemos um aumento no número de cancelamentos por volta dos 30 a 40 anos, o que pode indicar insatisfação ou algum evento específico nessa faixa etária."
    "\n- Clientes que cancelam tendem a ter menor taxa de utilização do cartão e menor tempo como cliente."
    "\n- As faixas salariais e categorias de cartão dos cancelados podem indicar segmentos mais vulneráveis que merecem atenção especial."
    "\n- Recomenda-se ações focadas em retenção para clientes próximos a 36 anos, incluindo ofertas personalizadas e campanhas de engajamento."
    "\n- Monitorar continuamente a taxa de utilização e tempo de relacionamento para identificar clientes com risco de cancelamento."
)

st.subheader("📜 Lista de Clientes Cancelados")
st.dataframe(cancelados.reset_index(drop=True))
