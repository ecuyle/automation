from hardware.relay import Relay

class Heater:
    def __init__(self, relayPin):
        print('Initializing heater on pin ' + relayPin)
        self.is_on = False
        self.relay = Relay(relayPin)
        self.turn_heater_on()
        self.turn_heater_off()

    def turn_heater_on(self):
        print('Turning heater on')
        self.relay.activate()
        self.is_on = True
    
    def turn_heater_off(self):
        print('Turning heater off')
        self.relay.cleanup()
        self.is_on = False

