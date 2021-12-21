import mysql.connector

cnn = mysql.connector.connect(host="localhost", user="root", 
passwd="", database="robot")

cur = cnn.cursor()
cur.execute("SELECT * FROM posicionmotores ")
datos = cur.fetchall()

for fila in datos:
    print(fila)


print(cnn)