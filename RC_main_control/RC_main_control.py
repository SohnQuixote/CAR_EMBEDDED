
from Raspi_MotorHAT import Raspi_MotorHAT,Raspi_DCMotor
import time
from pyPS4Controller.controller import Controller



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
        self.max = 45
        self.dir_max = 80
    def on_L3_up(self, value):
        #value의 범위를 모르겠음
        self.speed = (value/self.max) * 255
        self.myMotor.setSpeed(self.speed)
        self.myMotor.run(Raspi_MotorHAT.FORWARD)
        print(value)

    def on_L3_left(self, value):
        self.dir = (value/self.max) * self.dir_max
        self.dir +=250
        self.servo.setPWM(0,0,self.dir)
        print(value)

    def on_L3_down(self, value):
        self.speed = (value / self.max) * 255
        self.myMotor.setSpeed(self.speed)
        self.myMotor.run(Raspi_MotorHAT.BACKWARD)
        print(value)

    def on_L3_right(self, value):
        self.dir = (value / self.max) * self.dir_max
        self.dir += 330
        self.servo.setPWM(0, 0, self.dir)
        print(value)

    def on_L3_x_at_rest(self):
        self.myMotor.run(Raspi_MotorHAT.RELEASE)
        pass
    def on_L3_y_at_rest(self):
        pass
class RC(object):
    def __init__(self):
        controller = RC_control(interface="/dev/input/js0", connecting_using_ds4drv=False)
        controller.listen()

