from __future__ import annotations

from dataclasses import dataclass
from time import sleep
from typing import List, Sequence


@dataclass(frozen=True)
class FingerAngles:
    open_angle:   float = 0.0
    mid_angle:    float = 90.0
    closed_angle: float = 180.0


class Finger:
    def __init__(self, servo, name: str = "", angles: FingerAngles | None = None):
        self.servo  = servo
        self.name   = name
        self.angles = angles or FingerAngles()

    def set_position(self, level: int | str) -> None:
        angle = self._level_to_angle(self._normalize_level(level))
        self.servo.move_to(angle)

    def open(self)  -> None: self.set_position(0)
    def half(self)  -> None: self.set_position(1)
    def close(self) -> None: self.set_position(2)

    def open_close_hand(self, times: int = 1, delay: float = 0.5) -> None:
        for _ in range(times):
            self.close(); sleep(delay)
            self.open();  sleep(delay)

    def _level_to_angle(self, level: int) -> float:
        if level == 0: return self.angles.open_angle
        if level == 1: return self.angles.mid_angle
        if level == 2: return self.angles.closed_angle
        raise ValueError(f"[{self.name}] Nivel inválido: {level}. Debe ser 0, 1 o 2.")

    @staticmethod
    def _normalize_level(level: int | str) -> int:
        if isinstance(level, int):
            return level
        s = str(level).strip().lower()
        if s in {"open", "abierto", "0"}:  return 0
        if s in {"half", "media", "mitad", "1"}: return 1
        if s in {"close", "closed", "cerrado", "2"}: return 2
        raise ValueError(f"Nivel de posición desconocido: {level}")


class FingersController:
    def __init__(self, fingers: Sequence[Finger]):
        if len(fingers) != 5:
            raise ValueError("Se necesitan exactamente 5 dedos.")
        self.fingers: List[Finger] = list(fingers)

    def set_pose(self, pose: Sequence[int | str], delay_between: float = 0.0) -> None:
        if len(pose) != 5:
            raise ValueError("La pose debe tener 5 valores.")
        for finger, level in zip(self.fingers, pose):
            finger.set_position(level)
            if delay_between > 0:
                sleep(delay_between)

    def open_all(self)  -> None: self.set_pose([0, 0, 0, 0, 0])
    def close_all(self) -> None: self.set_pose([2, 2, 2, 2, 2])
    def half_all(self)  -> None: self.set_pose([1, 1, 1, 1, 1])

    def demo(self, times: int = 1, delay: float = 0.5) -> None:
        for _ in range(times):
            self.close_all(); sleep(delay)
            self.open_all();  sleep(delay)
