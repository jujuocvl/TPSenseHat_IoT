'''from sense_hat import SenseHat
sense = SenseHat()

sense.show_message("IOT Forever", text_colour=[0,0,255])'''

'''import time
from sense_hat import SenseHat
sense = SenseHat()
sense.show_letter("H", text_colour=[0,0,255], back_colour=[255, 0, 0])
time.sleep(2)
sense.clear()'''

'''import time
from sense_hat import SenseHat
sense = SenseHat()
sense.set_pixel(3,3, 255, 165, 0)
sense.set_pixel(3,4, 255, 165, 0)
sense.set_pixel(4,3, 255, 165, 0)
sense.set_pixel(4,4, 255, 165, 0)
time.sleep(2)
sense.clear()'''

'''import time
from sense_hat import SenseHat
sense = SenseHat()
x = [0, 255, 0] # vert
o = [255, 255, 255] # blanc
border = [
x, x, x, x, x, x, x, x,
x, o, o, o, o, o, o, x,
x, o, o, o, o, o, o, x,
x, o, o, o, o, o, o, x,
x, o, o, o, o, o, o, x,
x, o, o, o, o, o, o, x,
x, o, o, o, o, o, o, x,
x, x, x, x, x, x, x, x
]
sense.set_pixels(border)
time.sleep(2)
sense.clear()'''

'''from sense_hat import SenseHat
import time
sense = SenseHat()
sense.set_rotation(180)
sense.show_letter("L")
time.sleep(2)
sense.clear()'''

'''--------------------------------------HUMIDITY TEMPERATURE PRESSURE get_humidity(), _pressure(), _temperature()-----------------------------------------------'''
'''from sense_hat import SenseHat
import time
sense = SenseHat()
humidity = sense.get_humidity()
print(humidity)
time.sleep(3)
pressure = sense.get_pressure()
print(pressure)
time.sleep(3)
temperature = sense.get_temperature()
print(temeprature)
time.sleep(3)'''

'''----------------------------------------------------------ORIENTATION-----------------------------------------------------------------------------------------
from sense_hat import SenseHat
sense = SenseHat()
while True:
    pos = sense.get_orientation()
    print("pitch: {}, roll: {}, yaw: {}".format(pos["pitch"], pos["roll"],pos["yaw"]))'''

'''from sense_hat import SenseHat
sense = SenseHat()
while True:
    pos = sense.get_accelerometer_raw()
    if pos['x']>1 and pos['y']>1 and pos['z']>1 :
        print("x: {}, y: {}, z: {}".format(pos["x"], pos["y"], pos["z"]))'''

'''----------------------------------------------------------JOYSTICK-----------------------------------------------------------------------------------------
from sense_hat import SenseHat
sense = SenseHat()
while True:
    for event in sense.stick.get_events():
        print("The joystick was {} {}".format(event.action, event.direction))


from sense_hat import SenseHat
from signal import pause
sense = SenseHat()
def hello(event):
    print("toto")
sense.stick.direction_middle = hello
pause()'''

'''----------------------------------------------------------EXO RECAP-----------------------------------------------------------------------------------------'''

from sense_hat import SenseHat
from signal import pause
from threading import Timer
import paho.mqtt.client as mqtt

import time
mqttclient = mqtt.Client()
sense = SenseHat()
mode = None

mqttclient.loop_start()

class Repeat(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args,**self.kwargs)

def temperature():
    global mode
    mode="temperature"
    sense.show_letter("T", text_colour=[0,255,0])

def humidity():
    global mode
    mode = "humidity"
    sense.show_letter("H", text_colour=[0,255,0])
    

def acceleration():
    global mode
    mode = "accel"
    sense.show_letter("A", text_colour=[255,255,0])

def pressure():
    global mode
    mode = "pressure"
    sense.show_letter("P", text_colour=[0,255,0])

def all():
    global mode
    mode = "all"
    sense.show_letter("C", text_colour=[255,128,0])

def stop(event):
    global mode
    mode ="stop"
    print(event.action)
    if event.action == "held":
        h.cancel()
        t.cancel()
        a.cancel()
        p.cancel()
        exit()  
    sense.show_letter("S", text_colour=[255,0,0])
    time.sleep(2)
    sense.clear()

def printHumidity():
    global mode
    if mode == "humidity":
        hum = sense.get_humidity()
        print(f"Humidité : {hum}")
        mqttclient.publish("Orcival/rpi/humidity", payload=hum, qos=0, retain=True)
    

def printTemperature():
    global mode
    if mode == "temperature":
        temp = sense.get_temperature()
        print(f"Temperature : {temp}")
        mqttclient.publish("Orcival/rpi/temperature", payload=temp, qos=0, retain=True)

def printAcceleration():
    global mode
    if mode =="accel":
        pos = sense.get_accelerometer_raw()
        if pos['x']>1 or pos['y']>1 or pos['z']>1.2 :
            print("Accélération -> x: {}, y: {}, z: {}".format(pos["x"], pos["y"], pos["z"]))
            mqttclient.publish("Orcival/rpi/acceleration", payload=json.dumps(pos), qos=0, retain=True)

def printPressure():
    global mode
    if mode == "pressure":
        pres = sense.get_pressure()
        print(f"Pressure : {pres}")
        mqttclient.publish("Orcival/rpi/pressure", payload=pres, qos=0, retain=True)

sense.stick.direction_up = temperature
sense.stick.direction_down = humidity   
sense.stick.direction_right = pressure
sense.stick.direction_middle = stop
sense.stick.direction_left = acceleration

#lambda pour exécuter la fonction et pas juste utiliser le résultat de la fonction
t = Repeat(1.0, lambda: printTemperature()) 
t.start()

a = Repeat(0.1, lambda: printAcceleration())
a.start()

p = Repeat(1.0, lambda: printPressure())
p.start()

h = Repeat(1.0, lambda: printHumidity())
h.start()

mqttclient.loop_stop()


        
        
    





