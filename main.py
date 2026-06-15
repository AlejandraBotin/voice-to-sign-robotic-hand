import os
from alphabet import load_alphabet
from voice import inicializar_reconocedor, escuchar_palabra
from hand import inicializar_mano
from word_processor import procesar_palabra

MODEL_PATH    = os.environ.get("VOSK_MODEL", "modelos/vosk-model-small-es-0.42")
ALPHABET_PATH = "Alphabet.xlsx"
PALABRAS      = ["hola", "gracias", "adios", "parar"]

mapping        = load_alphabet(ALPHABET_PATH).mapping
recognizer     = inicializar_reconocedor(MODEL_PATH, PALABRAS)
fingers, wrist = inicializar_mano()

try:
    while True:
        texto = escuchar_palabra(recognizer)

        if texto == "parar":
            break

        if texto in PALABRAS:
            procesar_palabra(texto, mapping, fingers, wrist)

finally:
    wrist.flex_servo.stop()
    wrist.rot_servo.stop()
