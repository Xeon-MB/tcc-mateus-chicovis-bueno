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
        texto_mapa = "         -------------------"
        texto_mapa += "                PALCO       "
        for x in range(len(teatro)):
            assentos_str = " ".join(str(num) for num in teatro[x])
            texto_mapa += f"FILA {x} - {assentos_str}\n"
        caixa_texto.delete("1.0", "end")
        caixa_texto.insert("1.0", texto_mapa)
app = ctk.CTk()
app.title("asaaaa")
app.geometry("300x200")


label = ctk.CTkLabel(app, text="Gerenciador de Teatro", text_color="black")
label.pack(pady=20)

button1 = ctk.CTkButton(app, text="Mostrar Teatro", command=mostrar_teatro)
button1.pack(pady=30)

caixa_texto = ctk.CTkTextbox(
    app, width=500, height=260, font=("Courier New", 14)
)
caixa_texto.pack(pady=15)

app.mainloop()
