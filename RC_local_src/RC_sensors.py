#from sense_hat import SenseHat
#from time import *
#import paho.mqtt.client as mqtt
import json
import mysql.connector
from threading import Timer, Lock
from time import sleep
import signal
import sys
from sense_hat import SenseHat
from time import sleep
import datetime
host = '127.0.0.1'
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
        self.lock = Lock()
        self.db = mysql.connector.connect(host='43.201.122.161', user='sohn', password='1234', database='sohnDB', auth_plugin='mysql_native_password')
        self.cur = self.db.cursor()
        #self.client = mqtt.Client()
        #self.client.on_connect = self.on_connect
        #self.client.on_disconnect = self.on_disconnect
        #self.client.on_publish = self.on_publish
        #self.client.connect(host,port)
    def sensing_all(self):
        self.accelerometer = self.sense.get_accelerometer()
        self.compass = self.sense.get_compass()
        self.gyroscope = self.sense.get_gyroscope()
        self.humidity = self.sense.get_humidity()
        self.pressure = self.sense.get_pressure()
        self.temperature = self.sense.get_temperature()
        self.time = datetime.datetime.now()
    def get_all(self):
        self.sensing_all()
        self.query = "insert into sensing(time, acc_roll, acc_pitch, acc_yaw, gyro_roll , gyro_pitch,gyro_yaw , temperature , barometric , humidity) values (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s)"
        self.value = (self.time, self.accelerometer['roll'] , self.accelerometer['pitch'] ,self.accelerometer['yaw'] , self.gyroscope['roll'] ,self.gyroscope['pitch'],self.gyroscope['yaw'] , self.temperature ,
        self.pressure,self.humidity)

        self.lock.acquire()
        self.cur.execute(self.query, self.value)
        self.db.commit()
        self.lock.release()
    def play(self):
        while True:
            self.get_all()
            #self.client.loop_start()
            #self.client.publish('common' , self.get_all() , 1)
            #self.client.loop_stop()
            sleep(1)
s = Sensors()
if __name__ == "__main__":
    try:
        s.play()
    except KeyboardInterrupt:
        #s.client.disconnect()
        exit
        #sys.exit()
