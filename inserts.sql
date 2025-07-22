INSERT INTO Item_estoque (nome, data_fabricacao, data_validade, lote, fabricante) VALUES
('Dipirona 500mg (caixa)', '2024-01-15', '2026-01-15', 'DP24A01', 'Medley'),
('Amoxicilina 500mg (caixa)', '2024-03-20', '2026-03-20', 'AMX24C02', 'EMS'),
('Paracetamol 750mg (caixa)', '2024-02-10', '2027-02-10', 'PRC24B03', 'Neo Química'),
('Ibuprofeno 600mg (caixa)', '2024-05-01', '2026-05-01', 'IBP24E04', 'Aché'),
('Losartana 50mg (caixa)', '2023-11-30', '2025-11-30', 'LST23K05', 'Medley'),
('Seringa Descartável 5ml (caixa)', '2024-01-01', '2029-01-01', 'SRG24A06', 'BD'),
('Gaze Estéril (pacote)', '2024-04-10', '2029-04-10', 'GZE24D07', 'Cremer'),
('Omeprazol 20mg (caixa)', '2024-06-01', '2026-06-01', 'OMP24F08', 'Eurofarma'),
('Nimesulida 100mg (caixa)', '2024-07-15', '2026-07-15', 'NMS24G09', 'Cimed'),
('Captopril 25mg (caixa)', '2023-12-12', '2025-12-12', 'CPT23L10', 'Sandoz'),
('Vacina COVID-19 (Pfizer - frasco)', '2025-05-01', '2025-11-01', 'PZ25E011', 'Pfizer'),
('Vacina COVID-19 (CoronaVac - frasco)', '2025-04-10', '2025-10-10', 'CV25D012', 'Butantan'),
('Vacina Gripe (Influenza - frasco)', '2025-03-01', '2026-03-01', 'GR25C013', 'Sanofi'),
('Vacina Sarampo (Tríplice - frasco)', '2025-01-20', '2027-01-20', 'TRP25A014', 'Fiocruz'),
('Vacina Febre Amarela (frasco)', '2025-02-15', '2026-08-15', 'FA25B015', 'Bio-Manguinhos'),
('Vacina HPV (frasco)', '2025-06-05', '2027-06-05', 'HPV25F016', 'GSK'),
('Vacina Hepatite B (frasco)', '2025-07-01', '2027-07-01', 'HEB25G017', 'Butantan'),
('Vacina Tétano (dT - frasco)', '2025-03-18', '2026-09-18', 'DT25C018', 'Fiocruz'),
('Vacina Pneumocócica (frasco)', '2025-04-22', '2026-10-22', 'PNM25D019', 'Pfizer'),
('Vacina Rotavírus (frasco)', '2025-05-30', '2026-05-30', 'ROT25E020', 'GSK');

INSERT INTO Paciente (nome, cpf, rg, data_nascimento, endereco_rua, endereco_numero, endereco_bairro, endereco_cidade, genero) VALUES
('Ana Clara Sousa', '111.222.333-44', '2001002003004', '2001-05-15', 'Rua dos Cactos', '123', 'Centro', 'Quixadá', 'Feminino'),
('Bruno Costa Lima', '222.333.444-55', '2002003004005', '1995-09-20', 'Avenida das Flores', '45A', 'Junco', 'Quixadá', 'Masculino'),
('Carlos Eduardo Alves', '333.444.555-66', '2003004005006', '1988-02-10', 'Rua do Sertão', '789', 'Campo Novo', 'Quixadá', 'Masculino'),
('Daniela Martins Rocha', '444.555.666-77', '2004005006007', '2003-11-30', 'Travessa da Saudade', '10', 'Planalto Universitário', 'Quixadá', 'Feminino'),
('Eduardo Pereira', '555.666.777-88', '2005006007008', '1976-07-25', 'Rua Principal', 's/n', 'Centro', 'Ibicuitinga', 'Masculino'),
('Fernanda Gomes', '666.777.888-99', '2006007008009', '1999-01-12', 'Avenida Brasil', '1500', 'São João', 'Quixeramobim', 'Feminino'),
('Gustavo Oliveira', '777.888.999-00', '2007008009010', '2010-03-08', 'Rua da Lagoa', '250', 'Centro', 'Banabuiú', 'Masculino'),
('Helena Ferreira Santos', '888.999.000-11', '2008009010011', '1954-12-18', 'Rua 24 de Maio', '300', 'Combate', 'Quixadá', 'Feminino'),
('Igor Nogueira', '999.000.111-22', '2009010011012', '1992-08-05', 'Avenida Plácido Castelo', '2020', 'Centro', 'Quixadá', 'Masculino'),
('Juliana Azevedo', '000.111.222-33', '2010011012013', '2005-06-22', 'Rua dos Monólitos', '555', 'Baviera', 'Quixadá', 'Feminino');

