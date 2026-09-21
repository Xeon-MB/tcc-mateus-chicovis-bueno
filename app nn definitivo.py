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


colunas = ["A", "B", "C", "D", "E","F", "G", "H", "I", "J","K", "L", "M", "N", "O","P", "Q", "R", "S", "T"]
linhas = range(1, 11)

# ============================================================
# VARIÁVEIS
# ============================================================

valor_total = 0
historico = []

datas_filme1 = ["Segunda-Feira", "Quinta-Feira", "Domingo"]
datas_filme2 = ["Terça-Feira", "Sexta Feira"]
datas_filme3 = ["Quarta-Feira", "Sabado"]

sala1 = [[0 for _ in range(20)] for _ in range(10)]
sala2 = [[0 for _ in range(20)] for _ in range(10)]
sala3 = [[0 for _ in range(20)] for _ in range(10)]
# ============================================================
# banco fudido
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


# ============================================================
# CARREGAR RESERVAS DO BANCO PARA AS MATRIZES
# ============================================================

def carregar_banco():
    if cursor is None:
        return
    try:
        def carregar_sala(nome_tabela, matriz_sala):
            cursor.execute(f"SELECT fila, numero_cadeira, ocupado FROM {nome_tabela}")
            dados = cursor.fetchall()
            for fila, numero_cadeira, ocupado in dados:
                linha = ord(fila.upper()) - 65
                coluna = numero_cadeira - 1
                # Se ocupado for True no PostgreSQL, marca como 1 na matriz visual
                matriz_sala[linha][coluna] = 1 if ocupado else 0

        carregar_sala("assentos_sala_1", sala1)
        carregar_sala("assentos_sala_2", sala2)
        carregar_sala("assentos_sala_3", sala3)

        print("Matrizes carregadas e sincronizadas com a base de dados!")
    except Exception as erro:
        print(f"Erro fatal ao carregar banco: {erro}")

        conexao.commit()
        print("Matrizes carregadas do banco!")
    except Exception as erro:
        print("Erro ao carregar banco:")
        print(erro)


        conexao.commit()
        print("Matrizes carregadas do banco!")
    except Exception as erro:
        print("Erro ao carregar banco:")
        print(erro)


# ============================================================
# banco atualizado
# ============================================================

# ============================================================
# BANCO ATUALIZADO - SALVAR RESERVA
# ============================================================

def salvar_reserva_banco(sala, fila_index, lugar_index):
    if cursor is None:
        return False
    try:
        # Descobre qual tabela usar dependendo da matriz que chamou a função
        tabela = "assentos_sala_1" if sala is sala1 else ("assentos_sala_2" if sala is sala2 else "assentos_sala_3")
        
        letra_fila = chr(65 + fila_index)
        numero_cadeira = lugar_index + 1

        # Verifica o estado atual diretamente na tabela da sala específica
        cursor.execute(f"""
            SELECT ocupado FROM {tabela}
            WHERE fila = %s AND numero_cadeira = %s
        """, (letra_fila, numero_cadeira))
        
        assento = cursor.fetchone()
        
        if assento is None or assento[0] == True:
            print("Assento já reservado ou inexistente.")
            return False

        # Marca como ocupado
        cursor.execute(f"""
            UPDATE {tabela}
            SET ocupado = TRUE
            WHERE fila = %s AND numero_cadeira = %s
        """, (letra_fila, numero_cadeira))

        conexao.commit()
        return True
    except Exception as erro:
        print(f"Erro SQL ao salvar reserva: {erro}")
        conexao.rollback()
        return False, erro

# ============================================================
# banco CANCELAMENTOXDDD
# ============================================================
def cancelar_banco(sala, fila_index, lugar_index):
    if cursor is None:
        return False
    try:
        tabela = "assentos_sala_1" if sala is sala1 else ("assentos_sala_2" if sala is sala2 else "assentos_sala_3")
        
        letra_fila = chr(65 + fila_index)
        numero_cadeira = lugar_index + 1

        cursor.execute(f"""
            UPDATE {tabela}
            SET ocupado = FALSE
            WHERE fila = %s AND numero_cadeira = %s
        """, (letra_fila, numero_cadeira))

        conexao.commit()
        return True
    except Exception as erro:
        print(f"Erro SQL ao cancelar reserva: {erro}")
        conexao.rollback()
        return False


