from time import sleep
import pandas as pd

from servo_controller import ServoController
from finger import Finger, FingerAngles

PINS = {
    "Thumb": 17,
    "Index": 27,
    "Middle": 22,
    "Ring": 23,
    "Little": 24,
}

DEFAULT_ANGLES = FingerAngles(open_angle=0.0, mid_angle=90.0, closed_angle=180.0)

ALPHABET_PATH = "Alphabet.xlsx"
STEP_SLEEP = 1.2


def load_mapping_from_excel(path: str):
    df = pd.read_excel(path)

    required_cols = ["Character", "Thumb", "Index Finger", "Middle Finger", "Ring Finger", "Little Finger", "Wrist"]
    for c in required_cols:
        if c not in df.columns:
            raise ValueError(f"Falta columna '{c}' en el Excel. Columnas encontradas: {list(df.columns)}")

    mapping = {}
    for _, row in df.iterrows():
        ch = str(row["Character"]).strip()
        levels = [
            int(row["Thumb"]),
            int(row["Index Finger"]),
            int(row["Middle Finger"]),
            int(row["Ring Finger"]),
            int(row["Little Finger"]),
        ]
        wrist = int(row["Wrist"]) if not pd.isna(row["Wrist"]) else 0
        mapping[ch] = (levels, wrist)

    return mapping


def apply_pose(fingers, levels):
    for finger, level in zip(fingers, levels):
        finger.set_position(level)


def test_levels_all(fingers):
    print("\nTEST: niveles 0 -> 1 -> 2 -> 0 en TODOS los dedos")
    for level in [0, 1, 2, 0]:
        print(f"  set all -> {level}")
        for f in fingers:
            f.set_position(level)
        sleep(1.0)


def main():
    servos = {}
    fingers = []

    print("Inicializando servos...")
    for name, gpio in PINS.items():
        servos[name] = ServoController(pin=gpio, min_angle=0, max_angle=180)
        fingers.append(Finger(servo=servos[name], name=name, angles=DEFAULT_ANGLES))

    ordered_fingers = [
        next(f for f in fingers if f.name == "Thumb"),
        next(f for f in fingers if f.name == "Index"),
        next(f for f in fingers if f.name == "Middle"),
        next(f for f in fingers if f.name == "Ring"),
        next(f for f in fingers if f.name == "Little"),
    ]

    try:
        test_levels_all(ordered_fingers)

        print(f"\nCargando mapeo desde: {ALPHABET_PATH}")
        mapping = load_mapping_from_excel(ALPHABET_PATH)

        print(f"Total poses en Excel: {len(mapping)}")
        for ch, (levels, wrist) in mapping.items():
            print(f"Letra {ch}: dedos={levels} (wrist={wrist} ignorado)")
            apply_pose(ordered_fingers, levels)
            sleep(STEP_SLEEP)

        print("\nAbriendo mano (nivel 0) al final...")
        apply_pose(ordered_fingers, [0, 0, 0, 0, 0])
        sleep(1.0)

    finally:
        print("\nParando servos...")
        for s in servos.values():
            s.stop()
        print("Servos stopped.")


if __name__ == "__main__":
    main()
