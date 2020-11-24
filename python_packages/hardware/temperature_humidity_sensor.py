import Adafruit_DHT
import datetime
import time
import sys

sys.path.append('.')

from utils.utils import convert_celsius_to_fahrenheit

class Sensor:
    def __init__(self, sensorType, pin):
        self.sensorType = sensorType
        print(pin)
        print('Initializing sensor on pin ' + str(pin))
        self.pin = pin

    def get_humidity_and_temperature(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensorType, self.pin)
        return humidity, temperature

    def get_data(self):
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = self.get_humidity_and_temperature()
    
        timestamp_readable = datetime.datetime.now()
        timestamp_seconds = time.time()
    
        return {
            'temperature_raw': temperature,
            'temperature_f': convert_celsius_to_fahrenheit(temperature),
            'timestamp_seconds': timestamp_seconds,
            'timestamp_readable': timestamp_readable,
            'humidity': humidity
        }

