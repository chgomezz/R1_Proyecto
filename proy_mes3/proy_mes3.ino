/*Código en arduino que controla un brazo robótico de 5 GDL
  PROYECTO FINAL DE ROBÓTICA 1
  9no Semestre
  Diciembre-2021
*/

#include <Servo.h> //libreria para utilizar los servomotores
#include <Ticker.h> //Libreria que permite llamar(ejecutar) funciones de forma repetida cada cierto periodo de tiempo
#include "libManuel1.h" //libreria para que almacena las funciones

String cadena;
void setup() {
Serial.begin(9600);
delay(30);
pinMode(13 , OUTPUT);

// lcd.begin(16, 2);
// lcd.print("Iniciando sensores...");

//Se inicializa los pines que van a controlar los servomotores
 myservo0.attach(11);  //Servo 0 - Base
 myservo1.attach(10); //Servo 1 - Hombro(Derecho)
 myservomotor.attach(9); //Servo trabaja en conjunto con 1  - Hombro(Izquierdo)
 myservo2.attach(6); //Servo 2 - Codo
 myservo3.attach(5); //Servo 3 - Muñeca
 myservo4.attach(4); //Servo 4 - Muñeca(Rotacion centro)
 myservo5.attach(3); //Servo 5 - Pinza
 myservo6.attach(2);  //Cinta tranportadora
 
 

//Se inicializan las funciones que se ejecutarán en ticker
 ticservo0.start();
 ticservo1.start();
// ticservo3.start();
 ticservo2.start();
 ticservo3.start();
 ticservo4.start();
 ticservo5.start();
 
 ticmovposicion.start();
 
 myservo0.write(pos0);
 myservo1.write(pos1);
 myservomotor.write(posmotor);
 myservo2.write(pos2);
 myservo3.write(pos3);
 myservo4.write(pos4);
 myservo5.write(pos5);
 delay(700);

}
void loop() {
   //Inicia movimiento de la cinta transportadora
  //Giro Sentido Horario
  myservo6.write(180);
  //Aquí se estarán actualizando con Ticker las funciones para los servomotores
  
 
  ticservo5.update();
 
  ticservo0.update();
  ticservo1.update();

  ticservo2.update();
  ticservo3.update();
  ticservo4.update();
 
  //Lectura para el Serial
  if(Serial.available()){
    cadena="";
    cadena= Serial.readString();
    fnActuadores(cadena); //Si hay algo en el serial se ejecuta la funcion fnActuadores
    
    }
  if (var==true){
    ticmovposicion.update(); //Sirve para ejecutar la secuencia del brazo robótico
  }
}
