import subprocess
import sys


def verificar_e_instalar(pacote_import, pacote_pip=None):
    if pacote_pip is None:
        pacote_pip = pacote_import

    try:
        __import__(pacote_import)
    except ImportError:
        print(f"Biblioteca '{pacote_import}' não encontrada. Instalando...")
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            pacote_pip
        ])


# psycopg2-binary costuma ser mais simples de instalar no Windows
verificar_e_instalar("psycopg2", "psycopg2-binary")

import psycopg2


# ============================================================
# MATRIZ DE ASSENTOS
# ============================================================

colunas = [
    "A", "B", "C", "D", "E",
    "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T"
]

linhas = range(1, 11)


# ============================================================
# CONFIGURAÇÃO DO BANCO
# ============================================================

DB_CONFIG = {
    "dbname": "wow",
    "user": "postgres",
    "password": "root",
    "host": "localhost",
    "port": "5432"
}


conexao = None
cursor = None

try:
    # Conecta ao PostgreSQL
    conexao = psycopg2.connect(**DB_CONFIG)
    cursor = conexao.cursor()

    print("Conectado ao PostgreSQL com sucesso!")

    # ========================================================
    # SALA 1
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assentos_sala_1 (
            id SERIAL PRIMARY KEY,
            fila CHAR(1) NOT NULL,
            numero_cadeira INT NOT NULL,
            ocupado BOOLEAN DEFAULT FALSE NOT NULL
        )
    """)

    dados_assentos = []

    for coluna in colunas:
        for linha in linhas:
            dados_assentos.append(
                (coluna, linha, False)
            )

    cursor.executemany("""
        INSERT INTO assentos_sala_1
        (fila, numero_cadeira, ocupado)
        VALUES (%s, %s, %s)
    """, dados_assentos)

    print(f"Sala 1: {len(dados_assentos)} assentos cadastrados!")


    # ========================================================
    # SALA 2
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assentos_sala_2 (
            id SERIAL PRIMARY KEY,
            fila CHAR(1) NOT NULL,
            numero_cadeira INT NOT NULL,
            ocupado BOOLEAN DEFAULT FALSE NOT NULL
        )
    """)

    cursor.executemany("""
        INSERT INTO assentos_sala_2
        (fila, numero_cadeira, ocupado)
        VALUES (%s, %s, %s)
    """, dados_assentos)

    print(f"Sala 2: {len(dados_assentos)} assentos cadastrados!")


    # ========================================================
    # SALA 3
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assentos_sala_3 (
            id SERIAL PRIMARY KEY,
            fila CHAR(1) NOT NULL,
            numero_cadeira INT NOT NULL,
            ocupado BOOLEAN DEFAULT FALSE NOT NULL
        )
    """)

    cursor.executemany("""
        INSERT INTO assentos_sala_3
        (fila, numero_cadeira, ocupado)
        VALUES (%s, %s, %s)
    """, dados_assentos)

    print(f"Sala 3: {len(dados_assentos)} assentos cadastrados!")


    # ========================================================
    # SALVA AS ALTERAÇÕES
    # ========================================================

    conexao.commit()

    print("\nTudo certo!")
    print(f"Total de assentos cadastrados: {len(dados_assentos) * 3}")


except Exception as e:
    print(f"\nDeu erro: {e}")

    if conexao is not None:
        conexao.rollback()


finally:
    # Fecha cursor e conexão
    if cursor is not None:
        cursor.close()

    if conexao is not None:
        conexao.close()

    print("Conexão encerrada.")
