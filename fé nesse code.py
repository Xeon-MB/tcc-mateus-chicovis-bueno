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

import customtkinter as ctk
import psycopg2
from PIL import Image
from pathlib import Path

DB_CONFIG = {
    "dbname": "wow",
    "user": "postgres",
    "password": "root",
    "host": "localhost",
    "port": "5432"
}

# Lista global para armazenar temporariamente os assentos selecionados
assentos_selecionados = []
BASE_DIR = Path(__file__).resolve().parent

# ============================================================
# JANELA PRINCIPAL
# ============================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("CineSenai")
app.geometry("1920x1080")
try:
    app.state("zoomed")
except:
    pass

# ============================================================
# FRAMES DE LAYOUT (O SEGREDO PARA NÃO DAR ERRO DE PACK/GRID)
# ============================================================
# Menu na esquerda
menu_lateral = ctk.CTkFrame(app, width=220)
menu_lateral.pack(side="left", fill="y")

# Área principal na direita onde tudo vai aparecer
main_frame = ctk.CTkFrame(app)
main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# ============================================================
# FUNÇÕES DE BANCO DE DADOS E LÓGICA
# ============================================================
def buscar_estado_sala(numero_sala):
    """Busca os assentos ocupados da sala específica e retorna um dicionário."""
    status_assentos = {}
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Assumindo que tuas tabelas se chamam assentos_sala_1, assentos_sala_2, etc.
        tabela = f"assentos_sala_{numero_sala}" 
        cursor.execute(f"SELECT fila, numero_cadeira, ocupado FROM {tabela};")
        linhas = cursor.fetchall()

        for fila, numero, ocupado in linhas:
            chave = f"{fila}{numero}"
            status_assentos[chave] = ocupado

    except Exception as error:
        print(f"Erro ao consultar o banco de dados: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return status_assentos

def alternar_assento(btn):
    """Muda a cor do botão ao clicar e adiciona/remove da lista."""
    global assentos_selecionados
    
    # No CustomTkinter usa-se cget() para pegar propriedades e configure() para alterar
    cor_atual = btn.cget("fg_color")
    
    if cor_atual == "#ffffff": # Se está branco (livre)
        btn.configure(fg_color="#4CAF50", text_color="white") # Fica verde
        assentos_selecionados.append(btn.cget("text"))
    else: # Se já está verde
        btn.configure(fg_color="#ffffff", text_color="black") # Volta a ficar branco
        assentos_selecionados.remove(btn.cget("text"))

def confirmar_reserva(numero_sala):
    """Salva os assentos selecionados no banco de dados."""
    global assentos_selecionados
    if not assentos_selecionados:
        print("Nenhum assento selecionado!")
        return

    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        tabela = f"assentos_sala_{numero_sala}"

        for assento in assentos_selecionados:
            letra = assento[0]
            numero = assento[1:] # Pega do segundo caractere em diante (caso seja 'A10')
            query = f"UPDATE {tabela} SET ocupado = true WHERE fila = %s AND numero_cadeira = %s;"
            cursor.execute(query, (letra, numero))
        
        conn.commit()
        print(f"Reserva concluída na Sala {numero_sala}: {assentos_selecionados}")
        
        # Limpa a lista de seleções e recarrega a tela
        assentos_selecionados.clear()
        mostrar_tela_sala(numero_sala)

    except Exception as error:
        print(f"Erro ao operar no banco: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

# ============================================================
# FUNÇÕES DE INTERFACE (DESENHAR A SALA)
# ============================================================
def limpar_tela_principal():
    """Destrói todos os widgets dentro do main_frame antes de desenhar outra coisa."""
    global assentos_selecionados
    assentos_selecionados.clear() # Limpa as seleções pendentes se trocar de sala
    for widget in main_frame.winfo_children():
        widget.destroy()

def mostrar_tela_sala(numero_sala):
    """Constrói a grade de botões dentro do main_frame para a sala escolhida."""
    limpar_tela_principal()

    titulo = ctk.CTkLabel(main_frame, text=f"SALA {numero_sala}", font=("Arial", 28, "bold"))
    titulo.pack(pady=20)

    # Frame interno só para os botões da grade, usando pack no main_frame e grid internamente
    grade_frame = ctk.CTkFrame(main_frame)
    grade_frame.pack(pady=10)

    status_no_banco = buscar_estado_sala(numero_sala)

    filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K']
    colunas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    for r_idx, fila in enumerate(filas):
        for c_idx, coluna in enumerate(colunas):
            nome_assento = f"{fila}{coluna}"
            esta_ocupado = status_no_banco.get(nome_assento, False)

            if esta_ocupado:
                cor_fundo = "#f44336" # Vermelho
                cor_texto = "white"
                estado_botao = "disabled"
            else:
                cor_fundo = "#ffffff" # Branco
                cor_texto = "black"
                estado_botao = "normal"

            # Sintaxe corrigida do CustomTkinter
            btn = ctk.CTkButton(
                grade_frame,
                text=nome_assento,
                width=50,
                height=40,
                font=("Arial", 12, "bold"),
                fg_color=cor_fundo,
                text_color=cor_texto,
                text_color_disabled="white", 
                state=estado_botao
            )

            if estado_botao == "normal":
                btn.configure(command=lambda b=btn: alternar_assento(b))
            
            # Aqui usamos o grid dentro do grade_frame, não entra em conflito com pack!
            btn.grid(row=r_idx, column=c_idx, padx=5, pady=5)

    btn_reservar = ctk.CTkButton(
        main_frame,
        text='Confirmar Reserva',
        height=40,
        font=("Arial", 14, "bold"),
        fg_color="#0d761f",
        text_color="black",
        command=lambda: confirmar_reserva(numero_sala)
    )
    btn_reservar.pack(pady=30)


def ver_filmes():
    limpar_tela_principal()

    caminho_imagem1 = BASE_DIR / "odisseia.png"
    image1 = ctk.CTkImage(light_image=Image.open(caminho_imagem1), dark_image=Image.open(caminho_imagem1), size=(200, 300))

    filme1 = ctk.CTkButton(main_frame, text="", image=image1, width=200, height=300, fg_color="transparent")
    filme1.grid(row=0, column=0, padx=10)

    nome_filme1 = ctk.CTkLabel(main_frame, text="A Odisseia", font=("Arial", 15, "bold"))
    nome_filme1.grid(row=1, column=0, padx=10)

    duracao_filme1 = ctk.CTkLabel(main_frame, text="Duração: 2H52M", font=("Arial", 15))
    duracao_filme1.grid(row=2, column=0, padx=10)

    sala_filme1 = ctk.CTkLabel(main_frame, text="SALA: 1", font=("Arial", 15))
    sala_filme1.grid(row=3, column=0, padx=10)

    caminho_imagem2 = BASE_DIR / "homemaranha3.png"
    image2 = ctk.CTkImage(light_image=Image.open(caminho_imagem2), dark_image=Image.open(caminho_imagem2), size=(200, 300))

    filme2 = ctk.CTkButton(main_frame, text="", image=image2, width=200, height=300, fg_color="transparent")
    filme2.grid(row=0, column=1, padx=10)

    nome_filme2 = ctk.CTkLabel(main_frame, text="Homem Aranha 3", font=("Arial", 15, "bold"))
    nome_filme2.grid(row=1, column=1, padx=10)

    duracao_filme2 = ctk.CTkLabel(main_frame, text="Duração: 2H19M", font=("Arial", 15))
    duracao_filme2.grid(row=2, column=1, padx=10)

    sala_filme2 = ctk.CTkLabel(main_frame, text="SALA: 2", font=("Arial", 15))
    sala_filme2.grid(row=3, column=1, padx=10)

    caminho_imagem3 = BASE_DIR / "barbie.png"
    image3 = ctk.CTkImage(light_image=Image.open(caminho_imagem3), dark_image=Image.open(caminho_imagem3), size=(200, 300))

    filme1 = ctk.CTkButton(main_frame, text="", image=image3, width=200, height=300, fg_color="transparent")
    filme1.grid(row=0, column=2, padx=10)

    nome_filme1 = ctk.CTkLabel(main_frame, text="Barbie em Vida de Sereia", font=("Arial", 15, "bold"))
    nome_filme1.grid(row=1, column=2, padx=10)

    duracao_filme1 = ctk.CTkLabel(main_frame, text="Duração: 1H515M", font=("Arial", 15))
    duracao_filme1.grid(row=2, column=2, padx=10)

    sala_filme1 = ctk.CTkLabel(main_frame, text="SALA: 3", font=("Arial", 15))
    sala_filme1.grid(row=3, column=2, padx=10)
# ============================================================
# BOTÕES DO MENU LATERAL
# ============================================================
titulo_menu = ctk.CTkLabel(menu_lateral, text="CineSenai", font=("Arial", 25, "bold"))
titulo_menu.pack(pady=30)

filmes = ctk.CTkButton(menu_lateral, text="Ver Filmes em Cartaz", command=ver_filmes)
filmes.pack(padx=20, pady=10)

botao_sala1 = ctk.CTkButton(menu_lateral, text="Ver Sala 1", command=lambda: mostrar_tela_sala(1))
botao_sala1.pack(padx=20, pady=10)

botao_sala2 = ctk.CTkButton(menu_lateral, text="Ver Sala 2", command=lambda: mostrar_tela_sala(2))
botao_sala2.pack(padx=20, pady=10)

botao_sala3 = ctk.CTkButton(menu_lateral, text="Ver Sala 3", command=lambda: mostrar_tela_sala(3))
botao_sala3.pack(padx=20, pady=10)

calendario = ctk.CTkButton(menu_lateral, text="Calendário")
calendario.pack(padx=20, pady=10)

historico = ctk.CTkButton(menu_lateral, text="Histórico")
historico.pack(padx=20, pady=10)


botao_sair = ctk.CTkButton(menu_lateral, text="Sair", fg_color="red", hover_color="darkred", command=app.destroy)
botao_sair.pack(padx=20, pady=30, side="bottom")

app.mainloop()