from __future__ import annotations

from dataclasses import dataclass
from time import sleep
from typing import Union


@dataclass(frozen=True)
class WristAngles:
    flex_neutral:  float = 90.0
    flex_forward:  float = 0.0
    flex_backward: float = 180.0
    rot_neutral:   float = 0.0
    rot_left:      float = 0.0
    rot_right:     float = 180.0


class Wrist:
    def __init__(self, flex_servo, rot_servo, name: str = "wrist", angles: WristAngles | None = None):
        self.flex_servo = flex_servo
        self.rot_servo  = rot_servo
        self.name       = name
        self.angles     = angles or WristAngles()

    def neutral(self)   -> None: self.flex_servo.move_to(self.angles.flex_neutral);  self.rot_servo.move_to(self.angles.rot_neutral)
    def left(self)      -> None: self.rot_servo.move_to(self.angles.rot_left)
    def right(self)     -> None: self.rot_servo.move_to(self.angles.rot_right)
    def forward(self)   -> None: self.flex_servo.move_to(self.angles.flex_forward)
    def backward(self)  -> None: self.flex_servo.move_to(self.angles.flex_backward)

    def alternate_left_right(self, cycles: int = 2, delay: float = 0.25, end_neutral: bool = True) -> None:
        for _ in range(cycles):
            self.left();  sleep(delay)
            self.right(); sleep(delay)
        if end_neutral:
            self.rot_servo.move_to(self.angles.rot_neutral)

    def spin(self, cycles: int = 4, delay: float = 0.18, end_neutral: bool = True) -> None:
        for _ in range(cycles):
            self.left();  sleep(delay)
            self.right(); sleep(delay)
        if end_neutral:
            self.rot_servo.move_to(self.angles.rot_neutral)

    def apply_code(
        self,
        code: Union[int, str],
        *,
        delay_static: float = 0.0,
        dyn_cycles: int = 3,
        dyn_delay: float = 0.22,
        end_neutral: bool = True,
    ) -> None:
        c = self._normalize_code(code)

        static = {0: self.neutral, 1: self.left, 2: self.right, 3: self.forward, 4: self.backward}
        if c in static:
            static[c]()
            if delay_static > 0:
                sleep(delay_static)
            return

        if c == 5:
            self.spin(cycles=dyn_cycles, delay=dyn_delay, end_neutral=end_neutral)
            return
        if c == 6:
            self.alternate_left_right(cycles=dyn_cycles, delay=dyn_delay, end_neutral=end_neutral)
            return

        raise ValueError(f"[{self.name}] Código de muñeca no soportado: {c}")

    @staticmethod
    def _normalize_code(code: Union[int, str]) -> int:
        if isinstance(code, int):
            return code
        s = str(code).strip().lower()
        if s.isdigit():
            return int(s)
        alias = {
            "recta": 0, "neutral": 0,
            "izquierda": 1, "derecha": 2,
            "delante": 3, "atrás": 4, "atras": 4,
            "da vueltas": 5, "vueltas": 5,
            "izda/dcha": 6, "izda-dcha": 6,
        }
        if s in alias:
            return alias[s]
        raise ValueError(f"Código de muñeca desconocido: {code}")
