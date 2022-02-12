import psycopg2

conn = psycopg2.connect(
	dbname="postgres",
	user="postgres",
	password="123",
	host="localhost"
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