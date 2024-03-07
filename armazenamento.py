from main import *
import os

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import psutil
from tkinter import font as tkFont


def obter_status_recomendacao(uso_particao):
    percentual_livre = uso_particao.free / uso_particao.total * 100

    if percentual_livre > 20:
        status = "Bom"
        recomendacao = "Não é necessário liberar espaço."
    elif percentual_livre > 10:
        status = "Aviso"
        recomendacao = "Recomendado liberar espaço."
    else:
        status = "Crítico"
        recomendacao = "Liberar espaço imediatamente."

    return status, recomendacao

def obter_informacoes_armazenamento():
    informacoes_armazenamento = []
    for particao in psutil.disk_partitions():
        try:
            uso_particao = psutil.disk_usage(particao.mountpoint)
            status, recomendacao = obter_status_recomendacao(uso_particao)
            informacoes_armazenamento.append((
                particao.fstype,
                particao.mountpoint,
                f"{uso_particao.total / (1024 ** 3):.2f}",
                f"{uso_particao.used / (1024 ** 3):.2f}",
                f"{uso_particao.free / (1024 ** 3):.2f}",
                f"{uso_particao.percent:.2f}",
                status,
                recomendacao
            ))
        except PermissionError:
            print(f"Não foi possível acessar {particao.mountpoint}")

    labels = [info[1] for info in informacoes_armazenamento]
    percentuais = [info[5] for info in informacoes_armazenamento]

    return informacoes_armazenamento, labels, percentuais


def obter_informacoes_armazenamento_grafico():
    informacoes_armazenamento = []
    for particao in psutil.disk_partitions():
        try:
            if os.path.exists(particao.mountpoint):
                uso_particao = psutil.disk_usage(particao.mountpoint)
                status, recomendacao = obter_status_recomendacao(uso_particao)
                informacoes_armazenamento.append((particao.mountpoint, uso_particao.percent, status, recomendacao))
        except PermissionError as e:
            print(f"Não foi possível acessar {particao.mountpoint}: {e}")
        except OSError as e:
            print(f"Erro ao obter informações de {particao.mountpoint}: {e}")
    return informacoes_armazenamento

def atualizar_tela(treeview_armazenamento):
    # Atualizar informações de armazenamento
    treeview_armazenamento.delete(*treeview_armazenamento.get_children())
    for informacao in obter_informacoes_armazenamento():
        treeview_armazenamento.insert("", "end", values=informacao, tags=(informacao[6],))

def atualizar_tela_grafico(root, labels, percentuais, statuses, recomendacoes):
    # Atualizar informações de status e recomendação
    for i, label in enumerate(labels):
        try:
            status, recomendacao = obter_status_recomendacao(psutil.disk_usage(label))
            statuses[i]["text"] = f"Status: {status}"
            recomendacoes[i]["text"] = f"Recomendação: {recomendacao}"
        except Exception as e:
            print(f"Erro ao obter informações de {label}: {e}")

    # Estilo personalizado para os gráficos de pizza
    custom_colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#c2c2f0', '#ffb3e6', '#c2f0c2']

    # Atualizar gráficos de pizza
    plt.clf()
    fig, axs = plt.subplots(1, len(labels), figsize=(6, 3), facecolor='#233642')  # Defina a cor de fundo aqui
    fig.suptitle("Uso do Disco", color='white')  # Defina a cor do título

    for i, label in enumerate(labels):
        try:
            percentual_num = float(percentuais[i])
            axs[i].pie([percentual_num, 100 - percentual_num], labels=[f"Usado: {percentual_num:.2f}%", f"Livre: {100 - percentual_num:.2f}%"],
                       autopct='%1.1f%%', startangle=90, colors=custom_colors)
            axs[i].axis('equal')
            axs[i].set_title(label, color='yellow')  # Defina a cor do título do gráfico

            # Adicionar sombra ao gráfico de pizza
            axs[i].grid(color='white')

            # Configurar as cores do texto no gráfico
            for text in axs[i].texts + [axs[i].title]:
                text.set_color('white')
        except ValueError as ve:
            print(f"Erro ao processar percentual de {label}: {ve}")

    # Adicionar título ao canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    widget_canvas = canvas.get_tk_widget()
    widget_canvas.grid(row=0, column=0, sticky=NSEW, padx=100)



# Defina treeview_armazenamento como uma variável global

def armazenamento():
    global treeview_armazenamento

    frame_up = Frame(frame_right, width=800, height=270, relief="flat", bg=fundo)
    frame_up.grid(row=0, column=0, sticky=NSEW, padx=5)

    frame_down = Frame(frame_right, width=800, height=100, relief="flat", bg=fundo)
    frame_down.grid(row=1, column=0, sticky=NSEW, padx=1, pady=10)

    frame_grafico = Frame(frame_right, width=800, height=500, relief="flat", bg=fundo)
    frame_grafico.grid(row=2, column=0, sticky=NSEW, padx=1)

    label_armazenamento = Label(frame_up, text="Informações de Armazenamento", font=('Ivy 10 bold'), anchor='nw', fg='#FF914D', bg=fundo)
    label_armazenamento.grid(row=0, column=0, sticky=NSEW, padx=1)


    # Ensure treeview_armazenamento is initialized

    treeview_armazenamento = ttk.Treeview(frame_up, columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings", height="5")
    treeview_armazenamento.heading(1, text="Tipo")
    treeview_armazenamento.heading(2, text="Partição")
    treeview_armazenamento.heading(3, text="Total (GB)")
    treeview_armazenamento.heading(4, text="Usado (GB)")
    treeview_armazenamento.heading(5, text="Livre (GB)")
    treeview_armazenamento.heading(6, text="Percentual")
    treeview_armazenamento.heading(7, text="Status")
    treeview_armazenamento.heading(8, text="Recomendação")
    treeview_armazenamento.grid(row=1, column=0, sticky=NSEW, padx=1, pady=10)

    # Ajustar automaticamente a largura das colunas para o melhor ajuste
    size = [80, 90, 100, 100, 100, 100, 100, 200]
    c = 0
    for col in (1, 2, 3, 4, 5, 6, 7, 8):
        treeview_armazenamento.column(col, width=f"{size[c]}", anchor="center")
        treeview_armazenamento.heading(col, command=lambda c=col: treeview_sort_column(treeview_armazenamento, c, False))

        c+=1

    informacoes_armazenamento, labels, percentuais = obter_informacoes_armazenamento()

    if not informacoes_armazenamento:
        print("Nenhuma informação de armazenamento disponível.")
        return

    for informacao in informacoes_armazenamento:
        treeview_armazenamento.insert("", "end", values=informacao, tags=(informacao[6],))

    statuses = []
    recomendacoes = []

    r=0

    for label in labels:
        status_label = Label(frame_down, text="Status: ", anchor=NW, fg=co1, bg=fundo)
        recomendacao_label = Label(frame_down, text="Recomendação: ",anchor=NW, fg=co1, bg=fundo)
        status_label.grid(row=r, column=0, sticky=NSEW, padx=1)
        recomendacao_label.grid(row=r+1, column=0, sticky=NSEW, padx=1)
        statuses.append(status_label)
        recomendacoes.append(recomendacao_label)

    atualizar_tela_grafico(frame_grafico, labels, percentuais, statuses, recomendacoes)