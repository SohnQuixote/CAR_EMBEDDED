from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
import mysql.connector
from threading import Timer, Lock
from time import sleep
import signal
import sys
from sense_hat import SenseHat
from time import sleep
import datetime

def closeDB(signal, frame):
    print("BYE")
    mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
    cur.close()
    db.close()
    timer.cancel()
    timer2.cancel()
    sys.exit(0)

def polling():
    global cur, db, ready
    
    lock.acquire()
    cur.execute("select * from command order by time desc limit 1")
    for (id, time, cmd_string, arg_string, is_finish) in cur:
        if is_finish == 1 : break
        ready = (cmd_string, arg_string)
        cur.execute("update command set is_finish=1 where is_finish=0")

    db.commit()
    lock.release()
     
    global timer
    timer = Timer(0.1, polling)
    timer.start()

def sensing():
    global cur, db, sense

    pressure = sense.get_pressure()
    temp = sense.get_temperature()
    humidity = sense.get_humidity()

    time = datetime.datetime.now()
    num1 = round(pressure / 10000, 3)
    num2 = round(temp / 100, 2)
    num3 = round(humidity / 100, 2)
    meta_string = '0|0|0'
    is_finish = 0

    print(num1, num2, num3)
    query = "insert into sensing(time, num1, num2, num3, meta_string, is_finish) values (%s, %s, %s, %s, %s, %s)"
    value = (time, num1, num2, num3, meta_string, is_finish)

    lock.acquire()
    cur.execute(query, value)
    db.commit()
    lock.release()

    global timer2
    timer2 = Timer(1, sensing)
    timer2.start()

def go():
    myMotor.setSpeed(200)
    myMotor.run(Raspi_MotorHAT.FORWARD)

def back():
    myMotor.setSpeed(200)
    myMotor.run(Raspi_MotorHAT.BACKWARD)

def stop():
    myMotor.setSpeed(200)
    pwm.setPWM(0, 0, 330)

    myMotor.run(Raspi_MotorHAT.RELEASE)

def left():
    pwm.setPWM(0, 0, 250)

def mid():
    pass
def right():
    pwm.setPWM(0, 0, 410)

#init
lock = Lock()
db = mysql.connector.connect(host='43.201.122.161', user='sohn', password='1234', database='sohnDB', auth_plugin='mysql_native_password')
cur = db.cursor()
ready = None
timer = None

mh = Raspi_MotorHAT(addr=0x6f)
myMotor = mh.getMotor(2)
pwm = PWM(0x6F)
pwm.setPWMFreq(50)

sense = SenseHat()
timer2 = None
signal.signal(signal.SIGINT, closeDB)
class DB():

	def __init__(self):
		
		polling()
		sensing()

		#main thread
		while True:
			sleep(0.1)
			global ready
			if ready == None : continue

			cmd, arg = ready
			ready = None

			if cmd == "up" : go()
			if cmd == "back" : back()
			if cmd == "stop" : stop()
			if cmd == "left" : left()
			if cmd == "mid" : mid()
			if cmd == "right" : right()
if __name__ == "__main__":
	db = DB()
