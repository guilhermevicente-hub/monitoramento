# importando a funcao principal
from main import *

# importando funcoes
from home import resumo_home
from arm import armazenamento
from cpu_f import cpu
from atividade_f import atividades
from redes_f import rede


# ---------------- Funcao de Control  ----------------------------
def control(i):

    # Funcao Home
    if i == 'Home':
        for widget in frame_right.winfo_children():
            widget.destroy()

        resumo_home()

    # Funcao Armazenamento
    if i == 'armazenamento':
        for widget in frame_right.winfo_children():
            widget.destroy()
        
        armazenamento()
        
    # Funcao CPU
    if i == 'CPU':
        for widget in frame_right.winfo_children():
            widget.destroy()
        
        cpu()

    # Funcao Atividades
    if i == 'Atividades':
        for widget in frame_right.winfo_children():
            widget.destroy()

        atividades()

    # Funcao Redes
    if i == 'Redes':
        for widget in frame_right.winfo_children():
            widget.destroy()

        rede()

# ----------------------------- Frame Top  -------------------------

# logo
img_app = Image.open('images/s1.png')
img_app = img_app.resize((40,40))
img_app = ImageTk.PhotoImage(img_app)
app_ = Label(frame_top,width=1190, text=" Monitoramento do Sistema",height=42, image=img_app, compound=LEFT, relief="raised", anchor='center', font=('System 20 '), bg=fundo, fg=co1)
app_.grid(row=0, column=0,columnspan=350, sticky=NSEW, pady=0, padx=0)


# ----------------------------- Frame Left  -------------------------

# Home
img_Home = Image.open('images/home.png')
img_Home = img_Home.resize((20, 20))
img_Home = ImageTk.PhotoImage(img_Home)
b_Home = Button(frame_left,command=lambda:control('Home'), image=img_Home, compound=LEFT, text=" Informação do sistema",  bg=fundo, fg="white", font=('Ivy 12'), anchor="nw", relief=FLAT)
b_Home.grid(row=0, column=0, columnspan=1, sticky=NW, pady=0, padx=10)

# Armazenamento
img_Armazenamento = Image.open('images/s1.png')
img_Armazenamento = img_Armazenamento.resize((20, 20))
img_Armazenamento = ImageTk.PhotoImage(img_Armazenamento)
b_Armazenamento = Button(frame_left,command=lambda:control('armazenamento'), image=img_Armazenamento, compound=LEFT, text=" Armazenamento",  bg=fundo, fg="white", font=('Ivy 12 '), anchor="nw", relief=FLAT)
b_Armazenamento.grid(row=1, column=0, columnspan=1, sticky=NW, pady=0, padx=10)

# Atividades
img_Atividades = Image.open('images/s2.png')
img_Atividades = img_Atividades.resize((20, 20))
img_Atividades = ImageTk.PhotoImage(img_Atividades)
b_Atividades = Button(frame_left,command=lambda:control('Atividades'), image=img_Atividades, compound=LEFT, text=" Atividades",  bg=fundo, fg="white", font=('Ivy 12 '), anchor="nw", relief=FLAT)
b_Atividades.grid(row=2, column=0, columnspan=1, sticky=NW, pady=0, padx=10)

# CPU
img_CPU = Image.open('images/s4.png')
img_CPU = img_CPU.resize((20, 20))
img_CPU = ImageTk.PhotoImage(img_CPU)
b_CPU = Button(frame_left,command=lambda:control('CPU'), image=img_CPU, compound=LEFT, text=" CPU",  bg=fundo, fg="white", font=('Ivy 12 '), anchor="nw", relief=FLAT)
b_CPU.grid(row=3, column=0, columnspan=1, sticky=NW, pady=0, padx=10)

# Redes
img_Redes = Image.open('images/s7.png')
img_Redes = img_Redes.resize((20, 20))
img_Redes = ImageTk.PhotoImage(img_Redes)
b_Redes = Button(frame_left,command=lambda:control('Redes'), image=img_Redes, compound=LEFT, text=" Redes",  bg=fundo, fg="white", font=('Ivy 12 '), anchor="nw", relief=FLAT)
b_Redes.grid(row=4, column=0, columnspan=1, sticky=NW, pady=0, padx=10)


janela.mainloop()