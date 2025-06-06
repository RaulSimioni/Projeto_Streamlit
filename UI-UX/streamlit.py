import streamlit as st
import pandas as pd
import main as m
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Sistema de Academia Senai", layout="wide")



def colored_card(metric_emoji, metric_label, metric_value, bg_color):
    st.markdown(
        f"""
        <div style='background-color:{bg_color}; padding:20px; border-radius:10px; text-align:center;'>
            <p style='margin:0; font-weight:bold; color:white; font-size:24px;'>
                <span style='font-size:36px;'>{metric_emoji}</span> {metric_label}
            </p>
            <p style='margin:0; font-size:36px; color:white; font-weight:bold;'>{metric_value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def Dashboard():

    st.markdown("<h1 style='text-align:center;'>✔️ Dashboard Açai Londrina</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        colored_card("🛒", "Total de Vendas (R$)", f"R$ {valor_total:,.2f}", "#4CAF50")
    with col2:
        colored_card("💰", "Ticket Médio (R$)", f"R$ {ticket_medio:,.2f}", "#FF9800")
    with col3:
        colored_card("📦","Quantidade Vendida", int(quantidade_total), "#2196F3")

    st.markdown("---")
    col4, col5 = st.columns(2)
    with col4:
        colored_card("👤", "Cliente mais frequente", Top1Cliente, "#9C27B0")
    with col5:
        colored_card("📊", "Quantidade de Clientes por mês", int(total_clientes), "#FFC107")

    st.divider()

    st.markdown("<h1 style='text-align:center;'>Gráfico Evolução de vendas</h1>", unsafe_allow_html=True)
    vendas_mensais = df.groupby("data_venda")["valor_total"].sum().reset_index()
    vendas_mensais.set_index("data_venda", inplace=True)
    st.line_chart(vendas_mensais)


def Metricas():
    st.markdown(
        """
        <div style='text-align:center; padding: 20px 0;'>
            <h1 style='color:white;'>📊 Análise Estatística de Vendas</h1>
            <h4 style='color:white;'>✨ Explore insights detalhados sobre os produtos e categorias</h4>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("---")

    # Layout com colunas
    col1, col2 = st.columns([1, 2])

    with col1:
        top_n = st.selectbox(
            "🔢 Selecione o Top de Produtos",
            options=[5, 10],
            index=0,
            help="Escolha quantos produtos você deseja visualizar no ranking."
        )

    with col2:
        st.markdown(f"### 🛍️ Top {top_n} Produtos Mais Vendidos")

    # 📊 Gráfico interativo com Plotly
    top_produtos = (
        df_filtrado.groupby("produto")["quantidade"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig_produtos = px.bar(
        top_produtos,
        x="produto",
        y="quantidade",
        color="quantidade",
        color_continuous_scale="Aggrnyl",
        title=f"Top {top_n} Produtos por Quantidade Vendida",
        labels={"produto": "Produto", "quantidade": "Qtd Vendida"},
        template="plotly_white"
    )
    fig_produtos.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        title_x=0.5,
        showlegend=False
    )
    st.plotly_chart(fig_produtos, use_container_width=True)

    st.markdown("---")

    st.markdown("### 💵 Categorias Mais Lucrativas")

    # 💵 Gráfico horizontal interativo com Plotly
    categorias_lucrativas = (
        df_filtrado.groupby("categoria")["valor_total"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )

    fig_categorias = px.bar(
        categorias_lucrativas,
        x="valor_total",
        y="categoria",
        orientation='h',
        color="valor_total",
        color_continuous_scale="Aggrnyl",
        labels={"valor_total": "Receita Total", "categoria": "Categoria"},
        title="Receita Total por Categoria",
        template="plotly_white"
    )
    fig_categorias.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        title_x=0.5,
        showlegend=False
    )
    st.plotly_chart(fig_categorias, use_container_width=True)

    # Dica UX
    st.info("🔍 Dica: use os filtros laterais para refinar sua análise por mês, categoria ou produto!", icon="💡")





df = pd.read_csv("dados_vendas_acai.csv", encoding="utf-8")
df["data_venda"] = pd.to_datetime(df["data_venda"])
df["data_venda"] = df["data_venda"].dt.to_period("M").astype(str)

with st.sidebar:
    st.header("Filtros")
    meses_disponiveis = sorted(df["data_venda"].unique(), reverse=True)
    mes_selecionado = st.selectbox("Selecione o Mês", meses_disponiveis)
    st.info("Use os filtros para personalizar a sua consulta dos dados.")
    st.markdown("---")
    if "menu_ativo" not in st.session_state:
        st.session_state.menu_ativo = "Dashboard"

    if st.sidebar.button("Dashboard" ,type='tertiary'):
        st.session_state.menu_ativo = "Dashboard"
    if st.sidebar.button("Dados Estatisticos", type='tertiary'):
        st.session_state.menu_ativo = "Dados Estatisticos"

    menu = st.session_state.menu_ativo

df_filtrado = df[df["data_venda"] == mes_selecionado]

valor_total = df_filtrado["valor_total"].sum()
quantidade_total = df_filtrado["quantidade"].sum()
total_pedidos = df_filtrado.shape[0]
ticket_medio = valor_total / total_pedidos if total_pedidos > 0 else 0
total_clientes = df_filtrado["cliente"].nunique()
Top1Cliente = df_filtrado["cliente"].value_counts().idxmax() if not df_filtrado.empty else "N/A"

if menu == "Dashboard":
    Dashboard()
elif menu == "Dados Estatisticos":
    Metricas()



























