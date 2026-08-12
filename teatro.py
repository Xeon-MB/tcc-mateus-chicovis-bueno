import customtkinter as ctk


fila0 = [0,0,0,0,0,0,0,0,0,0]
fila1 = [0,0,0,0,0,0,0,0,0,0]
fila2 = [0,0,0,0,0,0,0,0,0,0]
fila3 = [0,0,0,0,0,0,0,0,0,0]
fila4 = [0,0,0,0,0,0,0,0,0,0]
fila5 = [0,0,0,0,0,0,0,0,0,0]
fila6 = [0,0,0,0,0,0,0,0,0,0]
fila7 = [0,0,0,0,0,0,0,0,0,0]
fila8 = [0,0,0,0,0,0,0,0,0,0]
fila9 = [0,0,0,0,0,0,0,0,0,0]

teatro = [fila0, fila1, fila2, fila3, fila4, fila5, fila6, fila7, fila8, fila9]

def mostrar_teatro():
        texto_mapa = "         -------------------\n"
        texto_mapa += "                PALCO       \n\n"
        for x in range(len(teatro)):
            assentos_str = " ".join(str(num) for num in teatro[x])
            texto_mapa += f"FILA {x} - {assentos_str}\n"
        caixa_texto.delete("1.0", "end")
        caixa_texto.insert("1.0", texto_mapa)
def mostrar_notificacao(texto,cor, duracao=2000):
    aviso = ctk.CTkLabel(app, text=texto, fg_color=cor, corner_radius=8)
    aviso.place(relx=0.5, rely=0.05, anchor="n")  

    app.after(duracao, aviso.destroy)

def fechar_caixas():
    if "fila" in globals() and fila.winfo_exists():
        fila.destroy()
    if "assento" in globals() and assento.winfo_exists():
        assento.destroy()


def abrir_reserva():
    fechar_caixas()
    mostrar_teatro()
    global fila
    global assento
    fila = ctk.CTkEntry(app, placeholder_text="Digite sua Fila")
    assento = ctk.CTkEntry(app, placeholder_text="Digite seu assento")
    fila.pack(pady=10)
    assento.pack(pady=10)
    fila.bind("<Return>", salvar_teatro)
    assento.bind("<Return>", salvar_teatro)

def abrir_cancela():
    fechar_caixas()
    mostrar_teatro()
    global fila
    global assento
    fila = ctk.CTkEntry(app, placeholder_text="Digite sua Fila(0-9)")
    assento = ctk.CTkEntry(app, placeholder_text="Digite seu assento(0-9)")
    fila.pack(pady=10)
    assento.pack(pady=10)
    fila.bind("<Return>", cancelar_reserva)
    assento.bind("<Return>", cancelar_reserva)


def salvar_teatro(event):
    fila_num = int(fila.get())
    assento_num = int(assento.get())
    if teatro[fila_num][assento_num] == 1:
        mostrar_notificacao(f"Lugar na fila {fila_num} e no assento {assento_num} já está reservado, escolha outro lugar!", "red")
    else: 
        teatro[fila_num][assento_num] = 1
        mostrar_notificacao(f"Lugar na fila {fila_num} e no assento {assento_num} reservado.", "green")
        mostrar_teatro()
        fila.destroy()
        assento.destroy()

def cancelar_reserva(event):
    fila_num = int(fila.get())
    assento_num = int(assento.get())
    if teatro[fila_num][assento_num] == 0:
        mostrar_notificacao(f"Lugar na fila {fila_num} e no assento {assento_num} não estava reservado!", "red")
    else: 
        teatro[fila_num][assento_num] = 0
        mostrar_notificacao(f"Lugar na fila {fila_num} e no assento {assento_num} cancelado.", "green")
        mostrar_teatro()
        fila.destroy()
        assento.destroy()
    
app = ctk.CTk()
app.title("Gerenciador de teatro")
app.geometry("500x300")


label = ctk.CTkLabel(app, text="Gerenciador de Teatro", text_color="white")
label.pack(pady=10)

button1 = ctk.CTkButton(app, text="Mostrar Teatro", command=mostrar_teatro)
button1.pack(pady=10)

button2 = ctk.CTkButton(app, text="Reservar", command=abrir_reserva)
button2.pack(pady=10)

button3 = ctk.CTkButton(app, text="Cancelar", command=abrir_cancela)
button3.pack(pady=10)

button4 = ctk.CTkButton(app, text="Sair", fg_color="red", command=app.destroy)
button4.pack(pady=10)

caixa_texto = ctk.CTkTextbox(
    app, width=500, height=260, font=("Courier New", 14)
)
caixa_texto.pack(pady=10)


app.mainloop()
