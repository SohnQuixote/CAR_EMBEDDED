
from Raspi_MotorHAT import Raspi_MotorHAT,Raspi_DCMotor
import time
from pyPS4Controller.controller import Controller
from sense_hat import SenseHat
import socket
import threading
HOST = '192.168.20.24' 
PORT = 12345 
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST,PORT))
'''

on_x_press
on_x_release
on_triangle_press
on_triangle_release
on_circle_press
on_circle_release
on_square_press
on_square_release
on_L1_press
on_L1_release
on_L2_press
on_L2_release
on_R1_press
on_R1_release
on_R2_press
on_R2_release
on_up_arrow_press
on_up_down_arrow_release
on_down_arrow_press
on_left_arrow_press
on_left_right_arrow_release
on_right_arrow_press
on_L3_up
on_L3_down
on_L3_left
on_L3_right
on_L3_x_at_rest  # L3 joystick is at rest after the joystick was moved and let go off on x axis
on_L3_y_at_rest  # L3 joystick is at rest after the joystick was moved and let go off on y axis
on_L3_press  # L3 joystick is clicked. This event is only detected when connecting without ds4drv
on_L3_release  # L3 joystick is released after the click. This event is only detected when connecting without ds4drv
on_R3_up
on_R3_down
on_R3_left
on_R3_right
on_R3_x_at_rest  # R3 joystick is at rest after the joystick was moved and let go off on x axis
on_R3_y_at_rest  # R3 joystick is at rest after the joystick was moved and let go off on y axis
on_R3_press  # R3 joystick is clicked. This event is only detected when connecting without ds4drv
on_R3_release  # R3 joystick is released after the click. This event is only detected when connecting without ds4drv
on_options_press
on_options_release
on_share_press  # this event is only detected when connecting without ds4drv
on_share_release  # this event is only detected when connecting without ds4drv
on_playstation_button_press  # this event is only detected when connecting without ds4drv
on_playstation_button_release  # this event is only detected when connecting without ds4drv






'''
R = [255,0,0]
X = [255,255,255]

'''
UP = [
X,X,X,X,X,X,X,X,
X,X,X,X,X,X,X,X,
X,X,X,X,X,X,X,X,
X,X,X,X,X,X,X,X,
X,X,X,X,X,X,X,X,
X,X,X,X,X,X,X,X,
X,X,X,X,X,X,X,X,
X,X,X,X,X,X,X,X,

]


'''



RIGHT = [
X,X,X,R,R,X,X,X,
X,X,R,R,R,R,X,X,
X,R,R,R,R,R,R,X,
X,X,X,R,R,X,X,X,
X,X,X,R,R,X,X,X,
X,X,X,R,R,X,X,X,
X,X,X,R,R,X,X,X,
X,X,X,R,R,X,X,X,

]

LEFT = [
X,X,X,R,R,X,X,X,
X,X,X,R,R,X,X,X,
X,X,X,R,R,X,X,X,
X,X,X,R,R,X,X,X,
X,X,X,R,R,X,X,X,
X,R,R,R,R,R,R,X,
X,X,R,R,R,R,X,X,
X,X,X,R,R,X,X,X,

]

UP = [
X,X,X,X,X,X,X,X,
X,X,R,X,X,X,X,X,
X,R,R,X,X,X,X,X,
R,R,R,R,R,R,R,R,
R,R,R,R,R,R,R,R,
X,R,R,X,X,X,X,X,
X,X,R,X,X,X,X,X,
X,X,X,X,X,X,X,X,

]
DOWN = [
X,X,X,X,X,X,X,X,
X,X,X,X,X,R,X,X,
X,X,X,X,X,R,R,X,
R,R,R,R,R,R,R,R,
R,R,R,R,R,R,R,R,
X,X,X,X,X,R,R,X,
X,X,X,X,X,R,X,X,
X,X,X,X,X,X,X,X,

]
IDLE = [
X,X,R,R,R,X,X,X,
X,R,X,X,X,R,R,X,
R,X,R,R,X,X,X,R,
R,X,X,X,X,R,X,R,
R,X,X,X,X,R,X,R,
R,X,R,R,X,X,X,R,
X,R,X,X,X,R,R,X,
X,X,R,R,R,R,X,X,

]

class RC_control(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.mh =  Raspi_MotorHAT(addr = 0x6f)
        self.myMotor = self.mh.getMotor(2)
        self.servo = self.mh._pwm
        self.servo.setPWMFreq(50)
        self.myMotor.setSpeed(150)
        self.speed = 0
        self.left = 250
        self.dir = 330
        self.right = 410
        self.max = 32767
        self.dir_max = 80
        self.sense = SenseHat()
        self.sense.clear()  

    def on_L3_up(self, value):
        #value의 범위를 모르겠음
        if(value<0):
            value = -value
        self.speed = (value/self.max) * 255
        self.speed = (int)(self.speed)
        self.myMotor.setSpeed(self.speed)
        self.myMotor.run(Raspi_MotorHAT.FORWARD)
        self.sense.set_pixels(UP)
        #print("speed"+str(value))

    def on_L3_left(self, value):
        
        if(value<0):
            value = -value
        self.dir = (value/self.max) * self.dir_max
        self.dir = 330 - self.dir
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
        self.sense.set_pixels(DOWN)
        #print("speed"+str(value))

    def on_L3_right(self, value):
        if(value<0):
            value = -value
        self.dir = (value / self.max) * self.dir_max
        self.dir += 330
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
    def on_R3_up(self,value):
        pass
    def on_R3_down(self,value):
        pass
    def on_R3_right(self,value):
        pass
    def on_R3_left(self,value):
        pass
class SERVER_control(Controller):
    def __init__(self,**kwargs):
        Controller.__init__(self, **kwargs)
        self.s = None
    def on_L3_up(self,value):
        pass
    def on_L3_down(self,value):
        pass
    def on_L3_right(self,value):
        pass
    def on_L3_left(self,value):
        pass
    def on_R3_up(self,value):
        if(self.s != None):
            self.s.send(("F"+(str)(value)).encode())
            repl = self.s.recv(1024)
    def on_R3_down(self,value):
        if(self.s != None):
            self.s.send(("B"+(str)(value)).encode())
            repl = self.s.recv(1024)
    def on_R3_right(self,value):
        if(self.s != None):
            self.s.send(("R"+(str)(value)).encode())
            repl = self.s.recv(1024)
    def on_R3_left(self,value):
        if(self.s != None):
            self.s.send(("L"+(str)(value)).encode())
            repl = self.s.recv(1024)
    def on_square_press(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST,PORT))
    def on_triangle_press(self):
        self.s.send(("A").encode())
        self.s.close()
        self.s = None
    def on_R1_press(self):
        self.s.send(("S").encode())

def main_control():
    controller = RC_control(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()
def serve_control():
    server_con = SERVER_control(interface="/dev/input/js0", connecting_using_ds4drv=False)
    server_con.listen()
class RC(object):
    def __init__(self):
        t1 = threading.Thread(target = main_control)
        t2 = threading.Thread(target = serve_control)
        t1.start()
        t2.start()

if __name__ == "__main__":
    RC_obj = RC()
