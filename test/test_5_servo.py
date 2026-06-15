from time import sleep
import pandas as pd

from servo_controller import ServoController
from finger import Finger, FingerAngles

# -----------------------
# CONFIG GPIO (BCM)
# Según tu tabla:
# pulgar  -> GPIO17 (pin físico 11)
# índice  -> GPIO27 (pin físico 13)
# corazón -> GPIO22 (pin físico 15)  (asumo "middle")
# anular  -> GPIO23 (pin físico 16)
# meñique -> GPIO24 (pin físico 18)
# -----------------------
PINS = {
    "Thumb": 17,
    "Index": 27,
    "Middle": 22,
    "Ring": 23,
    "Little": 24,
}

# Ajusta ángulos por dedo si alguno va al revés o no llega bien.
# Si un dedo abre/cierra al revés, intercambia open_angle y closed_angle,
# o pon open_angle=180 y closed_angle=0.
DEFAULT_ANGLES = FingerAngles(open_angle=0.0, mid_angle=90.0, closed_angle=180.0)

# Ruta del Excel en la Pi (ajústala si está en otro sitio)
ALPHABET_PATH = "Alphabet.xlsx"

# Tiempo entre poses (sube si tiembla o va muy rápido)
STEP_SLEEP = 1.2


def load_mapping_from_excel(path: str):
    df = pd.read_excel(path)

    # Normalizamos y nos quedamos con lo necesario
    required_cols = ["Character", "Thumb", "Index Finger", "Middle Finger", "Ring Finger", "Little Finger", "Wrist"]
    for c in required_cols:
        if c not in df.columns:
            raise ValueError(f"Falta columna '{c}' en el Excel. Columnas encontradas: {list(df.columns)}")

    mapping = {}
    for _, row in df.iterrows():
        ch = str(row["Character"]).strip()
        # niveles esperados 0/1/2
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
    # levels: [thumb, index, middle, ring, little]
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
    # Crear servos
    servos = {}
    fingers = []

    print("Inicializando servos...")
    for name, gpio in PINS.items():
        servos[name] = ServoController(pin=gpio, min_angle=0, max_angle=180)
        fingers.append(Finger(servo=servos[name], name=name, angles=DEFAULT_ANGLES))

    # Orden de dedos igual que el Excel: Thumb, Index, Middle, Ring, Little
    ordered_fingers = [
        next(f for f in fingers if f.name == "Thumb"),
        next(f for f in fingers if f.name == "Index"),
        next(f for f in fingers if f.name == "Middle"),
        next(f for f in fingers if f.name == "Ring"),
        next(f for f in fingers if f.name == "Little"),
    ]

    try:
        # 1) Prueba básica sincronizada
        test_levels_all(ordered_fingers)

        # 2) Barrido por el Excel
        print(f"\nCargando mapeo desde: {ALPHABET_PATH}")
        mapping = load_mapping_from_excel(ALPHABET_PATH)

        print(f"Total poses en Excel: {len(mapping)}")
        for ch, (levels, wrist) in mapping.items():
            # wrist lo ignoramos aquí (solo dedos)
            print(f"Letra {ch}: dedos={levels} (wrist={wrist} ignorado)")
            apply_pose(ordered_fingers, levels)
            sleep(STEP_SLEEP)

        # 3) Vuelta a abierto al final (por no dejarlo hecho un puño)
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
