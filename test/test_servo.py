from signal import pause
from servo_controller import ServoController
from time import sleep

SERVO_GPIO = 12

servo = ServoController(pin=SERVO_GPIO)

try:
    servo.move_to(angle=-90)
    sleep(1)
    servo.move_to(angle=0)
    sleep(1)
    servo.move_to(angle=90)
    sleep(1)
    servo.move_to(angle=0)
    sleep(1)
    servo.move_to(angle=-90)
    sleep(1)
    pause()

finally:
    servo.stop()
