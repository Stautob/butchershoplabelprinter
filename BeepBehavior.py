from RPi import GPIO
from kivy.clock import Clock

GPIO.setmode(GPIO.BCM)
BEEPER_PIN = 26
BEEPER_DELAY = 0.1
GPIO.setup(BEEPER_PIN, GPIO.OUT)


class BeepBehavior:
    def __init__(self):
        super(BeepBehavior, self).__init__()
        self.bind(on_press=self.beep)

    def beep(self, _):
        GPIO.output(BEEPER_PIN, GPIO.HIGH)
        Clock.schedule_once(lambda _: GPIO.output(BEEPER_PIN, GPIO.LOW), timeout=BEEPER_DELAY)
