from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep


class ServoController:
    def __init__(self, pin: int, min_angle: float = -90, max_angle: float = 90):
        factory = PiGPIOFactory()
        self.servo = AngularServo(
            pin,
            min_angle=min_angle,
            max_angle=max_angle,
            pin_factory=factory,
        )

    def move_to(self, angle: float, wait: float = 0):
        self.servo.angle = angle
        if wait > 0:
            sleep(wait)

    def stop(self):
        self.servo.detach()
