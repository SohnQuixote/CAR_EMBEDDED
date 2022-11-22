from RC_main_control import RC
from RC_sensors import Sensors
import threading
from time import sleep
def control():
    pass
    car = RC()
def sense():
    s = Sensors()
    s.play()
t1 = threading.Thread(target = control )
t2 = threading.Thread(target = sense )
t1.start()
t2.start()

t1.join()
t2.join()
