from hardware.heater import Heater

def main():
    heater = Heater(27)
    heater.turn_heater_on()

if __name__ == '__main__':
    main()
