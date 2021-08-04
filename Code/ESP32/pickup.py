from machine import Pin
from notifier import Notifier as nt
from utime import ticks_ms
msecs = ticks_ms()
        
class Status():
    
    def __init__(self):
        self.hi = Pin(2, Pin.IN)
        self.fi = msecs
        self.chori_ka_flag = False
    
    def robot_lifted(self):
        if (self.hi.value()==0) and (self.chori_ka_flag == False):
            self.chori_ka_flag = True
            self.fi=msecs
            print("cool")
        if self.hi.value()==1 and self.chori_ka_flag:
            self.chori_ka_flag = False
            self.fi=msecs
            print("chori")
            nt.robot_lifted()