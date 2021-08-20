import RPi.GPIO as GPIO
from time import sleep

class DMDBase(object):
    GPIO.setwarnings(False)
    
    def __init__(self, layout):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(layout.A, GPIO.OUT)
        GPIO.setup(layout.B, GPIO.OUT)
        GPIO.setup(layout.STROBE, GPIO.OUT)
        GPIO.setup(layout.OE, GPIO.OUT)
        
        #self.pwm = GPIO.PWM(layout.OE, 1000)
        
        self.gpio_out(layout.A, 0)
        self.gpio_out(layout.B, 0)
        self.gpio_out(layout.STROBE, 0)
        #self.gpio_out(layout.OE, 0)
        
        self.layout = layout

    def latch(self):
        self.gpio_out(self.layout.STROBE, 1)
        sleep(0.000001)
        self.gpio_out(self.layout.STROBE, 0)
        
    def gpioclean(self):
        GPIO.cleanup()
        
    def gpio_pwm_out(self, value):
        self.pwm.start(value)

    def gpio_out(self, pin, value):
        GPIO.output(pin, value)


