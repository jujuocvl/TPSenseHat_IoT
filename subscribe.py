import paho.mqtt.client as mqtt
# fonction appelée chaque fois qu'un nouveau message est publié sur un topic auquel on est abonné
def on_message(client, userdata, msg):
    print(msg.topic + " : " + msg.payload.decode("utf-8") )

mqttclient = mqtt.Client()
mqttclient.connect("192.168.3.174")
mqttclient.on_message = on_message
# ici on s'abonne au topic rpi/couleurs avec une qos de zéro.
mqttclient.subscribe("Orcival/rpi/#", qos=0)
# boucle infinie de scrutation du broker
mqttclient.loop_forever()