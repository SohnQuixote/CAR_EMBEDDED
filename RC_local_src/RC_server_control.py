import socket
import signal
HOST = '192.168.20.24'
from Raspi_MotorHAT import Raspi_MotorHAT,Raspi_DCMotor

def Bye(sig,frame):
    conn.close()

class RC_control():

    def __init__(self, **kwargs):
        #Controller.__init__(self, **kwargs)
        self.mh =  Raspi_MotorHAT(addr = 0x6f)
        self.myMotor = self.mh.getMotor(2)
        self.servo = self.mh._pwm
        self.servo.setPWMFreq(50)
        self.myMotor.setSpeed(150)
        self.speed = 0
        self.left = 200
        self.dir = 280
        self.right = 360
        self.max = 32767
        self.dir_max = 80
    def on_L3_up(self, value):
        #value의 범위를 모르겠음
        if(value<0):
            value = -value
        self.speed = (value/self.max) * 255
        self.speed = (int)(self.speed)
        self.myMotor.setSpeed(self.speed)
        self.myMotor.run(Raspi_MotorHAT.FORWARD)
        #print("speed"+str(value))

    def on_L3_left(self, value):
        
        if(value<0):
            value = -value
        self.dir = (value/self.max) * self.dir_max
        self.dir = 280 - self.dir
        self.dir = (int)(self.dir)
        self.servo.setPWM(0,0,self.dir)
        #self.sense.set_pixels(LEFT)
        #sleep(0.5)
        #print("dir"+str(self.dir))

    def on_L3_down(self, value):
        if(value<0):
            value = -value
        self.speed = (value / self.max) * 255
        self.speed = (int)(self.speed)
        self.myMotor.setSpeed(self.speed)

        self.myMotor.run(Raspi_MotorHAT.BACKWARD)
        #print("speed"+str(value))

    def on_L3_right(self, value):
        if(value<0):
            value = -value
        self.dir = (value / self.max) * self.dir_max
        self.dir += 280
        self.dir = (int)(self.dir)
        self.servo.setPWM(0, 0, self.dir)
        #self.sense.set_pixels(RIGHT)
        #sleep(0.5)
        #print("dir"+str(self.dir))

    def on_L3_x_at_rest(self):
        #self.myMotor.run(Raspi_MotorHAT.RELEASE)
        
        pass
    def on_L3_y_at_rest(self):
        #self.dir = 330
        #self.servo.setPWM(0,0,self.dir)
        pass
    def on_L1_press(self):
        pass

    def bye(self):
        self.myMotor.run(Raspi_MotorHAT.RELEASE)

# Server IP or Hostname
PORT = 12345 
# Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

#managing error exception
try:
    s.bind((HOST, PORT))
except socket.error:
    print ('Bind failed ')

s.listen(5)
print ('Socket awaiting messages')
(conn, addr) = s.accept()
print ('Connected')

RC = RC_control()


signal.signal(signal.SIGINT , Bye)


# awaiting for message
while True:
    data = None
    data = conn.recv(1024)
    if(len(data) ==0):
        continue
    if(data[0] == 65):
        (conn, addr) = s.accept()
    value = 0
    print(data)
    r_idx = 0
    l_idx = 0
    if(data[0] == 83):
        RC.bye()
    #print(data[0])
    if(len(data) <= 1):
        continue
    print (data[0])
    dir = data[0]
    #for i in range(1,len(data)):
        #if(data[i] == 70 or data[i] == 66 or data[i] == 82 or data[i] == 76):
            #r_idx = i
            #break
    #print(data[:r_idx])
    if (data[1] == 45):
        #idx = data.find(data[2:])
        #print(data[2:idx])
        value = (float)(data[2:])
        value = -value
        #l_idx = 2
        #print("good")
    elif(data[0] != 83 and len(data) >=2 ):
        #l_idx = 1
        #idx = data.find(data[1:])
        #print(data[1:idx])
        value = ((float)(data[1:]))
    
    #r_idx = data[l_idx:].find(70)
    #r_idx = min(r_idx,data[l_idx:].find(66))

    #r_idx = min(r_idx,data[l_idx:].find(82))
    #r_idx = min(r_idx,data[l_idx:].find(76))
    if(data[0] == 70):#F
        
        #value = ((float)(data[l_idx:r_idx]))

        RC.on_L3_up(value)
        #print("good")
        #print("good")
    elif(data[0] == 66):#B
    
        #value = ((float)(data[l_idx:r_idx]))
        RC.on_L3_down(value)
    elif(data[0] == 82):#R
    
        #value = ((float)(data[l_idx:r_idx]))
        RC.on_L3_right(value)
    elif(data[0] == 76): #L

        #value = ((float)(data[l_idx:r_idx]))
        RC.on_L3_left(value)
    elif(data[0] == 83):
        RC.bye()
    conn.send(("good)").encode())

    # Sending reply
	#conn.send(reply)
conn.close() 
# Close connections
