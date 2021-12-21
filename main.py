from ClaseProyectoV3 import MainFrame
from tkinter import Label, Tk, PhotoImage
def main():
    root = Tk()
    root.wm_title("control de brazo robotico")
    app = MainFrame(root)
    #imagen=PhotoImage(file="E:/fiuna2_2021/R1/Proyecto/proyecto_V2/foto.gif")
    #Label(root,image=imagen).place(x=700,y=200)
    app.mainloop()
if __name__=="__main__":
    main()

    