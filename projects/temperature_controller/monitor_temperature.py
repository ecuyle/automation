#!/usr/bin/python
import os.path
import Adafruit_DHT
import sys
import RPi.GPIO as GPIO
import json
import pathlib
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from functools import partial

sys.path.append('.')

from hardware.heater import Heater
from hardware.temperature_humidity_sensor import Sensor
from hardware.thermostat import Thermostat
from utils.utils import write_json

def initialize_log_file_if_needed(log_file):
    if os.path.isfile(log_file):
        return

    write_json({ "data": [] }, log_file)

def get_json_config(path_to_config):
    with open(path_to_config) as config_file:
        config = json.load(config_file)
        config_file.close()
        return config

def main():
    path_to_config_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), 'config')
    path_to_config = os.path.join(path_to_config_dir, 'thermostat_config.json')
    observer = Observer()

    try:
        sensor_args = {
            11: Adafruit_DHT.DHT11,
            22: Adafruit_DHT.DHT22,
            2302: Adafruit_DHT.AM2302
        }

        config = get_json_config(path_to_config)
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

        path_to_log_file = os.path.join(pathlib.Path(__file__).parent.absolute(), log_file)
        initialize_log_file_if_needed(path_to_log_file)

        thermostat = Thermostat(heater, sensor, min_temp, max_temp, {
            "log_file": path_to_log_file,
            "active_hours": active_hours,
        })

        def on_config_update(event):
            print(f'Config updated at {event.src_path}')
            config = get_json_config(path_to_config)
            print(config)
            # todo: create pick util to create these options in a more
            # standardized way
            thermostat.update_options({
                'active_hours': config.get('active_hours'),
                'cache_size': config.get('cache_size'),
                'log_file': config.get('log_file'),
                'max_temp': config.get('max_temp'),
                'min_temp': config.get('min_temp'),
                'polling_interval': config.get('polling_interval'),
            })

        event_handler = PatternMatchingEventHandler(patterns="*.json$", ignore_patterns="*.swp", ignore_directories=True, case_sensitive=True)
        event_handler.on_modified = on_config_update
        observer.schedule(event_handler, path_to_config_dir, recursive=True)
        observer.start()
        print('Observer started.')

        thermostat.start()
    except KeyboardInterrupt:
        thermostat.stop()
        print('\nCleaning up GPIO.')
        GPIO.cleanup()
        sys.exit(1)
    finally:
        print('Cleaning up observer.')
        observer.stop()
        observer.join()
        
if __name__ == '__main__':
    main()
