from hardware.heater import Heater

def main():
    heater = Heater(27)
    heater.turn_heater_off()

if __name__ == '__main__':
    main()
