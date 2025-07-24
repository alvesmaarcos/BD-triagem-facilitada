import panel as pn
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

pn.extension('tabulator', notifications=True)

DB_USER = "postgres"
DB_PASSWORD = "1307"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "fbd-triagem-facilitada"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
db_connection = psycopg2.connect(f"dbname='{DB_NAME}' user='{DB_USER}' host='{DB_HOST}' password='{DB_PASSWORD}'")
db_engine = create_engine(DATABASE_URL)

def carregar_pacientes():
    try:
        query = "SELECT id_paciente, nome FROM paciente ORDER BY nome"
        df = pd.read_sql(query, db_engine)
        return {row['nome']: row['id_paciente'] for index, row in df.iterrows()}
    except SQLAlchemyError:
        return {}

def carregar_profissionais():
    try:
        query = "SELECT id_profissional, nome FROM profissional ORDER BY nome"
        df = pd.read_sql(query, db_engine)
        return {row['nome']: row['id_profissional'] for index, row in df.iterrows()}
    except SQLAlchemyError:
        return {}

opcoes_pacientes = carregar_pacientes()
opcoes_profissionais = carregar_profissionais()
opcoes_prioridade = ['Vermelho (Emergência)', 'Amarelo (Urgente)', 'Verde (Não Urgente)', 'Azul (Eletivo)']


filtro_prioridade_select = pn.widgets.Select(name="Filtrar por Prioridade", options=["Todas"] + opcoes_prioridade)
id_remover_input = pn.widgets.TextInput(name="ID da Triagem para Remover")

paciente_select = pn.widgets.Select(name="Paciente*", options=list(opcoes_pacientes.keys()))
profissional_select = pn.widgets.Select(name="Profissional Responsável*", options=list(opcoes_profissionais.keys()))
prioridade_select = pn.widgets.Select(name="Classificação de Prioridade*", options=opcoes_prioridade)
descricao_input = pn.widgets.TextAreaInput(name="Descrição dos Sintomas", placeholder="Descreva os sintomas...", height=90)

id_update_input = pn.widgets.TextInput(name="ID da Triagem para Atualizar*")
novo_paciente_select = pn.widgets.Select(name="Novo Paciente", options=list(opcoes_pacientes.keys()))
novo_profissional_select = pn.widgets.Select(name="Novo Profissional", options=list(opcoes_profissionais.keys()))
nova_prioridade_select = pn.widgets.Select(name="Nova Prioridade", options=opcoes_prioridade)
nova_descricao_input = pn.widgets.TextAreaInput(name="Nova Descrição", placeholder="Deixe vazio se não quiser alterar", height=90)

button_consultar = pn.widgets.Button(name='Consultar')
button_inserir = pn.widgets.Button(name='Inserir Triagem')
button_remover = pn.widgets.Button(name='Remover por ID')
button_atualizar = pn.widgets.Button(name='Atualizar Triagem')

tabela_triagem = pn.widgets.Tabulator(layout='fit_data', height=600)

def carregar_dados_triagem(event=None):
    if not db_engine:
        pn.state.notifications.error("Sem conexão com o banco de dados.")
        return

    query = """
    SELECT 
        t.id_triagem AS "ID", p.nome AS "Paciente", prof.nome AS "Profissional",
        t.classificacao_de_prioridade AS "Prioridade", t.descricao AS "Descrição",
        t.data AS "Data e Hora"
    FROM triagem t
    JOIN paciente p ON t.id_paciente = p.id_paciente
    JOIN profissional prof ON t.id_profissional = prof.id_profissional
    """

    filtros = []
    if filtro_prioridade_select.value != "Todas":
        filtros.append(f"t.classificacao_de_prioridade = '{filtro_prioridade_select.value}'")

    if filtros:
        query += " WHERE " + " AND ".join(filtros)
    query += " ORDER BY t.data DESC"

    try:
        df = pd.read_sql_query(query, db_engine)
        if not df.empty:
            df['Data e Hora'] = pd.to_datetime(df['Data e Hora']).dt.strftime('%d/%m/%Y %H:%M')
        tabela_triagem.value = df
    except SQLAlchemyError as e:
        pn.state.notifications.error(f"Erro ao consultar dados: {e}")

