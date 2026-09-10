import subprocess
import sys

def verificar_e_instalar(pacote):
    try:
        __import__(pacote)
    except ImportError:
        print(f"Biblioteca '{pacote}' não encontrada. Instalando automaticamente...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

verificar_e_instalar("customtkinter")
verificar_e_instalar("pillow")
verificar_e_instalar("psycopg2")

import psycopg2
import customtkinter as ctk
from PIL import Image
from pathlib import Path

# ============================================================
# MATRIZES acho que nao vai precisar alterar
# ============================================================

fila01 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila11 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila21 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila31 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila41 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila51 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila61 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila71 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila81 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila91 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

sala1 = [fila01, fila11, fila21, fila31, fila41, fila51, fila61, fila71, fila81, fila91]

fila02 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila12 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila22 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila32 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila42 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila52 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila62 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila72 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila82 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila92 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

sala2 = [fila02, fila12, fila22, fila32, fila42, fila52, fila62, fila72, fila82, fila92]

fila03 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila13 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila23 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila33 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila43 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila53 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila63 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila73 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila83 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fila93 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

sala3 = [fila03, fila13, fila23, fila33, fila43, fila53, fila63, fila73, fila83, fila93]

# ============================================================
# VARIÁVEIS
# ============================================================

valor_total = 0
historico = []

datas_filme1 = ["Segunda-Feira", "Quarta-Feira", "Sexta-Feira", "Domingo"]
datas_filme2 = ["Terça-Feira", "Quinta-Feira", "Sabado"]

# ============================================================
# banco fudido
# ============================================================

try:
    conexao = psycopg2.connect(host="localhost", port="5432", dbname="wow", user="postgres", password="root")
    cursor = conexao.cursor()
    print("o bagual ta conectado conectado")
except Exception as erro:
    print("Erro ao conectar ao PostgreSQL:")
    print(erro)
    conexao = None
    cursor = None

# ============================================================
# CARREGAR RESERVAS DO BANCO PARA AS MATRIZES
# ============================================================

def carregar_banco():
    if cursor is None:
        return
    try:
        # ---------------- SALA 1 ----------------
        cursor.execute("""
            SELECT fila, numero, reservado
            FROM assentos
            WHERE sala_id = 1
        """)
        dados = cursor.fetchall()
        for fila, numero, reservado in dados:
            linha = ord(fila.upper()) - 65
            coluna = numero - 1
            if 0 <= linha < 10 and 0 <= coluna < 20:
                if reservado:
                    sala1[linha][coluna] = 1
                else:
                    sala1[linha][coluna] = 0

        # ---------------- SALA 2 ----------------
        cursor.execute("""
            SELECT fila, numero, reservado
            FROM assentos
            WHERE sala_id = 2
        """)
        dados = cursor.fetchall()
        for fila, numero, reservado in dados:
            linha = ord(fila.upper()) - 65
            coluna = numero - 1
            if 0 <= linha < 10 and 0 <= coluna < 20:
                if reservado:
                    sala2[linha][coluna] = 1
                else:
                    sala2[linha][coluna] = 0

        conexao.commit()
        print("Matrizes carregadas do banco!")
    except Exception as erro:
        print("Erro ao carregar banco:")
        print(erro)

# ============================================================
# banco atualizado
# ============================================================

def salvar_reserva_banco(sala, fila, lugar):
    if cursor is None:
        return False
    try:
        if sala is sala1:
            sala_id = 1
            filme_id = 1
        else:
            sala_id = 2
            filme_id = 2

        letra = chr(65 + fila)
        numero = lugar + 1

        cursor.execute("""
            SELECT id, reservado
            FROM assentos
            WHERE sala_id = %s
            AND fila = %s
            AND numero = %s
        """, (sala_id, letra, numero))

        assento = cursor.fetchone()
        if assento is None:
            print("Assento não encontrado no banco.")
            conexao.rollback()
            return False

        assento_id = assento[0]
        reservado = assento[1]

        if reservado:
            print("Esse assento já está reservado no banco.")
            conexao.rollback()
            return False

        cursor.execute("""
            UPDATE assentos
            SET reservado = TRUE
            WHERE id = %s
        """, (assento_id,))

        cursor.execute("""
            INSERT INTO reservas
            (filme_id, assento_id, preco)
            VALUES (%s, %s, %s)
        """, (filme_id, assento_id, 25.00))

        conexao.commit()
        return True
    except Exception as erro:
        print("Erro ao salvar reserva:")
        print(erro)
        conexao.rollback()
        return False

# ============================================================
# banco CANCELAMENTOXDDD
# ============================================================

def cancelar_banco(sala, fila, lugar):
    if cursor is None:
        return False
    try:
        if sala is sala1:
            sala_id = 1
        else:
            sala_id = 2

        letra = chr(65 + fila)
        numero = lugar + 1

        cursor.execute("""
            SELECT id
            FROM assentos
            WHERE sala_id = %s
            AND fila = %s
            AND numero = %s
        """, (sala_id, letra, numero))

        assento = cursor.fetchone()
        if assento is None:
            print("Assento não encontrado.")
            conexao.rollback()
            return False

        assento_id = assento[0]

        cursor.execute("""
            UPDATE assentos
            SET reservado = FALSE
            WHERE id = %s
        """, (assento_id,))

        cursor.execute("""
            DELETE FROM reservas
            WHERE assento_id = %s
        """, (assento_id,))

        conexao.commit()
        return True
    except Exception as erro:
        print("Erro ao cancelar reserva:")
        print(erro)
        conexao.rollback()
        return False

# ============================================================
# mostrar sala
# ============================================================

def mostrar_sala(sala, numero_sala):
    for widget in app.winfo_children():
        if widget != menu_lateral:
            widget.destroy()

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    titulo = ctk.CTkLabel(frame, text=f"SALA {numero_sala}", font=("Arial", 28, "bold"))
    titulo.pack(pady=20)

    tela = ctk.CTkLabel(frame, text="================ TELA ================", font=("Arial", 18))
    tela.pack(pady=10)

    assentos_frame = ctk.CTkFrame(frame)
    assentos_frame.pack(pady=20)

    for fila in range(10):
        letra = chr(65 + fila)
        label_fila = ctk.CTkLabel(assentos_frame, text=letra, width=30)
        label_fila.grid(row=fila, column=0, padx=5, pady=5)

        for lugar in range(20):
            if sala[fila][lugar] == 0:
                texto = f"{letra}{lugar + 1}"
            else:
                texto = "X"

            botao = ctk.CTkButton(assentos_frame, text=texto, width=45, height=35, state="disabled")
            botao.grid(row=fila, column=lugar + 1, padx=2, pady=2)

            if sala[fila][lugar] == 1:
                botao.configure(fg_color="red")
            else:
                botao.configure(fg_color="green")

# ============================================================
# RESERVA
# ============================================================

def reserva(sala, filme_id):
    for widget in app.winfo_children():
        if widget != menu_lateral:
            widget.destroy()

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    titulo = ctk.CTkLabel(frame, text="ESCOLHA SEU ASSENTO", font=("Arial", 28, "bold"))
    titulo.pack(pady=20)

    tela = ctk.CTkLabel(frame, text="================ TELA ================", font=("Arial", 18))
    tela.pack(pady=10)

    assentos_frame = ctk.CTkFrame(frame)
    assentos_frame.pack(pady=20)

    for fila in range(10):
        letra = chr(65 + fila)
        label_fila = ctk.CTkLabel(assentos_frame, text=letra, width=30)
        label_fila.grid(row=fila, column=0, padx=5, pady=5)

        for lugar in range(20):
            if sala[fila][lugar] == 0:
                botao = ctk.CTkButton(assentos_frame, text=f"{letra}{lugar + 1}", width=45, height=35, fg_color="green")
                botao.configure(command=lambda s=sala, f=fila, l=lugar, b=botao: fazer_reserva(s, f, l, b, filme_id))
            else:
                botao = ctk.CTkButton(assentos_frame, text="X", width=45, height=35, fg_color="red", state="disabled")

            botao.grid(row=fila, column=lugar + 1, padx=2, pady=2)

    voltar = ctk.CTkButton(frame, text="Voltar", command=menu_principal)
    voltar.pack(pady=20)

# ============================================================
# FAZER RESERVA
# ============================================================

def fazer_reserva(sala, fila, lugar, botao, filme_id):
    global valor_total
    if sala[fila][lugar] == 1:
        return

    sucesso = salvar_reserva_banco(sala, fila, lugar)
    if sucesso:
        sala[fila][lugar] = 1
        valor_total += 25
        letra = chr(65 + fila)
        numero = lugar + 1
        historico.append(f"Reserva: Sala {1 if sala is sala1 else 2} - Assento {letra}{numero} - R$ 25,00")
        botao.configure(text="X", fg_color="red", state="disabled")
        print(f"Assento {letra}{numero} reservado!")
    else:
        print("Não foi possível realizar a reserva.")

# ============================================================
# FILME 1
# ============================================================

def mostrar_filme1():
    for widget in app.winfo_children():
        if widget != menu_lateral:
            widget.destroy()

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=30, pady=30)

    titulo = ctk.CTkLabel(frame, text="A ODISSÉIA", font=("Arial", 32, "bold"))
    titulo.pack(pady=20)

    informacoes = ctk.CTkLabel(frame, text="Duração: 2H52M\nSala: 1", font=("Arial", 20))
    informacoes.pack(pady=10)

    botao = ctk.CTkButton(frame, text="ESCOLHER ASSENTO", width=250, height=50, command=lambda: reserva(sala1, 1))
    botao.pack(pady=30)

    voltar = ctk.CTkButton(frame, text="Voltar", command=mostrar_filmes)
    voltar.pack()

