CREATE TABLE Paciente (
    id_paciente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(20) NOT NULL UNIQUE,
    rg VARCHAR(20) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    endereco_rua VARCHAR(100) NOT NULL,
    endereco_numero VARCHAR(10) NOT NULL,
    endereco_complemento VARCHAR(50),
    endereco_bairro VARCHAR(50) NOT NULL,
    endereco_cidade VARCHAR(50) NOT NULL,
    genero VARCHAR(30)
);

CREATE TABLE Profissional (
    id_profissional SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    cpf VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE Item_estoque (
    id_itemestoque SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_fabricacao DATE,
    data_validade DATE NOT NULL,
    lote VARCHAR(50) NOT NULL,
    fabricante VARCHAR(100)
);

CREATE TABLE Medico (
    id_profissional INTEGER PRIMARY KEY,
    crm VARCHAR(20) NOT NULL UNIQUE,
    CONSTRAINT fk_medico_profissional FOREIGN KEY (id_profissional) REFERENCES Profissional(id_profissional) ON DELETE CASCADE
);

CREATE TABLE Enfermeiro (
    id_profissional INTEGER PRIMARY KEY,
    coren VARCHAR(20) NOT NULL UNIQUE,
    CONSTRAINT fk_enfermeiro_profissional FOREIGN KEY (id_profissional) REFERENCES Profissional(id_profissional) ON DELETE CASCADE
);

CREATE TABLE TecnicoEnfermagem (
    id_profissional INTEGER PRIMARY KEY,
    coren VARCHAR(20) NOT NULL,
    CONSTRAINT fk_tecnico_profissional FOREIGN KEY (id_profissional) REFERENCES Profissional(id_profissional) ON DELETE CASCADE
);

CREATE TABLE Paciente_Telefones (
    id_paciente INTEGER NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    CONSTRAINT pk_paciente_telefones PRIMARY KEY (id_paciente, telefone),
    CONSTRAINT fk_telefone_paciente FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente) ON DELETE CASCADE
);

CREATE TABLE Paciente_Alergias (
    id_paciente INTEGER NOT NULL,
    alergia VARCHAR(100) NOT NULL,
    CONSTRAINT pk_paciente_alergias PRIMARY KEY (id_paciente, alergia),
    CONSTRAINT fk_alergia_paciente FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente) ON DELETE CASCADE
);

CREATE TABLE Profissional_especializacao (
    id_profissional INTEGER NOT NULL,
    especializacao VARCHAR(100) NOT NULL,
    CONSTRAINT pk_profissional_especializacao PRIMARY KEY (id_profissional, especializacao),
    CONSTRAINT fk_especializacao_profissional FOREIGN KEY (id_profissional) REFERENCES Profissional(id_profissional) ON DELETE CASCADE
);

CREATE TABLE Video (
    id_video SERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(50),
    id_profissional INTEGER,
    CONSTRAINT fk_video_profissional FOREIGN KEY (id_profissional) REFERENCES Profissional(id_profissional) ON DELETE SET NULL
);

CREATE TABLE Vacina (
    id_vacina SERIAL PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    id_itemestoque INTEGER NOT NULL UNIQUE,
    CONSTRAINT fk_vacina_itemestoque FOREIGN KEY (id_itemestoque) REFERENCES Item_estoque(id_itemestoque) ON DELETE RESTRICT
);

CREATE TABLE Medicamento (
    id_medicamento SERIAL PRIMARY KEY,
    id_itemestoque INTEGER NOT NULL UNIQUE,
    CONSTRAINT fk_medicamento_itemestoque FOREIGN KEY (id_itemestoque) REFERENCES Item_estoque(id_itemestoque) ON DELETE RESTRICT
);

CREATE TABLE Atestado (
    id_atestado SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    descricao TEXT NOT NULL,
    periodo_afastamento VARCHAR(50),
    id_paciente INTEGER NOT NULL,
    id_medico INTEGER NOT NULL,
    CONSTRAINT fk_atestado_paciente FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    CONSTRAINT fk_atestado_medico FOREIGN KEY (id_medico) REFERENCES Medico(id_profissional)
);

