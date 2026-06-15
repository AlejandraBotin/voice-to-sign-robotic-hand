from time import sleep
import pandas as pd

from servo_controller import ServoController
from finger import Finger, FingerAngles

# -----------------------
# CONFIG GPIO (BCM)
# Pulgar -> GPIO17 (pin físico 11)
# Índice -> GPIO27 (pin físico 13)
# -----------------------
PINS = {
    "Thumb": 17,
    "Index": 27,
}

# Ajusta esto si alguno abre/cierra al revés o no llega bien
DEFAULT_ANGLES = FingerAngles(open_angle=0.0, mid_angle=90.0, closed_angle=180.0)

ALPHABET_PATH = "Alphabet.xlsx"
STEP_SLEEP = 1.2


def load_mapping_from_excel_thumb_index(path: str):
    df = pd.read_excel(path)

    required_cols = ["Character", "Thumb", "Index Finger"]
    for c in required_cols:
        if c not in df.columns:
            raise ValueError(
                f"Falta columna '{c}' en el Excel. Columnas encontradas: {list(df.columns)}"
            )

    mapping = {}
    for _, row in df.iterrows():
        ch = str(row["Character"]).strip()

        # niveles esperados 0/1/2
        thumb_level = int(row["Thumb"])
        index_level = int(row["Index Finger"])

        mapping[ch] = [thumb_level, index_level]

    return mapping


def apply_pose_two(fingers, levels):
    # levels: [thumb, index]
    for finger, level in zip(fingers, levels):
        finger.set_position(level)


def test_levels_two(fingers):
    print("\nTEST: niveles 0 -> 1 -> 2 -> 0 en Thumb + Index")
    for level in [0, 1, 2, 0]:
        print(f"  set both -> {level}")
        for f in fingers:
            f.set_position(level)
        sleep(1.0)


def main():
    servos = {}
    fingers = []

    print("Inicializando servos (Thumb + Index)...")
    for name, gpio in PINS.items():
        servos[name] = ServoController(pin=gpio, min_angle=0, max_angle=180)
        fingers.append(Finger(servo=servos[name], name=name, angles=DEFAULT_ANGLES))

    # Orden fijo: Thumb, Index
    ordered_fingers = [
        next(f for f in fingers if f.name == "Thumb"),
        next(f for f in fingers if f.name == "Index"),
    ]

    try:
        # 1) Prueba básica sincronizada
        test_levels_two(ordered_fingers)

        # 2) Barrido por el Excel (solo Thumb + Index)
        print(f"\nCargando mapeo desde: {ALPHABET_PATH}")
        mapping = load_mapping_from_excel_thumb_index(ALPHABET_PATH)

        print(f"Total poses en Excel: {len(mapping)}")
        for ch, levels in mapping.items():
            print(f"Letra {ch}: [Thumb, Index]={levels}")
            apply_pose_two(ordered_fingers, levels)
            sleep(STEP_SLEEP)

        # 3) Abrir al final
        print("\nAbriendo mano (nivel 0) al final...")
        apply_pose_two(ordered_fingers, [0, 0])
        sleep(1.0)

    finally:
        print("\nParando servos...")
        for s in servos.values():
            s.stop()
        print("Servos stopped.")


if __name__ == "__main__":
    main()