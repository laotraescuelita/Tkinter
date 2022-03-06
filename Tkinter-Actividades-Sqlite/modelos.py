import sqlite3

conn = sqlite3.connect("nombredelabasededatos.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS actividades
	(
		id integer primary key,
		actividad text,
		estado text default "incompleto"
	)
	""")

conn.close()
