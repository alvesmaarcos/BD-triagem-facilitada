
import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2 as pg
import sqlalchemy
from sqlalchemy import create_engine
import panel as pn


load_dotenv()


DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')


con = pg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)


cnx = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
sqlalchemy_engine = create_engine(cnx)


query = "select * from Paciente;"
df = pd.read_sql_query(query, sqlalchemy_engine)


pn.extension()
pn.extension('tabulator')
pn.extension(notifications=True)


flag = ''


nome = pn.widgets.TextInput(
    name="Nome",
    value='',
    placeholder='Digite o nome',
    disabled=False)
cpf = pn.widgets.TextInput(
    name="CPF",
    value='',
    placeholder='Digite o CPF',
    disabled=False)
rg = pn.widgets.TextInput( 
    name="RG",
    value='',
    placeholder='Digite o RG',
    disabled=False)
datanasc = pn.widgets.DatePicker(
    name='Data de Nascimento',
    disabled=False)
genero_widget = pn.widgets.RadioBoxGroup( 
    name='Gênero',
    options=['Não Informado', 'Masculino', 'Feminino', 'Outro'], 
    value='Não Informado')
endereco_rua = pn.widgets.TextInput( 
    name="Endereço (Rua)",
    value='',
    placeholder='Digite a rua',
    disabled=False)
endereco_numero = pn.widgets.TextInput( 
    name="Endereço (Número)",
    value='',
    placeholder='Digite o número',
    disabled=False)
endereco_bairro = pn.widgets.TextInput( 
    name="Endereço (Bairro)",
    value='',
    placeholder='Digite o bairro',
    disabled=False)
endereco_cidade = pn.widgets.TextInput( 
    name="Endereço (Cidade)",
    value='',
    placeholder='Digite a cidade',
    disabled=False)


buttonConsultar = pn.widgets.Button(name='Consultar', button_type='default')
buttonInserir = pn.widgets.Button(name='Inserir', button_type='default')
buttonExcluir = pn.widgets.Button(name='Excluir', button_type='default')
buttonAtualizar = pn.widgets.Button(name='Atualizar', button_type='default')

def queryAll():
    query = f"select * from Paciente"
    df = pd.read_sql_query(query, sqlalchemy_engine) 
    return pn.widgets.Tabulator(df)

def on_consultar():
    try:  
        query = f"select * from Paciente where ('{cpf.value_input}'='{flag}' or cpf='{cpf.value_input}')"
        df = pd.read_sql_query(query, sqlalchemy_engine) 
        table = pn.widgets.Tabulator(df)
        return table
    except Exception as e:
        return pn.pane.Alert(f'Não foi possível consultar: {str(e)}')

def on_inserir():
    try:            
        cursor = con.cursor()
        
        cursor.execute(
            "INSERT INTO Paciente(nome, cpf, rg, data_nascimento, endereco_rua, endereco_numero, endereco_bairro, endereco_cidade, genero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
            (
                nome.value_input, 
                cpf.value_input, 
                rg.value_input,
                datanasc.value, 
                endereco_rua.value_input,
                endereco_numero.value_input,
                endereco_bairro.value_input,
                endereco_cidade.value_input,
                genero_widget.value 
            )
        )
        con.commit()
        return queryAll()
    except Exception as e:
        con.rollback() 
        cursor.close()
        return pn.pane.Alert(f'Não foi possível inserir: {str(e)}')

def on_atualizar():
    try:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE Paciente SET nome = %s, data_nascimento = %s, genero = %s, endereco_rua = %s, endereco_numero = %s, endereco_bairro = %s, endereco_cidade = %s WHERE cpf = %s",
            (
                nome.value_input,
                datanasc.value,
                genero_widget.value,
                endereco_rua.value_input,
                endereco_numero.value_input,
                endereco_bairro.value_input,
                endereco_cidade.value_input,
                cpf.value_input
            )
        )
        con.commit()
        return queryAll()
    except Exception as e:
        con.rollback() 
        cursor.close()
        return pn.pane.Alert(f'Não foi possível atualizar: {str(e)}')


def on_excluir():
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM Paciente WHERE cpf = %s", (cpf.value_input,))
        rows_deleted = cursor.rowcount
        con.commit()
        
        if rows_deleted > 0:
            
            pass 
        else:
            
            pass
        
        return queryAll()
    except Exception as e:
        con.rollback()
        cursor.close()
        return pn.pane.Alert(f'Não foi possível excluir: {str(e)}')

def table_creator(cons, ins, atu, exc):
    if cons:
        return on_consultar()
    if ins:
        return on_inserir()
    if atu:
        return on_atualizar()
    if exc:
        return on_excluir()


interactive_table = pn.bind(table_creator, buttonConsultar, buttonInserir, buttonAtualizar, buttonExcluir)


pn.Row(
    pn.Column(
        '## Gerenciamento de Pacientes (CRUD)', 
        nome, cpf, rg, datanasc, genero_widget,
        pn.pane.Markdown("### Endereço:"),
        endereco_rua, endereco_numero,
        endereco_bairro, endereco_cidade,
        pn.Row(buttonConsultar),
        pn.Row(buttonInserir),
        pn.Row(buttonAtualizar),
        pn.Row(buttonExcluir)
    ),
    pn.Column(interactive_table)
).servable()