INSERT INTO Profissional (nome, cargo, cpf) VALUES
('Dr. Ricardo Borges', 'Médico', '123.456.789-10'),
('Dra. Márcia Andrade', 'Médico', '234.567.891-01'),
('Dr. Flávio Mendes', 'Médico', '345.678.910-12'),
('Dra. Lúcia Guimarães', 'Médico', '456.789.101-23'),
('Enf. Marcos Paulo', 'Enfermeiro', '567.891.012-34'),
('Enf. Patrícia Melo', 'Enfermeiro', '678.910.123-45'),
('Enf. Vanessa Cruz', 'Enfermeiro', '789.101.234-56'),
('Téc. Roberto Silva', 'Técnico de Enfermagem', '891.012.345-67'),
('Téc. Sandra Dias', 'Técnico de Enfermagem', '910.123.456-78'),
('Téc. Anderson Luiz', 'Técnico de Enfermagem', '012.345.678-90');

INSERT INTO Medico (id_profissional, crm) VALUES
(1, 'CE-12345'),
(2, 'CE-23456'),
(3, 'CE-34567'),
(4, 'CE-45678');

INSERT INTO Enfermeiro (id_profissional, coren) VALUES
(5, 'COREN-CE-11111'),
(6, 'COREN-CE-22222'),
(7, 'COREN-CE-33333');

INSERT INTO TecnicoEnfermagem (id_profissional, coren) VALUES
(8, 'COREN-CE-44444-TE'),
(9, 'COREN-CE-55555-TE'),
(10, 'COREN-CE-66666-TE');

INSERT INTO Paciente_Telefones (id_paciente, telefone) VALUES
(1, '(88) 99911-2233'), (2, '(88) 98822-3344'), (3, '(88) 99933-4455'),
(4, '(88) 98844-5566'), (5, '(85) 99955-6677'), (6, '(88) 98866-7788'),
(7, '(88) 99977-8899'), (8, '(88) 98888-9900'), (9, '(88) 99999-0011'),
(10, '(85) 98800-1122');

INSERT INTO Paciente_Alergias (id_paciente, alergia) VALUES
(1, 'Penicilina'), (2, 'Pólen'), (3, 'Frutos do mar'), (4, 'Nenhuma conhecida'),
(5, 'Dipirona'), (6, 'Lactose'), (7, 'Poeira'), (8, 'Iodo'),
(9, 'Nenhuma conhecida'), (10, 'Glúten');

INSERT INTO Profissional_especializacao (id_profissional, especializacao) VALUES
(1, 'Cardiologia'), (2, 'Pediatria'), (3, 'Clínica Geral'), (4, 'Dermatologia'),
(5, 'Enfermagem em Urgência'), (6, 'Saúde da Família'), (7, 'Obstetrícia'),
(8, 'Instrumentação Cirúrgica'), (9, 'Cuidados Intensivos'), (10, 'Vacinação');

