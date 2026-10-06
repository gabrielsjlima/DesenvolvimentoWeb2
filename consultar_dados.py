import sqlite3

conexao = sqlite3.connect("instance/eventos.db")

cursor = conexao.cursor()

# Consultando os eventos
cursor.execute("""SELECT id, nome, data, local, vagas FROM evento""")

eventos = cursor.fetchall()

print("===== EVENTOS =====")

for evento in eventos:
    print(
        f"ID: {evento[0]} | "
        f"Nome: {evento[1]} | "
        f"Data: {evento[2]} | "
        f"Local: {evento[3]} | "
        f"Vagas: {evento[4]}"
    )

# Consultando os participantes
cursor.execute("""SELECT id, nome, email FROM participante""")

participantes = cursor.fetchall()

print("===== PARTICIPANTES =====")

for participante in participantes:
    print(
        f"ID: {participante[0]} | "
        f"Nome: {participante[1]} | "
        f"Email: {participante[2]}"
    )

conexao.close()