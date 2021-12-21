int dirPin1 = 8;
int dirPin2 = 9;
int speedPin = 10;
int speedMotor = 255;
void setup() {
  pinMode(dirPin1,OUTPUT);
  pinMode(dirPin2,OUTPUT);
  pinMode(speedPin,OUTPUT);

}

void loop() {
  analogWrite(speedPin, speedMotor);
  digitalWrite(dirPin1, 0);
  digitalWrite(dirPin2, 1);
  

}
