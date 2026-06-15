# 🤖 Voice-to-Sign Robotic Hand

> A 3D-printed robotic hand that listens to spoken Spanish and translates it into **Spanish Sign Language (LSE)** gestures — letter by letter.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4B-red?logo=raspberrypi)
![Vosk](https://img.shields.io/badge/Speech-Vosk-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Overview

This project was developed as a Final Year Engineering Project (TFG) at ICAI – Universidad Pontificia Comillas. The goal is to bridge the communication gap for the 1.2 million people with hearing impairment in Spain, 96% of whom attend mainstream schools without a guaranteed sign language interpreter.

The system captures voice input, recognises the spoken word in real time, and physically moves a 3D-printed robotic hand to spell it out in the LSE dactylological alphabet — one servo-controlled letter at a time. A companion web interface makes it usable in a classroom from any device, no technical knowledge required.

**Total build cost: under €250.**

---

## Features

- 🎤 **Real-time Spanish speech recognition** via Vosk, processed locally on the Raspberry Pi
- ✋ **7 servo motors** — 5 independent fingers + 2-axis wrist movement
- 🌐 **Web interface** with live feedback via Server-Sent Events (SSE)
- 🖥️ **Simulation mode** — runs on any computer without physical hardware connected
- 📊 **Excel-based alphabet** (`Alphabet.xlsx`) — easy to extend or adapt to other sign languages
- 🧩 **Modular architecture** — each component is independently testable
- 💸 **Low cost and fully replicable** with off-the-shelf parts

---

## System Architecture

```
Microphone → Vosk (speech recognition) → word_processor.py
                                               ↓
                                         alphabet.py (Alphabet.xlsx)
                                               ↓
                              ┌────────────────┴────────────────┐
                           finger.py                        wrist.py
                              └────────────────┬────────────────┘
                                         servo_controller.py
                                               ↓
                                        GPIO (Raspberry Pi 4B)
                                               ↓
                                    7× Servo motors → 🤚 Hand
```

The web interface (`app.py`) runs the same pipeline via Flask, broadcasting state updates to the browser through SSE so the user sees each letter highlighted as the hand moves.

---

## Hardware

| Component | Model | Qty |
|---|---|---|
| Single-board computer | Raspberry Pi 4B | 1 |
| USB Microphone | SunFounder M-305 | 1 |
| Finger servos | SG90 | 5 |
| Wrist servos | MG90S | 2 |
| Transistors (GPIO protection) | 2N2222 | 7 |
| 3D-printed hand | [Instructables design](https://www.instructables.com) | 1 |
| External power supply | 5V battery pack | 1 |

The transistor circuit isolates the servo power rail from the Raspberry Pi GPIO pins, preventing damage from inrush current.

---

## Software

| Library | Purpose |
|---|---|
| `vosk` | Offline-capable speech recognition |
| `sounddevice` | Audio capture |
| `flask` | Web server and SSE streaming |
| `gpiozero` + `pigpio` | Servo PWM control via GPIO |
| `pandas` + `openpyxl` | Reading the alphabet definition from Excel |

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/voice-to-sign-hand.git
cd voice-to-sign-hand
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> On Raspberry Pi, `gpiozero` and `pigpio` are usually pre-installed. Run `sudo pigpiod` before starting the system.

### 3. Download the Vosk model
```bash
mkdir -p modelos
cd modelos
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip
```

### 4. (Optional) Set environment variables
```bash
export VOSK_MODEL=modelos/vosk-model-small-es-0.42   # default path
export MIC_DEVICE=1                                   # USB mic device index
```

---

## Usage

### Web interface (recommended)
```bash
python app.py
```
Then open `http://<raspberry-pi-ip>:5000` from any device on the same network.

If the hand is not connected, the system automatically enters **simulation mode** — the web interface still shows the full spelling animation so you can demo the project on any laptop.

### Command-line mode
```bash
python main.py
```

### Hardware diagnostics
```bash
python diagnostico.py
```
Step-by-step interactive check of every component: alphabet loading, finger movement, wrist movement, speech recognition, and full end-to-end flow.

---

## File Structure

```
├── app.py                  # Flask web server + SSE streaming
├── main.py                 # Command-line entry point
├── diagnostico.py          # Interactive hardware diagnostic script
│
├── alphabet.py             # Loads and parses Alphabet.xlsx
├── hand.py                 # Initialises all 7 servos
├── finger.py               # Individual finger control (levels 0/1/2)
├── wrist.py                # Wrist control (codes 0–6)
├── servo_controller.py     # Low-level PWM via gpiozero + pigpio
├── voice.py                # Vosk speech recognition
├── word_processor.py       # Spells a word letter by letter
│
├── Alphabet.xlsx           # LSE alphabet definition
├── templates/
│   └── index.html          # Web interface
├── test/                   # Unit and integration tests
└── requirements.txt
```

---

## Alphabet Format

`Alphabet.xlsx` defines the hand configuration for each character:

| Character | Thumb | Index Finger | Middle Finger | Ring Finger | Little Finger | Wrist |
|---|---|---|---|---|---|---|
| A | 2 | 2 | 2 | 2 | 2 | 0 |
| B | 0 | 0 | 0 | 0 | 0 | 0 |
| ... | | | | | | |

Finger values: `0` = open · `1` = half · `2` = closed  
Wrist codes: `0` neutral · `1` left · `2` right · `3` forward · `4` backward · `5–6` dynamic

To adapt the system to a different sign language, replace or extend `Alphabet.xlsx` — no code changes needed.

---

## Future Work

- Extend vocabulary beyond the alphabet to full common words
- Refine servo calibration for improved gesture legibility
- Validate the system with real users in educational settings
- Add an interactive learning mode to the web interface
- Explore lighter hardware alternatives (Raspberry Pi Pico, custom PCB)

---

## Author

**Alejandra Botín Lehm**  
ICAI – Universidad Pontificia Comillas  
Supervisor: Francisco Martín Martínez  

---

## License

This project is open source under the [MIT License](LICENSE).  
Feel free to replicate, adapt and improve it for your own accessibility projects.
