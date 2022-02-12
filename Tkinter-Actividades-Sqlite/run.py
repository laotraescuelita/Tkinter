from tkinter import *
import tkinter as tk
from indice import Inicio

raiz = Tk()
raiz.title(' Mi lista de actividades ')
raiz.geometry("500x500")

if __name__ == "__main__":
	inicio = Inicio( raiz )
	inicio.iniciar()
	raiz.mainloop()