# ============================================================
# FILME 2
# ============================================================

def mostrar_filme2():
    for widget in app.winfo_children():
        if widget != menu_lateral:
            widget.destroy()

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=30, pady=30)

    titulo = ctk.CTkLabel(frame, text="HOMEM-ARANHA 3", font=("Arial", 32, "bold"))
    titulo.pack(pady=20)

    informacoes = ctk.CTkLabel(frame, text="Duração: 2H19M\nSala: 2", font=("Arial", 20))
    informacoes.pack(pady=10)

    botao = ctk.CTkButton(frame, text="ESCOLHER ASSENTO", width=250, height=50, command=lambda: reserva(sala2, 2))
    botao.pack(pady=30)

    voltar = ctk.CTkButton(frame, text="Voltar", command=mostrar_filmes)
    voltar.pack()

# ============================================================
# terceiro filme
# ============================================================

def mostrar_filme3():
    for widget in app.winfo_children():
        if widget != menu_lateral:
            widget.destroy()

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=30, pady=30)

    titulo = ctk.CTkLabel(frame, text="BARBIE EM VIDA DE SEREIA", font=("Arial", 32, "bold"))
    titulo.pack(pady=20)

    informacoes = ctk.CTkLabel(frame, text="Duração: 1H15M\nSala: 3", font=("Arial", 20))
    informacoes.pack(pady=10)

    botao = ctk.CTkButton(frame, text="ESCOLHER ASSENTO", width=250, height=50, command=lambda: reserva(sala3, 3))
    botao.pack(pady=30)

    voltar = ctk.CTkButton(frame, text="Voltar", command=mostrar_filmes)
    voltar.pack()

