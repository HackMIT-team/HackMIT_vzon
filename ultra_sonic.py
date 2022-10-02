
import sys
import time
from pymata4 import pymata4

triggePin = 11
echo_pin = 12

board = pymata4.Pymata4()


def the_callback(data):
    if data[2] <= 50:
        print("Stop, Obstacle ahead")
        return



    else:
        print("go")

board.set_pin_mode_sonar(triggePin, echo_pin, the_callback)
while True:
        try:
                time.sleep(1)
                board.sonar_read(triggePin)
        except KeyboardInterrupt:
                board.shutdown()
                sys.exit(0)