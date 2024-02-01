from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.popup import Popup


class ScalePopup(Popup):

    def __init__(self, callback):
        super(ScalePopup, self).__init__()
        self.callback = callback

    def finish(self):
        self.dismiss()
        weight = self.ids.tif_pu.text
        Clock.schedule_once(lambda ignored: self.callback(0 if not weight else int(weight)), 0.11)


class ManualScale:

    def __init__(self):
        super(ManualScale, self).__init__()

    def measure(self, callback):
        Factory.ScalePopup(callback).open()


