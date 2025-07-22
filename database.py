import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Recupera as credenciais do banco de dados a partir das variáveis de ambiente
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_port = os.getenv("DB_PORT", 5432) # Porta padrão do PostgreSQL é 5432

# Verifica se todas as variáveis foram carregadas
if not all([db_host, db_name, db_user, db_pass]):
    raise ValueError("Uma ou mais variáveis de ambiente do banco de dados não foram definidas.")

# Cria a string de conexão (Database URL)
# O formato é: postgresql+psycopg2://usuario:senha@host:porta/database
DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# Cria o "motor" de conexão do SQLAlchemy
# O 'engine' é o ponto central de comunicação com o banco.
# echo=False para não imprimir todas as queries no console em produção. Mude para True se quiser debugar.
engine = create_engine(DATABASE_URL, echo=False)

# Bloco para testar a conexão diretamente executando o arquivo
if __name__ == "__main__":
    try:
        # Tenta estabelecer uma conexão
        with engine.connect() as connection:
            print("✅ Conexão com o banco de dados bem-sucedida!")
            
            # Exemplo de consulta simples para verificar
            query = text("SELECT version();")
            result = connection.execute(query)
            db_version = result.scalar()
            print(f"Versão do PostgreSQL: {db_version}")

    except Exception as e:
        print(f"❌ Falha ao conectar ao banco de dados: {e}")