from kivy.clock import Clock

from butchershoplabelprinter.app_config import *


if not DEBUG_MODE:
    from RPi import GPIO
    GPIO.setmode(GPIO.BCM)
    BEEPER_PIN = 26
    BEEPER_DELAY = 0.1
    GPIO.setup(BEEPER_PIN, GPIO.OUT)


class BeepBehavior:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(on_press=self.beep)

    def beep(self, _):
        if not DEBUG_MODE:
            GPIO.output(BEEPER_PIN, GPIO.HIGH)
            Clock.schedule_once(lambda _: GPIO.output(BEEPER_PIN, GPIO.LOW), timeout=BEEPER_DELAY)
