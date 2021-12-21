# -*- coding: UTF-8 -*-
# Script de lectura del código QR e imprime en pantalla
# este material es GNU captura imagenes con pyOpenCV
# reconoce codigos QR cpn pyzbar
import sys
import cv2
import numpy as np
from pyzbar.pyzbar import decode  # pip install zba r

# captura de imagen
cam1 = cv2.VideoCapture(1) #Abre la camara de video, con el numero 0 se abre la cámara de la compu, 1 para otras cámaras

cam1.set(3, 640)  #Tamaño de las imágenes que vamos a capturar
cam1.set(4, 480)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 20]  # Formato de la cámara en JPEG

sin_qr = 0

print("Presione s para salir del programa")

while (cam1.isOpened()):      # Mientras la cámara esté abierta realizamos el proceso de captura
    ret, frame = cam1.read()

    # detecta codigo qr cuando no reproduce video
    for barcode in decode(frame):   # la camara lee una imagen y se guarda en la variable frame
        myData = barcode.data.decode('utf-8') #Se decodifica el código QR
        print(myData) # Se imprime en pantalla el código decodificado
        pts = np.array([barcode.polygon], np.int32) # Se dibuja un recuadro en cada uno de los códigos detectados
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, (0, 255, 0), 2)  #Se convierte en texto lo que se decodifica en el código QR
        pts2 = barcode.rect
        cv2.putText(frame, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

    cv2.imshow('Introduzca su receta con Codigo QR', frame)

    # Sale del programa al presionar la tecla "s"
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

cam1.release()
cv2.destroyAllWindows()
