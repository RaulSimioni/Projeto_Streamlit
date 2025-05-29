import sqlite3 as sql
import pandas as pd
import streamlit as st

conn = sql.connect('biblioteca_db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS autores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')

cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor_id INTEGER,
    categoria_id INTEGER,
    ano INTEGER,
    quantidade_disponivel INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livro_id INTEGER NOT NULL,
    data_emprestimo TEXT NOT NULL,
    devolvido BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (livro_id) REFERENCES livros(id)
)
""")
conn.commit()

# autores = [
#     ("Machado de Assis",), ("Clarice Lispector",), ("Graciliano Ramos",),
#     ("Monteiro Lobato",), ("Jorge Amado",), ("Carlos Drummond de Andrade",),
#     ("Cecília Meireles",), ("Fernando Pessoa",), ("José Saramago",),
#     ("Agatha Christie",)
# ]
# cursor.executemany("INSERT INTO autores (nome) VALUES (?)", autores)


# categorias = [
#     ("Romance",), ("Ficção Científica",), ("Fantasia",), ("Suspense",),
#     ("Poesia",), ("História",), ("Biografia",), ("Drama",), ("Mistério",),
#     ("Aventura",)
# ]
# cursor.executemany("INSERT INTO categorias (nome) VALUES (?)", categorias)

# livros = [
#     ("Dom Casmurro", 1, 1, 1899, 3), ("A Hora da Estrela", 2, 8, 1977, 4),
#     ("Vidas Secas", 3, 8, 1938, 5), ("Sítio do Pica-Pau Amarelo", 4, 10, 1921, 2),
#     ("Gabriela, Cravo e Canela", 5, 1, 1958, 3), ("A Rosa do Povo", 6, 5, 1945, 6),
#     ("Romanceiro da Inconfidência", 7, 5, 1953, 4), ("Mensagem", 8, 5, 1934, 5),
#     ("Ensaio sobre a Cegueira", 9, 8, 1995, 3), ("O Assassinato no Expresso do Oriente", 10, 4, 1934, 7)
# ]
# cursor.executemany("INSERT INTO livros (titulo, autor_id, categoria_id, ano, quantidade_disponivel) VALUES (?, ?, ?, ?, ?)", livros)

# emprestimos = [
#     (1, "2025-05-20", 0), (2, "2025-05-21", 1), (3, "2025-05-22", 0),
#     (4, "2025-05-23", 1), (5, "2025-05-24", 0), (6, "2025-05-25", 1),
#     (7, "2025-05-26", 0), (8, "2025-05-27", 1), (9, "2025-05-28", 0),
#     (10, "2025-05-29", 1)
# ]
# cursor.executemany("INSERT INTO emprestimos (livro_id, data_emprestimo, devolvido) VALUES (?, ?, ?)", emprestimos)

conn.commit()

st.header("Dashboard Biblioteca")

st.subheader("📂 Todos os livros com nome do autor e da categoria.")
df_group = pd.read_sql_query('''
    SELECT livros.titulo, autores.nome AS autor, categorias.nome AS categoria
    FROM livros
    JOIN autores ON livros.autor_id = autores.id
    JOIN categorias ON livros.categoria_id = categorias.id;
''', conn)
st.dataframe(df_group)

st.subheader("📂 Filtro de livros por ano de publicação.")
df_ano = pd.read_sql_query('''
    SELECT livros.titulo, livros.ano
    FROM livros
''', conn)

st.subheader("🔍 Filtro: WHERE ano < 1995")
valor_min = st.slider("Selecione o ano máximo", 1899, 1995, 1995)
query = "SELECT titulo, ano FROM livros WHERE ano < ?"
df_filtro = pd.read_sql_query(query, conn, params=(valor_min,))
st.dataframe(df_filtro)

query = """
    SELECT 
        (SELECT SUM(quantidade_disponivel) FROM livros) AS total_livros,
        (SELECT COUNT(*) FROM emprestimos) AS total_emprestimos,
        (SELECT COUNT(*) FROM emprestimos WHERE devolvido = 1) AS total_devolvidos
