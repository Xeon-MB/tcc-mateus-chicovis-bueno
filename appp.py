import customtkinter as ctk
from PIL import Image

# ==========================================
# VARIÁVEIS GLOBAIS E INICIALIZAÇÃO DE DADOS
# ==========================================

# Estrutura da Sala 1
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

# Estrutura da Sala 2
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

# Dados do Sistema
global valor_total
valor_total = 0
historico = []

# Variáveis de Interface
sala_definida1 = None
sala_definida2 = None


# ==========================================
# FUNÇÕES DE INTERFACE E UTILIDADES
# ==========================================

def tirar_menu():
    if "menu" in globals() and menu.winfo_exists():
        menu.destroy()


# ==========================================
# FUNÇÕES DE EXIBIÇÃO DE SALAS
# ==========================================

def mostrar_sala1():
    global sala_definida1
    if sala_definida1 is not None and sala_definida1.winfo_exists():
        sala_definida1.destroy()

    sala_definida1 = ctk.CTkFrame(menu, fg_color="transparent")
    sala_definida1.grid(row=1, column=0, padx=10)

    for fila in range(10):
        for lugar in range(20):
            if sala1[fila][lugar] == 0:
                cor = "green"
            elif sala1[fila][lugar] == 1:
                cor = "red"
            else:
                cor = "yellow"

            botao = ctk.CTkButton(sala_definida1, text=str(lugar + 1), width=20, height=10, fg_color=cor)
            botao.grid(row=fila, column=lugar, padx=5, pady=5)


def mostrar_sala2():
    global sala_definida2
    if sala_definida2 is not None and sala_definida2.winfo_exists():
        sala_definida2.destroy()

    sala_definida2 = ctk.CTkFrame(menu, fg_color="transparent")
    sala_definida2.grid(row=1, column=1, padx=10)

    for fila in range(10):
        for lugar in range(20):
            if sala2[fila][lugar] == 0:
                cor = "green"
            elif sala2[fila][lugar] == 1:
                cor = "red"
            else:
                cor = "yellow"

            botao = ctk.CTkButton(sala_definida2, text=str(lugar + 1), width=20, height=10, fg_color=cor)
            botao.grid(row=fila, column=lugar, padx=5, pady=5)


def menu_salas():
    global menu
    tirar_menu()

    menu = ctk.CTkFrame(app, width=1900, fg_color="transparent")
    menu.pack(side="left", fill="y")

    titulo = ctk.CTkLabel(menu, text="sala 1")
    titulo.grid(row=0, column=0)

    mostrar_sala1()

    titulo = ctk.CTkLabel(menu, text="sala 2")
    titulo.grid(row=0, column=1)

    mostrar_sala2()


# ==========================================
# FUNÇÕES DE RESERVA
# ==========================================

def fazer_reserva(sala, fila, lugar, botao):
    global menu
    global valor
    global preco
    global preco_bilhete
    global valor_total

    if "preco" in globals() and preco.winfo_exists():
        preco.destroy()

    preco_bilhete = 25.00
    valor = valor + 25
    valor_total = valor_total + 25
    sala[fila][lugar] = 1

    botao.configure(fg_color="red")

    preco = ctk.CTkLabel(menu, text=f"Total: R${valor:.2f}")
    preco.grid(column=5, columnspan=10)

    r = f"Reserva de {preco_bilhete:.2f} feita!"
    historico.append(r)


def reserva(sala):
    global menu
    global valor
    valor = 0

    tirar_menu()

    menu = ctk.CTkFrame(app)
    menu.pack()

    titulo = ctk.CTkLabel(menu, text=f"Sala")
    titulo.grid(row=0, column=11)

    for fila in range(10):
        for lugar in range(20):
            if sala[fila][lugar] == 0:
                cor = "green"
            elif sala[fila][lugar] == 1:
                cor = "red"
            else:
                cor = "yellow"

            botao = ctk.CTkButton(menu, text=str(lugar + 1), width=20, height=10, fg_color=cor)
            botao.configure(command=lambda s=sala, f=fila, l=lugar, b=botao: fazer_reserva(s, f, l, b))
            botao.grid(row=(fila+1), column=(lugar+1), padx=5, pady=5)

    feito = ctk.CTkButton(menu, text="Reserva Feita!", command=mostrar_filmes)
    feito.grid(column=6, columnspan=10)


