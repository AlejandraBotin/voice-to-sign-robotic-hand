from time import sleep
from alphabet import get_pose

DELAY_ENTRE_LETRAS  = 0.5
DELAY_ENTRE_PALABRAS = 1.0


def procesar_palabra(palabra, mapping, fingers, wrist):
    for letra in palabra.upper():
        try:
            fingers_pose, wrist_code = get_pose(mapping, letra)
            fingers.set_pose(fingers_pose, delay_between=0.05)
            wrist.apply_code(wrist_code)
            sleep(DELAY_ENTRE_LETRAS)
        except KeyError:
            pass
    sleep(DELAY_ENTRE_PALABRAS)
