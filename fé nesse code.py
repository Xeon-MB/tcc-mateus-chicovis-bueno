import subprocess
import sys
from pathlib import Path

def verificar_e_instalar(pacote):
    try:
        __import__(pacote)
    except ImportError:
        print(f"Biblioteca '{pacote}' não encontrada. A instalar automaticamente...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

verificar_e_instalar("customtkinter")
verificar_e_instalar("pillow")
verificar_e_instalar("psycopg2")

import customtkinter as ctk
import psycopg2
from PIL import Image

# ============================================================
# CONFIGURAÇÕES E CONSTANTES
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
# INICIALIZAÇÃO DA JANELA PRINCIPAL
# ============================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("CineSenai")
app.geometry("1920x1080")

try:
    app.state("zoomed")
except Exception:
    pass

# Frames de layout principal
menu_lateral = ctk.CTkFrame(app, width=250, fg_color="#1e1e24")
menu_lateral.pack(side="left", fill="y")

main_frame = ctk.CTkFrame(app)
main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)


# ============================================================
# LÓGICA DE BASE DE DADOS E ASSENTOS
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
        print(f"Erro ao consultar a base de dados: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()
            
    return status_assentos


def alternar_assento(btn):
    global assentos_selecionados
    cor_atual = btn.cget("fg_color")
    nome_assento = btn.cget("text")
    
    # Se estiver selecionando (muda para verde)
    if cor_atual in ["#ffffff", "#f44336"]: 
        if nome_assento not in assentos_selecionados:
            assentos_selecionados.append(nome_assento)
            btn.configure(fg_color="#4CAF50", text_color="white")
    else:
        # Se clicar de novo para desmarcar, devolve a cor original
        if nome_assento in assentos_selecionados:
            assentos_selecionados.remove(nome_assento)
            btn.configure(fg_color="#ffffff", text_color="black")


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

        # 1. Atualiza todos os assentos selecionados no banco
        for assento in assentos_selecionados:
            letra = assento[0]
            numero = assento[1:]
            query = f"UPDATE {tabela} SET ocupado = true WHERE fila = %s AND numero_cadeira = %s;"      
            cursor.execute(query, (letra, numero))

        # 2. Prepara e insere o histórico
        assentos_str = ", ".join(assentos_selecionados) 
        texto_historico = f"Reserva na Sala {numero_sala} - Assentos: {assentos_str}"
        query2 = "INSERT INTO historico (movimentacao) VALUES (%s);"
        cursor.execute(query2, (texto_historico,))
        
        # 3. Confirma a transação
        conn.commit()
        print(f"Reserva concluída na Sala {numero_sala}: {assentos_str}")
        
        # 4. Limpa a seleção e atualiza a interface
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

        # 1. Atualiza todos os assentos selecionados no banco
        for assento in assentos_selecionados:
            letra = assento[0]
            numero = assento[1:]
            query = f"UPDATE {tabela} SET ocupado = false WHERE fila = %s AND numero_cadeira = %s;"      
            cursor.execute(query, (letra, numero))

        # 2. Prepara e insere o histórico
        assentos_str = ", ".join(assentos_selecionados) 
        texto_historico = f"Cancelamento na Sala {numero_sala} - Assentos: {assentos_str}"
        query2 = "INSERT INTO historico (movimentacao) VALUES (%s);"
        cursor.execute(query2, (texto_historico,))
        
        # 3. Confirma a transação
        conn.commit()
        print(f"Reserva concluída na Sala {numero_sala}: {assentos_str}")
        
        # 4. Limpa a seleção e atualiza a interface
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
# COMPONENTES REUTILIZÁVEIS DA UI
# ============================================================
def limpar_tela_principal():
    global assentos_selecionados
    assentos_selecionados.clear()
    for widget in main_frame.winfo_children():
        widget.destroy()


def criar_card_filme(container, nome, duracao, sala, caminho_img, coluna):
    frame_card = ctk.CTkFrame(container, fg_color="transparent")
    frame_card.grid(row=0, column=coluna, padx=40)

    try:
        img = Image.open(caminho_img)
    except FileNotFoundError:
        img = Image.new("RGB", (200, 300), color="#2b2b36")

    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 300))

    btn_img = ctk.CTkButton(
        frame_card,
        text="",
        image=ctk_img,
        width=200,
        height=300,
        fg_color="transparent",
        hover_color="#3a3a48",
        command=lambda: mostrar_tela_sala(sala)
    )
    btn_img.pack()

    ctk.CTkLabel(frame_card, text=nome, font=("Arial", 18, "bold")).pack(pady=(15, 5))
    ctk.CTkLabel(frame_card, text=f"Duração: {duracao}", font=("Arial", 15)).pack()
    ctk.CTkLabel(frame_card, text=f"SALA: {sala}", font=("Arial", 15, "bold"), text_color="#3498db").pack()


