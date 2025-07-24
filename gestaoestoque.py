import os
from dotenv import load_dotenv

import pandas as pd
from sqlalchemy import create_engine, text
import panel as pn
pn.extension()

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
if PORT is None or PORT == '':
    PORT = 5432
else:
    PORT = int(PORT)

DBNAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASS")

# Cria engine para conexão
engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}")

# Cria a tabela Item_estoque se não existir
create_table_sql = text("""
CREATE TABLE IF NOT EXISTS Item_estoque (
    nome VARCHAR(200),
    data_fabricacao DATE,
    data_validade DATE,
    lote VARCHAR(100),
    fabricante VARCHAR(100)
)
""")
with engine.begin() as conn:
    conn.execute(create_table_sql)

# Widgets para inserção
nome = pn.widgets.TextInput(name="Nome")
data_fabricacao = pn.widgets.DatePicker(name="Data de Fabricação")
data_validade = pn.widgets.DatePicker(name="Data de Validade")
lote = pn.widgets.TextInput(name="Lote")
fabricante = pn.widgets.TextInput(name="Fabricante")
botao_inserir = pn.widgets.Button(name="Inserir", button_type="primary")

# Widgets para busca e remoção
busca_nome = pn.widgets.TextInput(name="Buscar por nome")
botao_buscar = pn.widgets.Button(name="Buscar", button_type="primary")

remover_nome = pn.widgets.TextInput(name="Remover vacina pelo nome exato")
botao_remover = pn.widgets.Button(name="Remover", button_type="danger")

# Feedback
status = pn.pane.Markdown("")

# Painel da tabela
painel_tabela = pn.pane.DataFrame(pd.DataFrame(), width=1000, height=300)

# Função para atualizar painel da tabela lendo do banco
def atualizar_tabela(filtro_nome=None):
    query = "SELECT * FROM Item_estoque"
    params = {}
    if filtro_nome:
        query += " WHERE nome ILIKE :nome"
        params["nome"] = f"%{filtro_nome}%"
    query += " ORDER BY nome ASC"
    df = pd.read_sql(text(query), engine, params=params)
    painel_tabela.object = df

# Inicializa com todos os dados
atualizar_tabela()

# Função para inserir dados
def inserir_item(event):
    if not all([nome.value, data_fabricacao.value, data_validade.value, lote.value, fabricante.value]):
        status.object = "❌ Preencha todos os campos antes de inserir."
        return
    try:
        insert_sql = text("""
            INSERT INTO Item_estoque (nome, data_fabricacao, data_validade, lote, fabricante)
            VALUES (:nome, :data_fabricacao, :data_validade, :lote, :fabricante)
        """)
        with engine.begin() as conn:
            conn.execute(insert_sql, {
                "nome": nome.value,
                "data_fabricacao": data_fabricacao.value,
                "data_validade": data_validade.value,
                "lote": lote.value,
                "fabricante": fabricante.value
            })
        status.object = "✅ Item inserido com sucesso!"
        atualizar_tabela()
        # Limpa os campos
        nome.value = ""
        data_fabricacao.value = None
        data_validade.value = None
        lote.value = ""
        fabricante.value = ""
    except Exception as e:
        status.object = f"❌ Erro ao inserir: {e}"

# Função para buscar por nome
def buscar_item(event):
    filtro = busca_nome.value.strip()
    atualizar_tabela(filtro_nome=filtro)
    status.object = f"🔎 Exibindo resultados para: '{filtro}'" if filtro else "🔎 Exibindo todos os itens."

# Função para remover item por nome exato
def remover_item(event):
    nome_remover = remover_nome.value.strip()
    if not nome_remover:
        status.object = "❌ Informe o nome exato da vacina para remover."
        return
    try:
        delete_sql = text("DELETE FROM Item_estoque WHERE nome = :nome")
        with engine.begin() as conn:
            result = conn.execute(delete_sql, {"nome": nome_remover})
        if result.rowcount > 0:
            status.object = f"🗑️ Vacina '{nome_remover}' removida com sucesso."
        else:
            status.object = f"⚠️ Vacina '{nome_remover}' não encontrada."
        atualizar_tabela()
        remover_nome.value = ""
    except Exception as e:
        status.object = f"❌ Erro ao remover: {e}"

# Conecta botões às funções
botao_inserir.on_click(inserir_item)
botao_buscar.on_click(buscar_item)
botao_remover.on_click(remover_item)

# Layout completo
layout = pn.Column(
    "## 💉 Estoque de Vacinas e Medicamentos",
    pn.Row(nome, lote),
    pn.Row(fabricante),
    pn.Row(data_fabricacao, data_validade),
    botao_inserir,
    pn.Spacer(height=10),
    pn.Row(busca_nome, botao_buscar),
    pn.Row(remover_nome, botao_remover),
    status,
    pn.Spacer(height=20),
    painel_tabela
)

layout.servable()
