import RPi.GPIO as GPIO
import time

class Relay:
    def __init__(self, relayPin=27):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        
        # pin used by relay switch
        #   - GPIO27 (BCM) = Pin 11 (Board)
        self.relay = int(relayPin)
        
    def activate(self):
        # setup relay GPIO mode, set state to 'HIGH'
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay, GPIO.OUT)
        GPIO.output(self.relay, GPIO.HIGH)
        print('Relay Sensor activated on GPIO pin # ', self.relay)
        time.sleep(0.5)

    def cleanup(self):
        print('Cleaning up relay')
        GPIO.cleanup()