# ============================================================
# TELAS DO SISTEMA
# ============================================================
def mostrar_tela_inicial():
    limpar_tela_principal()

    boas_vindas = ctk.CTkLabel(
        main_frame,
        text="Bem-vindo ao CineSenai",
        font=("Arial", 42, "bold"),
        text_color="#4CAF50"
    )
    boas_vindas.pack(pady=(150, 20))

    subtitulo = ctk.CTkLabel(
        main_frame,
        text="Sistema de Gestão de Reservas e Bilheteira",
        font=("Arial", 22)
    )
    subtitulo.pack(pady=10)


def ver_calendario():
    limpar_tela_principal()

    titulo = ctk.CTkLabel(
        main_frame,
        text="Programação da Semana",
        font=("Arial", 32, "bold"),
        text_color="#3498db"
    )
    titulo.pack(pady=30)

    dias = [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo"
    ]

    for dia in dias:
        filme = filmes_dias[dia]

        card = ctk.CTkFrame(
            main_frame,
            width=700,
            height=70,
            fg_color="#2b2b36",
            corner_radius=10
        )
        card.pack(pady=7, padx=100)
        card.pack_propagate(False)

        lbl_dia = ctk.CTkLabel(
            card,
            text=dia,
            font=("Arial", 18, "bold"),
            width=220
        )
        lbl_dia.pack(side="left", padx=20)

        lbl_filme = ctk.CTkLabel(
            card,
            text=filme,
            font=("Arial", 18)
        )
        lbl_filme.pack(side="left", padx=20)


def ver_filmes():
    limpar_tela_principal()

    titulo = ctk.CTkLabel(main_frame, text="Filmes em Cartaz", font=("Arial", 32, "bold"))
    titulo.pack(pady=40)

    container_filmes = ctk.CTkFrame(main_frame, fg_color="transparent")
    container_filmes.pack(pady=20)

    criar_card_filme(container_filmes, "A Odisseia", "2H52M", 1, BASE_DIR / "odisseia.png", 0)
    criar_card_filme(container_filmes, "Homem Aranha 3", "2H19M", 2, BASE_DIR / "homemaranha3.png", 1)
    criar_card_filme(container_filmes, "Barbie em Vida de Sereia", "1H15M", 3, BASE_DIR / "barbie.png", 2)


def mostrar_tela_sala(numero_sala):
    limpar_tela_principal()

    titulo = ctk.CTkLabel(main_frame, text=f"SALA {numero_sala}", font=("Arial", 28, "bold"))
    titulo.pack(pady=20)

    grade_frame = ctk.CTkFrame(main_frame)
    grade_frame.pack(pady=10)

    status_no_banco = buscar_estado_sala(numero_sala)

    filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K']
    colunas = list(range(1, 21))

    for r_idx, fila in enumerate(filas):
        for c_idx, coluna in enumerate(colunas):
            nome_assento = f"{fila}{coluna}"
            esta_ocupado = status_no_banco.get(nome_assento, False)

            if esta_ocupado:
                cor_fundo = "#f44336"
                cor_texto = "white"
                estado_botao = "normal"
            else:
                cor_fundo = "#ffffff"
                cor_texto = "black"
                estado_botao = "normal"

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
            
            btn.grid(row=r_idx, column=c_idx, padx=5, pady=5)

    frame_acoes = ctk.CTkFrame(main_frame, fg_color="transparent")
    frame_acoes.pack(pady=20)

    btn_reservar = ctk.CTkButton(
        frame_acoes,
        text='Confirmar Reserva',
        height=45,
        font=("Arial", 15, "bold"),
        fg_color="#0d761f",
        hover_color="#095415",
        text_color="white",
        command=lambda: confirmar_reserva(numero_sala)
    )
    btn_reservar.pack(side="left", padx=10)

    btn_cancelar = ctk.CTkButton(
        frame_acoes,
        text='Cancelar Reserva',
        height=45,
        font=("Arial", 15, "bold"),
        fg_color="#c92a2a",
        hover_color="#911f1f",
        text_color="white",
        command=lambda: cancelar_reserva(numero_sala)
    )
    btn_cancelar.pack(side="left", padx=10)


