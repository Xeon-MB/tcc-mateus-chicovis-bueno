import subprocess
import sys
from pathlib import Path

# ============================================================
# INSTALAÇÃO AUTOMÁTICA DE BIBLIOTECAS
# ============================================================
def verificar_e_instalar(pacote):
    try:
        __import__(pacote)
    except ImportError:
        print(f"Instalando {pacote}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

verificar_e_instalar("customtkinter")
verificar_e_instalar("pillow")
verificar_e_instalar("psycopg2")

import customtkinter as ctk
import psycopg2
from PIL import Image

# ============================================================
# CONFIGURAÇÕES DO BANCO DE DADOS E VARIÁVEIS
# ============================================================
DB_CONFIG = {
    "dbname": "wow",
    "user": "postgres",
    "password": "root",
    "host": "localhost",
    "port": "5432"
}

assentos_selecionados = []
BASE_DIR = Path(__file__).resolve().parent

filmes_dias = {
    "Segunda-feira": "A Odisseia",
    "Terça-feira": "Homem-Aranha 3",
    "Quarta-feira": "Barbie em Vida de Sereia",
    "Quinta-feira": "A Odisseia",
    "Sexta-feira": "Homem-Aranha 3",
    "Sábado": "Barbie em Vida de Sereia",
    "Domingo": "A Odisseia"
}

# ============================================================
# CONFIGURAÇÃO DA JANELA PRINCIPAL
# ============================================================
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("CineSenai")
app.geometry("1280x720")
app.configure(fg_color="#121212")

# Layout de telas
menu_lateral = ctk.CTkFrame(app, width=220, fg_color="#1a1a1a", corner_radius=0)
menu_lateral.pack(side="left", fill="y")

main_frame = ctk.CTkFrame(app, fg_color="#121212", corner_radius=0)
main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)


