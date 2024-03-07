# importando Tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkscrolledframe import ScrolledFrame

# Importando Pillow
from PIL import Image, ImageTk

# cores 

co0 = "#333333"  # preta / black
co1 = "#feffff"  # branca / white
co2 = "#6f9fbd"  # azul
co3 = "#ECF0F1"  # castanha / grey
co4 = "#403d3d"   # letra / 
co5 = "#e06636"   # 
co6 = "#ff9166"   # 
co7 = "#ef5350"   # red
co8 = "#263238"   # Verde / green
co9 = "#34495E"   # Azul carregado / dark blue
co10 = "#38576b"  # sidebar

fundo = "#233642"
fundo_right = "#2E2E2E"

# criando janela
janela = Tk()
janela.geometry('1193x600+0+0')
janela.title('')
janela.configure(background=fundo)
janela.resizable(width=FALSE, height=FALSE)

style = ttk.Style(janela)
style.theme_use("clam")
style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))


#---------------------------- Criando frames --------------------------------

frame_top = Frame(janela, width=1193,height=60, bg=fundo, relief="flat",)
frame_top.grid(row=0, column=0, sticky=NSEW, padx=0, columnspan=4)

frame_left = Frame(janela, width=100,height=515, bg=fundo , relief="flat",)
frame_left.grid(row=1, column=0, sticky=NSEW, padx=1,pady=20)

frame_right = Frame(janela, width=800,height=515, relief="flat",bg=fundo)
frame_right.grid(row=1, column=1, sticky=NSEW, padx=1, pady=20)