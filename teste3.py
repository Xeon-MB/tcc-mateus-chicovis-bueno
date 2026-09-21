import tkinter as tk
from tkinter import messagebox #AQUI ESTOU IMPORTANDO A FUNÇÃO DE APRESENTAR UMA MENSAGEM DE SUCESSO NA TELA
import psycopg2

# Configurações de conexão com o banco de dados
DB_CONFIG = {
    "dbname": "wow",
    "user": "postgres",
    "password": "root",
    "host": "localhost",
    "port": "5432"
}

# Variável para armazenar temporariamente as escolhas do usuário na sessão atual
nome = []

def buscar_assentos_ocupados():
    #Busca no banco de dados e retorna um dicionário mapeando 'FilaCadeira' -> status_ocupado
    status_assentos = {}
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Seleciona a fila, o número e o status de ocupação
        cursor.execute("SELECT fila, numero_cadeira, ocupado FROM assentos;")
        linhas = cursor.fetchall()

        # Transforma o resultado em uma lista como por ex: {"A1": False, "A2": True}
        for fila, numero, ocupado in linhas:
            chave = f"{fila}{numero}"
            status_assentos[chave] = ocupado

    except Exception as error:
        print(f"Erro ao consultar o banco de dados: {error}")
        # Caso falhe a conexão, criamos um dicionário vazio para não quebrar o app
    finally:
        cursor.close()
        conn.close()
        return status_assentos

def alternar_assento(btn):
    global nome
    if btn['bg'] == "#ffffff":
        btn.config(bg="#4CAF50", fg="white")
        nome.append(btn['text'])
    else:
        btn.config(bg="#ffffff", fg="black")
        nome.remove(btn['text'])

def reservar(a):
    # Exibe a caixa de mensagem de sucesso na tela
    messagebox.showinfo(
        "Reserva Concluída",
        f"Os seguintes assentos foram reservados com sucesso:\n{nome}"
    )

# Configuração da janela principal
root = tk.Tk()
root.title("Sistema de Reserva - Cinema")
root.geometry("350x550")
root.config(bg="#595757")

# 1. FAZ A CONSULTA NO BANCO DE DADOS ANTES DE CRIAR A INTERFACE
assentos_no_banco = buscar_assentos_ocupados()

# Indicador da Tela do Cinema
lbl_tela = tk.Label(root, text="TELA DO CINEMA", bg="#111111", fg="#ffffff", font=("Arial", 11, "bold"), pady=5)
lbl_tela.grid(row=0, column=0, columnspan=5, sticky="we", padx=10, pady=10)

filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
colunas = [1, 2, 3, 4, 5]

# Criação da grade
for r_idx in range(len(filas)):
    fila = filas[r_idx]
    for c_idx in range(len(colunas)):
        coluna = colunas[c_idx]
        nome_assento = f"{fila}{coluna}"

        # 2. VERIFICA SE O ASSENTO CONSTATADO ESTÁ OCUPADO NO DICIONÁRIO
        # .get(nome_assento) busca a string do nome do assento na variável que fizemos a consulta no banco e pega o valor do seu estado
        esta_ocupado = assentos_no_banco.get(nome_assento)

        if esta_ocupado:      #Aqui se o resultado for TRUE, executa esse IF. Será true com o assento marcado como ocupado
            # Configuração disabled para assento já ocupado (Vermelho e Inativo)
            cor_fundo = "#f44336"
            cor_texto = "#ffffff"
            estado_botao = "disabled"
        else:
            # Configuração normal para assento livre
            cor_fundo = "#ffffff"
            cor_texto = "black"
            estado_botao = "normal"

        # Criação do botão aplicando as propriedades dinâmicas
        btn = tk.Button(
            root,
            text=nome_assento,
            width=5,
            height=2,
            font=("Arial", 9, "bold"),
            bg=cor_fundo,
            fg=cor_texto,
            disabledforeground="white",    #Essa propriedade é caso o botão esteja desabilitado, qual a cor da fonte.
            state=estado_botao # Controla se o botão pode ser clicado ou não
        )

        # Só adiciona o comando de clique se o assento não estiver inativo
        if estado_botao == "normal":
            btn.config(command=lambda b=btn: alternar_assento(b))
            
        # Posiciona na grade
        btn.grid(row=r_idx + 1, column=c_idx, padx=4, pady=4)

# Botão de confirmação de reserva
btn_reservar = tk.Button(root,
                         text='Reservar',
                         height=2,
                         font=("Arial", 9, "bold"),
                         bg="#0d761f",
                         fg="black",
                         command=lambda: reservar(nome))

btn_reservar.grid(row=9, column=0, columnspan=5, sticky="ew", padx=4, pady=4)

# Inicializa a aplicação
root.mainloop()