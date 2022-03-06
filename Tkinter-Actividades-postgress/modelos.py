import psycopg2

conn = psycopg2.connect(
	dbname="nombredelabasededatos",
	user="nombredelusuario",
	password="contraseña",
	host="servidor"
	)

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS actividades
	(
		id serial primary key,
		actividad varchar,
		estado varchar default 'incompleto'
	);
	""")
conn.commit()

cursor.close()
conn.close()