# ============================================================
# MOSTRAR FILMES
# ============================================================

def mostrar_filmes():
    for widget in app.winfo_children():
        if widget != menu_lateral:
            widget.destroy()

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=30, pady=30)

    titulo = ctk.CTkLabel(frame, text="FILMES EM CARTAZ", font=("Arial", 32, "bold"))
    titulo.pack(pady=30)

    filme1 = ctk.CTkButton(frame, text="A ODISSÉIA\n2H52M - SALA 1", width=300, height=100, command=mostrar_filme1)
    filme1.pack(pady=15)

    filme2 = ctk.CTkButton(frame, text="HOMEM-ARANHA 3\n2H19M - SALA 2", width=300, height=100, command=mostrar_filme2)
    filme2.pack(pady=15)

    filme3 = ctk.CTkButton(frame, text="BARBIE EM VIDA DE SEREIA\n1H15M - SALA 3", width=300, height=100, command=mostrar_filme3)
    filme3.pack(pady=15)

# ============================================================
# CANCELAMENTO
# ============================================================

def menu_cancelar():
    for widget in app.winfo_children():
        if widget != menu_lateral:
            widget.destroy()

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=30, pady=30)

    titulo = ctk.CTkLabel(frame, text="CANCELAR RESERVA", font=("Arial", 30, "bold"))
    titulo.pack(pady=30)

    opcao = ctk.CTkOptionMenu(frame, values=["Selecione uma opção", "Sala 1", "Sala 2", "Sala 3"], command=selecionar)
    opcao.pack(pady=20)

