#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ReferenceListProperty


###########################################################


class TimePicker(TextInput):

    pHint_x = NumericProperty(0.7)
    pHint_y = NumericProperty(0.7)
    pHint = ReferenceListProperty(pHint_x, pHint_y)

    def __init__(self, touch_switch=False, *args, **kwargs):
        super(TimePicker, self).__init__(*args, **kwargs)

        self.touch_switch = touch_switch
        self.init_ui()

    def init_ui(self):
        self.text = current_time()
        self.halign = "center"
        self.valign = "middle"
        self.popup = TimePopup(on_dismiss=self.update_value, title="Time")
        self.bind(focus=self.show_popup)

    def show_popup(self, _, val):
        """
        Open popup if textinput focused,
        and regardless update the popup size_hint
        """
        self.popup.size_hint = self.pHint
        if val:
            # Automatically dismiss the keyboard
            # that results from the textInput
            Window.release_all_keyboards()
            self.popup.open()

    def update_value(self, time_popup):
        self.text = time_popup.ids.tif_pu.text
        self.focus = False


class TimePopup(Popup):

    def finish(self):
        if self.ids.tif_pu.validate_time():
            self.dismiss()


def current_time():
    return datetime.now().strftime("%H:%M")


if __name__ == "__main__":
    from kivy.base import runTouchApp

    c = TimePicker()
    runTouchApp(c)
