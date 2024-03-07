from main import *
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, Frame, Label, Button, NSEW

def obter_informacoes_atividades():
    # Obter a lista de processos em execução
    processos = []
    for processo in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
        nome_processo = processo.info['name'].lower()

        # Verificar se o processo não faz parte do Windows
        if 'windows' not in nome_processo and 'explorer.exe' not in nome_processo:
            processos.append((processo.info['pid'], nome_processo, processo.info['status'],
                              f"{processo.info['cpu_percent']:.2f}%", f"{processo.info['memory_percent']:.2f}%"))
    return processos

def identificar_lentidao(processos):
    # Identificar processos que podem estar causando lentidão (exemplo: alto uso de CPU ou memória)
    processos_lentidao = []
    for processo in processos:
        if float(processo[3].replace('%', '')) > 50 or float(processo[4].replace('%', '')) > 50:
            processos_lentidao.append(processo)
    return processos_lentidao

def atualizar_tela_atividades(treeview_atividades, treeview_lentidao):
    # Atualizar informações de atividades e processos causando lentidão
    treeview_atividades.delete(*treeview_atividades.get_children())
    treeview_lentidao.delete(*treeview_lentidao.get_children())

    processos = obter_informacoes_atividades()
    processos_lentidao = identificar_lentidao(processos)

    for processo in processos:
        treeview_atividades.insert("", "end", values=processo)

    for processo_lentidao in processos_lentidao:
        treeview_lentidao.insert("", "end", values=processo_lentidao)


def atividades():

    frame_atividades = Frame(frame_right, width=900, height=370, relief="flat", bg=fundo)
    frame_atividades.grid(row=0, column=0, sticky=NSEW, padx=20)

    frame_lentidao = Frame(frame_right, width=900, height=370, relief="flat", bg=fundo)
    frame_lentidao.grid(row=1, column=0, sticky=NSEW, padx=20)

    label_atividades = Label(frame_atividades, text="Atividades do Sistema", font=('Ivy 10 bold'), anchor='nw', fg='#FF914D', bg=fundo)
    label_atividades.grid(row=0, column=0, sticky=NSEW, padx=1)

    label_lentidao = Label(frame_lentidao, text="Programas Causando Lentidão", font=('Ivy 10 bold'), anchor='nw', fg='#FF914D', bg=fundo)
    label_lentidao.grid(row=0, column=0, sticky=NSEW, padx=1)

    treeview_atividades = ttk.Treeview(frame_atividades, columns=(1, 2, 3, 4, 5), show="headings", height="5")
    treeview_atividades.heading(1, text="PID")
    treeview_atividades.heading(2, text="Nome")
    treeview_atividades.heading(3, text="Status")
    treeview_atividades.heading(4, text="CPU (%)")
    treeview_atividades.heading(5, text="Memória (%)")

    size_atividades = [80, 200, 80, 80, 80]
    for col in (1, 2, 3, 4, 5):
        treeview_atividades.column(col, width=f"{size_atividades[col-1]}", anchor="center")

    treeview_lentidao = ttk.Treeview(frame_lentidao, columns=(1, 2, 3, 4, 5), show="headings", height="5")
    treeview_lentidao.heading(1, text="PID")
    treeview_lentidao.heading(2, text="Nome")
    treeview_lentidao.heading(3, text="Status")
    treeview_lentidao.heading(4, text="CPU (%)")
    treeview_lentidao.heading(5, text="Memória (%)")

    size_lentidao = [80, 200, 80, 80, 80]
    for col in (1, 2, 3, 4, 5):
        treeview_lentidao.column(col, width=f"{size_lentidao[col-1]}", anchor="center")
   

    vsb_a = ttk.Scrollbar(frame_atividades, orient="vertical", command=treeview_atividades.yview)
    treeview_atividades.configure(yscrollcommand=vsb_a.set)
    treeview_atividades.grid(column=0, row=1, sticky='nsew')
    vsb_a.grid(column=1, row=1, sticky='ns')


    vsb_l = ttk.Scrollbar(frame_lentidao, orient="vertical", command=treeview_lentidao.yview)
    treeview_lentidao.configure(yscrollcommand=vsb_l.set)
    treeview_lentidao.grid(column=0, row=1, sticky='nsew')
    vsb_l.grid(column=1, row=1, sticky='ns')

    atualizar_tela_atividades(treeview_atividades, treeview_lentidao)