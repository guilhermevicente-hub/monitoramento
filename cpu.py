from main import *
import os
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, Frame, Label, NSEW
from colour import Color

def obter_informacoes_cpu():
    informacoes_cpu = []
    for i, percentual in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        informacoes_cpu.append((f"Núcleo {i+1}", f"{percentual:.2f}%"))

    return informacoes_cpu

def obter_recomendacao_cpu(percentual):
    if percentual < 30:
        return "O desempenho está excelente!"
    elif percentual < 60:
        return "O desempenho está bom, mas pode ser otimizado."
    else:
        return "O desempenho está elevado. Considere fechar aplicativos não essenciais."

def atualizar_tela_cpu(treeview_cpu, frame_grafico_cpu):
    treeview_cpu.delete(*treeview_cpu.get_children())
    for informacao in obter_informacoes_cpu():
        treeview_cpu.insert("", "end", values=informacao)

    atualizar_tela_grafico_cpu(frame_grafico_cpu)

def atualizar_tela_grafico_cpu(root):
    percentuais = psutil.cpu_percent(percpu=True, interval=1)

    plt.clf()
    fig, ax = plt.subplots(figsize=(6, 3), facecolor='#233642')  # Cor de fundo
    #fig.suptitle("Desempenho da CPU", color='white')  # Cor do título

    gradientes = list(Color("#E8E8E8").range_to(Color("#6A5ACD"), len(percentuais)))  # Cores suaves
    for i, (percentual, gradiente) in enumerate(zip(percentuais, gradientes)):
        cor_rgb = gradiente.rgb
        destaque = 'orange' if percentual == max(percentuais) else cor_rgb  # Destacar o núcleo de maior uso
        ax.bar(i, percentual, color=destaque, edgecolor='black', linewidth=1, alpha=0.8, zorder=3)

    ax.set_xticks(range(len(percentuais)))
    ax.set_xticklabels([f"Núcleo {i+1}" for i in range(len(percentuais))], rotation=0, ha="right", color='white')

    ax.grid(color='white', linestyle='--', linewidth=0.5, zorder=0)

    for text in ax.texts + ax.get_xticklabels() + [ax.title]:
        text.set_color('white')

    for text in ax.texts + ax.get_yticklabels() + [ax.title]:
        text.set_color('white')

    canvas = FigureCanvasTkAgg(fig, master=root)
    widget_canvas = canvas.get_tk_widget()
    widget_canvas.grid(row=0, column=0, sticky=NSEW, padx=100)


def cpu():
    frame_cpu = Frame(frame_right, width=800, height=370, relief="flat", bg=fundo)
    frame_cpu.grid(row=3, column=0, sticky=NSEW, padx=5)

    frame_grafico_cpu = Frame(frame_right, width=800, height=500, relief="flat", bg=fundo)
    frame_grafico_cpu.grid(row=4, column=0, sticky=NSEW, padx=1)

    label_cpu = Label(frame_cpu, text="Desempenho da CPU", font=('Ivy 10 bold'), anchor='nw', fg='#FF914D', bg=fundo)
    label_cpu.grid(row=0, column=0, sticky=NSEW, padx=1)

    treeview_cpu = ttk.Treeview(frame_cpu, columns=(1, 2), show="headings", height="5")
    treeview_cpu.heading(1, text="Núcleo")
    treeview_cpu.heading(2, text="Percentual")
    treeview_cpu.grid(row=1, column=0, sticky=NSEW, padx=1, pady=10)

    size_cpu = [80, 120]
    for col in (1, 2):
        treeview_cpu.column(col, width=f"{size_cpu[col-1]}", anchor="center")

    atualizar_tela_cpu(treeview_cpu, frame_grafico_cpu)

    recomendacao_label = Label(frame_cpu, text="", anchor='w',font=('Ivy 10'), fg=co1, bg=fundo)
    recomendacao_label.grid(row=2, column=0, sticky=NSEW, padx=1)

    atualizar_recomendacao_cpu(recomendacao_label)

def obter_recomendacao_cpu_global():
    percentual_global = psutil.cpu_percent(interval=1)

    if percentual_global < 30:
        return "O desempenho global da CPU está excelente!"
    elif percentual_global < 60:
        return "O desempenho global da CPU está bom, mas pode ser otimizado."
    else:
        return "O desempenho global da CPU está elevado. Considere fechar aplicativos não essenciais."

def atualizar_recomendacao_cpu(label):
    recomendacao = obter_recomendacao_cpu_global()
    label["text"] = f"Recomendação: {recomendacao}"