# ============================================================
# SELECIONAR SALA PARA CANCELAR
# ============================================================

def selecionar(opcao):
    if opcao == "Sala 1":
        mostrar_cancelamento(sala1, 1)
    elif opcao == "Sala 2":
        mostrar_cancelamento(sala2, 2)
    elif opcao == "Sala 3":
        mostrar_cancelamento(sala3, 3)

# ============================================================
# MOSTRAR ASSENTOS PARA CANCELAMENTO
# ============================================================

def mostrar_cancelamento(sala, numero_sala):
    for widget in app.winfo_children():
        if widget != menu_lateral:
            widget.destroy()

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    titulo = ctk.CTkLabel(frame, text=f"CANCELAR — SALA {numero_sala}", font=("Arial", 28, "bold"))
    titulo.pack(pady=20)

    assentos_frame = ctk.CTkFrame(frame)
    assentos_frame.pack(pady=20)

    for fila in range(10):
        letra = chr(65 + fila)
        label_fila = ctk.CTkLabel(assentos_frame, text=letra, width=30)
        label_fila.grid(row=fila, column=0, padx=5, pady=5)

        for lugar in range(20):
            if sala[fila][lugar] == 1:
                botao = ctk.CTkButton(assentos_frame, text=f"{letra}{lugar + 1}", width=45, height=35, fg_color="red")
                botao.configure(command=lambda s=sala, f=fila, l=lugar, b=botao: fazer_cancela(s, f, l, b))
            else:
                botao = ctk.CTkButton(assentos_frame, text=f"{letra}{lugar + 1}", width=45, height=35, fg_color="green", state="disabled")

            botao.grid(row=fila, column=lugar + 1, padx=2, pady=2)

    voltar = ctk.CTkButton(frame, text="Voltar", command=menu_cancelar)
    voltar.pack(pady=20)

# ============================================================
# FAZER CANCELAMENTO
# ============================================================

def fazer_cancela(sala, fila, lugar, botao):
    global valor_total
    if sala[fila][lugar] == 0:
        return

    sucesso = cancelar_banco(sala, fila, lugar)
    if sucesso:
        sala[fila][lugar] = 0
        if valor_total >= 25:
            valor_total -= 25
        letra = chr(65 + fila)
        numero = lugar + 1
        historico.append(f"Cancelamento: Sala {1 if sala is sala1 else 2} - Assento {letra}{numero} - R$ 25,00")
        botao.configure(text=f"{letra}{numero}", fg_color="green", state="disabled")
        print(f"Reserva do assento {letra}{numero} cancelada!")
    else:
        print("Não foi possível cancelar.")

# ============================================================
# CALENDÁRIO
# ============================================================

def mostrar_filme_data(data):
    if data in datas_filme1:
        mostrar_filme1()
    elif data in datas_filme2:
        mostrar_filme2()

