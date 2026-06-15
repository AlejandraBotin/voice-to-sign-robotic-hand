from time import sleep
from signal import pause

from servo_controller import ServoController
from finger import Finger, FingerAngles
from alphabet import load_alphabet, get_pose

# -----------------------
# CONFIG
# -----------------------
THUMB_GPIO = 12  # BCM

# Ajusta estos si tu pulgar abre/cierra al revés o no llega:
THUMB_ANGLES = FingerAngles(
    open_angle=-90.0,
    mid_angle=0.0,
    closed_angle=90.0
)

# Ruta a tu excel/csv del alfabeto (si lo tienes en la misma carpeta)
ALPHABET_PATH = "Alphabet.xlsx"   # o "alphabet.csv"


def test_thumb_levels(thumb: Finger):
    print("\nTEST: Thumb levels 0->1->2->0")
    thumb.open()
    sleep(5)

    thumb.half()
    sleep(5)

    thumb.close()
    sleep(5)

    thumb.open()
    sleep(5)


def test_thumb_letters(thumb: Finger, alphabet_path: str):
    """
    Lee el archivo del alfabeto, y para cada letra aplica SOLO el nivel del thumb.
    Ignora el resto de dedos y muñeca (porque aún no están conectados).
    """
    print(f"\nCargando alfabeto desde: {alphabet_path}")
    data = load_alphabet(alphabet_path)

    # Pon aquí las letras que quieras probar
    letters = ["A", "B", "C", "D", "E"]

    for ch in letters:
        fingers_pose, wrist_pos = get_pose(data.mapping, ch)

        thumb_level = fingers_pose[0]  # [Thumb, Index, Middle, Ring, Little]
        print(f"Letra {ch}: thumb_level={thumb_level} (wrist={wrist_pos} ignorado)")

        thumb.set_position(thumb_level)
        # sleep(1.5)


def main():
    # Servo real del pulgar
    thumb_servo = ServoController(pin=THUMB_GPIO)

    # Finger wrapper (niveles 0/1/2)
    thumb = Finger(servo=thumb_servo, name="Thumb", angles=THUMB_ANGLES)

    try:
        # 1) Prueba básica niveles
        test_thumb_levels(thumb)

        # 2) Prueba “letras” desde el excel/csv (si existe)
        # Si no tienes el archivo aún, comenta esta línea.
        # test_thumb_letters(thumb, ALPHABET_PATH)
        pause()

    finally:
        thumb_servo.stop()
        print("\nThumb servo stopped.")


if __name__ == "__main__":
    main()
