import Adafruit_DHT
from hardware.temperature_humidity_sensor import Sensor

def main():
    sensor = Sensor(Adafruit_DHT.AM2302, 17)
    print(sensor.get_data())

if __name__ == '__main__':
    main()