# ==========================================
# FUNÇÕES DE SAÍDA E NAVEGAÇÃO
# ==========================================

def fechar():
    janela = ctk.CTkToplevel(app)
    janela.title("Sair?")
    janela.geometry("320x150")

    aviso = ctk.CTkLabel(janela, text="Quar realmente sair?")
    aviso.pack(padx=0, pady=30)

    sim = ctk.CTkButton(janela, text="Sair", fg_color="red", text_color="white", command=app.destroy)
    sim.pack(side="left", anchor="n", padx=10)

    nao = ctk.CTkButton(janela, text="Continuar", fg_color="Green", text_color="white", command=janela.destroy)
    nao.pack(side="left", anchor="n", padx=10)


def mostrar_filmes():
    global menu
    global sala_filme

    tirar_menu()

    menu = ctk.CTkFrame(app, width=1900, fg_color="transparent")
    menu.pack(side="left", fill="y")

    image1 = ctk.CTkImage(light_image=Image.open("odisseia.png"), dark_image=Image.open("odisseia.png"), size=(200, 300))
    image2 = ctk.CTkImage(light_image=Image.open("homemaranha3.png"), dark_image=Image.open("homemaranha3.png"), size=(200, 300))
    image3 = ctk.CTkImage(light_image=Image.open("barbie.png"), dark_image=Image.open("barbie.png"), size=(200, 300))

    sala_filme = sala1
    filme1 = ctk.CTkButton(menu, text="", image=image1, width=200, height=300, fg_color="transparent", command=lambda s=sala_filme: reserva(s))
    filme1.grid(row=0, column=0, padx=10)

    nome_filme1 = ctk.CTkLabel(menu, text="A Odisseia", font=("Arial", 15, "bold"))
    nome_filme1.grid(row=1, column=0, padx=10)

    duracao_filme1 = ctk.CTkLabel(menu, text="Duração: 2H52M", font=("Arial", 15))
    duracao_filme1.grid(row=2, column=0, padx=10)

    sala_filme1 = ctk.CTkLabel(menu, text="SALA: 1", font=("Arial", 15))
    sala_filme1.grid(row=3, column=0, padx=10)

    sala_filme = sala2
    filme2 = ctk.CTkButton(menu, text="", image=image2, width=200, height=300, fg_color="transparent", command=lambda s=sala_filme: reserva(s))
    filme2.grid(row=0, column=1, padx=10)

    nome_filme2 = ctk.CTkLabel(menu, text="Homem Aranha 3", font=("Arial", 15, "bold"))
    nome_filme2.grid(row=1, column=1, padx=10)

    duracao_filme2 = ctk.CTkLabel(menu, text="Duração: 2H19M", font=("Arial", 15))
    duracao_filme2.grid(row=2, column=1, padx=10)

    sala_filme2 = ctk.CTkLabel(menu, text="SALA: 2", font=("Arial", 15))
    sala_filme2.grid(row=3, column=1, padx=10)


def menu_calendario():
    global menu
    tirar_menu()

    calendar = ctk.CTkFrame(app)
    calendar.pack()

    label = ctk.CTkLabel(calendar, text="Semana Atual")
    label.grid(row=0, column=3)

    for i in range(7):
        button = ctk.CTkButton(calendar, text=f"Dia: {i+1}", width=20, height=10)
        button.grid(row=1, column=i, padx=10)


# ==========================================
# FUNÇÕES DE CANCELAMENTO
# ==========================================