def ver_historico():
    limpar_tela_principal()
    
    titulo = ctk.CTkLabel(
        main_frame, 
        text="Histórico de Movimentações", 
        font=("Arial", 28, "bold"),
        text_color="#3498db"
    )
    titulo.pack(pady=(20, 10))

    area_scroll = ctk.CTkScrollableFrame(
        main_frame, 
        width=800, 
        height=600, 
        fg_color="transparent"
    )
    area_scroll.pack(fill="both", expand=True, padx=40, pady=20)

    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT movimentacao FROM historico ORDER BY id DESC;"
        cursor.execute(query)

        resultado = cursor.fetchall()
        
        if not resultado:
            aviso = ctk.CTkLabel(area_scroll, text="Nenhum histórico encontrado.", font=("Arial", 16, "italic"))
            aviso.pack(pady=20)

        for linha in resultado:
            texto_movimentacao = linha[0]

            card = ctk.CTkFrame(
                area_scroll, 
                fg_color="#2b2b36", 
                corner_radius=8
            )
            card.pack(fill="x", padx=10, pady=5)

            lbl_texto = ctk.CTkLabel(
                card, 
                text=texto_movimentacao, 
                font=("Arial", 15), 
                anchor="w",
                justify="left"
            )
            lbl_texto.pack(fill="x", padx=15, pady=15)

    except Exception as error:
        erro_lbl = ctk.CTkLabel(area_scroll, text=f"Erro ao carregar histórico: {error}", text_color="#f44336")
        erro_lbl.pack(pady=20)
        
    finally:
        if conn:
            cursor.close()
            conn.close()


# ============================================================
# BOTÕES DO MENU LATERAL
# ============================================================
titulo_menu = ctk.CTkLabel(menu_lateral, text="CineSenai", font=("Arial", 28, "bold"))
titulo_menu.pack(pady=(30, 40))

def criar_botao_menu(texto, comando):
    btn = ctk.CTkButton(
        menu_lateral, 
        text=texto, 
        command=comando,
        fg_color="transparent",
        hover_color="#2b2b36",
        text_color="white",
        font=("Arial", 16),
        anchor="w",
        height=45
    )
    btn.pack(fill="x", padx=15, pady=5)
    return btn

btn_inicio = criar_botao_menu("Início", mostrar_tela_inicial)
btn_filmes = criar_botao_menu("Filmes em Cartaz", ver_filmes)
btn_sala1 = criar_botao_menu("Ver Sala 1", lambda: mostrar_tela_sala(1))
btn_sala2 = criar_botao_menu("Ver Sala 2", lambda: mostrar_tela_sala(2))
btn_sala3 = criar_botao_menu("Ver Sala 3", lambda: mostrar_tela_sala(3))
btn_calendario = criar_botao_menu("Calendário", ver_calendario)
btn_historico = criar_botao_menu("Histórico", lambda: ver_historico())

botao_sair = ctk.CTkButton(
    menu_lateral, 
    text="Sair", 
    fg_color="#c92a2a", 
    hover_color="#911f1f", 
    command=app.destroy,
    font=("Arial", 15, "bold"),
    height=45
)
botao_sair.pack(fill="x", padx=20, pady=30, side="bottom")

# ============================================================
# EXECUÇÃO DO APLICATIVO
# ============================================================
mostrar_tela_inicial()
app.mainloop()