INSERT INTO Video (titulo, descricao, categoria, id_profissional) VALUES
('Como aferir a pressão arterial', 'Um guia passo a passo para medir a pressão em casa.', 'Tutorial', 5),
('Prevenção de Dengue', 'Dicas para evitar a proliferação do mosquito Aedes aegypti.', 'Saúde Pública', 2),
('Alimentação Saudável para Diabéticos', 'O que comer para controlar a diabetes.', 'Nutrição', 1),
('Primeiros Socorros: Engasgo', 'Aprenda a manobra de Heimlich.', 'Emergência', 6),
('A importância da vacinação infantil', 'Entenda porque o calendário vacinal é crucial.', 'Imunização', 2),
('Exercícios para a Terceira Idade', 'Atividades leves para manter o corpo ativo.', 'Fisioterapia', 3),
('Como usar a bombinha para asma', 'Tutorial de uso de inaladores para asma.', 'Tutorial', 7),
('Cuidados com a pele no sol do sertão', 'Dicas de protetor solar e hidratação.', 'Dermatologia', 4),
('O que é hipertensão?', 'Explicação sobre a doença e seus riscos.', 'Cardiologia', 1),
('Amamentação: Primeiros Passos', 'Dicas para mães de primeira viagem.', 'Pediatria', 2);

INSERT INTO Vacina (tipo, id_itemestoque) VALUES
('COVID-19 Pfizer', 11), ('COVID-19 CoronaVac', 12), ('Gripe Influenza', 13),
('Sarampo (Tríplice Viral)', 14), ('Febre Amarela', 15), ('HPV', 16),
('Hepatite B', 17), ('Tétano (dT)', 18), ('Pneumocócica 13', 19),
('Rotavírus Humano', 20);

INSERT INTO Medicamento (id_itemestoque) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

INSERT INTO Triagem (descricao, classificacao_de_prioridade, id_paciente, id_profissional) VALUES
('Dor de cabeça e febre baixa', 'Verde (Não Urgente)', 1, 8),
('Tosse persistente há 3 dias', 'Verde (Não Urgente)', 2, 8),
('Dor no peito e falta de ar', 'Vermelho (Emergência)', 3, 5),
('Corte profundo no dedo', 'Amarelo (Urgente)', 4, 9),
('Pressão arterial 180x110 mmHg', 'Vermelho (Emergência)', 5, 6),
('Reação alérgica leve, manchas na pele', 'Amarelo (Urgente)', 6, 9),
('Vômito e diarreia', 'Amarelo (Urgente)', 7, 10),
('Acompanhamento de rotina', 'Azul (Eletivo)', 8, 10),
('Crise de ansiedade', 'Amarelo (Urgente)', 9, 7),
('Renovação de receita', 'Azul (Eletivo)', 10, 5);

INSERT INTO Profissional_Gerencia_ItemEstoque (id_profissional, id_itemestoque) VALUES
(5, 1), (5, 2), (5, 3), (6, 11), (6, 12), (6, 13), (1, 5), (2, 8), (7, 6), (7, 7);

INSERT INTO Atestado (data, descricao, periodo_afastamento, id_paciente, id_medico) VALUES
('2025-07-21', 'Paciente com diagnóstico de virose.', '3 dias', 1, 3),
('2025-07-20', 'Paciente com crise de enxaqueca.', '2 dias', 2, 1),
('2025-07-21', 'Paciente em observação por suspeita de infarto.', '5 dias', 3, 1),
('2025-07-20', 'Paciente necessitou de sutura no dedo indicador.', '1 dia', 4, 4),
('2025-07-21', 'Paciente com pico hipertensivo.', '7 dias', 5, 1),
('2025-07-19', 'Paciente com reação alérgica a medicamento.', '2 dias', 6, 2),
('2025-07-18', 'Paciente com gastroenterite aguda.', '4 dias', 7, 3),
('2025-07-21', 'Compareceu a consulta de rotina.', 'N/A', 8, 2),
('2025-07-20', 'Paciente com crise de ansiedade generalizada.', '5 dias', 9, 3),
('2025-07-21', 'Consulta para renovação de receita controlada.', 'N/A', 10, 1);

