from tkinter import Label, Frame, NSEW
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


def obter_informacoes_cpu():
    informacoes_cpu = []
    for i, percentual in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        informacoes_cpu.append((f"Núcleo {i+1}", f"{percentual:.2f}%"))

    return informacoes_cpu


def resumo_home():
    # Criar frames para cada seção
    frame_armazenamento = Frame(frame_right, width=200, height=100, relief="flat", bg=fundo)
    frame_armazenamento.grid(row=0, column=0, padx=10, pady=10)

    frame_cpu = Frame(frame_right, width=200, height=100, relief="flat", bg=fundo)
    frame_cpu.grid(row=0, column=1, padx=10, pady=10)

    frame_atividades = Frame(frame_right, width=200, height=100, relief="flat", bg=fundo)
    frame_atividades.grid(row=0, column=2, padx=10, pady=10)

    frame_rede = Frame(frame_right, width=200, height=100, relief="flat", bg=fundo)
    frame_rede.grid(row=0, column=3, padx=10, pady=10)

    # Adicionar labels para cada seção
    label_armazenamento = Label(frame_armazenamento, text="Armazenamento", font=('Ivy 8'), anchor='nw', fg='#FF914D', bg=fundo)
    label_armazenamento.grid(row=0, column=0, sticky=NSEW, padx=1)

    label_cpu = Label(frame_cpu, text="CPU", font=('Ivy 8'), anchor='nw', fg='#FF914D', bg=fundo)
    label_cpu.grid(row=0, column=0, sticky=NSEW, padx=1)

    label_atividades = Label(frame_atividades, text="Atividades", font=('Ivy 8'), anchor='nw', fg='#FF914D', bg=fundo)
    label_atividades.grid(row=0, column=0, sticky=NSEW, padx=1)

    label_rede = Label(frame_rede, text="Rede", font=('Ivy 8'), anchor='nw', fg='#FF914D', bg=fundo)
    label_rede.grid(row=0, column=0, sticky=NSEW, padx=1)

    # Atualizar informações para cada seção
    informacoes_armazenamento, _, _ = obter_informacoes_armazenamento()
    percentuais_cpu = psutil.cpu_percent(percpu=True, interval=1)
    processos = obter_informacoes_atividades()
    informacoes_rede = obter_informacoes_rede()

    # Adicionar labels com os resumos
    label_resumo_armazenamento = Label(frame_armazenamento, text=f"Total Partições: {len(informacoes_armazenamento)}", anchor='nw', fg='#FFFFFF', bg=fundo)
    label_resumo_armazenamento.grid(row=1, column=0, sticky=NSEW, padx=1)

    label_resumo_cpu = Label(frame_cpu, text=f"Núcleos: {len(percentuais_cpu)}", anchor='nw', fg='#FFFFFF', bg=fundo)
    label_resumo_cpu.grid(row=1, column=0, sticky=NSEW, padx=1)

    label_resumo_atividades = Label(frame_atividades, text=f"Total Processos: {len(processos)}", anchor='nw', fg='#FFFFFF', bg=fundo)
    label_resumo_atividades.grid(row=1, column=0, sticky=NSEW, padx=1)

    label_resumo_rede = Label(frame_rede, text=f"Interfaces de Rede: {len(informacoes_rede)}", anchor='nw', fg='#FFFFFF', bg=fundo)
    label_resumo_rede.grid(row=1, column=0, sticky=NSEW, padx=1)