# ============================================================
# FUNÇÕES DE BANCO DE DADOS
# ============================================================
def buscar_estado_sala(numero_sala):
    status_assentos = {}
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        tabela = f"assentos_sala_{numero_sala}"
        cursor.execute(f"SELECT fila, numero_cadeira, ocupado FROM {tabela};")
        linhas = cursor.fetchall()

        for fila, numero, ocupado in linhas:
            chave = f"{fila}{numero}"
            status_assentos[chave] = ocupado

    except Exception as error:
        print(f"Erro ao buscar assentos: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()
            
    return status_assentos


def alternar_assento(btn, nome_assento):
    global assentos_selecionados

    if nome_assento in assentos_selecionados:
        # Desmarcar o assento
        assentos_selecionados.remove(nome_assento)
        btn.configure(fg_color="#ffffff", text_color="#000000")
    else:
        # Marcar o assento
        assentos_selecionados.append(nome_assento)
        btn.configure(fg_color="#e50914", text_color="#ffffff")


def confirmar_reserva(numero_sala):
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
            numero = assento[1:]
            query = f"UPDATE {tabela} SET ocupado = true WHERE fila = %s AND numero_cadeira = %s;"
            cursor.execute(query, (letra, numero))

        assentos_str = ", ".join(assentos_selecionados)
        texto_historico = f"Reserva na Sala {numero_sala} - Assentos: {assentos_str}"
        cursor.execute("INSERT INTO historico (movimentacao) VALUES (%s);", (texto_historico,))
        
        conn.commit()
        assentos_selecionados.clear()
        mostrar_tela_sala(numero_sala)

    except Exception as error:
        print(f"Erro no banco: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()


def cancelar_reserva(numero_sala):
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
            numero = assento[1:]
            query = f"UPDATE {tabela} SET ocupado = false WHERE fila = %s AND numero_cadeira = %s;"
            cursor.execute(query, (letra, numero))

        assentos_str = ", ".join(assentos_selecionados)
        texto_historico = f"Cancelamento na Sala {numero_sala} - Assentos: {assentos_str}"
        cursor.execute("INSERT INTO historico (movimentacao) VALUES (%s);", (texto_historico,))
        
        conn.commit()
        assentos_selecionados.clear()
        mostrar_tela_sala(numero_sala)

    except Exception as error:
        print(f"Erro no banco: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()


# ============================================================
# AUXILIARES DE INTERFACE
# ============================================================
def limpar_tela_principal():
    global assentos_selecionados
    assentos_selecionados.clear()
    for widget in main_frame.winfo_children():
        widget.destroy()


def criar_card_filme(container, nome, duracao, sala, caminho_img, coluna):
    frame_card = ctk.CTkFrame(container, fg_color="transparent")
    frame_card.grid(row=0, column=coluna, padx=25)

    try:
        img = Image.open(caminho_img)
    except FileNotFoundError:
        img = Image.new("RGB", (180, 260), color="#2b2b36")

    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(180, 260))

    btn_img = ctk.CTkButton(
        frame_card,
        text="",
        image=ctk_img,
        width=180,
        height=260,
        fg_color="transparent",
        hover_color="#2b2b36",
        command=lambda: mostrar_tela_sala(sala)
    )
    btn_img.pack()

    ctk.CTkLabel(frame_card, text=nome, font=("Arial", 16, "bold"), text_color="#ffffff").pack(pady=(10, 2))
    ctk.CTkLabel(frame_card, text=f"Duração: {duracao}", font=("Arial", 13), text_color="#aaaaaa").pack()
    ctk.CTkLabel(frame_card, text=f"SALA {sala}", font=("Arial", 14, "bold"), text_color="#e50914").pack(pady=(2, 0))


# ============================================================
# TELAS DO SISTEMA
# ============================================================
def mostrar_tela_inicial():
    limpar_tela_principal()

    ctk.CTkLabel(
        main_frame,
        text="Bem-vindo ao CineSenai",
        font=("Arial", 36, "bold"),
        text_color="#ffffff"
    ).pack(pady=(150, 10))

    ctk.CTkLabel(
        main_frame,
        text="Selecione uma opção no menu lateral para começar.",
        font=("Arial", 16),
        text_color="#aaaaaa"
    ).pack(pady=10)


def ver_calendario():
    limpar_tela_principal()

    ctk.CTkLabel(
        main_frame,
        text="PROGRAMAÇÃO DA SEMANA",
        font=("Arial", 26, "bold"),
        text_color="#ffffff"
    ).pack(pady=20)

    dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]

    for dia in dias:
        filme = filmes_dias[dia]

        card = ctk.CTkFrame(main_frame, width=600, height=50, fg_color="#1a1a1a", corner_radius=8)
        card.pack(pady=5)
        card.pack_propagate(False)

        ctk.CTkLabel(card, text=dia, font=("Arial", 15, "bold"), text_color="#e50914", width=180, anchor="w").pack(side="left", padx=20)
        ctk.CTkLabel(card, text=filme, font=("Arial", 15), text_color="#ffffff").pack(side="left", padx=10)


def ver_filmes():
    limpar_tela_principal()

    ctk.CTkLabel(main_frame, text="FILMES EM CARTAZ", font=("Arial", 28, "bold"), text_color="#ffffff").pack(pady=20)

    container_filmes = ctk.CTkFrame(main_frame, fg_color="transparent")
    container_filmes.pack(pady=20)

    criar_card_filme(container_filmes, "A Odisseia", "2H52M", 1, BASE_DIR / "odisseia.png", 0)
    criar_card_filme(container_filmes, "Homem Aranha 3", "2H19M", 2, BASE_DIR / "homemaranha3.png", 1)
    criar_card_filme(container_filmes, "Barbie em Vida de Sereia", "1H15M", 3, BASE_DIR / "barbie.png", 2)


def mostrar_tela_sala(numero_sala):
    limpar_tela_principal()

    # Título da Sala
    ctk.CTkLabel(
        main_frame, 
        text=f"ESCOLHA SEUS ASSENTOS - SALA {numero_sala}", 
        font=("Arial", 22, "bold"), 
        text_color="#ffffff"
    ).pack(pady=(10, 15))

    # Área de rolagem caso o monitor seja pequeno
    scroll_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent", height=420)
    scroll_frame.pack(fill="both", expand=True, padx=10)

    grade_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    grade_frame.pack(anchor="center")

    status_no_banco = buscar_estado_sala(numero_sala)

    # EXACTAMENTE 200 ASSENTOS: 10 filas (A até J) x 20 colunas (1 até 20)
    filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    colunas = list(range(1, 21))

    for r_idx, fila in enumerate(filas):
        # Letra da Fila no lado esquerdo
        lbl_fila = ctk.CTkLabel(grade_frame, text=fila, font=("Arial", 12, "bold"), text_color="#aaaaaa", width=25)
        lbl_fila.grid(row=r_idx, column=0, padx=(0, 10), pady=3)

        for c_idx, coluna in enumerate(colunas):
            nome_assento = f"{fila}{coluna}"
            esta_ocupado = status_no_banco.get(nome_assento, False)

            if esta_ocupado:
                cor_fundo = "#333333"
                cor_texto = "#777777"
                texto_btn = "✕"
            else:
                cor_fundo = "#ffffff"
                cor_texto = "#000000"
                texto_btn = str(coluna)

            btn = ctk.CTkButton(
                grade_frame,
                text=texto_btn,
                width=32,
                height=30,
                corner_radius=4,
                font=("Arial", 10, "bold"),
                fg_color=cor_fundo,
                text_color=cor_texto,
                hover_color="#e50914" if not esta_ocupado else "#333333"
            )

            if not esta_ocupado:
                btn.configure(command=lambda b=btn, a=nome_assento: alternar_assento(b, a))

            # Cria um espaço no meio das cadeiras simulando o corredor do cinema
            espaco_corredor = (2, 12) if coluna == 10 else (2, 2)
            btn.grid(row=r_idx, column=c_idx+1, padx=espaco_corredor, pady=3)

    # Indicador de Tela de Cinema
    frame_tela = ctk.CTkFrame(scroll_frame, fg_color="#222225", height=12, corner_radius=6)
    frame_tela.pack(fill="x", padx=120, pady=(25, 5))
    
    ctk.CTkLabel(scroll_frame, text="T E L A", font=("Arial", 11, "bold"), text_color="#777777").pack()

    # Legenda e Botões no Rodapé
    rodape = ctk.CTkFrame(main_frame, fg_color="transparent")
    rodape.pack(fill="x", pady=(10, 0))

    # Legenda de Status
    legenda = ctk.CTkFrame(rodape, fg_color="transparent")
    legenda.pack(side="left")

    # Item Disponível
    ctk.CTkFrame(legenda, width=12, height=12, fg_color="#ffffff", corner_radius=2).pack(side="left", padx=(0, 5))
    ctk.CTkLabel(legenda, text="Disponível", font=("Arial", 12), text_color="#aaaaaa").pack(side="left", padx=(0, 15))

    # Item Indisponível
    ctk.CTkFrame(legenda, width=12, height=12, fg_color="#333333", corner_radius=2).pack(side="left", padx=(0, 5))
    ctk.CTkLabel(legenda, text="Indisponível", font=("Arial", 12), text_color="#aaaaaa").pack(side="left", padx=(0, 15))

    # Item Selecionado
    ctk.CTkFrame(legenda, width=12, height=12, fg_color="#e50914", corner_radius=2).pack(side="left", padx=(0, 5))
    ctk.CTkLabel(legenda, text="Selecionado", font=("Arial", 12), text_color="#aaaaaa").pack(side="left")

    # Botões de Ação
    frame_acoes = ctk.CTkFrame(rodape, fg_color="transparent")
    frame_acoes.pack(side="right")

    ctk.CTkButton(
        frame_acoes,
        text="Confirmar Reserva",
        font=("Arial", 13, "bold"),
        fg_color="#e50914",
        hover_color="#b80710",
        command=lambda: confirmar_reserva(numero_sala)
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        frame_acoes,
        text="Cancelar Reserva",
        font=("Arial", 13, "bold"),
        fg_color="#2b2b30",
        hover_color="#3a3a40",
        command=lambda: cancelar_reserva(numero_sala)
    ).pack(side="left")


def ver_historico():
    limpar_tela_principal()
    
    ctk.CTkLabel(
        main_frame, 
        text="HISTÓRICO DE MOVIMENTAÇÕES", 
        font=("Arial", 26, "bold"),
        text_color="#ffffff"
    ).pack(pady=20)

    area_scroll = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    area_scroll.pack(fill="both", expand=True, padx=20, pady=10)

    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT movimentacao FROM historico ORDER BY id DESC;")

        resultado = cursor.fetchall()
        
        if not resultado:
            ctk.CTkLabel(area_scroll, text="Nenhum histórico encontrado.", font=("Arial", 15), text_color="#aaaaaa").pack(pady=20)

        for linha in resultado:
            card = ctk.CTkFrame(area_scroll, fg_color="#1a1a1a", corner_radius=6)
            card.pack(fill="x", padx=10, pady=4)

            ctk.CTkLabel(card, text=linha[0], font=("Arial", 13), text_color="#ffffff", anchor="w").pack(fill="x", padx=15, pady=10)

    except Exception as error:
        ctk.CTkLabel(area_scroll, text=f"Erro ao carregar histórico: {error}", text_color="#e50914").pack(pady=20)
    finally:
        if conn:
            cursor.close()
            conn.close()


# ============================================================
# MENU LATERAL DE NAVEGAÇÃO
# ============================================================
ctk.CTkLabel(menu_lateral, text="CINESENAI", font=("Arial", 22, "bold"), text_color="#e50914").pack(pady=(30, 30))

def criar_botao_menu(texto, comando):
    btn = ctk.CTkButton(
        menu_lateral, 
        text=texto, 
        command=comando,
        fg_color="transparent",
        hover_color="#2b2b30",
        text_color="#ffffff",
        font=("Arial", 14),
        anchor="w",
        height=40
    )
    btn.pack(fill="x", padx=10, pady=2)
    return btn

criar_botao_menu("Início", mostrar_tela_inicial)
criar_botao_menu("Filmes em Cartaz", ver_filmes)
criar_botao_menu("Ver Sala 1", lambda: mostrar_tela_sala(1))
criar_botao_menu("Ver Sala 2", lambda: mostrar_tela_sala(2))
criar_botao_menu("Ver Sala 3", lambda: mostrar_tela_sala(3))
criar_botao_menu("Calendário", ver_calendario)
criar_botao_menu("Histórico", ver_historico)

ctk.CTkButton(
    menu_lateral, 
    text="Sair", 
    fg_color="#e50914", 
    hover_color="#b80710", 
    command=app.destroy,
    font=("Arial", 13, "bold"),
    height=38
).pack(fill="x", padx=15, pady=20, side="bottom")

# ============================================================
# INICIALIZAÇÃO
# ============================================================
mostrar_tela_inicial()
app.mainloop()