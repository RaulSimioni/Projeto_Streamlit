import pandas as pd
import matplotlib.pyplot as plt


dataset = pd.read_csv('dados_vendas_acai.csv', delimiter=',', encoding='utf-8')

#● Indicadores: total de vendas, ticket médio, quantidade vendida
#● Número total de clientes únicos
#● Número total de clientes únicos

valor_total = dataset["valor_total"].sum()
quantidade_total = dataset["quantidade"].sum()
total_pedidos = dataset["data_venda"].count()
ticket_medio = valor_total / total_pedidos if total_pedidos > 0 else 0
total_clientes = dataset["cliente"].nunique()
Top1Cliente = dataset["cliente"].value_counts().idxmax()

dataset["data_venda"] = pd.to_datetime(dataset["data_venda"])
dataset["ano_mes"] = dataset["data_venda"].dt.to_period("M").astype(str)

# Agrupamento por mês
vendas_mensais = dataset.groupby("ano_mes")["valor_total"].sum().reset_index()

# Prepara o DataFrame de vendas mensais
df = pd.read_csv("dados_vendas_acai.csv", encoding="utf-8")
df["data_venda"] = pd.to_datetime(df["data_venda"])
df["ano_mes"] = df["data_venda"].dt.to_period("M").astype(str)
vendas_mensais = df.groupby("ano_mes")["valor_total"].sum().reset_index()
vendas_mensais.set_index("ano_mes", inplace=True)