def inserir(event):
    if not all([paciente_select.value, profissional_select.value, prioridade_select.value]):
        pn.state.notifications.warning("Preencha todos os campos obrigatórios (*).")
        return

    cursor = None
    try:
        cursor = db_connection.cursor()
        id_paciente = opcoes_pacientes[paciente_select.value]
        id_profissional = opcoes_profissionais[profissional_select.value]

        query = "INSERT INTO triagem (id_paciente, id_profissional, classificacao_de_prioridade, descricao) VALUES (%s, %s, %s, %s);"
        cursor.execute(query, (id_paciente, id_profissional, prioridade_select.value, descricao_input.value))

        db_connection.commit()
        pn.state.notifications.success("Nova triagem registrada!")
    except (Exception, psycopg2.Error) as e:
        if db_connection: db_connection.rollback()
        pn.state.notifications.error(f"Erro ao inserir: {e}")
    finally:
        if cursor: cursor.close()
        carregar_dados_triagem()

def remover(event):
    if not id_remover_input.value:
        pn.state.notifications.warning("Digite o ID da triagem para remover.")
        return

    cursor = None
    try:
        cursor = db_connection.cursor()
        id_para_remover = int(id_remover_input.value)
        cursor.execute("DELETE FROM triagem WHERE id_triagem = %s;", (id_para_remover,))

        db_connection.commit()
        if cursor.rowcount > 0:
            pn.state.notifications.success(f"Triagem ID {id_para_remover} removida!")
        else:
            pn.state.notifications.warning(f"Triagem ID {id_para_remover} não encontrada.")
    except (Exception, psycopg2.Error) as e:
        if db_connection: db_connection.rollback()
        pn.state.notifications.error(f"Erro ao remover: {e}")
    finally:
        if cursor: cursor.close()
        carregar_dados_triagem()

def atualizar(event):
    if not id_update_input.value:
        pn.state.notifications.warning("Digite o ID da triagem a ser atualizada.")
        return

    cursor = None
    try:
        cursor = db_connection.cursor()
        id_triagem = int(id_update_input.value)
        updates = []
        valores = []

        if novo_paciente_select.value:
            updates.append("id_paciente = %s")
            valores.append(opcoes_pacientes[novo_paciente_select.value])

        if novo_profissional_select.value:
            updates.append("id_profissional = %s")
            valores.append(opcoes_profissionais[novo_profissional_select.value])

        if nova_prioridade_select.value:
            updates.append("classificacao_de_prioridade = %s")
            valores.append(nova_prioridade_select.value)

        if nova_descricao_input.value:
            updates.append("descricao = %s")
            valores.append(nova_descricao_input.value)

        if not updates:
            pn.state.notifications.warning("Nenhum campo de atualização foi preenchido.")
            return
        query = f"UPDATE triagem SET {', '.join(updates)} WHERE id_triagem = %s"
        valores.append(id_triagem)
        cursor.execute(query, tuple(valores))
        db_connection.commit()

        if cursor.rowcount > 0:
            pn.state.notifications.success(f"Triagem ID {id_triagem} atualizada com sucesso!")
        else:
            pn.state.notifications.warning(f"Triagem ID {id_triagem} não encontrada.")
    except Exception as e:
        if db_connection: db_connection.rollback()
        pn.state.notifications.error(f"Erro ao atualizar: {e}")
    finally:
        if cursor: cursor.close()
        carregar_dados_triagem()

button_consultar.on_click(carregar_dados_triagem)
button_inserir.on_click(inserir)
button_remover.on_click(remover)
button_atualizar.on_click(atualizar)

painel_controle = pn.Column(
    "## CRUD de Triagem",
    "### Consultar Registros",
    filtro_prioridade_select,
    button_consultar,
    pn.layout.Divider(),
    "### Adicionar Nova Triagem",
    paciente_select,
    profissional_select,
    prioridade_select,
    descricao_input,
    button_inserir,
    pn.layout.Divider(),
    "### Remover Triagem",
    id_remover_input,
    button_remover,
    pn.layout.Divider(),
    "### Atualizar Triagem",
    id_update_input,
    novo_paciente_select,
    novo_profissional_select,
    nova_prioridade_select,
    nova_descricao_input,
    button_atualizar,
    width=350
)

layout = pn.Row(
    painel_controle,
    pn.Column(
        tabela_triagem,
        sizing_mode='stretch_width'
    )
)

carregar_dados_triagem()
layout.servable()

if __name__ == "__main__":
    pn.serve(layout, port=5007, show=True)