import customtkinter as ctk

app = ctk.CTk()
app.geometry("500x400")

def mostrar_notificacao():
    # Faz o texto aparecer flutuando no topo
    aviso_rapido.place(relx=0.5, rely=0.1, anchor="center")
    
    # Some sozinho depois de 2 segundos (2000ms)
    app.after(2000, aviso_rapido.place_forget)

# Criamos apenas um LABEL com cor de fundo, simulando o balão
aviso_rapido = ctk.CTkLabel(
    app, 
    text="✔️ Ação concluída com sucesso!", 
    fg_color="#1f538d",  # Cor de fundo do balão
    text_color="white", 
    corner_radius=8,     # Bordas arredondadas direto no texto
    padx=15, pady=8      # Margem interna para o texto não colar na borda
)

# Botão do seu app
ctk.CTkButton(app, text="Salvar", command=mostrar_notificacao).pack(pady=50)

app.mainloop()
