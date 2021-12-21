from logging import disable
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import mysql.connector
import MySQLdb
import serial
import time
import threading
import datetime
from clasesBDPosiciones import posiciones

##para el QR
import sys
import cv2
import numpy as np
from pyzbar.pyzbar import decode  # pip install zba r
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import imutils

class MainFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=1200, height=800,bg="gray7")                
        self.master = master    
        self.master.protocol('WM_DELETE_WINDOW',self.askQuit)
        self.pack()
        self.hilo1 = threading.Thread(target=self.lector_codigo_QR,daemon=True)
        self.hilo2 = threading.Thread(target=self.decision,daemon=True)
        self.arduino = serial.Serial("COM8",9600,timeout=1.0)
        time.sleep(1)
        self.home= StringVar()
        self.home= "30,110,45,0,70,45"
        self.terminarCiclo= StringVar()
        self.terminarCiclo = "si"
        self.contadorChico = IntVar()
        self.contadorGrande = IntVar()
        self.contadorChico = 0
        self.contadorGrande = 0
        self.posicion = IntVar()
        self.posicion = 0
        self.iniciarProceso = False
        
        #self.value_color = StringVar()
        self.value_pres = StringVar()
        self.mode = IntVar()
        self.cantidadCiclos = 0
        self.value_mot0 = StringVar()
        self.value_mot1 = StringVar()
        self.value_mot2 = StringVar()
        self.value_mot3 = StringVar()
        self.value_mot4 = StringVar()
        self.value_mot5 = StringVar()
        self.caja= StringVar()
        

        self.listaCiclo= ""

        #self.value_mot6 = StringVar()
        self.auto = IntVar()
        self.envi=""        
        self.create_widgets()
        self.isRun=True
        self.hilo1.start()
        self.hilo2.start()
        self.BDmotores=posiciones()
        #self.BDsensor=sensores()
        self.llenaDatos()
        self.veces=0
        #self.colorInt=0
        self.fn_estadorun("disabled") 
        self.fn_estadoconfigure("disabled")
        
    def askQuit(self):
        self.isRun=False
        cad= 'mot:' + self.home 
        self.arduino.write(cad.encode('ascii'))
        time.sleep(1.1)
        self.arduino.close()
        #self.hilo1.join(0.1)
        self.master.quit()
        self.master.destroy()
        print("*** finalizando...")

    def fn_estadoconfigure(self,estado):
        self.m0.configure(state=estado)
        self.m1.configure(state=estado)
        self.m2.configure(state=estado)
        self.m3.configure(state=estado)
        self.m4.configure(state=estado)
        self.m5.configure(state=estado)
        #self.m6.configure(state=estado)

        self.btn_guardar.configure(state=estado)
        self.btn1.configure(state=estado)
        self.btn2.configure(state="disabled")
        self.btn3.configure(state=estado)
        self.btn4.configure(state=estado)
        self.btn5.configure(state=estado) 
        self.btn6.configure(state="disabled")
        #self.btn7.configure(state="disabled")
        if self.veces>0 and self.mode.get()==1:
            self.btn6.configure(state="normal")
    
    def fn_estadorun(self,estado):
        self.btn7.configure(state=estado)
        self.btn8.configure(state=estado)
        self.btn9.configure(state=estado)
        self.btn10.configure(state=estado) 

    
    def lector_codigo_QR(self):
        
        while self.isRun:
            
            # captura de imagen
            cam1 = cv2.VideoCapture(1) #Abre la camara de video, con el numero 0 se abre la cámara de la compu, 1 para otras cámaras

            cam1.set(3, 480)  #Tamaño de las imágenes que vamos a capturar
            cam1.set(4, 480)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 20]  # Formato de la cámara en JPEG

            sin_qr = 0

            print("Presione s para salir del programa")

            while (cam1.isOpened()):      # Mientras la cámara esté abierta realizamos el proceso de captura
                ret, frame = cam1.read()
                frame = imutils.resize(frame, width=480)

                # detecta codigo qr cuando no reproduce video
                for barcode in decode(frame):   # la camara lee una imagen y se guarda en la variable frame
                    myData = barcode.data.decode('utf-8') #Se decodifica el código QR
                    print(myData) # Se imprime en pantalla el código decodificado
                    self.caja= myData
                    pts = np.array([barcode.polygon], np.int32) # Se dibuja un recuadro en cada uno de los códigos detectados
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)  #Se convierte en texto lo que se decodifica en el código QR
                    pts2 = barcode.rect
                    cv2.putText(frame, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

                #cv2.imshow('Introduzca su receta con Codigo QR', frame)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)

                self.lblVideo.configure(image=img)
                self.lblVideo.image = img
                #self.lblVideo.after(10, lector_codigo_QR)
                
                '''
                # Sale del programa al presionar la tecla "s"
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    break
                '''
    def iniciarP(self):
        self.iniciarProceso = True
        self.terminarCiclo = "si"
        self.decision()

    def terminarP(self):
        self.iniciarProceso = True
        self.terminarCiclo = "si"

    def decision(self):
        while self.iniciarProceso == True:
            if self.terminarCiclo == "si":
                self.terminarCiclo = "no"
                if self.caja == "Chico":
                    if self.contadorChico < 18:
                        self.contadorChico += 1
                        self.posicion = 1 #atender que ciclo usar (para mover caja chica)
                        self.agrega_ciclo()
                    if self.contadorChico == 18:
                        self.contadorChico = 0 
                        self.posicion = 3 #atender que ciclo usar (para cambiar caja chica)
                        self.agrega_ciclo()
                    
                if self.caja == "Grande":
                    if self.contadorGrande < 18:
                        self.contadorGrande += 1
                        self.posicion = 1 #atender que ciclo usar (para mover caja grande)
                        self.agrega_ciclo()
                    if self.contadorGrande == 18:
                        self.contadorGrande = 0 
                        self.posicion = 3 #atender que ciclo usar (para cambiar caja Grande)
                        self.agrega_ciclo()

            self.terminarCiclo = self.arduino.readline().decode('ascii').strip()
                
        
        
    '''
    def getSensorValues(self):
        while self.isRun:
            cad =self.arduino.readline().decode('ascii').strip()
            if cad:
                pos=cad.index(":")
                label=cad[:pos]
                value=cad[pos+1:]
                if label == 'pres':
                    self.value_pres.set(value)
                    self.saveValor(value)
                if label == 'color':
                    self.value_color.set(value)
                    self.colorInt=int(value)
              
    def saveValor(self,value):
        if value=="1":
            FyH=datetime.datetime.now()
            if self.colorInt<300:
                tipo="blanco"
            else:
                tipo="rojo"
            self.BDsensor.inserta_sensor(FyH,self.colorInt,tipo)
    '''
    
    def limpiaGrid(self):
        for item in self.grid.get_children():
            self.grid.delete(item)

    def llenaDatos(self):
        datos = self.BDmotores.consulta_pos()
        for row in datos:
            self.grid.insert("",END,text=row[0], values=(row[1],row[2],row[3],row[4], row[5], row[6], ))

        if len(self.grid.get_children()) > 0:
            self.grid.selection_set( self.grid.get_children()[0])

        cantidadC = open('cantidadCiclos.txt')
        self.listaCiclo = cantidadC.readlines()
        cantidadC.close()
        self.cbblistaCiclo['values']= self.listaCiclo
        

    def fsave_position(self):
        self.BDmotores.agrega_pos(self.value_mot0.get(),self.value_mot1.get(),self.value_mot2.get(),
        self.value_mot3.get(), self.value_mot4.get(), self.value_mot5.get())
        self.limpiaGrid()
        self.llenaDatos()
    
    def fEliminar(self):
        selected = self.grid.focus()
        clave = self.grid.item(selected,'text')
        if clave == '':
            messagebox.showwarning("Eliminar", 'Debe seleccionar un registro.')
        else:
            r = messagebox.askquestion("Eliminar", "¿Desea eliminar el registro seleccionado?")
            if r == messagebox.YES:
                n = self.BDmotores.elimina_pos(clave)
                if n == 1:
                    self.limpiaGrid()
                    self.llenaDatos()
                    messagebox.showinfo("Eliminar", 'Elemento eliminado correctamente.')
                else:
                    messagebox.showwarning("Eliminar", 'No fue posible eliminar el elemento.')

    def fModificar(self):
        selected = self.grid.focus()
        clave = self.grid.item(selected,'text')
        if clave == '':
            messagebox.showwarning("Modificar", 'Debe seleccionar un elemento.')
        else: 
            self.btn2.configure(state="normal")
            valores = self.grid.item(selected,'values')
            self.clave = self.grid.item(selected,'text')
            self.scale0.set(valores[0])
            self.scale1.set(valores[1])
            self.scale2.set(valores[2])
            self.scale3.set(valores[3])
            self.scale4.set(valores[4])
            self.scale5.set(valores[5])
            
    
    def guardarcambios(self):
        self.BDmotores.modifica_pos (self.value_mot0.get(), self.value_mot1.get(), self.value_mot2.get(), self.value_mot3.get(), self.value_mot4.get(),self.value_mot5.get(),self.clave)
        self.limpiaGrid()
        self.llenaDatos()
        self.btn2.configure(state="disabled")
        messagebox.showinfo("Modificar", 'Elemento modificado correctamente.')

    def fEnviaMot0(self):
        #time.sleep(2)
        cad = ""
        cad = "mot0:" + self.value_mot0.get()
        self.arduino.write(cad.encode('ascii'))
        self.txtres.insert(1.0,cad+"\n")
        print("cad", cad)

    def fEnviaMot1(self):
        #time.sleep(2)
        cad = ""
        cad = "mot1:" + self.value_mot1.get()
        self.arduino.write(cad.encode('ascii'))
        self.txtres.insert(1.0,cad+"\n")

    def fEnviaMot2(self):
        #time.sleep(2)
        cad = ""
        cad = "mot2:" + self.value_mot2.get()
        self.arduino.write(cad.encode('ascii'))
        self.txtres.insert(1.0,cad+"\n")

    def fEnviaMot3(self):
        #time.sleep(2)
        cad = ""
        cad = "mot3:" + self.value_mot3.get()
        self.arduino.write(cad.encode('ascii'))
        self.txtres.insert(1.0,cad+"\n")

    def fEnviaMot4(self):
        #time.sleep(2)
        cad = ""
        cad = "mot4:" + self.value_mot4.get()
        self.arduino.write(cad.encode('ascii'))
        self.txtres.insert(1.0,cad+"\n")

    def fEnviaMot5(self):
        #time.sleep(2)
        cad = ""
        cad = "mot5:" + self.value_mot5.get()
        self.arduino.write(cad.encode('ascii'))
        self.txtres.insert(1.0,cad+"\n")
    '''
    def fEnviaMot6(self):
        cad = "mot6:" + self.value_mot6.get()
        self.arduino.write(cad.encode('ascii'))
        self.txtres.insert(1.0,cad+"\n")
    '''

    def envi_motors(self):
        selected = self.grid.focus()
        clave = self.grid.item(selected,'text')
        if clave == '':
            messagebox.showwarning("Modificar", 'Debe seleccionar un elemento.')
        else: 
            valores = self.grid.item(selected,'values')
            self.clave = self.grid.item(selected,'text')
            mot=valores[0]+","+valores[1]+","+valores[2]+","+valores[3]+","+valores[4]+","+valores[5]
            cad="mot:"+mot
            self.arduino.write(cad.encode('ascii'))
            self.txtres.insert(1.0,cad+"\n")
            print(cad)

    ##### para guardar los ciclos en txt ###
    def agregar_ciclo_nuevo(self):
        cantidadC = open('cantidadCiclos.txt')
        self.listaCiclo = cantidadC.readlines()
        self.cantidadCiclos= len(self.listaCiclo )
        
        cantidadC = open('cantidadCiclos.txt', 'a')
        cadena= "Ciclo " + str(self.cantidadCiclos) + "\n"
        cantidadC.write(cadena)

        cantidadC = open('cantidadCiclos.txt')
        self.listaCiclo = cantidadC.readlines()
        cantidadC.close()
        self.cbblistaCiclo['values']= self.listaCiclo
        self.btn6.configure(state="normal")

        archivo= open('ciclos.txt')
        lineas = archivo.readlines()
        self.cantidadlineas= len(lineas)
        if self.cantidadlineas != 0:
            archivo= open('ciclos.txt', 'a')
            archivo.write('\n')
        
        archivo.close()



    
    def agregar_ciclo_Mod(self):
        selected = self.grid.focus()
        clave = self.grid.item(selected,'text')
        if clave == '':
            messagebox.showwarning("Añadir", 'Debe seleccionar un elemento para agregarlo al ciclo de trabajo.')
        else:
            #self.btn6.configure(state="normal")
            valores = self.grid.item(selected,'values')
            mot=valores[0]+","+valores[1]+","+valores[2]+","+valores[3]+","+valores[4]+","+valores[5]
            cad = "to:" + mot
            archivo= open('ciclos.txt', 'a')
            archivo.write(cad)
            archivo.close()
            self.txtres.insert(1.0,cad+"\n")

            '''
            self.arduino.write(cad .encode('ascii'))
            self.txtres.insert(1.0,cad+"\n")
            self.veces+=1
            '''
    def agrega_ciclo(self):
            self.btn6.configure(state="normal")
            archivo= open('ciclos.txt')
            lineas = archivo.readlines()
            
            linea = lineas[posicion]
            c = 't'
            lst = []
            for pos, char in enumerate(linea):
                if (char == c):
                    lst.append(pos)

            for i in range(0, len(lst)):
                if i < len(lst)-1:
                    cad = linea[lst[i]: lst[i+1]]
                else:
                    cad = linea[lst[i]:]
                
                self.arduino.write(cad .encode('ascii'))
                time.sleep(1.2)
                self.txtres.insert(1.0,cad+"\n")
                print(cad)
                self.veces+=1
            '''
            valores = self.grid.item(selected,'values')
            mot=valores[0]+","+valores[1]+","+valores[2]+","+valores[3]+","+valores[4]+","+valores[5]
            cad = "to:" + mot
            self.arduino.write(cad .encode('ascii'))
            self.txtres.insert(1.0,cad+"\n")
            self.veces+=1
            '''
        #### hasta aca
    def borrar_ciclo(self):
        cad = "delete:" + self.home
        self.veces=0
        self.arduino.write(cad .encode('ascii'))
        self.txtres.insert(1.0,"ciclo eliminado\n")
        self.btn6.configure(state="disabled")

    def fstart_ciclo(self):
        self.posicion = self.cbblistaCiclo.current()
        self.agrega_ciclo()
        cad = "run:"+str(self.veces)
        self.arduino.write(cad .encode('ascii'))
        self.txtres.insert(1.0,"iniciando ciclo\n")
    
    def fpausa(self):
        cad = "pause:0"
        self.arduino.write(cad .encode('ascii'))
        self.txtres.insert(1.0,"ciclo pausado\n")

    def fncontinue(self):
        cad = "continue:0"
        self.arduino.write(cad .encode('ascii'))
        self.txtres.insert(1.0,"continuando...\n")

    def fstop_ciclo(self):
        cad = "stop:" + self.home
        self.arduino.write(cad .encode('ascii'))
        self.txtres.insert(1.0,"finalizando ciclo\n")

    def fnMode(self):
        if self.mode.get() ==1:
            self.fn_estadoconfigure("normal")
            self.fn_estadorun("disabled")
            messagebox.showinfo("Estado", '''En este modo se pueden agregar, modificar y eliminar
las posiciones, asi como realizar pruebas para uno o todos los motores.''')
        elif self.mode.get() ==2:
            self.fn_estadorun("normal")
            self.fn_estadoconfigure("disabled")
            messagebox.showinfo("Estado", "En este modo se puede ejecutar el ciclo de trabajo.")
        
    def create_widgets(self):
        motores=Frame(self,width=350,height=620,bg='gray22')
        motores.place(x=10,y=10)

        Label(motores,text="MOTOR 0 ",fg="DeepSkyBlue",bg="gray22").place(x=10,y=30)
        self.scale0=Scale(motores, from_=0, to=180,orient='horizontal',tickinterval=30,
         length=220,variable=self.value_mot0,fg="white",bg="gray22")
        self.scale0.place(x=75,y=10)        
        self.m0=Button(motores,text="OK", command=self.fEnviaMot0,fg="white",bg="gray22")
        self.m0.place(x=310,y=30)

        Label(motores,text="MOTOR 1 ",fg="DeepSkyBlue",bg="gray22").place(x=10,y=100)
        self.scale1=Scale(motores, from_=50, to=160,orient='horizontal',tickinterval=30,
         length=220,variable=self.value_mot1,fg="white",bg="gray22")
        self.scale1.place(x=75,y=80)        
        self.m1=Button(motores,text="OK", command=self.fEnviaMot1,fg="white",bg="gray22")
        self.m1.place(x=310,y=100)

        Label(motores,text="MOTOR 2 ",fg="DeepSkyBlue",bg="gray22").place(x=10,y=170)
        self.scale2= Scale(motores, from_=0, to=180,orient='horizontal',tickinterval=30,
         length=220,variable=self.value_mot2,fg="white",bg="gray22")
        self.scale2.place(x=75,y=150)      
        self.m2=Button(motores,text="OK", command=self.fEnviaMot2,fg="white",bg="gray22")
        self.m2.place(x=310,y=170)

        Label(motores,text="MOTOR 3 ",fg="DeepSkyBlue",bg="gray22").place(x=10,y=240)
        self.scale3= Scale(motores, from_=0, to=180,orient='horizontal',tickinterval=30,
         length=220,variable=self.value_mot3,fg="white",bg="gray22")
        self.scale3.place(x=75,y=220)        
        self.m3=Button(motores,text="OK", command=self.fEnviaMot3,fg="white",bg="gray22")
        self.m3.place(x=310,y=240)

        Label(motores,text="MOTOR 4 ",fg="DeepSkyBlue",bg="gray22").place(x=10,y=310)
        self.scale4= Scale(motores, from_=0, to=180,orient='horizontal',tickinterval=30,
         length=220,variable=self.value_mot4,fg="white",bg="gray22")
        self.scale4.place(x=75,y=290)        
        self.m4=Button(motores,text="OK", command=self.fEnviaMot4,fg="white",bg="gray22")
        self.m4.place(x=310,y=310)

        Label(motores,text="MOTOR 5 ",fg="DeepSkyBlue",bg="gray22").place(x=10,y=380)
        self.scale5= Scale(motores, from_=30, to=200,orient='horizontal',tickinterval=30,
         length=220,variable=self.value_mot5,fg="white",bg="gray22")
        self.scale5.place(x=75,y=360)        
        self.m5=Button(motores,text="OK", command=self.fEnviaMot5,fg="white",bg="gray22")
        self.m5.place(x=310,y=380)
        '''
        Label(motores,text="MOTOR 7 ",fg="DeepSkyBlue",bg="gray22").place(x=10,y=450)
        self.scale7= Scale(motores, from_=0, to=60,orient='horizontal',tickinterval=10,
         length=220,variable=self.value_mot7,fg="white",bg="gray22",relief="flat")
        self.scale7.place(x=75,y=430)
        self.m7=Button(motores,text="OK", command=self.fEnviaMot7,fg="white",bg="gray22")
        self.m7.place(x=310,y=450)
        '''
        self.btn_guardar = Button(motores,text="Guardar",command=self.fsave_position,fg="white",bg="gray22")
        self.btn_guardar.place(x=260, y=510)
         
        frame3 = Frame(self,bg="yellow" )
        frame3.place(x=370,y=10,width=400, height=129)
        self.grid = ttk.Treeview(frame3, columns=("col1","col2","col3","col4", "col5", "col6"))        
        self.grid.column("#0",width=50)
        self.grid.column("col1",width=50, anchor=CENTER)
        self.grid.column("col2",width=50, anchor=CENTER)
        self.grid.column("col3",width=50, anchor=CENTER)
        self.grid.column("col4",width=50, anchor=CENTER)
        self.grid.column("col5",width=50, anchor=CENTER)
        self.grid.column("col6",width=50, anchor=CENTER)
        #self.grid.column("col7",width=50, anchor=CENTER)

        self.grid.heading("#0", text="Nro.", anchor=CENTER)
        self.grid.heading("col1", text="mot1", anchor=CENTER)
        self.grid.heading("col2", text="mot2", anchor=CENTER)
        self.grid.heading("col3", text="mot3", anchor=CENTER)
        self.grid.heading("col4", text="mot4", anchor=CENTER) 
        self.grid.heading("col5", text="mot5", anchor=CENTER)
        self.grid.heading("col6", text="mot6", anchor=CENTER)
        #self.grid.heading("col7", text="mot7", anchor=CENTER)
        self.grid.pack(side=LEFT,fill = Y)
        sb = Scrollbar(frame3, orient=VERTICAL)
        sb.pack(side=RIGHT, fill = Y)
        self.grid.config(yscrollcommand=sb.set)
        sb.config(command=self.grid.yview)
        self.grid['selectmode']='browse'

        Frbdmotores=Frame(self,width=300,height=100,bg='gray22')
        Frbdmotores.place(x=370,y=150)
        self.btn1 =Button(Frbdmotores ,text="Modificar",command=self.fModificar,fg="white",bg="gray22")
        self.btn1.place(x=5, y=5)
        self.btn2=Button(Frbdmotores ,text="Guardar cambios",command=self.guardarcambios,fg="white",bg="gray22")
        self.btn2.place(x=80, y=5)
        self.btn3=Button(Frbdmotores ,text="Eliminar",command=self.fEliminar,fg="white",bg="gray22")
        self.btn3.place(x=190, y=5)
        self.btn4=Button(Frbdmotores ,text="Enviar",command=self.envi_motors,fg="white",bg="gray22")
        self.btn4.place(x=250, y=5)
        self.btn5=Button(Frbdmotores ,text="Agregar nuevo ciclo",command=self.agregar_ciclo_nuevo,fg="white",bg="gray22" )
        self.btn5.place(x=40, y=35)
        self.btn6=Button(Frbdmotores ,text="borrar ciclo",command=self.borrar_ciclo,fg="white",bg="gray22")
        self.btn6.place(x=180, y=35)
        self.btn7=Button(Frbdmotores ,text="añadir al ciclo",command=self.agregar_ciclo_Mod,fg="white",bg="gray22")
        self.btn7.place(x=5, y=65)

        paux=Frame(self)
        paux.place(x=370,y=260)
        newscroll=Scrollbar(paux)
        newscroll.pack(side='right',fill='y')
        self.txtres=Text(paux,width=25,height=4,yscrollcommand=newscroll.set)
        self.txtres.pack(side='left')
        newscroll.config(command=self.txtres.yview)
        
        principal=Frame(self,width=250,height=70,bg='gray22')
        principal.place(x=370,y=350)
        Radiobutton(principal,text="CONFIGURAR",value=1,variable=self.mode,bg="DeepSkyBlue").place(x=10,y=5)
        Radiobutton(principal,text="CORRER",value=2,variable=self.mode,bg="DeepSkyBlue").place(x=10,y=35)
        Button(principal ,text="OK", command=self.fnMode,fg="white",bg="gray22").place(x=200,y=8)

        FrEjecutar=Frame(self,width=290,height=190,bg='gray22')
        FrEjecutar.place(x=850,y=10)
        self.btn7= Button(FrEjecutar,text="INICIAR",command=self.fstart_ciclo, fg="white",bg="green")
        self.btn7.place(x=10, y=5)
        self.btn8=Button(FrEjecutar,text="Detener",command=self.fpausa,fg="white",bg="red")
        self.btn8.place(x=10, y=35)
        self.btn10=Button(FrEjecutar,text="Continuar",command=self.fncontinue,fg="white",bg="red")
        self.btn10.place(x=10, y=65)
        self.btn9=Button(FrEjecutar,text="FINALIZAR",command=self.fstop_ciclo,fg="white",bg="dodger blue")
        self.btn9.place(x=10, y=95)
        self.cbblistaCiclo= ttk.Combobox(FrEjecutar,width=30, state= 'readonly')
        self.cbblistaCiclo.place(x=10, y= 125)
        #cantidadC = open('cantidadCiclos.txt')
        #self.listaCiclo = cantidadC.readlines()
        #cantidadC.close()
        self.cbblistaCiclo['values']= self.listaCiclo
        #self.cbblistaCiclo.current(0)

        FrCamara=Frame(self,width=480,height=480,bg='gray22')
        FrCamara.place(x=675,y=260)
        self.lblVideo = Label(FrCamara)
        self.lblVideo.grid(column=0, row=3, columnspan=2)
        

        '''
        sensores=Frame(FrEjecutar ,width=270,height=60,bg="gray22")
        sensores.place(x=5,y=125)
        Label(sensores,text="Detector de color: ",fg="white",bg="gray22").place(x=5,y=5)
        Label(sensores,width=6,textvariable=self.value_color,fg="white",bg="gray22").place(x=130,y=5)
        Label(sensores,text="Presencia de objeto: ",fg="white",bg="gray22").place(x=5,y=35)
        Label(sensores,width=18, textvariable=self.value_pres ,fg="white",bg="gray22").place(x=130,y=35)
        '''