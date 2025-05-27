import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Dashboard de Clientes", layout="wide")

data_frame = pd.read_csv('clientes.csv', delimiter=',', encoding='latin1')

categoria_counts = data_frame['Categoria'].value_counts()

df_Cancelados = data_frame[data_frame['Categoria'] == "Cancelado"]
cartao_counts = df_Cancelados['Categoria Cartão'].value_counts()

df_salario_anual = df_Cancelados['Faixa Salarial Anual'].value_counts()

qnt_cancelados = len(df_Cancelados)

st.title("📊 Dashboard de Clientes")
st.markdown("Bem-vindo ao painel de clientes! Aqui você pode visualizar a distribuição das categorias e outras métricas importantes.")

st.subheader("📜 Lista de Clientes Cancelados")
st.dataframe(df_Cancelados)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("📌 Estatísticas")
    st.metric(label="Total de Clientes", value=len(data_frame))
    st.metric(label="Clientes Cancelados", value=qnt_cancelados)
    st.metric(label="Clientes Ativos", value=len(data_frame) - qnt_cancelados)

with col2:
    st.subheader("Distribuição das Categorias")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(categoria_counts, labels=categoria_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 
    plt.title('Distribuição das Categorias')
    st.pyplot(fig)

with col3:
    st.subheader("Quantidade de meses como cliente dos usuários cancelados")
    
    fig, ax = plt.subplots(figsize=(8, 5)) 
    ax.hist(df_Cancelados['Meses como Cliente'], bins=20, color='skyblue', edgecolor='black')
    ax.set_title('Meses Ativos dos clientes cancelados', fontsize=14)
    ax.set_xlabel('Meses', fontsize=12)
    ax.set_ylabel('Quantidade de Clientes', fontsize=12)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)
