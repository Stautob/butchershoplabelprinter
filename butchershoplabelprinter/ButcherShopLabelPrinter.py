import json
from math import ceil
import time

import os
from typing import List
# os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.app import App
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.factory import Factory
from kivy.factory import Factory
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from butchershoplabelprinter.printer.Printer import Printer
from butchershoplabelprinter.ui.BeepButton import BeepButton

from butchershoplabelprinter.dto.Animal import Animal
from butchershoplabelprinter.dto.Cut import Cut

from butchershoplabelprinter.ui.DatePicker import DatePicker
from butchershoplabelprinter.BeepBehavior import BeepBehavior
from butchershoplabelprinter.settings.ExtendedSettings import ExtendedSettings
from butchershoplabelprinter.label.PrinterLabel import PrinterLabel
from butchershoplabelprinter.scale.ManualScale import ManualScale

from butchershoplabelprinter.scale.Scale import Scale

from butchershoplabelprinter.ui.TimePicker import TimePicker

from butchershoplabelprinter.app_config import *

if not DEBUG_MODE:
    from RPi import GPIO

SCALE_POWER_PIN = 5
PRINTER_POWER_PIN = 6
if not DEBUG_MODE:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SCALE_POWER_PIN, GPIO.OUT)
    GPIO.setup(PRINTER_POWER_PIN, GPIO.OUT)
POWER_DELAY = 0.9


