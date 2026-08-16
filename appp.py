import customtkinter as ctk
from PIL import Image

fila0 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
fila1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
fila2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
fila3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
fila4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
fila5 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
fila6 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
fila7 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
fila8 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
fila9 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

sala1 = [fila0, fila1, fila2, fila3, fila4, fila5, fila6, fila7, fila8, fila9]
sala2 = [fila0, fila1, fila2, fila3, fila4, fila5, fila6, fila7, fila8, fila9]
sala3 = [fila0, fila1, fila2, fila3, fila4, fila5, fila6, fila7, fila8, fila9]

def tirar_menu():
    if "menu" in globals() and menu.winfo_exists():
        menu.destroy()

def mostrar_salas():
    global menu
    tirar_menu()
    menu = ctk.CTkFrame(app, width=1900, fg_color="transparent")
    menu.pack(side="left", fill="y")
    
    titulo = ctk.CTkLabel(menu, text="sala 1")
    titulo.pack()
    
    assentos = ctk.CTkFrame(menu, fg_color="transparent")
    assentos.pack()

    for fila in range(10):
        for lugar in range(20):

            if sala1[fila][lugar] == 0:
                cor = "green"
            elif sala1[fila][lugar] == 1:
                cor = "red"
            else:
                cor = "yellow"

            botao = ctk.CTkButton(assentos,text=str(lugar + 1),width=50,height=40,fg_color=cor)
            botao.grid(row=fila,column=lugar,padx=5,pady=5)

def fechar():
    janela = ctk.CTkToplevel(app)
    janela.title("Sair?")
    janela.geometry("320x150")
    
    aviso = ctk.CTkLabel(janela, text="Quar realmente sair?")
    aviso.pack(padx=0, pady = 30)
    
    
    sim = ctk.CTkButton(janela, text="Sair", fg_color="red", text_color="white", command=app.destroy)
    sim.pack(side = "left", anchor = "n",padx = 10)
    
    
    nao = ctk.CTkButton(janela, text="Continuar", fg_color="Green", text_color="white", command=janela.destroy)
    nao.pack(side = "left", anchor = "n", padx = 10)
    
def mostrar_filmes():
    global menu
    tirar_menu()
    menu = ctk.CTkFrame(app, width=1900, fg_color="transparent")
    menu.pack(side="left", fill="y")
    
    image1 = ctk.CTkImage(light_image=Image.open("odisseia.png"), dark_image=Image.open("odisseia.png"), size=(200,300))
    image2 = ctk.CTkImage(light_image=Image.open("homemaranha3.png"), dark_image=Image.open("homemaranha3.png"), size=(200,300))
    image3 = ctk.CTkImage(light_image=Image.open("barbie.png"), dark_image=Image.open("barbie.png"), size=(200,300))
    
    filme1 = ctk.CTkButton(menu, text="",image = image1, width=200, height=300, fg_color="transparent")
    filme1.grid(row=0, column = 0, padx=10)
    nome_filme1 = ctk.CTkLabel(menu, text="A Odisseia", font=("Arial", 15, "bold"))
    nome_filme1.grid(row=1, column = 0, padx=10)
    duracao_filme1 = ctk.CTkLabel(menu, text="Duração: 2H52M", font=("Arial", 15))
    duracao_filme1.grid(row=2, column = 0, padx=10)
    sala_filme1 = ctk.CTkLabel(menu, text="SALA: 1", font=("Arial", 15))
    sala_filme1.grid(row=3, column = 0, padx=10)
    
    filme2 = ctk.CTkButton(menu, text="",image = image2, width=200, height=300, fg_color="transparent")
    filme2.grid(row=0, column = 1, padx=10)
    nome_filme2 = ctk.CTkLabel(menu, text="Homem Aranha 3", font=("Arial", 15, "bold"))
    nome_filme2.grid(row=1, column = 1, padx=10)
    duracao_filme2 = ctk.CTkLabel(menu, text="Duração: 2H19M", font=("Arial", 15))
    duracao_filme2.grid(row=2, column = 1, padx=10)
    sala_filme2 = ctk.CTkLabel(menu, text="SALA: 2", font=("Arial", 15))
    sala_filme2.grid(row=3, column = 1, padx=10)
    
    filme3 = ctk.CTkButton(menu, text="",image = image3, width=200, height=300, fg_color="transparent")
    filme3.grid(row=0, column = 2, padx=10)
    nome_filme3 = ctk.CTkLabel(menu, text="Barbie", font=("Arial", 15, "bold"))
    nome_filme3.grid(row=1, column = 2, padx=10)
    duracao_filme3 = ctk.CTkLabel(menu, text="Duração: 1H54M", font=("Arial", 15))
    duracao_filme3.grid(row=2, column = 2, padx=10)
    sala_filme3 = ctk.CTkLabel(menu, text="SALA: 3", font=("Arial", 15))
    sala_filme3.grid(row=3, column = 2, padx=10)
        

app = ctk.CTk()
app.title("Gerenciador de Teatro")
app.geometry("700x400")

titulo = ctk.CTkLabel(app, text="Gerenciador de Teatro", font=("Arial", 24, "bold"))
titulo.pack(padx=0, pady=30)

barra_lateral = ctk.CTkFrame(app, width=180)
barra_lateral.pack(side="left", fill = "y")

titulo_barra = ctk.CTkLabel(barra_lateral,text="MENU",font=("Arial", 20, "bold"))
titulo_barra.pack(pady=(30, 20))

botao_filmes = ctk.CTkButton(barra_lateral, text="Filmes", fg_color="transparent", font=("Arial", 15), command=mostrar_filmes)
botao_filmes.pack()

botao_salas = ctk.CTkButton(barra_lateral, text="Ver Salas", fg_color="transparent", font=("Arial", 15), command=mostrar_salas)
botao_salas.pack()

calendario = ctk.CTkButton(barra_lateral, text="Sala", fg_color="transparent", font=("Arial", 15))
calendario.pack()

botao_sair = ctk.CTkButton(barra_lateral, text="Sair", fg_color="transparent", font=("Arial", 15), command = fechar)
botao_sair.pack()


app.mainloop()