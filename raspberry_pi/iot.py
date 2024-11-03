import paho.mqtt.client as mqtt
from smbus import SMBus

# Parámetros de configuración
broker = ""
port = 8883
topic = "pico/luz"

username = "" 
password = ""


addr = 0x8 # bus address
bus = SMBus(1) # para usar /dev/ic2-1


# Callback cuando se establece la conexión
def on_connect(client, userdata, flags, rc):
    print("Conectado con código de resultado " + str(rc))
    if rc == 0:
        print("Suscribiéndose al tópico")
        client.subscribe("pico/luz")
        client.subscribe("pico/puerta")
    else:
        print("Error al conectarse, código: " + str(rc))

# Callback cuando se recibe un mensaje
def on_message(client, userdata, msg):
    mensaje = float(msg.payload.decode())
    print("Mensaje recibido: " + msg.topic + " -> " + str(mensaje))
    
    if msg.topic == "pico/puerta":
        if mensaje == 1:
            bus.write_byte(addr, 0) # Envia mensaje para abrir
        else:
            bus.write_byte(addr, 1) # Envia mensaje para cerrar
    
    if msg.topic == "pico/luz":
        print("Intensidad de luz", mensaje)
        if mensaje > 70:
            bus.write_byte(addr, 2) # envia mensaje para apagar
        else:
            bus.write_byte(addr, 3) # envia mensaje para encender

def on_subscribe(client, userdata, mid, granted_qos):
    print("Suscrito a: "+str(mid)+" "+str(granted_qos))

# Callback para mensajes de log y que aparezcan en terminal
def on_log(client, userdata, level, buf):
    print("Log: ", buf)

# Crear una instancia del cliente MQTT
client = mqtt.Client(client_id="raspberrypi", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)

# Asignar callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_log = on_log

# Activando TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# Establecer usuario y contraseña
client.username_pw_set(username, password)

# Conectar al broker
client.connect(broker, port, 60)

# Mantener la conexión abierta y escuchando mensajes
client.loop_forever(timeout=0.5)