def fazer_cancela(sala, fila, lugar, botao):
    global menu
    global valor
    global preco
    global valor_total

    if "preco" in globals() and preco.winfo_exists():
        preco.destroy()

    valor = 0
    valor = valor + 25
    valor_total = valor_total - 25
    sala[fila][lugar] = 0

    botao.configure(fg_color="green")

    preco = ctk.CTkLabel(menu, text=f"Total: R${valor:.2f}")
    preco.grid(column=5, columnspan=10)

    r = f"Cancelamento de {preco_bilhete} feito!"
    historico.append(r)


def selecionado(option):
    global menu

    if option == "Sala 1":
        sala = sala1
    elif option == "Sala 2":
        sala = sala2

    for fila in range(10):
        for lugar in range(20):
            if sala[fila][lugar] == 0:
                cor = "green"
            elif sala[fila][lugar] == 1:
                cor = "red"
            else:
                cor = "yellow"

            botao = ctk.CTkButton(menu, text=str(lugar + 1), width=20, height=10, fg_color=cor)
            botao.configure(command=lambda s=sala, f=fila, l=lugar, b=botao: fazer_cancela(s, f, l, b))
            botao.grid(row=(fila+1), column=(lugar+1), padx=5, pady=5)


def menu_cancelar():
    global menu
    tirar_menu()

    menu = ctk.CTkFrame(app, width=1900)
    menu.pack()

    t_cancela = ctk.CTkLabel(menu, text="Qual sala você quer botao_cancelar?")
    t_cancela.grid(row=1, column=0)

    option = ctk.CTkOptionMenu(menu, values=["Sala 1", "Sala 2"], command=selecionado)
    option.grid(row=2, column=0, pady=10)

    feito = ctk.CTkButton(menu, text="Cancela Feita", command=menu_cancelar)
    feito.grid(row=3, column=0, pady=10)


# ==========================================
# FUNÇÕES DE HISTÓRICO
# ==========================================

def menu_historico():
    global menu
    global valor_total

    tirar_menu()

    menu = ctk.CTkFrame(app, width=1900)
    menu.pack()

    for x in range(len(historico)):
        h = ctk.CTkLabel(menu, text=historico[x])
        h.grid(row=x, column=0)

    i = ctk.CTkLabel(menu, text=f"Valor Total: R${valor_total:.2f}")
    i.grid(column=0)


# ==========================================
# APLICAÇÃO PRINCIPAL (GUI)
# ==========================================

app = ctk.CTk()
app.title("Gerenciador de Teatro")
app.attributes('-fullscreen', True)

titulo = ctk.CTkLabel(app, text="Gerenciador de Teatro", font=("Arial", 24, "bold"))
titulo.pack(padx=0, pady=30)

barra_lateral = ctk.CTkFrame(app, width=180)
barra_lateral.pack(side="left", fill="y")

titulo_barra = ctk.CTkLabel(barra_lateral, text="MENU", font=("Arial", 20, "bold"))
titulo_barra.pack(pady=(30, 20))

botao_filmes = ctk.CTkButton(barra_lateral, text="Fazer Reservas", fg_color="transparent", font=("Arial", 15), command=mostrar_filmes)
botao_filmes.pack()

botao_cancelar = ctk.CTkButton(barra_lateral, text="Cancelar Reserva", fg_color="transparent", font=("Arial", 15), command=menu_cancelar)
botao_cancelar.pack()

botao_salas = ctk.CTkButton(barra_lateral, text="Ver Salas", fg_color="transparent", font=("Arial", 15), command=menu_salas)
botao_salas.pack()

botao_calendario = ctk.CTkButton(barra_lateral, text="Calendário", fg_color="transparent", font=("Arial", 15), command=menu_calendario)
botao_calendario.pack()

botao_historico = ctk.CTkButton(barra_lateral, text="Histórico", fg_color="transparent", font=("Arial", 15), command=menu_historico)
botao_historico.pack()

botao_sair = ctk.CTkButton(barra_lateral, text="Sair", fg_color="transparent", font=("Arial", 15), command=fechar)
botao_sair.pack()

app.mainloop()