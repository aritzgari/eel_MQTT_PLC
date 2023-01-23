#Para instalar pip install Eel
import paho.mqtt.client as mqtt
import eel

eel.init('web') 

# Iniciación de variables.
broker = "localhost"
port = 1883
diccionario = {}
lista = []

#Permite activar una salida del plc al dar la orden a Node-red mediante MQTT
@eel.expose
def activarpy():
    client1 = mqtt.Client("Pruebas")
    client1.connect(broker, port)
    client1.publish("Boton", True)

#Permite desactivar salidas del plc al dar la orden a Node-red mediante MQTT
@eel.expose
def desactivarpy():
    client1 = mqtt.Client("Pruebas")
    client1.connect(broker, port)
    client1.publish("Boton", False)

#Este apartado te permite tomar datos del PLC 
@eel.expose
def datospy():
    # Función lanzada al intentar establecer la conexión
    def on_connect(client, userdata, flags, rc):
        # Esto se muestra al conectar. El código debería de ser 0 si es sin errores.
        # print(f"Connected with result code {rc}")
        # El nombre del topic al que hay que conectarse.
        client.subscribe("Datos")
        
    # Lo obtenido del mensaje 
    def on_message(client, userdata, msg):
        global lista
        # Comprobar que le llega la información
        print(f"Message received [{msg.topic}]: {msg.payload}")
        # Pasamos la información a una variable a tratar
        diccionario = {msg.topic: msg.payload}
        # Decodificar de tipo bytes a string
        diccionario = diccionario['Datos'].decode(
            'UTF-8').replace("false", "False").replace("true", "True")
        # Pasar del string a diccionario.
        diccionario = eval(diccionario)
        # Parar el loop una vez completado un pedido de datos
        if diccionario['Salida']==True:
            diccionario['Salida']="Encendido"
        else:
            diccionario['Salida']="Apagado"
        #Poner todo en una sola lista a enviar    
        lista = [diccionario['Salida'], diccionario['Real'],
                 diccionario['Entero'], diccionario['Output']]
        # Parece que al poner esto aqui se controla un poco el flujo de peticiones o algo y permite que no se atasque.
        client.loop_stop()
        
    # Conectar y tomar los datos
    client = mqtt.Client("Pruebas")
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    # loop de escucha en este caso es con start para poder seguir ejecutando la pantalla
    client.connect('127.0.0.1', 1883)
    client.loop_start()
    
    return lista

#Este apartado te permite escribir variables reales en PLC
@eel.expose
def inputdatos(a):
    client1 = mqtt.Client("Pruebas")
    client1.connect(broker, port)
    client1.publish("Input", a)


eel.start('main.html')




