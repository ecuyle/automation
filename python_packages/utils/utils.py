import datetime
import json

def convert_celsius_to_fahrenheit(degrees_in_celsius):
    return degrees_in_celsius * 9/5.0 + 32

def write_json(data, filename='sensor_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True, default=str)

def get_current_hour():
    return datetime.datetime.now().hour

