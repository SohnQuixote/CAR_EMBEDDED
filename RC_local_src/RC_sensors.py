from sense_hat import SenseHat
from time import *
import paho.mqtt.client as mqtt
import json
host = 'localhost'
port = 1883


class Sensors(object):
    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
        else:
            print("Bad connection Returned code=", rc)


    def on_disconnect(self,client, userdata, flags, rc=0):
        print(str(rc))


    def on_publish(self,client, userdata, mid):
        print("In on_pub callback mid= ", mid)
    
    def __init__(self):
        global host
        global port
        self.sense = SenseHat()
        self.accelerometer = self.sense.get_accelerometer()
        self.compass = self.sense.get_compass()
        self.gyroscope = self.sense.get_gyroscope()
        self.humidity = self.sense.get_humidity()
        self.pressure = self.sense.get_pressure()
        self.temperature = self.sense.get_temperature()
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.connect(host,port)
    def sensing_all(self):
        self.accelerometer = self.sense.get_accelerometer()
        self.compass = self.sense.get_compass()
        self.gyroscope = self.sense.get_gyroscope()
        self.humidity = self.sense.get_humidity()
        self.pressure = self.sense.get_pressure()
        self.temperature = self.sense.get_temperature()
    def get_all(self):
        self.sensing_all()
        result = json.dumps({"accelerometer" : self.accelerometer , "compass":self.compass , "gyroscope":self.gyroscope , "humidity":self.humidity , "pressure":self.pressure , "temperature":self.
            temperature})
        return result
    def play(self):
        while True:
            #print(self.get_all())
            self.client.loop_start()
            self.client.publish('common' , self.get_all() , 1)
            self.client.loop_stop()
            sleep(1)
s = Sensors()
if __name__ == "__main__":
    try:
        s.play()
    except KeyboardInterrupt:
        s.client.disconnect()
        exit
        #sys.exit()