# ============================================================
# MOSTRAR SALA E PERMITIR RESERVA
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

    for fila_index in range(10):
        letra = chr(65 + fila_index)
        label_fila = ctk.CTkLabel(assentos_frame, text=letra, width=30)
        label_fila.grid(row=fila_index, column=0, padx=5, pady=5)

        for lugar_index in range(20):
            # Se o estado na matriz for 0 (Livre)
            if sala[fila_index][lugar_index] == 0:
                texto = f"{letra}{lugar_index + 1}"
                # Cria o botão verde e ATIVO, passando os dados para fazer_reserva
                botao = ctk.CTkButton(assentos_frame, text=texto, width=45, height=35, fg_color="green")
                # O lambda "congela" os valores de fila e lugar para aquele botão específico
                botao.configure(command=lambda s=sala, f=fila_index, l=lugar_index, b=botao: fazer_reserva(s, f, l, b, numero_sala))
            
            # Se o estado na matriz for 1 (Ocupado)
            else:
                texto = "X"
                # Cria o botão vermelho e DESATIVADO
                botao = ctk.CTkButton(assentos_frame, text=texto, width=45, height=35, fg_color="red", state="disabled")

            botao.grid(row=fila_index, column=lugar_index + 1, padx=2, pady=2)



# ============================================================
# FAZER RESERVA
# ============================================================

def fazer_reserva(sala, fila_index, lugar_index, botao, numero_sala):
    global valor_total

    # Se o assento já estiver marcado como 1 na matriz, ignora o clique
    if sala[fila_index][lugar_index] == 1:
        return

    # Tenta salvar no banco de dados PRIMEIRO
    sucesso = salvar_reserva_banco(sala, fila_index, lugar_index)
    
    if sucesso:
        # Se o PostgreSQL confirmou a gravação, atualizamos a interface gráfica
        sala[fila_index][lugar_index] = 1
        valor_total += 25
        
        letra = chr(65 + fila_index)
        numero = lugar_index + 1
        
        # Adiciona a ação ao histórico
        historico.append(f"Reserva: Sala {numero_sala} - Assento {letra}{numero} - R$ 25,00")
        
        # Muda a cor do botão para vermelho e desativa o clique
        botao.configure(text="X", fg_color="red", state="disabled")
        print(f"Assento {letra}{numero} reservado com sucesso na Sala {numero_sala}!")
    else:
        print("Erro: Não foi possível confirmar a reserva na base de dados.")

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

    botao = ctk.CTkButton(frame, text="ESCOLHER ASSENTO", width=250, height=50)
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

    botao = ctk.CTkButton(frame, text="ESCOLHER ASSENTO", width=250, height=50)
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

    botao = ctk.CTkButton(frame, text="ESCOLHER ASSENTO", width=250, height=50)
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
    elif data in datas_filme3:
        mostrar_filme3()

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

    titulo = ctk.CTkLabel(app, text="CineSenai", font=("Arial", 40, "bold"))
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
app.title("CineSenai")
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

titulo_menu = ctk.CTkLabel(menu_lateral, text="Menu Lateral", font=("Arial", 25, "bold"))
titulo_menu.pack(pady=30)

botao_reserva = ctk.CTkButton(menu_lateral, text="Reservar ingresso", command=mostrar_filmes)
botao_reserva.pack(padx=20, pady=10)

botao_cancelar = ctk.CTkButton(menu_lateral, text="Cancelar reserva", command=menu_cancelar)
botao_cancelar.pack(padx=20, pady=10)

botao_sala1 = ctk.CTkButton(menu_lateral, text="Ver Sala 1", command=lambda: mostrar_sala(sala1, 1))
botao_sala1.pack(padx=20, pady=10)

botao_sala2 = ctk.CTkButton(menu_lateral, text="Ver Sala 2", command=lambda: mostrar_sala(sala2, 2))
botao_sala2.pack(padx=20, pady=10)

botao_sala3 = ctk.CTkButton(menu_lateral, text="Ver Sala 3", command=lambda: mostrar_sala(sala3, 3))
botao_sala3.pack(padx=20, pady=10)

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
