from tkinter import *
import tkinter as tk
from tkinter import ttk


class ObjetosTkinter:
	def __init__(self):
		self.etiquetas = {}
		self.registros = {}
		self.combos = {}
		self.marcos = {}

	def crearetiquetas(self, raiz, nombres):			
		for i,j in enumerate( nombres ):
			self.etiquetas[j] = Label( raiz, text=nombres[i] )
		return self.etiquetas
	
	def crearentradas(self, raiz, nombres):		
		for i,j in enumerate( nombres ):
			self.registros[j] = Entry( raiz )
		return self.registros

	def crearcombos(self, raiz, nombres, valores):
		for i,j in enumerate( nombres ):
			self.combos[j] = ttk.Combobox( raiz, value=valores)
			self.combos[j].current(0)
		return self.combos

	def crearmarcos(self, raiz, nombres):
		for i,j in enumerate( nombres ):
			self.marcos[j] = Frame( raiz )
		return self.marcos