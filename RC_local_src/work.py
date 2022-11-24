
from Raspi_MotorHAT import Raspi_MotorHAT,Raspi_DCMotor
import time
mh = Raspi_MotorHAT(addr = 0x6f)
myMotor = mh.getMotor(2)
servo = mh._pwm
servo.setPWMFreq(50)
myMotor.setSpeed(150)
myMotor.run(Raspi_MotorHAT.FORWARD)
time.sleep(1)
myMotor.run(Raspi_MotorHAT.RELEASE)
a=0
speed = 150
left = 250
middle = 330
right =410
while(True):
	command = input()
	if(command =="F"):
		myMotor.run(Raspi_MotorHAT.FORWARD)
	elif(command == "B"):
		myMotor.run(Raspi_MotorHAT.BACKWARD)
	elif(command == "S"):
		myMotor.run(Raspi_MotorHAT.RELEASE)
	elif(command =="+"):
		speed +=10
		print(speed)
	elif (command == "-"):
		speed -=10
		print(speed)
	if(speed <0):
		speed = 1
	if(speed>255):
		speed =255
	myMotor.setSpeed(speed)
	if(command =="L"):
		middle -=10
		if(middle<250):
			middle =250
		servo.setPWM(0,0,middle)
	elif(command == "R"):
		middle +=10
		if(middle>right):
			middle = right
		servo.setPWM(0,0,middle)
	elif(command ==  "M"):
		middle = 330
		servo.setPWM(0,0,330)
	elif(command == "FL"):
		middle = left
		servo.setPWM(0,0,middle)
	elif(command =="FR"):
		middle = right
		servo.setPWM(0,0,right)
	#servo.setPWM(0,0,200)
	#time.sleep(1)
	#servo.setPWM(0,0,330)
	#time.sleep(1)
	#servo.setPWM(0,0,430)
	#time.sleep(1)
	#a+=1
	#if(a==5):
		#break
