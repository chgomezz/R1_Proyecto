#interface para mover brazo Robot
#Autor: Victor Romero Bautista
#Mexico

#importar librerias 
import tkinter
from tkinter import *
from time import sleep
from tkinter import messagebox
from pyfirmata import Arduino, util, SERVO

#configuracion de placa Arduino
board = Arduino('COM8')
sleep(5)

#Pines donde se conectaran los servos del brazo robot
pinS1 = 2 #base
pinS2 = 3 #antebrazo
pinS3 = 4 #brazo
pinS4 = 5 #gripper

board.digital[pinS1].mode = SERVO
board.digital[pinS2].mode = SERVO
board.digital[pinS3].mode = SERVO
board.digital[pinS4].mode = SERVO


#Funciones para mover articulaciones del brazo Robot

def servo1(posiciones1):
    #escritura de angulo en Servomotor
    board.digital[pinS1].write(posiciones1)

def servo2(posiciones2):
    #escritura de angulo en Servomotor
    board.digital[pinS2].write(posiciones2)

def servo3(posiciones3):
    #escritura de angulo en Servomotor
    board.digital[pinS3].write(posiciones3)

#abrir Gripper
def abrir():
    board.digital[pinS4].write(90)

#Cerrar Gripper
def cerrar():
    board.digital[pinS4].write(0)

#informacion
def info():
    tkMessageBox.showinfo("Informacion",
                            "Modo de uso: \nDesplazar cada perilla para mover las articulaciones del brazo robot \nPara abrir y cerrar el gripper, precione los respectivos botones")

##############################################3
##############################################

root = Tk()
root.title("Control de Brazo Robot")
root.minsize(800,450)


#Widgets ###################################
###########################################
#logo
img = PhotoImage(file="lg.gif")
widget = Label(root, image=img)
widget.grid(column=1, row=1)

#etiqueta 1
var = StringVar()
etiqueta = Label(root, textvariable=var, relief=FLAT, pady=5)
var.set("Eezy Bot Arm  \n Victor Romero")
etiqueta.grid(column=2, row=1)

#etiqueta apoyo
var2 = StringVar()
etiquetaAp = Label(root,textvariable=var2)
var2.set(" ")
etiquetaAp.grid(column=2,row=7)

#etiqueta apoyo2
var3 = StringVar()
etiquetaAy = Label(root,textvariable=var3)
var3.set(" ")
etiquetaAy.grid(column=2,row=5)

#Barra de posicion base
angulo1 = Scale(root,
                command = servo1,
                from_=30,
                to = 150,
                orient = HORIZONTAL,
                length = 300,
                troughcolor = 'gray',
                width=30,
                cursor='dot',
                label = 'Posicion Base')
angulo1.grid(column=2, row=2)

#Barra de posicion brazo
angulo2 = Scale(root,
                command = servo2,
                from_=100,
                to = 179,
                orient = HORIZONTAL,
                length = 300,
                troughcolor = 'gray',
                width=30,
                cursor='dot',
                label = 'Posicion Brazo')
angulo2.grid(column=2, row=3)

#Barra de posicion antebrazo
angulo3 = Scale(root,
                command = servo3,
                from_=70,
                to = 179,
                orient = HORIZONTAL,
                length = 300,
                troughcolor = 'gray',
                width=30,
                cursor='dot',
                label = 'Posicion Antebrazo')
angulo3.grid(column=2, row=4)

##Gripper

#Abrir
BoA = Button(root,
                text="Abrir Gripper",
                command=abrir,
                relief=RAISED,
                activebackground='green',
                bd=3,
                height=2,
                width=17)
BoA.grid(column=2, row=6)

#Cerrar
BoC = Button(root,
                text="Cerrar Gripper",
                command=cerrar,
                relief=RAISED,
                activebackground='red',
                bd=3,
                height=2,
                width=17)
BoC.grid(column=2, row=8)

#boton informacion
Binf = Button(root,
                text="Modo de uso",
                relief=GROOVE,
                command=info)
Binf.grid(column=1,row=2)


root.mainloop()