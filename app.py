import json
import os
import queue
import threading

from flask import Flask, Response, render_template, stream_with_context

from alphabet import load_alphabet

MODEL_PATH    = os.environ.get("VOSK_MODEL", "modelos/vosk-model-small-es-0.42")
ALPHABET_PATH = "Alphabet.xlsx"
PALABRAS      = ["hola", "gracias", "adios", "bien", "mal", "por favor"]

try:
    from hand import inicializar_mano
    from voice import inicializar_reconocedor, escuchar_palabra
    fingers, wrist = inicializar_mano()
    recognizer     = inicializar_reconocedor(MODEL_PATH, PALABRAS)
    MANO_DISPONIBLE = True
except Exception:
    fingers = wrist = recognizer = None
    MANO_DISPONIBLE = False

mapping = load_alphabet(ALPHABET_PATH).mapping

app = Flask(__name__)

_event_queue: queue.Queue = queue.Queue()
_escuchando = False
_lock = threading.Lock()


def _broadcast(tipo: str, datos: dict = {}):
    _event_queue.put({"type": tipo, **datos})


def _bucle_escucha():
    global _escuchando

    _broadcast("escuchando")

    while True:
        with _lock:
            if not _escuchando:
                break

        if MANO_DISPONIBLE:
            texto = escuchar_palabra(recognizer)
        else:
            from time import sleep
            sleep(4)
            texto = "hola"

        with _lock:
            if not _escuchando:
                break

        if texto not in PALABRAS:
            continue

        _broadcast("palabra_reconocida", {"palabra": texto})
        _deletrear(texto)

        with _lock:
            if not _escuchando:
                break

        _broadcast("escuchando")

    _broadcast("parado")


def _deletrear(palabra: str):
    from alphabet import get_pose
    from time import sleep

    letras = [l for l in palabra.upper() if l in mapping]

    for i, letra in enumerate(letras):
        with _lock:
            if not _escuchando:
                return

        _broadcast("letra", {"letra": letra, "indice": i, "total": len(letras)})

        if MANO_DISPONIBLE:
            fingers_pose, wrist_code = get_pose(mapping, letra)
            fingers.set_pose(fingers_pose, delay_between=0.05)
            wrist.apply_code(wrist_code)
            sleep(0.5)
        else:
            sleep(0.6)

    _broadcast("fin_palabra", {"palabra": palabra})


@app.route("/")
def index():
    return render_template("index.html", palabras=PALABRAS, mano=MANO_DISPONIBLE)


@app.route("/iniciar", methods=["POST"])
def iniciar():
    global _escuchando
    with _lock:
        if _escuchando:
            return {"ok": False, "error": "Ya está escuchando"}, 409
        _escuchando = True

    t = threading.Thread(target=_bucle_escucha, daemon=True)
    t.start()
    return {"ok": True}


@app.route("/status")
def status():
    return {"palabras": PALABRAS, "mano": MANO_DISPONIBLE}


@app.route("/parar", methods=["POST"])
def parar():
    global _escuchando
    with _lock:
        _escuchando = False
    return {"ok": True}


@app.route("/eventos")
def eventos():
    def generate():
        while True:
            try:
                evento = _event_queue.get(timeout=30)
                yield f"data: {json.dumps(evento)}\n\n"
            except queue.Empty:
                yield 'data: {"type":"ping"}\n\n'

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
