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
def mostrar_notificacao(texto, duracao=2000):
    aviso = ctk.CTkLabel(app, text=texto, fg_color="green", corner_radius=8)
    aviso.place(relx=0.5, rely=0.05, anchor="n")  # aparece no topo, centralizado

    app.after(duracao, aviso.destroy)
def reserva():
    mostrar_teatro()
    fila = ctk.CTkEntry(app, placeholder_text="Digite sua Fila")
    assento = ctk.CTkEntry(app, placeholder_text="Digite seu assento")
    fila.pack(pady=10)
    assento.pack(pady=10)
    fila = fila.get()
    assento = assento.get()
    teatro[fila][assento] = 1
    mostrar_notificacao(f"Lugar na fila {fila} e no assento {assento} reservado!")
app = ctk.CTk()
app.title("Gerenciador de teatro")
app.geometry("300x200")


label = ctk.CTkLabel(app, text="Gerenciador de Teatro", text_color="black")
label.pack(pady=10)

button1 = ctk.CTkButton(app, text="Mostrar Teatro", command=mostrar_teatro)
button1.pack(pady=10)

button2 = ctk.CTkButton(app, text="Reservar", command=reserva)
button2.pack(pady=10)

caixa_texto = ctk.CTkTextbox(
    app, width=500, height=260, font=("Courier New", 14)
)
caixa_texto.pack(pady=10)


app.mainloop()
