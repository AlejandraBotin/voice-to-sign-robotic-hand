import os
from time import sleep
from alphabet import load_alphabet, get_pose
from voice import inicializar_reconocedor, escuchar_palabra
from hand import inicializar_mano
from word_processor import procesar_palabra

MODEL_PATH    = os.environ.get("VOSK_MODEL", "modelos/vosk-model-small-es-0.42")
ALPHABET_PATH = "Alphabet.xlsx"
PALABRAS      = ["hola", "gracias", "adios", "parar"]


def separador(titulo):
    print(f"\n{'='*50}\n  {titulo}\n{'='*50}")

def ok(msg):
    print(f"  [OK] {msg}")

def esperar(msg="Pulsa ENTER para continuar..."):
    input(f"\n  >> {msg}")


def check_alfabeto():
    separador("Lectura del Excel")
    data = load_alphabet(ALPHABET_PATH)
    ok(f"Archivo leído. Caracteres cargados: {len(data.mapping)}")

    for letra in ["A", "B", "C"]:
        try:
            fingers_pose, wrist_code = get_pose(data.mapping, letra)
            ok(f"Letra '{letra}' → dedos={fingers_pose}, muñeca={wrist_code}")
        except KeyError as e:
            print(f"  [ERROR] {e}")

    esperar()
    return data.mapping


def check_mano(fingers, wrist):
    separador("Inicialización de la mano")
    ok("Dedos y muñeca inicializados")

    print("  Abriendo mano..."); fingers.open_all(); ok("Abierta"); sleep(2)
    print("  Cerrando mano..."); fingers.close_all(); ok("Cerrada"); sleep(2)
    print("  Volviendo a abrir..."); fingers.open_all(); ok("Abierta"); sleep(1)

    esperar()


def check_muneca(wrist):
    separador("Movimientos de la muñeca")

    movimientos = [
        ("Posición neutra",       wrist.neutral),
        ("Rotación izquierda",    wrist.left),
        ("Rotación derecha",      wrist.right),
        ("Flexión hacia delante", wrist.forward),
        ("Flexión hacia atrás",   wrist.backward),
    ]
    for nombre, fn in movimientos:
        print(f"  {nombre}..."); fn(); ok(nombre); sleep(2)

    print("  Movimiento dinámico (izda/dcha)...")
    wrist.apply_code(6, dyn_cycles=3, dyn_delay=0.3)
    ok("Dinámico completado"); sleep(1)

    wrist.neutral()
    esperar()


def check_letras(mapping, fingers, wrist):
    separador("Letras del alfabeto")

    for letra in ["A", "B", "C"]:
        fingers_pose, wrist_code = get_pose(mapping, letra)
        print(f"  Letra '{letra}': dedos={fingers_pose}, muñeca={wrist_code}")
        fingers.set_pose(fingers_pose, delay_between=0.05)
        wrist.apply_code(wrist_code)
        ok(f"'{letra}' ejecutada"); sleep(0.5)

    sleep(1)
    esperar()


def check_voz():
    separador("Reconocimiento de voz")
    print("  Cargando modelo Vosk...")
    recognizer = inicializar_reconocedor(MODEL_PATH, PALABRAS)
    ok("Modelo cargado")

    print("  Di una de estas palabras: hola / gracias / adios / parar")
    texto = escuchar_palabra(recognizer)
    ok(f"Reconocida: '{texto}'")

    esperar()
    return recognizer


def check_flujo_completo(mapping, recognizer, fingers, wrist):
    separador("Flujo completo")
    print("  Sistema listo. Di una palabra (parar para salir)...")

    while True:
        texto = escuchar_palabra(recognizer)
        ok(f"Reconocido: '{texto}'")
        if texto == "parar":
            break
        if texto in PALABRAS:
            procesar_palabra(texto, mapping, fingers, wrist)


print("\n  DIAGNÓSTICO — MANO BIÓNICA LSE")
print("  Cada paso espera confirmación antes de continuar.\n")

mapping        = check_alfabeto()
fingers, wrist = inicializar_mano()

try:
    check_mano(fingers, wrist)
    check_muneca(wrist)
    check_letras(mapping, fingers, wrist)
    recognizer = check_voz()
    check_flujo_completo(mapping, recognizer, fingers, wrist)
finally:
    wrist.flex_servo.stop()
    wrist.rot_servo.stop()

print("\n  Todos los checks completados.")
