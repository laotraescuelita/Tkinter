import sqlite3

conn = sqlite3.connect("base.db")
cursor = conn.cursor()

cursor.execute("""SELECT * FROM actividades""")
actividades = cursor.fetchall()
print( actividades )

#cursor.execute("""Drop table actividades""")

conn.close()

