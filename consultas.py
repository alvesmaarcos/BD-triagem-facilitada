import panel as pn
import pandas as pd
from sqlalchemy import create_engine, MetaData, select, and_, delete, insert, update
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import datetime

# Configuração da extensão do Panel
pn.extension("tabulator", notifications=True, sizing_mode="stretch_width")

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Conexão com o banco de dados
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.reflect(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# Mapeamento das tabelas
consulta_table = metadata.tables['consulta']
prescricao_table = metadata.tables['prescricao']
paciente_table = metadata.tables['paciente']
medico_table = metadata.tables['medico']
profissional_table = metadata.tables['profissional']
medicamento_table = metadata.tables['medicamento']
itemestoque_table = metadata.tables['item_estoque']

# --- Widgets de Interface (Estilo Feio e Simplificado) ---

# --- FILTROS (AGORA COM TABELAS DE SELEÇÃO) ---
tabela_pacientes_filtro = pn.widgets.Tabulator(
    pd.DataFrame(columns=['id_paciente', 'nome']),
    titles={'id_paciente': 'ID', 'nome': 'Nome do Paciente'},
    pagination='local', page_size=3, height=150, layout='fit_data', disabled=True
)
tabela_medicos_filtro = pn.widgets.Tabulator(
    pd.DataFrame(columns=['id_profissional', 'nome']),
    titles={'id_profissional': 'ID', 'nome': 'Nome do Médico'},
    pagination='local', page_size=3, height=150, layout='fit_data', disabled=True
)
selecao_paciente_filtro = pn.widgets.StaticText(name="Filtrar por Paciente", value="Nenhum")
selecao_medico_filtro = pn.widgets.StaticText(name="Filtrar por Médico", value="Nenhum")
filtro_data = pn.widgets.DatePicker(name='Filtrar por Data')
botao_filtrar = pn.widgets.Button(name="Consultar")
botao_limpar_filtros = pn.widgets.Button(name="Limpar Filtros")


# Tabela principal de Consultas
colunas_consulta_fields = ["id_consulta", "id_paciente", "paciente_nome", "id_medico", "medico_nome", "data", "hora_inicio", "hora_fim", "diagnostico"]
tabela_consultas = pn.widgets.Tabulator(
    pd.DataFrame(columns=colunas_consulta_fields),
    titles={"id_consulta": "ID Consulta", "id_paciente": "ID Paciente", "paciente_nome": "Paciente", "id_medico": "ID Médico", "medico_nome": "Médico", "data": "Data", "hora_inicio": "Início", "hora_fim": "Fim", "diagnostico": "Diagnóstico"},
    pagination='local', page_size=10, height=350, layout='fit_data', disabled=True
)

# Formulário de Edição
input_id_consulta = pn.widgets.StaticText(name="ID Consulta", value="")
input_paciente_edit = pn.widgets.AutocompleteInput(name="Paciente", options=[], placeholder="Selecione ou digite o nome do paciente...")
input_medico_edit = pn.widgets.AutocompleteInput(name="Médico", options=[], placeholder="Selecione ou digite o nome do médico...")
input_data_edit = pn.widgets.DatePicker(name="Data")
input_hora_inicio_edit = pn.widgets.TimePicker(name="Hora Início")
input_hora_fim_edit = pn.widgets.TimePicker(name="Hora Fim")
input_diagnostico_edit = pn.widgets.TextAreaInput(name="Diagnóstico", height=100)
tabela_prescricao_edit = pn.widgets.Tabulator(
    pd.DataFrame(columns=["id_medicamento", "nome_medicamento", "dosagem", "frequencia"]),
    titles={"id_medicamento": "ID", "nome_medicamento": "Medicamento", "dosagem": "Dosagem", "frequencia": "Frequência"},
    editors={"dosagem": "input", "frequencia": "input"}, pagination='local', page_size=5, height=200
)
botao_salvar = pn.widgets.Button(name="Atualizar")
botao_deletar = pn.widgets.Button(name="Excluir")

# --- Formulário de Inclusão (COM TABELAS DE SELEÇÃO) ---
tabela_pacientes_novo = pn.widgets.Tabulator(
    pd.DataFrame(columns=['id_paciente', 'nome']),
    titles={'id_paciente': 'ID', 'nome': 'Nome do Paciente'},
    pagination='local', page_size=5, height=200, layout='fit_data', disabled=True
)
tabela_medicos_novo = pn.widgets.Tabulator(
    pd.DataFrame(columns=['id_profissional', 'nome']),
    titles={'id_profissional': 'ID', 'nome': 'Nome do Médico'},
    pagination='local', page_size=5, height=200, layout='fit_data', disabled=True
)
selecao_paciente_novo = pn.widgets.StaticText(name="Paciente Selecionado", value="Nenhum")
selecao_medico_novo = pn.widgets.StaticText(name="Médico Selecionado", value="Nenhum")

input_data_novo = pn.widgets.DatePicker(name="Data")
input_hora_inicio_novo = pn.widgets.TimePicker(name="Hora Início")
input_hora_fim_novo = pn.widgets.TimePicker(name="Hora Fim")
input_diagnostico_novo = pn.widgets.TextAreaInput(name="Diagnóstico", height=100)
tabela_prescricao_nova = pn.widgets.Tabulator(
    pd.DataFrame(columns=["id_medicamento", "nome_medicamento", "dosagem", "frequencia"]),
    titles={"id_medicamento": "ID", "nome_medicamento": "Medicamento", "dosagem": "Dosagem", "frequencia": "Frequência"},
    editors={"dosagem": "input", "frequencia": "input"}, pagination='local', page_size=5, height=200
)
botao_inserir = pn.widgets.Button(name="Inserir")

# --- Lógica da Aplicação ---

def get_id_from_selection(value):
    """Extrai o ID de uma string no formato 'ID - Nome'."""
    if not value or ' - ' not in value: return None
    try: return int(value.split(' - ')[0])
    except (ValueError, IndexError): return None

def carregar_consultas(event=None):
    query = select(
        consulta_table.c.id_consulta, paciente_table.c.id_paciente, paciente_table.c.nome.label("paciente_nome"),
        medico_table.c.id_profissional.label("id_medico"), profissional_table.c.nome.label("medico_nome"),
        consulta_table.c.data, consulta_table.c.hora_inicio, consulta_table.c.hora_fim, consulta_table.c.diagnostico
    ).select_from(
        consulta_table.join(paciente_table, consulta_table.c.id_paciente == paciente_table.c.id_paciente)
        .join(medico_table, consulta_table.c.id_medico == medico_table.c.id_profissional)
        .join(profissional_table, medico_table.c.id_profissional == profissional_table.c.id_profissional)
    ).order_by(consulta_table.c.data.desc(), consulta_table.c.hora_inicio.desc())
    
    filtros = []
    id_paciente_filtro = get_id_from_selection(selecao_paciente_filtro.value)
    if id_paciente_filtro:
        filtros.append(consulta_table.c.id_paciente == id_paciente_filtro)
    
    id_medico_filtro = get_id_from_selection(selecao_medico_filtro.value)
    if id_medico_filtro:
        filtros.append(consulta_table.c.id_medico == id_medico_filtro)

    if filtro_data.value:
        filtros.append(consulta_table.c.data == filtro_data.value)
        
    if filtros:
        query = query.where(and_(*filtros))
        
    result = session.execute(query).fetchall()
    
    if result:
        df = pd.DataFrame(result, columns=result[0].keys())
        if 'hora_inicio' in df.columns:
            df['hora_inicio'] = df['hora_inicio'].apply(lambda t: t.strftime('%H:%M:%S') if pd.notna(t) and isinstance(t, datetime.time) else '')
        if 'hora_fim' in df.columns:
            df['hora_fim'] = df['hora_fim'].apply(lambda t: t.strftime('%H:%M:%S') if pd.notna(t) and isinstance(t, datetime.time) else '')
    else:
        df = pd.DataFrame(columns=colunas_consulta_fields)
        
    tabela_consultas.value = df

def carregar_dados_para_selecao():
    # Carrega pacientes
    query_pacientes = select(paciente_table.c.id_paciente, paciente_table.c.nome).order_by(paciente_table.c.nome)
    df_pacientes = pd.DataFrame(session.execute(query_pacientes).fetchall(), columns=['id_paciente', 'nome'])
    tabela_pacientes_filtro.value = df_pacientes
    tabela_pacientes_filtro.disabled = False
    tabela_pacientes_novo.value = df_pacientes
    tabela_pacientes_novo.disabled = False
    
    # Carrega médicos
    query_medicos = select(profissional_table.c.id_profissional, profissional_table.c.nome)\
        .select_from(profissional_table.join(medico_table, profissional_table.c.id_profissional == medico_table.c.id_profissional))\
        .order_by(profissional_table.c.nome)
    df_medicos = pd.DataFrame(session.execute(query_medicos).fetchall(), columns=['id_profissional', 'nome'])
    tabela_medicos_filtro.value = df_medicos
    tabela_medicos_filtro.disabled = False
    tabela_medicos_novo.value = df_medicos
    tabela_medicos_novo.disabled = False

def limpar_filtros(event=None):
    selecao_paciente_filtro.value = 'Nenhum'
    selecao_medico_filtro.value = 'Nenhum'
    filtro_data.value = None
    tabela_pacientes_filtro.selection = []
    tabela_medicos_filtro.selection = []
    carregar_consultas()
    
def preencher_campos_edicao(event):
    if not event.new:
        input_id_consulta.value = ''; input_paciente_edit.value = ''; input_medico_edit.value = ''
        input_data_edit.value = None; input_hora_inicio_edit.value = None; input_hora_fim_edit.value = None
        input_diagnostico_edit.value = ''; tabela_prescricao_edit.value = pd.DataFrame(columns=tabela_prescricao_edit.value.columns)
        return
    index = event.new[0]
    row = tabela_consultas.value.iloc[index]
    input_id_consulta.value = str(row['id_consulta'])
    paciente_selecionado = f"{row['id_paciente']} - {row['paciente_nome']}"
    medico_selecionado = f"{row['id_medico']} - {row['medico_nome']}"
    input_paciente_edit.options = [paciente_selecionado]; input_paciente_edit.value = paciente_selecionado
    input_medico_edit.options = [medico_selecionado]; input_medico_edit.value = medico_selecionado
    input_data_edit.value = pd.to_datetime(row['data']).date()
    try:
        input_hora_inicio_edit.value = datetime.datetime.strptime(row['hora_inicio'], '%H:%M:%S').time() if row['hora_inicio'] else None
    except (TypeError, ValueError):
        input_hora_inicio_edit.value = None
    try:
        input_hora_fim_edit.value = datetime.datetime.strptime(row['hora_fim'], '%H:%M:%S').time() if row['hora_fim'] else None
    except (TypeError, ValueError):
        input_hora_fim_edit.value = None

    input_diagnostico_edit.value = row['diagnostico']
    cols = ["id_medicamento", "nome_medicamento", "dosagem", "frequencia"]
    query_prescricao = select(prescricao_table.c.id_medicamento, itemestoque_table.c.nome.label("nome_medicamento"), prescricao_table.c.dosagem, prescricao_table.c.frequencia)\
        .select_from(prescricao_table.join(medicamento_table, prescricao_table.c.id_medicamento == medicamento_table.c.id_medicamento)\
        .join(itemestoque_table, medicamento_table.c.id_itemestoque == itemestoque_table.c.id_itemestoque))\
        .where(prescricao_table.c.id_consulta == row['id_consulta'])
    result_prescricao = session.execute(query_prescricao).fetchall()
    df_prescricao = pd.DataFrame(result_prescricao, columns=cols) if result_prescricao else pd.DataFrame(columns=cols)
    tabela_prescricao_edit.value = df_prescricao

# --- Funções de callback para seleção nas tabelas ---
def on_paciente_select_filtro(event):
    if not event.new: return
    index = event.new[0]
    row = tabela_pacientes_filtro.value.iloc[index]
    selecao_paciente_filtro.value = f"{row['id_paciente']} - {row['nome']}"

def on_medico_select_filtro(event):
    if not event.new: return
    index = event.new[0]
    row = tabela_medicos_filtro.value.iloc[index]
    selecao_medico_filtro.value = f"{row['id_profissional']} - {row['nome']}"

def on_paciente_select_novo(event):
    if not event.new: 
        selecao_paciente_novo.value = "Nenhum"
        return
    index = event.new[0]
    row = tabela_pacientes_novo.value.iloc[index]
    selecao_paciente_novo.value = f"{row['id_paciente']} - {row['nome']}"

def on_medico_select_novo(event):
    if not event.new:
        selecao_medico_novo.value = "Nenhum"
        return
    index = event.new[0]
    row = tabela_medicos_novo.value.iloc[index]
    selecao_medico_novo.value = f"{row['id_profissional']} - {row['nome']}"

def salvar_alteracoes(event):
    if not input_id_consulta.value:
        pn.state.notifications.warning("Selecione uma consulta para editar.")
        return
    id_consulta = int(input_id_consulta.value)
    # Na edição, mantemos o Autocomplete, então a lógica é diferente
    id_paciente = get_id_from_selection(input_paciente_edit.value)
    id_medico = get_id_from_selection(input_medico_edit.value)
    if not id_paciente:
        pn.state.notifications.error("Paciente inválido na edição. Por favor, selecione uma opção da lista.")
        return
    if not id_medico:
        pn.state.notifications.error("Médico inválido na edição. Por favor, selecione uma opção da lista.")
        return
    try:
        stmt = update(consulta_table).where(consulta_table.c.id_consulta == id_consulta).values(
            id_paciente=id_paciente, id_medico=id_medico, data=input_data_edit.value,
            hora_inicio=input_hora_inicio_edit.value, hora_fim=input_hora_fim_edit.value,
            diagnostico=input_diagnostico_edit.value)
        session.execute(stmt)
        session.execute(delete(prescricao_table).where(prescricao_table.c.id_consulta == id_consulta))
        for _, row in tabela_prescricao_edit.value.iterrows():
            if pd.notna(row['id_medicamento']):
                session.execute(insert(prescricao_table).values(
                    id_consulta=id_consulta, id_medicamento=int(row['id_medicamento']),
                    dosagem=row['dosagem'], frequencia=row['frequencia']))
        session.commit()
        pn.state.notifications.success("Consulta atualizada com sucesso!")
        carregar_consultas()
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f"Erro ao salvar: {e}")