def menu_calendario():
    for widget in app.winfo_children():
        if widget != menu_lateral:
            widget.destroy()

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=30, pady=30)

    titulo = ctk.CTkLabel(frame, text="CALENDÁRIO", font=("Arial", 30, "bold"))
    titulo.pack(pady=30)

    dias = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sabado", "Domingo"]
    for dia in dias:
        botao = ctk.CTkButton(frame, text=dia, width=250, command=lambda d=dia: mostrar_filme_data(d))
        botao.pack(pady=5)

# ============================================================
# HISTÓRICO
# ============================================================

def menu_historico():
    for widget in app.winfo_children():
        if widget != menu_lateral:
            widget.destroy()

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=30, pady=30)

    titulo = ctk.CTkLabel(frame, text="HISTÓRICO", font=("Arial", 30, "bold"))
    titulo.pack(pady=20)

    if len(historico) == 0:
        texto = ctk.CTkLabel(frame, text="Nenhuma reserva realizada nesta sessão.", font=("Arial", 18))
        texto.pack(pady=20)
    else:
        for item in historico:
            texto = ctk.CTkLabel(frame, text=item, font=("Arial", 16))
            texto.pack(pady=5)

    total = ctk.CTkLabel(frame, text=f"Valor total atual: R$ {valor_total:.2f}", font=("Arial", 20, "bold"))
    total.pack(pady=30)

# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu_principal():
    for widget in app.winfo_children():
        if widget != menu_lateral:
            widget.destroy()

    titulo = ctk.CTkLabel(app, text="CINETICA", font=("Arial", 40, "bold"))
    titulo.pack(pady=100)

    texto = ctk.CTkLabel(app, text="Sistema de gerenciamento de cinema", font=("Arial", 20))
    texto.pack()

# ============================================================
# FECHAR PROGRAMA
# ============================================================

def fechar_programa():
    try:
        if cursor is not None:
            cursor.close()
        if conexao is not None:
            conexao.close()
        print("PostgreSQL fechado!")
    except Exception as erro:
        print("Erro ao fechar PostgreSQL:")
        print(erro)

    app.destroy()

# ============================================================
# JANELA PRINCIPAL
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Cinetica")
app.geometry("1200x700")

try:
    app.state("zoomed")
except:
    pass

# ============================================================
# MENU LATERAL
# ============================================================

menu_lateral = ctk.CTkFrame(app, width=220)
menu_lateral.pack(side="left", fill="y")

titulo_menu = ctk.CTkLabel(menu_lateral, text="CINETICA", font=("Arial", 25, "bold"))
titulo_menu.pack(pady=30)

botao_reserva = ctk.CTkButton(menu_lateral, text="Reservar ingresso", command=mostrar_filmes)
botao_reserva.pack(padx=20, pady=10)

botao_cancelar = ctk.CTkButton(menu_lateral, text="Cancelar reserva", command=menu_cancelar)
botao_cancelar.pack(padx=20, pady=10)

botao_sala1 = ctk.CTkButton(menu_lateral, text="Ver Sala 1", command=lambda: mostrar_sala(sala1, 1))
botao_sala1.pack(padx=20, pady=10)

botao_sala2 = ctk.CTkButton(menu_lateral, text="Ver Sala 2", command=lambda: mostrar_sala(sala2, 2))
botao_sala2.pack(padx=20, pady=10)

botao_calendario = ctk.CTkButton(menu_lateral, text="Calendário", command=menu_calendario)
botao_calendario.pack(padx=20, pady=10)

botao_historico = ctk.CTkButton(menu_lateral, text="Histórico", command=menu_historico)
botao_historico.pack(padx=20, pady=10)

botao_sair = ctk.CTkButton(menu_lateral, text="Sair", fg_color="red", hover_color="darkred", command=fechar_programa)
botao_sair.pack(padx=20, pady=30)

# ============================================================
# CARREGAR DADOS DO POSTGRESQL
# ============================================================

carregar_banco()

# ============================================================
# INICIAR PROGRAMA
# ============================================================

menu_principal()
app.mainloop()