"""
df_counts = pd.read_sql_query(query, conn)

st.subheader("📂 Estatísticas Gerais")

col1, col2, col3 = st.columns(3)
col1.metric("📚 Total de Livros", df_counts['total_livros'][0])
col2.metric("📖 Total de Empréstimos", df_counts['total_emprestimos'][0])
col3.metric("✅ Total de Devolvidos", df_counts['total_devolvidos'][0])


query = """
    SELECT 
        (SELECT SUM(quantidade_disponivel) FROM livros) AS total_livros,
        (SELECT COUNT(*) FROM emprestimos) AS total_emprestimos,
        (SELECT COUNT(*) FROM emprestimos WHERE devolvido = 1) AS total_devolvidos
"""

query = """
    SELECT categorias.nome AS categoria, COUNT(livros.id) AS total_livros
    FROM livros
    JOIN categorias ON livros.categoria_id = categorias.id
    GROUP BY categorias.nome;
"""
df_categorias = pd.read_sql_query(query, conn)

st.subheader("📂 Quantidade de categorias")
st.dataframe(df_categorias)

# Obter autores e categorias do banco
cursor.execute("SELECT id, nome FROM autores")
autores_data = cursor.fetchall()
autores_dict = {nome: id for id, nome in autores_data}

cursor.execute("SELECT id, nome FROM categorias")
categorias_data = cursor.fetchall()
categorias_dict = {nome: id for id, nome in categorias_data}

st.subheader("➕ Registro de Novo Livro ou Empréstimo")
opcao = st.radio("O que deseja registrar?", ["📖 Novo Livro", "🔄 Novo Empréstimo"])

if opcao == "📖 Novo Livro":
    with st.form("form_livro"):
        titulo = st.text_input("Nome do livro")
        ano = st.number_input("Ano do livro", min_value=0, max_value=2100, step=1)

        autor_nome = st.text_input("Nome do Autor")
        categoria_nome = st.selectbox("Categoria", list(categorias_dict.keys()))

        quantidade_disponivel = st.number_input("Quantidade Disponível", min_value=0, step=1)
        enviar_livro = st.form_submit_button("Inserir Livro")

        if enviar_livro and titulo and autor_nome:
            if autor_nome not in autores_dict:
                cursor.execute("INSERT INTO autores (nome) VALUES (?)", (autor_nome,))
                conn.commit()
                cursor.execute("SELECT id FROM autores WHERE nome = ?", (autor_nome,))
                autor_id = cursor.fetchone()[0]
                autores_dict[autor_nome] = autor_id
            else:
                autor_id = autores_dict[autor_nome]

            categoria_id = categorias_dict[categoria_nome]
            cursor.execute("""
                INSERT INTO livros (titulo, autor_id, categoria_id, ano, quantidade_disponivel) 
                VALUES (?, ?, ?, ?, ?)
            """, (titulo, autor_id, categoria_id, ano, quantidade_disponivel))
            conn.commit()
            st.success("✅ Livro inserido com sucesso!")
            st.rerun()

if opcao == "🔄 Novo Empréstimo":
    cursor.execute("SELECT id, titulo FROM livros")
    livros_data = cursor.fetchall()
    livros_dict = {f"{id} - {titulo}": id for id, titulo in livros_data}

    with st.form("form_emprestimo"):
        livro_label = st.selectbox("Livro", list(livros_dict.keys()))
        data_emprestimo = st.date_input("Data do Empréstimo")
        devolvido = st.checkbox("Devolvido?")
        enviar_emprestimo = st.form_submit_button("Registrar Empréstimo")

        if enviar_emprestimo:
            livro_id = livros_dict[livro_label]
            cursor.execute("""
                INSERT INTO emprestimos (livro_id, data_emprestimo, devolvido) 
                VALUES (?, ?, ?)
            """, (livro_id, data_emprestimo, int(devolvido))) 
            conn.commit()
            st.success("✅ Empréstimo registrado com sucesso!")
            st.rerun()

#Formulário para editar um autor (alterar o nome)

st.subheader("✏️ Alterar Nome de Autor")
autor_antigo = st.selectbox("Selecione o autor que deseja renomear", list(autores_dict.keys()))
autor_novo = st.text_input("Novo nome para o autor selecionado")
if st.button("Atualizar Autor") and autor_novo:
    cursor.execute("UPDATE autores SET nome = ? WHERE id = ?", (autor_novo, autores_dict[autor_antigo]))
    conn.commit()
    st.success(f"✅ Autor '{autor_antigo}' atualizado para '{autor_novo}'!")
    st.rerun()

st.subheader("✏️ Editar Livro Existente")
cursor.execute("""
    SELECT livros.id, livros.titulo, autores.nome, categorias.nome, livros.quantidade_disponivel
    FROM livros
    JOIN autores ON livros.autor_id = autores.id
    JOIN categorias ON livros.categoria_id = categorias.id
