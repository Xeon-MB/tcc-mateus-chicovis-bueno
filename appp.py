import customtkinter as ctk

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
        

app = ctk.CTk()
app.title("Gerenciador de Teatro")
app.geometry("700x400")

titulo = ctk.CTkLabel(app, text="Gerenciador de Teatro", font=("Arial", 24, "bold"))
titulo.pack(padx=0, pady=30)

barra_lateral = ctk.CTkFrame(app, width=180)
barra_lateral.pack(side="left", fill = "y")

titulo_barra = ctk.CTkLabel(barra_lateral,text="MENU",font=("Arial", 20, "bold"))
titulo_barra.pack(pady=(30, 20))

botao_filmes = ctk.CTkButton(barra_lateral, text="Filmes", fg_color="transparent", font=("Arial", 15))
botao_filmes.pack()

botao_salas = ctk.CTkButton(barra_lateral, text="Ver Salas", fg_color="transparent", font=("Arial", 15))
botao_salas.pack()

botao_sair = ctk.CTkButton(barra_lateral, text="Sair", fg_color="transparent", font=("Arial", 15), command = fechar)
botao_sair.pack()


app.mainloop()