class AnimalButton(BeepBehavior, ButtonBehavior, BoxLayout):
    background_color = ListProperty([1, 1, 1, 1])
    background_normal = StringProperty('atlas://data/images/defaulttheme/button')

    background_down = StringProperty(background_disabled_normal=StringProperty('atlas://data/images/defaulttheme/button_disabled'))
    background_disabled_down = StringProperty('atlas://data/images/defaulttheme/button_disabled_pressed')
    border = ListProperty([16, 16, 16, 16])

    def __init__(self, text: str, image_source: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.source = image_source


class GameNoPopup(Popup):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def finish(self):
        self.dismiss()
        self.callback(self.ids.tif_pu.text)


class AnimalsScreen(Screen):
    title = "main"

    def __init__(self, animals):
        super().__init__(name=AnimalsScreen.title)
        self.update_animals(animals)

    def update_animals(self, animals):
        grid_animals = self.ids.grid_animals
        grid_animals.clear_widgets()
        grid_animals.rows = ceil(len(animals) / grid_animals.cols)
        for animal in animals:
            button = Factory.AnimalButton(text=animal.title, image_source=animal.image_source)
            button.bind(on_release=App.get_running_app().switch_to_button)
            grid_animals.add_widget(button)


class CutScreen(Screen):

    def __init__(self, animal):
        super().__init__(name=animal.title)
        self.animal = animal
        self.ids.lbl_title.text = animal.title
        self.ids.img_title.source = animal.image_source

        ButcherShopLabelPrinterApp.bind(on_active_scale=lambda _, s: print("New Scale: ", s))

        self.show_or_hide_scale_buttons(animal, App.get_running_app().scale)
        grid_cuts = self.ids.grid_cuts
        grid_cuts.rows = ceil(len(animal.cuts) / grid_cuts.cols)
        for cut in animal.cuts:
            button = Factory.BigButton(text=cut.title, size_hint=(0.333, 0.488))
            button.bind(on_press=lambda _, cut=cut: self.print_label(cut))
            grid_cuts.add_widget(button)

    def show_or_hide_buttons(self, animal: Animal, scale: Scale):
        if not animal.game_no:
            self.ids.lbl_title.size_hint_x += self.ids.tif_game_no.size_hint_x
            self.ids.lay_bar.remove_widget(self.ids.tif_game_no)
        if scale.tarable:
            self.ids.lbl_title.size_hint_x += self.ids.btn_tare.size_hint_x
            self.ids.lay_bar.remove_widget(self.ids.btn_tare)
        if scale.isReal:
            self.ids.lbl_title.size_hint_x += self.ids.btn_weight.size_hint_x
            self.ids.lay_bar.remove_widget(self.ids.btn_weight)

    def print_label(self, cut: Cut):
        App.get_running_app().scale.measure(lambda weight: self.print_label_with_weight(cut, weight))

    def print_label_with_weight(self, cut: Cut, weight_in_g: float):
        app =  App.get_running_app()
        printer: Printer = app.printer_class()
        game_no = self.ids.tif_game_no.text
        printer_label: PrinterLabel = app.printer_label_class(cut, weight_in_g, game_no)
        printer.print_label(printer_label)

    def popup(self, text, translation):
        button = BeepButton(text="OK", font_size="24sp", size_hint=(0.3, 0.3), padding=(20, 20),
                            pos_hint={'center_x': 0.5})
        label = Label(text=translation, font_size="24sp", valign='middle')
        content = BoxLayout(orientation="vertical")
        content.add_widget(label)
        content.add_widget(button)
        popup = Popup(title=text, title_align="center", title_size="30sp", content=content, size_hint=(0.7, 0.5))
        button.bind(on_release=popup.dismiss)
        popup.open()


    def open_game_no_popup(self):
        Factory.GameNoPopup(self.set_game_no).open()

    def set_game_no(self, no: int):
        self.ids.tif_game_no.text = no



def set_date_if_necessary(dismiss_popup, new_date, new_time):
    import os
    os.system('sudo date +%Y%m%d -s "{}{:>02}{:>02}"'.format(new_date[2], new_date[1], new_date[0]))
    os.system('sudo date +%T -s "{}:{}:00"'.format(new_time[0], new_time[1]))
    os.system('sudo /sbin/hwclock -w')
    dismiss_popup()


class ButcherShopLabelPrinterApp(App):
    config: ConfigParser = ConfigParser()
    config.read(os.path.dirname(__file__) + '/butchershoplabelprinter.ini')

    sm = ScreenManager(transition=NoTransition())
    animals: List[Animal] = []
    scale: Scale = None
    active_scale = ObjectProperty()
    printer_label_class: type[PrinterLabel] = None
    printer_class: type[Printer] = None

    with open(os.path.dirname(__file__) + '/items.json') as json_file:
        items = json.load(json_file)
        animals.extend([Animal(animal) for animal in items['animals']])

    def __init__(self):
        super().__init__()
        ButcherShopLabelPrinterApp.scale = ButcherShopLabelPrinterApp.get_scale(ButcherShopLabelPrinterApp.config.get("usage", "active_scale_module"))
        ButcherShopLabelPrinterApp.printer_label_class = ButcherShopLabelPrinterApp.get_label(ButcherShopLabelPrinterApp.config.get("printer", "active_label"))
        ButcherShopLabelPrinterApp.printer_class = ButcherShopLabelPrinterApp.get_printer(ButcherShopLabelPrinterApp.config.get("printer", "active_printer"))

    def switch_to_button(self, btn):
        self.sm.current = btn.text

    def switch_to_main(self):
        self.sm.current = AnimalsScreen.title

    def cut(self):
        self.printer.cut()

    def tare(self):
        self.scale.tare()

    def set_date_popup(self):
        btn_ok = BeepButton(text="OK", font_size="24sp")
        content = BoxLayout(orientation="vertical", spacing=10)
        date_label = DatePicker(font_size="30sp")
        time_label = TimePicker(font_size="30sp")
        content.add_widget(date_label)
        content.add_widget(time_label)
        content.add_widget(btn_ok)
        popup = Popup(title="Datum", title_align="center", title_size="30sp", content=content, size_hint=(0.5, 0.5))
        btn_ok.bind(on_release=lambda _: set_date_if_necessary(popup.dismiss, date_label.text.split("."), time_label.text.split(":")))
        popup.open()

    def measure_popup(self):
        self.scale.measure(self.open_measure_popup)

    def open_measure_popup(self, weight):
        btn_ok = BeepButton(text="OK", font_size="24sp")
        content = BoxLayout(orientation="vertical", spacing=10)
        label = Label(text=str(weight) + " g", font_size="30sp")
        content.add_widget(label)
        content.add_widget(btn_ok)
        popup = Popup(title="Gewicht", title_align="center", title_size="30sp", content=content, size_hint=(0.5, 0.5))
        btn_ok.bind(on_release=popup.dismiss)
        popup.open()

    def build(self):
        toggle_on_off_devices()
        self.settings_cls = ExtendedSettings
        animals_screen = AnimalsScreen(self.get_active_animals(self.get_active_game_sets()))
        if not callable(getattr(self.scale, "tare", None)):
            as_ids = animals_screen.ids
            as_ids.lbl_title.size_hint_x += as_ids.btn_tare.size_hint_x
            as_ids.bl_title_bar.remove_widget(as_ids.btn_tare)
            as_ids.lbl_title.size_hint_x += as_ids.btn_weight.size_hint_x
            as_ids.bl_title_bar.remove_widget(as_ids.btn_weight)

        self.main_widget = animals_screen
        self.sm.add_widget(self.main_widget)
        self.sm.current = AnimalsScreen.title
        for animal in ButcherShopLabelPrinterApp.animals:
            self.sm.add_widget(CutScreen(animal))
        return self.sm

    def try_shutdown(self):
        btn_ok = BeepButton(text="OK", font_size="24sp")
        btn_cncl = BeepButton(text="Abbrechen", font_size="24sp")
        content = BoxLayout(orientation="horizontal", spacing=10)
        content.add_widget(btn_cncl)
        content.add_widget(btn_ok)
        popup = Popup(title="Drucker Herunterfahren?", title_align="center", title_size="30sp", content=content,
                      size_hint=(0.7, 0.3))
        btn_cncl.bind(on_release=popup.dismiss)
        btn_ok.bind(on_release=lambda _: Clock.schedule_once(self.shutdown, 0.11))
        popup.open()

    def shutdown(self, _):
        print("shutdown")
        toggle_on_off_devices()
        if not DEBUG_MODE:
            GPIO.cleanup()
        os.system('systemctl poweroff')

    def get_active_game_sets(self):
        return ButcherShopLabelPrinterApp.config.get("usage", "active_game_sets").split(';')

    def get_active_animals(self, active_game_sets):
        return [a for a in ButcherShopLabelPrinterApp.animals if any(s in a.sets for s in active_game_sets)]

    def build_settings(self, settings: ExtendedSettings):
        settings.add_json_panel('Benutzereinstellungen', ButcherShopLabelPrinterApp.config, filename=os.path.dirname(__file__) + '/settings.json')

    def on_config_change(self, config, section, key, value):
        config.set(section, key, value)
        if key == "active_game_sets":
            self.main_widget.update_animals(self.get_active_animals(value.split(';')))
        elif key == "active_label":
            ButcherShopLabelPrinterApp.printer_label_class = ButcherShopLabelPrinterApp.get_label(value)
        elif key == "active_printer":
            ButcherShopLabelPrinterApp.printer_class = ButcherShopLabelPrinterApp.get_printer(value)
        elif key == "active_scale_module":
            ButcherShopLabelPrinterApp.scale = ButcherShopLabelPrinterApp.get_scale(value)
            ButcherShopLabelPrinterApp.active_scale = ButcherShopLabelPrinterApp.get_scale(value)
            # TODO update Tare button

    @staticmethod
    def get_scale(key: str) -> Scale:
        matching = [s for s in Scale.__subclasses__() if s.id[0] == key]
        return matching[0]() if matching else ManualScale()
    
    @staticmethod
    def get_printer(key: str) -> type[Printer]:
        matching = [s for s in Printer.__subclasses__() if s.id[0] == key]
        return matching[0] if matching else Printer
    
    @staticmethod
    def get_label(key: str) -> type[PrinterLabel]:
        matching = [s for s in PrinterLabel.__subclasses__() if s.id[0] == key]
        return matching[0] if matching else PrinterLabel


def available_game_sets():
    return set((s for animal in ButcherShopLabelPrinterApp.animals for s in animal.sets))


def toggle_on_off_devices():
    if not DEBUG_MODE:
        GPIO.output(SCALE_POWER_PIN, GPIO.HIGH)
        GPIO.output(PRINTER_POWER_PIN, GPIO.HIGH)
        time.sleep(POWER_DELAY)
        GPIO.output(SCALE_POWER_PIN, GPIO.LOW)
        GPIO.output(PRINTER_POWER_PIN, GPIO.LOW)

def start():
    ButcherShopLabelPrinterApp().run()
    toggle_on_off_devices()

if __name__ == '__main__':
    start()