""")
livros_info = cursor.fetchall()
livros_dict = {f"{id} - {titulo}": id for id, titulo, _, _, _ in livros_info}

livro_escolhido = st.selectbox("Selecione o livro para editar", list(livros_dict.keys()))

if livro_escolhido:
    livro_id = livros_dict[livro_escolhido]
    livro_original = next(item for item in livros_info if item[0] == livro_id)
    _, titulo_atual, autor_atual, categoria_atual, qtd_atual = livro_original

    with st.form("form_editar_livro"):
        novo_titulo = st.text_input("Novo título", value=titulo_atual)
        novo_autor = st.text_input("Novo autor", value=autor_atual)
        nova_categoria = st.selectbox("Nova categoria", list(categorias_dict.keys()), index=list(categorias_dict.keys()).index(categoria_atual))
        nova_qtd = st.number_input("Nova quantidade disponível", min_value=0, step=1, value=qtd_atual)
        salvar_edicao = st.form_submit_button("Salvar Alterações")

        if salvar_edicao:
            if novo_autor not in autores_dict:
                cursor.execute("INSERT INTO autores (nome) VALUES (?)", (novo_autor,))
                conn.commit()
                cursor.execute("SELECT id FROM autores WHERE nome = ?", (novo_autor,))
                novo_autor_id = cursor.fetchone()[0]
                autores_dict[novo_autor] = novo_autor_id
            else:
                novo_autor_id = autores_dict[novo_autor]

            nova_categoria_id = categorias_dict[nova_categoria]

            cursor.execute("""
                UPDATE livros 
                SET titulo = ?, autor_id = ?, categoria_id = ?, quantidade_disponivel = ?
                WHERE id = ?
            """, (novo_titulo, novo_autor_id, nova_categoria_id, nova_qtd, livro_id))
            conn.commit()
            st.success("✅ Livro atualizado com sucesso!")
            st.rerun()

st.subheader("🗑️ Deletar Livro ou Autor")


opcao = st.radio("O que deseja excluir?", ["📖 Deletar Livro", "📝 Deletar Autor"])
if opcao == "📖 Deletar Livro":
    livros_df = cursor.execute("SELECT id, titulo FROM livros").fetchall()
    livros_dict = {str(livro[0]): livro[1] for livro in livros_df}
    livro_id_selecionado = st.selectbox("Selecione o livro para deletar:", list(livros_dict.keys()), format_func=lambda x: livros_dict[x])

    if st.button("🗑️ Confirmar Exclusão"):
        cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id_selecionado,))
        conn.commit()
        st.success("✅ Livro excluído com sucesso!")
if opcao == "📝 Deletar Autor":
    autores_df = cursor.execute("SELECT id, nome FROM autores").fetchall()
    autores_dict = {str(autor[0]): autor[1] for autor in autores_df}
    autor_id_selecionado = st.selectbox("Selecione o autor para deletar:", list(autores_dict.keys()), format_func=lambda x: autores_dict[x])

    if st.button("🗑️ Confirmar Exclusão"):
        cursor.execute("DELETE FROM autores WHERE id = ?", (autor_id_selecionado,))
        conn.commit()
        st.success("✅ Autor excluído com sucesso!")
