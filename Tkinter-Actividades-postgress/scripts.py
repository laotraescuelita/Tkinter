import psycopg2

conn = psycopg2.connect(
	dbname="postgres",
	user="postgres",
	password="123",
	host="localhost"
	)

cursor = conn.cursor()

cursor.execute("SELECT * FROM actividades")
actividades = cursor.fetchall()
print( actividades )
#cursor.execute("""Drop table actividades""")
cursor.close()
conn.close()

