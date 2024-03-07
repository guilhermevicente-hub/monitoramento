from main import *
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, Frame, Label, NSEW

def obter_informacoes_rede():
    # Obter informações sobre o uso da rede
    informacoes_rede = []
    for interface, dados in psutil.net_if_stats().items():
        if interface != 'lo':  # Ignorar interface local (loopback)
            informacoes_rede.append((interface, dados.speed, f"{dados.isup}", f"{dados.duplex}", f"{dados.mtu}"))
    return informacoes_rede



def atualizar_tela_rede(treeview_rede):
    # Atualizar informações da rede
    treeview_rede.delete(*treeview_rede.get_children())
    for informacao in obter_informacoes_rede():
        treeview_rede.insert("", "end", values=informacao)

def rede():
    frame_rede = Frame(frame_right, width=800, height=200, relief="flat", bg=fundo)
    frame_rede.grid(row=3, column=0, sticky=NSEW, padx=5)

    label_rede = Label(frame_rede, text="Informações de Rede", font=('Ivy 10 bold'), anchor='nw', fg='#FF914D', bg=fundo)
    label_rede.grid(row=0, column=0, sticky=NSEW, padx=1)

    treeview_rede = ttk.Treeview(frame_rede, columns=(1, 2, 3, 4, 5), show="headings", height="5")
    treeview_rede.heading(1, text="Interface")
    treeview_rede.heading(2, text="Velocidade (Mbps)")
    treeview_rede.heading(3, text="Ativa")
    treeview_rede.heading(4, text="Duplex")
    treeview_rede.heading(5, text="MTU")
    treeview_rede.grid(row=1, column=0, sticky=NSEW, padx=1, pady=10)

    size_rede = [150, 150, 80, 80, 80]
    for col in (1, 2, 3, 4, 5):
        treeview_rede.column(col, width=f"{size_rede[col-1]}", anchor="center")

    informacoes_rede = obter_informacoes_rede()

    for informacao in informacoes_rede:
        treeview_rede.insert("", "end", values=informacao)

    # Defina treeview_rede como uma variável global se necessário