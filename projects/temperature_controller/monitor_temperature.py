#!/usr/bin/python
import Adafruit_DHT
import sys
import time
import datetime
import json
import RPi.GPIO as GPIO

sys.path.append('.')

from hardware.heater import Heater
from hardware.temperature_humidity_sensor import Sensor
from hardware.thermostat import Thermostat

def main():
    try:
        sensor_args = {
            '11': Adafruit_DHT.DHT11,
            '22': Adafruit_DHT.DHT22,
            '2302': Adafruit_DHT.AM2302
        }
        if len(sys.argv) == 4 and sys.argv[1] in sensor_args:
            sensorType = sensor_args[sys.argv[1]]
            pin = sys.argv[2]
            relayPin = sys.argv[3]
        else:
            print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
            print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
            sys.exit(1)
        
        sensor = Sensor(sensorType, pin)
        heater = Heater(relayPin)
        thermostat = Thermostat(heater, sensor, minTemp=66.0, maxTemp=68.0, log_file='/home/pi/Code/automation/projects/temperature_controller/sensor_data.json')
        thermostat.start()
    except KeyboardInterrupt:
        thermostat.stop()
        print('\nCleaning up GPIO')
        GPIO.cleanup()
        sys.exit(1)
        
        cycles_since_last_write = 0

if __name__ == '__main__':
    main()
