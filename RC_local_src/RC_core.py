from RC_main_control import RC
from RC_sensors import Sensors
#from RC_DB import DB
import threading
import signal
import sys

def signal_handler(sig,frame):
    t1.close()
    t2.close()
    sys.exit(0)

from time import sleep
def control():
    pass
    car = RC()
def sense():
    s = Sensors()
    s.play()
def db():
    db = DB()
t1 = threading.Thread(target = control )
t2 = threading.Thread(target = sense )
#t3 = threading.Thread(target = db)
t1.start()
t2.start()
#t3.start()
signal.signal(signal.SIGINT , signal_handler)

t1.join()
t2.join()
#t3.join()
