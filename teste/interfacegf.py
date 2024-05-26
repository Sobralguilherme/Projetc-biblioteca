import tkinter as tk

def on_button_click():
    message_box = tk.messagebox.showinfo("Informação", "Você clicou no botão!")
    # Fechar a caixa de mensagem após um tempo
    message_box.after(2000, lambda: message_box.destroy())

root = tk.Tk()
root.title("Exemplo Tkinter")

button = tk.Button(root, text="Clique Aqui!", command=on_button_click)
button.pack(padx=20, pady=20)

root.mainloop()
