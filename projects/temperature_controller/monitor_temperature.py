#!/usr/bin/python
import os.path
import Adafruit_DHT
import sys
import RPi.GPIO as GPIO
import json

sys.path.append('.')

from hardware.heater import Heater
from hardware.temperature_humidity_sensor import Sensor
from hardware.thermostat import Thermostat
from utils.utils import write_json

def initialize_log_file_if_needed(log_file):
    if os.path.isfile(log_file):
        return

    write_json({ "data": [] }, log_file)

def main():
    try:
        sensor_args = {
            11: Adafruit_DHT.DHT11,
            22: Adafruit_DHT.DHT22,
            2302: Adafruit_DHT.AM2302
        }

        with open('thermostat_config.json') as config_file:
            config = json.load(config_file)
            print(config)
            active_hours = config.get('active_hours')
            sensor_type = config.get('sensor')
            sensor_pin = config.get('sensor_pin')
            relay_pin = config.get('relay_pin')
            min_temp = config.get('min_temp')
            max_temp = config.get('max_temp')
            log_file = config.get('log_file')
        
        sensor_value = sensor_args.get(sensor_type)
        if sensor_value is None:
            print('Sensor type {0} is not supported. Values must be [11|22|2302]'.format(sensor_type))
            sys.exit(1)

        sensor = Sensor(sensor_value, sensor_pin)
        heater = Heater(relay_pin)

        initialize_log_file_if_needed(log_file)

        thermostat = Thermostat(heater, sensor, min_temp, max_temp, {
            "log_file": log_file,
            "active_hours": active_hours,
        })
        thermostat.start()
    except KeyboardInterrupt:
        thermostat.stop()
        print('\nCleaning up GPIO')
        GPIO.cleanup()
        sys.exit(1)
        
        cycles_since_last_write = 0

if __name__ == '__main__':
    main()
