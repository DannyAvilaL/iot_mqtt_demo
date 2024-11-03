// Include the Wire library for I2C
#include <Wire.h>
#include <Servo.h>

// LED on pin 13
const int ledPin = 13; 
//Pin a conectar el servo
int pinServo = 2;

//Se crea un nuevo objeto del servo
Servo servo;


void setup() {
  // Iniciando la conexion al bus
  Wire.begin(0x8);
  servo.attach(pinServo);

  Serial.begin(9600);
  
  // Callback para cuando se reciba un mensaje por i2c          
  Wire.onReceive(receiveEvent);

  // pin 13 para encender y apagar el led
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}

// Funcion que se ejecuta como callback
void receiveEvent(int howMany) {
  while (Wire.available()) 
  {
    int command = Wire.read(); // Leyendo los bytes
    Serial.println(command);

    // En caso de que se quiera abrir o cerrar la puerta
    if(command == 1)
    {
      servo.write(180);
    }
    else if (command == 0)
    {
      servo.write(0);
    } // en caso de que sea encender o apagr el led
    else if (command == 2) {
      digitalWrite(ledPin, 0);
    }
    else if (command == 3) {
      digitalWrite(ledPin, 1);
    }

    Wire.write(1);
  }
}


void loop() {
  delay(100);
}