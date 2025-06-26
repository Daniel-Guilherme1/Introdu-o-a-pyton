import sqlite3

# Conexão com o banco
conn = sqlite3.connect("frota_taxi.db")
cursor = conn.cursor()

# Criando tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS CLIENTE (
    id_cliente INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS TAXI (
    placa TEXT PRIMARY KEY,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    ano_fab INTEGER NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS CORRIDA (
    id_corrida INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    placa TEXT,
    data_pedido TEXT,
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente),
    FOREIGN KEY (placa) REFERENCES TAXI(placa)
);
''')

# Inserindo dados
clientes = [
    (1532, 'Asdrúbal', '448.754.253-65'),
    (1755, 'Doriana', '567.387.387-44'),
    (1780, 'Quincas', '546.373.762-03'),
    (2001, 'Livia', '432.111.888-99'),
    (2002, 'Bruno', '123.456.789-00'),
    (2003, 'Marina', '234.567.890-10'),
    (2004, 'Tiago', '321.654.987-77'),
    (2005, 'Camila', '789.456.123-33'),
    (2006, 'Renato', '890.321.678-11'),
    (2007, 'Juliana', '111.222.333-44')
]

taxis = [
    ('BRA1234', 'Toyota', 'Corolla', 2023),
    ('XYZ9876', 'Hyundai', 'HB20S', 2024),
    ('WYP8765', 'Fiat', 'Mobi', 2021),
    ('PYZ3456', 'Fiat', 'Argo', 2022),
    ('GHII1234', 'Renault', 'Logan', 2023),
    ('KLM5678', 'Fiat', 'Pulse', 2024),
    ('NOP4321', 'Nissan', 'Versa', 2023),
    ('QRS8765', 'Chevrolet', 'Onix Plus', 2024),
    ('TUV9999', 'Volkswagen', 'Virtus', 2023),
    ('BXC1234', 'Honda', 'City', 2024),
    ('ZXC5678', 'Caoa Chery', 'Arrizo 6', 2024),
    ('LMN8765', 'Peugeot', '208', 2023)
]

corridas = [
    (1755, 'BRA1234', '10/06/2024'),
    (1982, 'XYZ9876', '11/06/2024'),
    (2001, 'GHII1234', '12/06/2024'),
    (2002, 'KLM5678', '13/06/2024'),
    (2003, 'NOP4321', '14/06/2024'),
    (2004, 'QRS8765', '15/06/2024'),
    (2005, 'TUV9999', '16/06/2024'),
    (2006, 'BXC1234', '17/06/2024'),
    (2007, 'ZXC5678', '18/06/2024'),
    (1780, 'LMN8765', '19/06/2024')
]

# Populando as tabelas
cursor.executemany('INSERT OR IGNORE INTO CLIENTE VALUES (?, ?, ?)', clientes)
cursor.executemany('INSERT OR IGNORE INTO TAXI VALUES (?, ?, ?, ?)', taxis)
cursor.executemany('INSERT INTO CORRIDA (id_cliente, placa, data_pedido) VALUES (?, ?, ?)', corridas)

conn.commit()

# ==================== CONSULTAS ====================

print("\n1. Nomes e CPFs de todos os clientes:")
for row in cursor.execute("SELECT nome, cpf FROM CLIENTE"):
    print(row)

print("\n2. Táxis da marca Fiat:")
for row in cursor.execute("SELECT * FROM TAXI WHERE marca = 'Fiat'"):
    print(row)

print("\n3. Corridas realizadas (data e nome do cliente):")
for row in cursor.execute('''
    SELECT C.data_pedido, CL.nome 
    FROM CORRIDA C
    JOIN CLIENTE CL ON C.id_cliente = CL.id_cliente
'''):
    print(row)

print("\n4. Clientes que usaram táxis do modelo Corolla:")
for row in cursor.execute('''
    SELECT DISTINCT CL.nome
    FROM CORRIDA C
    JOIN CLIENTE CL ON C.id_cliente = CL.id_cliente
    JOIN TAXI T ON C.placa = T.placa
    WHERE T.modelo = 'Corolla'
'''):
    print(row)

print("\n5. Quantidade de corridas por táxi:")
for row in cursor.execute('''
    SELECT T.placa, T.modelo, COUNT(*) AS total_corridas
    FROM CORRIDA C
    JOIN TAXI T ON C.placa = T.placa
    GROUP BY T.placa
'''):
    print(row)

print("\n6. Táxis fabricados antes de 2024:")
for row in cursor.execute("SELECT * FROM TAXI WHERE ano_fab < 2024"):
    print(row)

# Fechando conexão
conn.close()