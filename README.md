# iot_mqtt_demo
Este es un proyecto de demostración para el uso de MQTT básico entre una Raspberry Pico W y una Raspberry Pi 4 + Arduino 1

El código se tiene en 3 partes:

- Arduino:
  - Se tiene un script .ino que lee la información por medio del protocolo I2C enviada por una raspberry Pi 4 (master)

- Raspberry Pi:
  - Script en python que lee la información del broker de HiveMQ por medio de MQTT y según los valores de los tópicos suscritos envía la señal al aruino (esclavo) para encender o apagar un led o mover un servomotor.

- Raspberry Pico W:
  - Script en python que lee la información de un sensor integrado de temperatura, y un fotoresistor para obtener el % de iluminación. Envía estos datos a través de los tópicos definidos

## Tópicos creados

- pico/temperatura --> Raspberry Pico W (publissher), Raspberry Pi (suscritptor)
- pico/puerta --> Raspberry Pico W (publissher), Raspberry Pi (suscritptor)
- pico/luz --> Raspberry Pico W (publissher), Raspberry Pi (suscritptor)
- pico/led --> Raspberry Pico W (suscriptor)



