import codigo
import streamlit as st


st.title("Estatísticas das Notas 📊")
for key, value in codigo.estatisticas.items():
    st.write(f"**{key}**:")
    st.write(value)

# Exibir frequência média por série
st.subheader("Frequência Média por Série")
frequencia_media = codigo.data_frame.groupby('serie')['frequencia_%'].mean()
st.write(round(frequencia_media, 2))


