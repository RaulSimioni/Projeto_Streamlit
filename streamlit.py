import main as m
import streamlit as st

st.title("Análise Estatística e Visualização de Dados")

# Exibir tabela de dados
st.subheader("Dados Brutos")
st.dataframe(m.data_frame.head(10))

# Estatísticas básicas
st.subheader("Estatísticas Básicas")
st.write(f"Média da idade: {m.data_frame['idade'].mean():.2f}")
st.write(f"Média do salário: {m.data_frame['salario'].mean():.2f}")
st.write(f"Moda da idade: {m.data_frame['idade'].mode().values}")
st.write(f"Moda do salário: {m.data_frame['salario'].mode().values}")
st.write(f"Mediana da idade: {m.data_frame['idade'].median():.2f}")
st.write(f"Mediana do salário: {m.data_frame['salario'].median():.2f}")
st.write(f"Variância da idade: {m.data_frame['idade'].var():.2f}")
st.write(f"Variância do salário: {m.data_frame['salario'].var():.2f}")
st.write(f"Amplitude da idade: {m.data_frame['idade'].max() - m.data_frame['idade'].min()}")
st.write(f"Amplitude do salário: {m.data_frame['salario'].max() - m.data_frame['salario'].min()}")


st.subheader("Gráfico de Distribuição por Estado")
st.pyplot(m.plot1())

st.subheader("Boxplot de Salário por Departamento")
st.pyplot(m.plot2())


st.subheader("Gráfico de dispersão entre idade e salario, colorido por departamento.")
st.pyplot(m.plot3())