CREATE TABLE Consulta (
    id_consulta SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME,
    diagnostico TEXT,
    id_paciente INTEGER NOT NULL,
    id_medico INTEGER NOT NULL,
    id_atestado INTEGER UNIQUE,
    CONSTRAINT fk_consulta_paciente FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    CONSTRAINT fk_consulta_medico FOREIGN KEY (id_medico) REFERENCES Medico(id_profissional),
    CONSTRAINT fk_consulta_atestado FOREIGN KEY (id_atestado) REFERENCES Atestado(id_atestado)
);

CREATE TABLE Triagem (
    id_triagem SERIAL PRIMARY KEY,
    data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descricao TEXT,
    classificacao_de_prioridade VARCHAR(50) NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_profissional INTEGER NOT NULL,
    CONSTRAINT fk_triagem_paciente FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    CONSTRAINT fk_triagem_profissional FOREIGN KEY (id_profissional) REFERENCES Profissional(id_profissional)
);

CREATE TABLE Fila (
    id_fila SERIAL PRIMARY KEY,
    hora_entrada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data DATE NOT NULL,
    tipo_consulta VARCHAR(100),
    id_triagem INTEGER NOT NULL UNIQUE,
    id_profissional INTEGER,
    id_paciente INTEGER NOT NULL,
    CONSTRAINT fk_fila_triagem FOREIGN KEY (id_triagem) REFERENCES Triagem(id_triagem),
    CONSTRAINT fk_fila_profissional FOREIGN KEY (id_profissional) REFERENCES Profissional(id_profissional),
    CONSTRAINT fk_fila_paciente FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente)
);

CREATE TABLE Prescricao (
    id_consulta INTEGER NOT NULL,
    id_medicamento INTEGER NOT NULL,
    dosagem VARCHAR(100) NOT NULL,
    frequencia VARCHAR(100) NOT NULL,
    CONSTRAINT pk_prescricao PRIMARY KEY (id_consulta, id_medicamento),
    CONSTRAINT fk_prescricao_consulta FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta) ON DELETE CASCADE,
    CONSTRAINT fk_prescricao_medicamento FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento) ON DELETE RESTRICT
);

CREATE TABLE Paciente_Recebe_Vacina (
    id_paciente INTEGER NOT NULL,
    id_vacina INTEGER NOT NULL,
    id_profissional INTEGER NOT NULL,
    data_aplicacao DATE NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT pk_paciente_recebe_vacina PRIMARY KEY (id_paciente, id_vacina, id_profissional, data_aplicacao),
    CONSTRAINT fk_recebe_vacina_paciente FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    CONSTRAINT fk_recebe_vacina_vacina FOREIGN KEY (id_vacina) REFERENCES Vacina(id_vacina),
    CONSTRAINT fk_recebe_vacina_profissional FOREIGN KEY (id_profissional) REFERENCES Profissional(id_profissional)
);

CREATE TABLE Paciente_Assiste_Video (
    id_paciente INTEGER NOT NULL,
    id_video INTEGER NOT NULL,
    data_visualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_paciente_assiste_video PRIMARY KEY (id_paciente, id_video),
    CONSTRAINT fk_assiste_video_paciente FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    CONSTRAINT fk_assiste_video_video FOREIGN KEY (id_video) REFERENCES Video(id_video)
);

CREATE TABLE Profissional_Gerencia_ItemEstoque (
    id_profissional INTEGER NOT NULL,
    id_itemestoque INTEGER NOT NULL,
    CONSTRAINT pk_profissional_gerencia_itemestoque PRIMARY KEY (id_profissional, id_itemestoque),
    CONSTRAINT fk_gerencia_profissional FOREIGN KEY (id_profissional) REFERENCES Profissional(id_profissional),
    CONSTRAINT fk_gerencia_itemestoque FOREIGN KEY (id_itemestoque) REFERENCES Item_estoque(id_itemestoque)
);

CREATE TABLE Paciente_Fila (
    id_paciente INTEGER NOT NULL,
    id_fila INTEGER NOT NULL,
    CONSTRAINT pk_paciente_fila PRIMARY KEY (id_paciente, id_fila),
    CONSTRAINT fk_paciente_fila_paciente FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    CONSTRAINT fk_paciente_fila_fila FOREIGN KEY (id_fila) REFERENCES Fila(id_fila) ON DELETE CASCADE
);