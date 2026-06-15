from servo_controller import ServoController
from finger import Finger, FingerAngles, FingersController
from wrist import Wrist, WristAngles

GPIO_THUMB      = 17
GPIO_INDEX      = 27
GPIO_MIDDLE     = 22
GPIO_RING       = 23
GPIO_LITTLE     = 24
GPIO_WRIST_ROT  = 12
GPIO_WRIST_FLEX = 13


def inicializar_mano():
    angulos = FingerAngles(open_angle=0.0, mid_angle=90.0, closed_angle=180.0)

    fingers = FingersController([
        Finger(ServoController(GPIO_THUMB),   "Thumb",   angulos),
        Finger(ServoController(GPIO_INDEX),   "Index",   angulos),
        Finger(ServoController(GPIO_MIDDLE),  "Middle",  angulos),
        Finger(ServoController(GPIO_RING),    "Ring",    angulos),
        Finger(ServoController(GPIO_LITTLE),  "Little",  angulos),
    ])

    wrist = Wrist(
        flex_servo=ServoController(GPIO_WRIST_FLEX),
        rot_servo=ServoController(GPIO_WRIST_ROT),
        angles=WristAngles(
            flex_neutral=90.0, flex_forward=0.0, flex_backward=180.0,
            rot_neutral=90.0,  rot_left=0.0,     rot_right=180.0,
        ),
    )

    return fingers, wrist
