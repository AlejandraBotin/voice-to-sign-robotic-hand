from signal import pause

from servo_controller import ServoController
from time import sleep

SERVO_GPIO = 12  # GPIO BCM (pin físico 32)

servo = ServoController(pin=SERVO_GPIO)

try:
    # 0 → 90
    servo.move_to(angle=-90)
    sleep(1)
    servo.move_to(angle=0)
    sleep(1)

    # 90 → 180
    servo.move_to(angle=90)
    sleep(1)

    # 180 → 0
    servo.move_to(angle=0)
    sleep(1)

    # 0 → 180 directo
    servo.move_to(angle=-90)
    sleep(1)
    pause()

finally:
    servo.stop()