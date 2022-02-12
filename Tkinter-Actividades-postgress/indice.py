from tkinter import *
import tkinter as tk
from tkinter import ttk
from objetos_tkinter import ObjetosTkinter
import psycopg2


class Inicio():
	def __init__(self, raiz):
		self.raiz = raiz		
		self.etiquetas = {}
		self.marcos = {}		
		self.btn_agregar = None 
		self.entrada = None
		self.titulo = None
		self.actividades = None
		self.advertencia = []
		self.dezplamiento_arbol = None
		self.diagrama = None
	
	def iniciar(self):
		#Clase que nos ayuda a construir los objetos de tkinte
		objetos = ObjetosTkinter()
		#marcos que tienen el contenido.
		marcos = ["cabeza","cuerpo","arbol"]
		self.marcos = objetos.crearmarcos(self.raiz, marcos)
		self.marcos["cabeza"].grid(row=0, column=0)
		
		#las actividades que se introcuden en el encabezado
		self.titulo = Label(self.marcos["cabeza"], text="Aquí se ingresaran las actividades")
		self.titulo.grid(row=0, column=0, sticky=W, padx=10, pady=10)
		self.entrada = Entry(self.marcos["cabeza"])
		self.entrada.grid(row=1, column=0, sticky=W, padx=10, pady=10)
		self.btn_agregar = Button( self.marcos["cabeza"], text="Agregar", command=self.agregar)
		self.btn_agregar.grid( row=1, column=1, sticky=W, padx=10, pady=10)
		
		#en est aparte del marco tendremos un diagrama llamdo árbol.		
		#La barra de desplazamiento dentro del diagrama
		self.marcos["arbol"].grid(row=1,column=0)
		self.dezplamiento_arbol = Scrollbar(self.marcos["arbol"])
		self.dezplamiento_arbol.grid(row=0, column=1, sticky='ns')#pack(side=RIGHT, fill=Y)
		# Crear el árbol
		self.diagrama = ttk.Treeview(self.marcos["arbol"], yscrollcommand=self.dezplamiento_arbol.set, selectmode="extended")
		self.diagrama.grid(row=0,column=0, sticky=W,pady=10,padx=10)
		self.dezplamiento_arbol.config(command=self.diagrama.yview)
		self.diagrama["columns"] = ("id","actividad","estado")
		# Formato de columnas
		self.diagrama.column("#0", width=0, stretch=NO)
		self.diagrama.column("id", anchor=W, width=50)
		self.diagrama.column("actividad", anchor=CENTER, width=250)
		self.diagrama.column("estado", anchor=W, width=100)
		# Crer encabezados del diagrama
		self.diagrama.heading("#0", text="", anchor=W)
		self.diagrama.heading("id", text="Id", anchor=W)
		self.diagrama.heading("actividad", text="Actividad", anchor=CENTER)
		self.diagrama.heading("estado", text="Estado", anchor=W)
		# Intercambiar colores al ingresar las actividades
		self.diagrama.tag_configure('oddrow', background="white")
		self.diagrama.tag_configure('evenrow', background="lightblue")
		
		#extraer los datos de la base de datos
		conn = psycopg2.connect(
			dbname="postgres",
			user="postgres",
			password="123",
			host="localhost"
			)

		cursor = conn.cursor()
		cursor.execute("SELECT * FROM actividades")
		self.actividades = cursor.fetchall()
		print( self.actividades )		
		cursor.close()
		conn.close()

		for i,actividad in enumerate(self.actividades):
			if i%2 == 0:
				self.diagrama.insert(parent='', index='end', iid=i, text="", values=(actividad[0], actividad[1], actividad[2]), tags=('evenrow',))
			else:
				self.diagrama.insert(parent='', index='end', iid=i, text="", values=(actividad[0], actividad[1], actividad[2]), tags=('oddrow',))
		
		self.marcos["cuerpo"].grid(row=2, column=0)
		self.btn_eliminar = Button( self.marcos["cuerpo"], text="Eliminar", command=self.eliminar)
		self.btn_eliminar.grid( row=0, column=0, sticky=W, padx=10,pady=10)
		
		self.marcos["cuerpo"].grid(row=2, column=0)
		self.btn_actualizar = Button( self.marcos["cuerpo"], text="Actualizar", command=self.actualizar)
		self.btn_actualizar.grid( row=0, column=1, sticky=W, padx=10,pady=10)
		
	def actualizar(self):
		actividades_arbol_seleccionado = self.diagrama.focus()
		if actividades_arbol_seleccionado:
			actividad_tabla_actualizar = self.diagrama.item(actividades_arbol_seleccionado, 'values')[0]
					
			#actualizar de la base de datos
			conn = psycopg2.connect(
			dbname="postgres",
			user="postgres",
			password="123",
			host="localhost"
			)

			cursor = conn.cursor()
			sentencia = "UPDATE actividades set estado=%s where id=%s;"
			parametros = ("completo",actividad_tabla_actualizar)
			cursor.execute(sentencia,parametros)			
			conn.commit()
			cursor.close()
			conn.close()
	
			
			self.iniciar()

	def eliminar(self):		
		actividad_arbol_eliminar = self.diagrama.selection()		
		actividades_arbol_seleccionado = self.diagrama.focus()
		actividad_tabla_elimnar = self.diagrama.item(actividades_arbol_seleccionado, 'values')[0]
		if actividades_arbol_seleccionado:
			for actividad in actividades_arbol_seleccionado:
				self.diagrama.delete(actividad)		
			
			#Eliminar de la base de datos
			conn = psycopg2.connect(
			dbname="postgres",
			user="postgres",
			password="123",
			host="localhost"
			)

			cursor = conn.cursor()
			sentencia = "DELETE FROM actividades where id=%s;"
			parametros = (actividad_tabla_elimnar,)
			cursor.execute(sentencia,parametros)			
			conn.commit()
			cursor.close()
			conn.close()
	

			self.iniciar()
		


	def agregar(self):
		#verificar que haya informacion en el cuadro de texto.		
		import re 
		validar_actividad = "[A-Za-z0-9 .-]+"
		if not re.search(validar_actividad, self.entrada.get()):
			self.entrada.delete(0,END)				
			self.advertencia.append( Label(self.marcos["cabeza"],text="No es una actividad valida") )
			i = len( self.advertencia ) - 1
			self.advertencia[i].grid(row=0,column=1,sticky=W,padx=10,pady=10)
			self.advertencia[i].configure(bg="pink")
			self.entrada.focus()
			return
		else:			
			#Si la actividad cumple con las validaciones ingresarlo en la base.			
			conn = psycopg2.connect(
			dbname="postgres",
			user="postgres",
			password="123",
			host="localhost"
			)

			cursor = conn.cursor()
			sentencia = "INSERT INTO actividades( actividad ) VALUES(%s);"
			parametros = (self.entrada.get(),)			
			cursor.execute(sentencia,parametros)			
			conn.commit()
			cursor.close()
			conn.close()
				
			self.marcos["cabeza"].destroy()
			self.marcos["arbol"].destroy()
			self.marcos["cuerpo"].destroy()
						
			self.iniciar()