def deletar_consulta(event):
    if not input_id_consulta.value:
        pn.state.notifications.warning("Nenhuma consulta selecionada para excluir.")
        return
    id_consulta = int(input_id_consulta.value)
    try:
        stmt = delete(consulta_table).where(consulta_table.c.id_consulta == id_consulta)
        session.execute(stmt)
        session.commit()
        pn.state.notifications.success(f"Consulta {id_consulta} excluída com sucesso!")
        tabela_consultas.selection = []
        carregar_consultas()
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f"Erro ao excluir consulta: {e}")

def inserir_consulta(event):
    id_paciente = get_id_from_selection(selecao_paciente_novo.value)
    id_medico = get_id_from_selection(selecao_medico_novo.value)
    if not id_paciente:
        pn.state.notifications.error("Nenhum paciente selecionado. Por favor, clique em um paciente na tabela.")
        return
    if not id_medico:
        pn.state.notifications.error("Nenhum médico selecionado. Por favor, clique em um médico na tabela.")
        return
    try:
        stmt = insert(consulta_table).values(
            id_paciente=id_paciente, id_medico=id_medico, data=input_data_novo.value,
            hora_inicio=input_hora_inicio_novo.value, hora_fim=input_hora_fim_novo.value,
            diagnostico=input_diagnostico_novo.value
        ).returning(consulta_table.c.id_consulta)
        result = session.execute(stmt)
        id_consulta_novo = result.scalar_one()
        for _, row in tabela_prescricao_nova.value.iterrows():
            if pd.notna(row['id_medicamento']):
                session.execute(insert(prescricao_table).values(
                    id_consulta=id_consulta_novo, id_medicamento=int(row['id_medicamento']),
                    dosagem=row['dosagem'], frequencia=row['frequencia']))
        session.commit()
        pn.state.notifications.success("Consulta inserida com sucesso!")
        selecao_paciente_novo.value = 'Nenhum'; selecao_medico_novo.value = 'Nenhum'
        tabela_pacientes_novo.selection = []; tabela_medicos_novo.selection = []
        input_data_novo.value = None; input_hora_inicio_novo.value = None; input_hora_fim_novo.value = None
        input_diagnostico_novo.value = ''; tabela_prescricao_nova.value = pd.DataFrame(columns=tabela_prescricao_nova.value.columns)
        carregar_consultas()
    except Exception as e:
        session.rollback()
        pn.state.notifications.error(f"Erro ao inserir consulta: {e}")

