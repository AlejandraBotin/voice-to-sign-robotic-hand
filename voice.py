import os
import queue
import json

import sounddevice as sd
from vosk import Model, KaldiRecognizer

SAMPLERATE   = 48000
BLOCKSIZE    = 8000
DEVICE_INDEX = int(os.environ.get("MIC_DEVICE", 1))


def inicializar_reconocedor(model_path: str, palabras: list) -> KaldiRecognizer:
    model   = Model(model_path)
    grammar = json.dumps(palabras, ensure_ascii=False)
    return KaldiRecognizer(model, SAMPLERATE, grammar)


def escuchar_palabra(recognizer: KaldiRecognizer) -> str:
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=SAMPLERATE,
        blocksize=BLOCKSIZE,
        device=DEVICE_INDEX,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                resultado = json.loads(recognizer.Result())
                texto = resultado.get("text", "").strip()
                if texto:
                    return texto
