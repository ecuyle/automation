import datetime
import time
import json
import sys

sys.path.append('.')

from utils.utils import write_json

class Thermostat:
    def __init__(self, heater, sensor, minTemp, maxTemp, polling_interval=60, cache_size=5, log_file='sensor_data.json'):
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.heater = heater
        self.sensor = sensor
        self.is_started = False
        self.cache = []
        self.cache_size = cache_size
        self.log_file = log_file
        self.polling_interval = polling_interval

    def start(self):
        print('Starting thermostat')
        self.is_started = True
        while (self.is_started):
            sensor_data = self.sensor.get_data()
            tempf = sensor_data.get('temperature_f')
        
            if (tempf < self.minTemp and not self.heater.is_on):
                message = 'Turning heater on'
                print(message)
                sensor_data['message'] = message
                self.heater.turn_heater_on()
            elif (tempf >= self.maxTemp and self.heater.is_on):
                message = 'Turning heater off'
                print(message)
                sensor_data['message'] = message
                self.heater.turn_heater_off()

            sensor_data['is_heater_on'] = self.heater.is_on

            if (len(self.cache) == self.cache_size):
                with open(self.log_file) as json_file:
                    data = json.load(json_file)
                    data['data'] = data['data'] + self.cache
        
                write_json(data)
                self.cache = []
            else:
                self.cache.append(sensor_data)

            print(sensor_data)
            time.sleep(self.polling_interval)

    def stop(self):
        print('Stopping thermostat.')
        self.is_started = False
        