# --- Conexão dos Widgets com a Lógica (Event Handlers) ---
tabela_pacientes_filtro.param.watch(on_paciente_select_filtro, 'selection')
tabela_medicos_filtro.param.watch(on_medico_select_filtro, 'selection')
tabela_pacientes_novo.param.watch(on_paciente_select_novo, 'selection')
tabela_medicos_novo.param.watch(on_medico_select_novo, 'selection')

# Funções de busca para o Autocomplete da Edição (não foi removido)
input_paciente_edit.param.watch(lambda e: setattr(input_paciente_edit, 'options', buscar_pacientes(e.new)), 'value_input')
input_medico_edit.param.watch(lambda e: setattr(input_medico_edit, 'options', buscar_medicos(e.new)), 'value_input')

botao_filtrar.on_click(carregar_consultas)
botao_limpar_filtros.on_click(limpar_filtros)
tabela_consultas.param.watch(preencher_campos_edicao, 'selection')
botao_salvar.on_click(salvar_alteracoes)
botao_deletar.on_click(deletar_consulta)
botao_inserir.on_click(inserir_consulta)

# --- Layout da Aplicação (Ultra Simplificado) ---

filtros_view = pn.Column(
    pn.pane.Markdown("Filtro de Consultas"),
    pn.pane.Markdown("Selecione um Paciente para Filtrar:"),
    tabela_pacientes_filtro,
    selecao_paciente_filtro,
    pn.pane.Markdown("Selecione um Médico para Filtrar:"),
    tabela_medicos_filtro,
    selecao_medico_filtro,
    filtro_data, 
    pn.Row(botao_filtrar, botao_limpar_filtros)
)
edicao_view = pn.Column(
    pn.pane.Markdown("Editar / Remover Consulta"),
    input_id_consulta, input_paciente_edit, input_medico_edit, input_data_edit,
    input_hora_inicio_edit, input_hora_fim_edit, input_diagnostico_edit,
    pn.pane.Markdown("Prescrição (Edição)"),
    tabela_prescricao_edit, pn.Row(botao_salvar, botao_deletar)
)
novo_view = pn.Column(
    pn.pane.Markdown("Adicionar Nova Consulta"),
    pn.pane.Markdown("1. Selecione um Paciente:"),
    tabela_pacientes_novo,
    selecao_paciente_novo,
    pn.pane.Markdown("2. Selecione um Médico:"),
    tabela_medicos_novo,
    selecao_medico_novo,
    pn.pane.Markdown("3. Preencha os detalhes e a prescrição:"),
    input_data_novo, input_hora_inicio_novo, input_hora_fim_novo, input_diagnostico_novo,
    tabela_prescricao_nova,
    botao_inserir
)
app_layout = pn.Column(
    pn.pane.Markdown("Gerenciamento de Consultas"),
    filtros_view, tabela_consultas, edicao_view, novo_view,
    sizing_mode="stretch_width"
)

# Carrega os dados iniciais ao iniciar a aplicação
carregar_consultas()
carregar_dados_para_selecao()


# Torna o layout "servível"
app_layout.servable()
