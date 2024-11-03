from machine import Pin, ADC
from time import sleep
import network
from umqtt.simple import MQTTClient
import config
import time

# Topicos
MQTT_TOPIC_TEMPERATURE = 'pico/temperature'
MQTT_TOPIC_LED = 'pico/led'
MQTT_TOPIC_LUZ = 'pico/luz'

# MQTT Parametros del archivo de confi.py
MQTT_SERVER = config.mqtt_server
MQTT_PORT = 0
MQTT_USER = config.mqtt_username
MQTT_PASSWORD = config.mqtt_password
MQTT_CLIENT_ID = b"raspberrypi_picow"
MQTT_KEEPALIVE = 7200
MQTT_SSL = True   # set to False if using local Mosquitto MQTT broker
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}

# PARA LEER LA TEMPERATURA
adcpin = 4
photoPIN = 26
# PARA EL LED
led = machine.Pin(15, machine.Pin.OUT)
led1 = machine.Pin('LED', machine.Pin.OUT) #Para saber que está enviando info

sensor = machine.ADC(adcpin)

def ReadTemperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)

def readLight(photoGP):
    photoRes = ADC(Pin(26))
    light = photoRes.read_u16()
    light = round(light/65535*100,2)
    return light


# Funcion para conectarse al wifi
def initialize_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # conectarse al router
    wlan.connect(ssid, password)

    # Espera a que la conexion se realice
    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        sleep(1)

    # Valida la conexión
    if wlan.status() != 3:
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True

# Fucion para conectarse al broker MQTT
def connect_mqtt():
    try:
        client = MQTTClient(client_id=MQTT_CLIENT_ID,
                            server=MQTT_SERVER,
                            port=MQTT_PORT,
                            user=MQTT_USER,
                            password=MQTT_PASSWORD,
                            keepalive=MQTT_KEEPALIVE,
                            ssl=MQTT_SSL,
                            ssl_params=MQTT_SSL_PARAMS)
        client.connect()
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)

# Funcion para publicar en el topico
def publish_mqtt(client, topic, value):
    client.publish(topic, value)
    print(topic, value)
    print("Publicado")
    
# Funcion para suscribirse a un topico
def subscribe_mqtt(client, topic):
    client.subscribe(topic)
    print('Suscribiendose a topico:', topic) 

# Callback que se ejecuta al recibir un mensaje por un tópico
def my_callback(topic, message):
    print('Mensaje recibido en topico:', topic)
    print('Mensaje:', message)
    
    # Para revisar si el led se prende o apaga
    if message == b'ON':
        print('Encendiendo LED')
        led.value(1) 
    elif message == b'OFF':
        print('Apagando LED')
        led.value(0)  # Turn LED OFF
    else:
        print('Comando inválido')

def main():
    try:
        if not initialize_wifi(config.wifi_ssid, config.wifi_password):
            print('Error al conectarse al wifi...finalizando ejecución')
        else:
            
            # Parpadeo de LED para indicar la conexión exitosa al router
            led1.value(True)
            time.sleep(1)  
            led1.value(False) 
            time.sleep(1)
            
            client = connect_mqtt()
            client.set_callback(my_callback)
            subscribe_mqtt(client, MQTT_TOPIC_LED)
            
            tiempo_inicial = time.time() 
            
            # Loop infinito
            while True:
                
                tiempo_actual = time.time() 
                diferencia = tiempo_actual - tiempo_inicial
                
                # Cada 10 segundos se lee y envía la info de la temperatura
                if diferencia >= 10:
                    temperature= ReadTemperature()
                    publish_mqtt(client, MQTT_TOPIC_TEMPERATURE, str(temperature))
                    tiempo_inicial = tiempo_actual
                    
                # Cada 2 segundos se lee y envía la info de pct de luz
                luz = readLight(photoPIN)
                publish_mqtt(client, MQTT_TOPIC_LUZ, str(luz))
                # Para actualizar la lectura de mensajes
                client.check_msg()
  
                # breve parpadeo para validar que hay comunicacion
                led1.value(True) 
                sleep(1)
                led1.value(False) 
                sleep(1)

    except Exception as e:
       print('Error main:', e)
    

main()