INSERT INTO Fila (data, tipo_consulta, id_triagem, id_profissional, id_paciente) VALUES
('2025-07-21', 'Clínica Geral', 1, 3, 1),
('2025-07-20', 'Clínica Geral', 2, 1, 2),
('2025-07-21', 'Cardiologia', 3, 1, 3),
('2025-07-20', 'Dermatologia', 4, 4, 4),
('2025-07-21', 'Cardiologia', 5, 1, 5),
('2025-07-19', 'Pediatria', 6, 2, 6),
('2025-07-18', 'Clínica Geral', 7, 3, 7),
('2025-07-21', 'Pediatria', 8, 2, 8),
('2025-07-20', 'Clínica Geral', 9, 3, 9),
('2025-07-21', 'Cardiologia', 10, 1, 10);

INSERT INTO Consulta (data, hora_inicio, hora_fim, diagnostico, id_paciente, id_medico, id_atestado) VALUES
('2025-07-21', '10:00:00', '10:20:00', 'Virose comum', 1, 3, 1),
('2025-07-20', '11:30:00', '11:55:00', 'Enxaqueca tensional', 2, 1, 2),
('2025-07-21', '08:15:00', '09:00:00', 'Angina instável. Encaminhado para internação.', 3, 1, 3),
('2025-07-20', '14:00:00', '14:25:00', 'Ferimento corto-contuso', 4, 4, 4),
('2025-07-21', '09:30:00', '09:50:00', 'Crise hipertensiva', 5, 1, 5),
('2025-07-19', '15:10:00', '15:30:00', 'Urticária medicamentosa', 6, 2, 6),
('2025-07-18', '16:00:00', '16:20:00', 'Gastroenterite viral', 7, 3, 7),
('2025-07-21', '13:00:00', '13:15:00', 'Check-up pediátrico de rotina', 8, 2, 8),
('2025-07-20', '17:00:00', '17:40:00', 'Transtorno de Ansiedade Generalizada (TAG)', 9, 3, 9),
('2025-07-21', '14:45:00', '15:00:00', 'Hipertensão Arterial Sistêmica (HAS) - controlada', 10, 1, 10);

INSERT INTO Paciente_Fila (id_paciente, id_fila) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10);

INSERT INTO Prescricao (id_consulta, id_medicamento, dosagem, frequencia) VALUES
(1, 1, '1 comprimido', 'de 6 em 6 horas se febre ou dor'),
(2, 4, '1 comprimido', 'de 8 em 8 horas se dor intensa'),
(3, 10, '1 comprimido', 'de 12 em 12 horas'),
(5, 5, '1 comprimido', 'diariamente pela manhã'),
(6, 8, '1 comprimido', 'em jejum pela manhã'),
(7, 3, '1 comprimido', 'de 8 em 8 horas se dor'),
(9, 8, '1 comprimido', 'em jejum'),
(10, 5, '1 comprimido', 'diariamente pela manhã'),
(1, 3, '1 comprimido', 'se dor, intercalado com dipirona'),
(4, 2, '1 comprimido', 'de 8 em 8 horas por 7 dias');

INSERT INTO Paciente_Recebe_Vacina (id_paciente, id_vacina, id_profissional, data_aplicacao) VALUES
(1, 3, 10, '2025-04-15'), (2, 3, 10, '2025-04-15'),
(3, 1, 9, '2025-05-20'), (4, 2, 9, '2025-05-21'),
(5, 7, 8, '2025-06-10'), (6, 4, 10, '2025-06-11'),
(7, 5, 9, '2025-06-12'), (8, 6, 8, '2025-07-01'),
(9, 8, 10, '2025-07-02'), (10, 3, 10, '2025-04-16');

INSERT INTO Paciente_Assiste_Video (id_paciente, id_video) VALUES
(1, 10), (2, 5), (3, 9), (4, 4), (5, 1), (6, 7), (7, 2), (8, 6), (9, 1), (10, 3);