import sqlite3

conexao = sqlite3.connect("instance/eventos.db")

cursor = conexao.cursor()

# criando a tabela evento
cursor.execute("""
CREATE TABLE IF NOT EXISTS evento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data TEXT NOT NULL,
    local TEXT,
    vagas INTEGER
)
""")

# criando a tabela participante
cursor.execute("""
CREATE TABLE IF NOT EXISTS participante (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

# criando a tabela inscricao
cursor.execute("""
CREATE TABLE IF NOT EXISTS inscricao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participante_id INTEGER NOT NULL,
    evento_id INTEGER NOT NULL,
    data_inscricao TEXT NOT NULL,
    FOREIGN KEY (participante_id) REFERENCES participante(id),
    FOREIGN KEY (evento_id) REFERENCES evento(id)
)
""")

# Inserindo eventos
cursor.execute("""
INSERT INTO evento (nome, data, local, vagas) VALUES (?, ?, ?, ?)""", 
("Semana da Computação","2026-09-10","Auditório",120))

cursor.execute("""
INSERT INTO evento (nome, data, local, vagas) VALUES (?, ?, ?, ?)""", 
("Workshop de Python","2026-09-15","Laboratório 3",40))

# Inserindo participantes
cursor.execute("""INSERT INTO participante (nome, email) VALUES (?, ?)""", 
("Gabriel Lima","gabriel@gmail.com"))

cursor.execute("""INSERT INTO participante (nome, email) VALUES (?, ?)""", 
("João Silva","joao@gmail.com"))

conexao.commit()
conexao.close()