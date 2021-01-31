import time
import json
import sys

sys.path.append('.')

from utils.utils import write_json, get_current_hour

class Thermostat:
    DEFAULT_CACHE_SIZE = 5
    DEFAULT_POLLING_INTERVAL = 60

    def __init__(self, heater, sensor, min_temp, max_temp, options):
        self.heater = heater
        self.sensor = sensor
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.active_hours = options.get("active_hours")
        self.log_file = options.get("log_file")
        self.cache_size = options.get("cache_size") or self.DEFAULT_CACHE_SIZE
        self.polling_interval = options.get("polling_interval") or self.DEFAULT_POLLING_INTERVAL
        self.is_started = False
        self.cache = []

    def is_in_active_hours(self):
        # Active hours weren't configured, thermostat should still function
        # as expected.
        if self.active_hours is None:
            return True

        for start, end in self.active_hours:
            current_hour = get_current_hour()
            if current_hour >= start and current_hour < end:
                return True

        return False

    def should_start_heater(self, current_tempf):
        return current_tempf < self.min_temp and not self.heater.is_on and self.is_in_active_hours()

    def should_stop_heater(self, current_tempf):
        return self.heater.is_on and (current_tempf >= self.max_temp or not self.is_in_active_hours())

    def start(self):
        print('Starting thermostat')
        self.is_started = True
        while (self.is_started):
            sensor_data = self.sensor.get_data()
            sensor_data['is_in_active_hours'] = self.is_in_active_hours()
            tempf = sensor_data.get('temperature_f')
        
            if (self.should_start_heater(tempf)):
                message = 'Turning heater on'
                print(message)
                sensor_data['message'] = message
                self.heater.turn_heater_on()
            elif (self.should_stop_heater(tempf)):
                message = 'Turning heater off'
                print(message)
                sensor_data['message'] = message
                self.heater.turn_heater_off()

            sensor_data['is_heater_on'] = self.heater.is_on

            if (len(self.cache) == self.cache_size and self.log_file is not None):
                # todo: use util to get json config
                with open(self.log_file) as json_file:
                    data = json.load(json_file)
                    json_file.close()
                    data['data'] = data['data'] + self.cache
        
                write_json(data, self.log_file)
                self.cache = []
            elif (self.log_file is not None):
                self.cache.append(sensor_data)

            print(sensor_data)
            time.sleep(self.polling_interval)

    def stop(self):
        print('Stopping thermostat.')
        self.is_started = False
        self.heater.turn_heater_off()

    def update_options(self, options):
        print('Updating thermostat options')
        self.active_hours = options.get('active_hours')
        self.cache_size = options.get('cache_size') or self.DEFAULT_CACHE_SIZE
        self.log_file = options.get('log_file')
        self.max_temp = options.get('max_temp')
        self.min_temp = options.get('min_temp')
        self.polling_interval = options.get('polling_interval') or self.DEFAULT_POLLING_INTERVAL
        
