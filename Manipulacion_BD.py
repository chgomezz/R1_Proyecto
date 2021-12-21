import mysql.connector

class Manipulacion_BD:# con esta clae podemos acceder de diferentes formas a los datos de una tabla de la base de  datos

    def __init__(self):
        self.cnn = mysql.connector.connect(host="localhost", user="root", 
        passwd="admin", database="bdEjemploPy")

    def __str__(self):
        datos=self.consulta_empleado()
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux
    
    def consulta_empleado(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM empleados")
        datos = cur.fetchall()
        cur.close()    
        return datos

    def inserta_empleado(self,ci, Name, ampellido, departamento):
        cur = self.cnn.cursor()
        sql='''INSERT INTO countries (ISO3, CountryName, Capital, CurrencyCode) 
        VALUES('{}', '{}', '{}', '{}')'''.format(ci, Name, ampellido, departamento)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n    

    def elimina_empleado(self,Id):
        cur = self.cnn.cursor()
        sql='''DELETE FROM empleado WHERE Id = {}'''.format(Id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n   

    def modifica_empleado(self,Id, ci, Name, ampellido, departamento):
        cur = self.cnn.cursor()
        sql='''UPDATE countries SET ISO3='{}', CountryName='{}', Capital='{}',
        CurrencyCode='{}' WHERE Id={}'''.format(ci, Name, ampellido, departamento, Id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n   
