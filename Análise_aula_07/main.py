import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_and_clean_data(path):
    df = pd.read_csv(path)
    df = df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'))

    df = df[(df['year'] >= 2000) & (df['year'] <= 2015)]
    for col in df.columns:
        if df[col].dtype == 'object' or str(df[col].dtype) == 'category':
            mode = df[col].mode()
            if not mode.empty:
                df[col].fillna(mode[0], inplace=True)
        else:
            mean = df[col].mean()
            df[col].fillna(mean, inplace=True)

    df['status'] = df['status'].astype('category')

    key_vars = [
        'life_expectancy', 'hepatitis_b', 'polio', 'diphtheria', 'adult_mortality',
        'infant_deaths', 'under-five_deaths', 'gdp', 'total_expenditure',
        'percentage_expenditure', 'income_composition_of_resources', 'population',
        'schooling', 'alcohol', 'bmi', 'hiv/aids', 'thinness__1-19_years', 'thinness_5-9_years'
    ]
    df = df.dropna(subset=key_vars)

    return df



def plot_scatter_with_regression(df, x_col, y_col, title, xlabel, ylabel):
    plt.figure(figsize=(7, 5))
    sns.regplot(data=df, x=x_col, y=y_col, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    st.pyplot(plt)
    plt.clf()


st.title("Análise da Expectativa de Vida (2000-2015) - Simplificado")
df = load_and_clean_data("./Life_Expectancy_Data.csv")

immunization_vars = ['hepatitis_b', 'polio', 'diphtheria']
mortality_vars = ['adult_mortality', 'infant_deaths', 'under-five_deaths']
economy_vars = ['gdp', 'total_expenditure', 'percentage_expenditure', 'income_composition_of_resources', 'population']
social_vars = ['schooling', 'alcohol', 'bmi', 'hiv/aids', 'thinness__1-19_years', 'thinness_5-9_years']

st.header("1. Correlações entre fatores e expectativa de vida")
selected_vars = immunization_vars + mortality_vars + economy_vars + social_vars
corrs = df[selected_vars + ['life_expectancy']].corr()['life_expectancy'].sort_values()
st.write(corrs)
st.write("\nAnálise: Valores negativos indicam que o fator reduz a expectativa de vida; positivos indicam aumento.")

st.header("2. Expectativa de vida < 65 e gasto em saúde")
low_life_df = df[df['life_expectancy'] < 65]
st.write(f"Número de registros com expectativa < 65: {len(low_life_df)}")

st.header("3. Mortalidade infantil e adulta x Expectativa de vida")
for col in ['adult_mortality', 'infant_deaths']:
    plot_scatter_with_regression(df, col, 'life_expectancy', f'Expectativa de vida vs {col.replace("_", " ")}', col.replace("_", " "), 'Expectativa de vida')
cor_adult = df['adult_mortality'].corr(df['life_expectancy'])
cor_infant = df['infant_deaths'].corr(df['life_expectancy'])
st.write(f"Correlação mortalidade adulta e expectativa: {cor_adult:.3f}")
st.write(f"Correlação mortalidade infantil e expectativa: {cor_infant:.3f}")
st.write("Análise: Correlações negativas indicam impacto adverso das mortalidades na expectativa de vida.")

st.header("4. Hábitos e estilo de vida x Expectativa de vida")
habits = ['alcohol', 'bmi', 'hiv/aids', 'thinness__1-19_years', 'thinness_5-9_years']
for col in habits:
    plot_scatter_with_regression(df, col, 'life_expectancy', f'Expectativa de vida vs {col.replace("_", " ")}', col.replace("_", " "), 'Expectativa de vida')
st.write("Análise: Correlação indica que hábitos impactam positivamente ou negativamente a expectativa.")

st.header("5. Escolaridade e Expectativa de vida")
plot_scatter_with_regression(df, 'schooling', 'life_expectancy', 'Expectativa de vida vs Escolaridade', 'Escolaridade (anos)', 'Expectativa de vida')
st.write("Análise: Escolaridade tende a ter correlação positiva, refletindo melhores condições.")

st.header("6. Consumo de álcool e Expectativa de vida")
plot_scatter_with_regression(df, 'alcohol', 'life_expectancy', 'Expectativa de vida vs Consumo de álcool', 'Consumo de álcool', 'Expectativa de vida')
st.write("Análise: Observa se que o consumo de álcool tem impacto negativo.")

st.header("7. População e Expectativa de vida")
plot_scatter_with_regression(df, 'population', 'life_expectancy', 'Expectativa de vida vs População', 'População', 'Expectativa de vida')
st.write("Análise: População pode sugerir pressões sobre recursos, impactando expectativa.")

st.header("8. Imunização e Expectativa de vida")
for col in immunization_vars:
    plot_scatter_with_regression(df, col, 'life_expectancy', f'Expectativa de vida vs {col.replace("_", " ")}', col.replace("_", " "), 'Expectativa de vida')
st.write("Análise: Imunização está positivamente correlacionada com maior expectativa.")

st.header("Conclusão")
st.write("Fatores como mortalidade, escolaridade e imunização têm impacto claro na expectativa de vida. Gasto em saúde e hábitos também influenciam.")


