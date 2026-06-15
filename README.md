# Voice-to-Sign Robotic Hand

A voice-controlled robotic hand designed to improve accessibility and communication by translating spoken letters into sign language gestures.

## Project Overview

This project combines speech recognition, embedded systems and robotics to create a low-cost assistive technology solution. A user pronounces a word, the system recognizes the spoken input in real time, and a 3D-printed robotic hand reproduces the corresponding sign language gesture through a set of servomotors.

The objective is to facilitate communication and promote educational inclusion by providing a visual representation of spoken language through sign language.

## Features

* Real-time speech recognition in Spanish using Vosk.
* Raspberry Pi-based processing.
* 3D-printed robotic hand.
* Servo motor control through PWM signals.
* Modular architecture allowing easy addition of new gestures and commands.
* Offline operation without requiring an internet connection.
* Low-cost and scalable design.

## System Architecture

1. Audio is captured through a microphone connected to the Raspberry Pi.
2. The speech recognition module converts audio into text.
3. The detected letter is matched with a predefined gesture database.
4. Angular positions are sent to the corresponding servomotors.
5. The robotic hand performs the sign language gesture.

## Hardware

* Raspberry Pi
* USB Microphone
* PCA9685 Servo Driver
* SG90/MG90S Servomotors
* 3D-Printed Robotic Hand
* External Power Supply

## Software

* Python
* Vosk Speech Recognition
* PyAudio
* Adafruit PCA9685 Library
* Raspberry Pi OS

## Applications

* Educational environments
* Accessibility and inclusion projects
* Human-robot interaction research
* Assistive technologies for communication

## Future Improvements

* Recognition of sentences.
* Support for dynamic sign language gestures.
* Bidirectional communication system.
* Mobile application integration.
* Machine learning-based gesture generation.

---

**Author:** Alejandra Botín  **Director:** Francisco Martín<br>
**Degree:** Double Major in Telecommunications Engineering and Business Analytics<br>
**Institution:** ICAI - Universidad Pontificia Comillas

