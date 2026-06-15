from time import sleep
from signal import pause

from servo_controller import ServoController
from finger import Finger, FingerAngles
from alphabet import load_alphabet, get_pose

THUMB_GPIO = 12

THUMB_ANGLES = FingerAngles(
    open_angle=-90.0,
    mid_angle=0.0,
    closed_angle=90.0
)

ALPHABET_PATH = "Alphabet.xlsx"


def test_thumb_levels(thumb: Finger):
    print("\nTEST: Thumb levels 0->1->2->0")
    thumb.open();  sleep(5)
    thumb.half();  sleep(5)
    thumb.close(); sleep(5)
    thumb.open();  sleep(5)


def test_thumb_letters(thumb: Finger, alphabet_path: str):
    print(f"\nCargando alfabeto desde: {alphabet_path}")
    data = load_alphabet(alphabet_path)

    letters = ["A", "B", "C", "D", "E"]

    for ch in letters:
        fingers_pose, wrist_pos = get_pose(data.mapping, ch)
        thumb_level = fingers_pose[0]
        print(f"Letra {ch}: thumb_level={thumb_level} (wrist={wrist_pos} ignorado)")
        thumb.set_position(thumb_level)


def main():
    thumb_servo = ServoController(pin=THUMB_GPIO)
    thumb = Finger(servo=thumb_servo, name="Thumb", angles=THUMB_ANGLES)

    try:
        test_thumb_levels(thumb)
        pause()
    finally:
        thumb_servo.stop()
        print("\nThumb servo stopped.")


if __name__ == "__main__":
    main()
