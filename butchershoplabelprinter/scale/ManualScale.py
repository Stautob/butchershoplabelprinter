from typing import Callable, Tuple
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.popup import Popup

from butchershoplabelprinter.scale.Scale import Scale


class ScalePopup(Popup):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def finish(self):
        self.dismiss()
        weight = self.ids.tif_pu.text
        Clock.schedule_once( lambda _: self.callback(0 if not weight else int(weight)), 0.11 )


class ManualScale(Scale):

    id : Tuple[str,str] = ("manual", "Manuell")

    def measure(self, callback: Callable[[float], None]) -> None:
        Factory.ScalePopup(callback).open()

