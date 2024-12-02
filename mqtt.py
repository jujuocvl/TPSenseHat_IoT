import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import json
import time
sense = SenseHat()

mqttclient = mqtt.Client()
mqttclient.connect("192.168.3.174") #ip broker
# Démarre la boucle de scrutation du réseau. Nécessaire pour que le mqttclient MQTT maintienne
# sa connection au broker. A faire une fois au début du programme
mqttclient.loop_start()

humidity = sense.get_humidity()
temperature = sense.get_temperature()
pressure = sense.get_pressure()
acceleration = sense.get_accelerometer_raw()

# exemple de publication de la valeur 58 sur un topic avec conservation de la dernière info publiée
'''while True:
    mqttclient.publish("Orcival/rpi/temperature", payload=temperature, qos=0, retain=True)
    mqttclient.publish("Orcival/rpi/humidity", payload=humidity, qos=0, retain=True)
    mqttclient.publish("Orcival/rpi/pressure", payload=pressure, qos=0, retain=True)
    mqttclient.publish("Orcival/rpi/acceleration", payload=json.dumps(acceleration), qos=0, retain=True)

    time.sleep(1)'''

# a faire a la fin du programme
mqttclient.loop_stop()