import mysql.connector
import MySQLdb
class posiciones:
    def __init__(self):
        self.cnn = mysql.connector.connect(host="localhost", user="root", 
        passwd="", database="robot")
    def __str__(self):
        datos=self.consulta_pos()
        dat=""
        for row in datos:
            dat=dat + str(row) + "\n"
        return dat
    def consulta_pos(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM posicionmotores")
        datos = cur.fetchall()
        cur.close()    
        return datos
    def buscar_pos(self, numero):
        cur = self.cnn.cursor()
        sql= "SELECT * FROM posicionmotores WHERE numero = {}".format(numero)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()    
        return datos
    def agrega_pos(self, m0, m1, m2, m3, m4, m5):
        cur = self.cnn.cursor()
        sql='''INSERT INTO posicionmotores (motor_0, motor_1, motor_2, motor_3, motor_4, motor_5) 
        VALUES('{}','{}', '{}', '{}','{}', '{}')'''.format(m0, m1, m2, m3, m4, m5)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n    
    def elimina_pos(self,numero):
        cur = self.cnn.cursor()
        sql='''DELETE FROM posicionmotores WHERE numero = {}'''.format(numero)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()
        cur.close()
        return n
    def modifica_pos(self, m0, m1, m2, m3, m4, m5, numero):
        cur = self.cnn.cursor()
        sql='''UPDATE posicionmotores SET motor_0='{}', motor_1='{}', motor_2='{}', motor_3='{}',
        motor_4='{}', motor_5='{}' WHERE numero={}'''.format( m0 ,m1, m2, m3, m4, m5, numero)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n   
