from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.popup import Popup


class ScalePopup(Popup):

    def __init__(self, callback):
        super(ScalePopup, self).__init__()
        self.callback = callback
        Clock.schedule_once(self.show_keyboard)

    def show_keyboard(self, event):
        self.ids.tif_weight.focus = True

    def finish(self):
        self.dismiss()
        input = self.ids.tif_weight.text
        self.callback(0 if not input else int(input))


class ManualScale:

    def __init__(self):
        super(ManualScale, self).__init__()

    def measure(self, callback):
        Factory.ScalePopup(callback).open()
