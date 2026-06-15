from time import sleep

from servo_controller import ServoController
from wrist import Wrist, WristAngles

ROT_GPIO = 12


class DummyServo:
    def move_to(self, angle: float):
        pass


def main():
    rot_servo  = ServoController(pin=ROT_GPIO, min_angle=0, max_angle=180)
    dummy_flex = DummyServo()

    angles = WristAngles(rot_neutral=90, rot_left=180, rot_right=0)
    wrist  = Wrist(flex_servo=dummy_flex, rot_servo=rot_servo, angles=angles)

    try:
        print("Neutral (0)")
        wrist.apply_code(0, delay_static=1)

        print("Left (1)")
        wrist.apply_code(1, delay_static=1)

        print("Right (2)")
        wrist.apply_code(2, delay_static=1)

        print("Alternate L/R (6)")
        wrist.apply_code(6, dyn_cycles=4, dyn_delay=0.35)
        sleep(1)

        print("Spin (5)")
        wrist.apply_code(5, dyn_cycles=5, dyn_delay=0.25)

        print("Done.")

    finally:
        rot_servo.stop()
        print("Wrist servo stopped.")


if __name__ == "__main__":
    main()
