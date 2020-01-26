import json
from datetime import date
from math import ceil

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os 
os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.app import App
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import ListProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.textinput import TextInput

from BeepBehavior import BeepBehavior
from DummyScale import DummyScale
from ExtendedSettings import ExtendedSettings
from ManualScale import ManualScale


class AnimalButton(BeepBehavior, ButtonBehavior, BoxLayout):
    background_color = ListProperty([1, 1, 1, 1])
    background_normal = StringProperty('atlas://data/images/defaulttheme/button')

    background_down = StringProperty(
        background_disabled_normal=StringProperty('atlas://data/images/defaulttheme/button_disabled'))
    background_disabled_down = StringProperty('atlas://data/images/defaulttheme/button_disabled_pressed')
    border = ListProperty([16, 16, 16, 16])

    def __init__(self, text, image_source):
        super(AnimalButton, self).__init__()
        self.text = text
        self.source = image_source


class NumericInput(TextInput):

    def __init__(self, **kwargs):
        super(NumericInput, self).__init__(**kwargs)
        keyboard = Window.request_keyboard(self.keyboard_close, self, input_type="number")
        if keyboard.widget:
            vkeyboard = keyboard.widget
            vkeyboard.layout = "numeric.json"

    def keyboard_close(self):
        pass


class BeepButton(Button, BeepBehavior):

    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)


class GameNoPopup(Popup):

    def __init__(self, callback):
        super(GameNoPopup, self).__init__()
        self.callback = callback

    def finish(self):
        self.dismiss()
        self.callback(self.ids.tif_pu.text)


class AnimalsScreen(Screen):
    title = "main"

    def __init__(self, animals):
        super(AnimalsScreen, self).__init__(name=AnimalsScreen.title)
        self.update_animals(animals)

    def update_animals(self, animals):
        grid_animals = self.ids.grid_animals
        grid_animals.clear_widgets()
        grid_animals.rows = ceil(len(animals) / grid_animals.cols)
        for animal in animals:
            button = Factory.AnimalButton(text=animal.title, image_source=animal.image_source)
            button.bind(on_release=App.get_running_app().switch_to_button)
            grid_animals.add_widget(button)


class TextPosition:
    (W, H) = 1109, 696

    def __init__(self, text, font_size, x_part, y_part, align_right):
        self.text = text
        self.font = ImageFont.truetype(font="resources/label/font.otf", size=font_size)
        self.x_part = x_part
        self.y_part = y_part
        self.align_right = align_right

    def draw(self, draw):
        if self.align_right:
            w, h = draw.textsize(self.text, font=self.font)
            draw.text((TextPosition.W / self.x_part - w, TextPosition.H / self.y_part), self.text, fill="black",
                      font=self.font)
        else:
            draw.text((TextPosition.W / self.x_part, TextPosition.H / self.y_part), self.text, fill="black",
                      font=self.font)


class CutScreen(Screen):

    def __init__(self, animal):
        super(CutScreen, self).__init__(name=animal.title)
        self.animal = animal
        self.ids.lbl_title.text = animal.title
        self.ids.img_title.source = animal.image_source
        if not animal.game_no:
            self.ids.lbl_title.size_hint_x += self.ids.tif_game_no.size_hint_x
            self.ids.lay_bar.remove_widget(self.ids.tif_game_no)
        grid_cuts = self.ids.grid_cuts
        grid_cuts.rows = ceil(len(animal.cuts) / grid_cuts.cols)
        for cut in animal.cuts:
            button = Factory.BigButton(text=cut.title, size_hint=(0.333, 0.488))
            button.bind(on_press=self.print_label)
            grid_cuts.add_widget(button)

    def print_label(self, btn):
        scale = App.get_running_app().scale
        scale.measure(lambda w: self.send_label_to_printer(
            self.fill_in_label([p for p in self.animal.cuts if p.title == btn.text][0], w)))

    def send_label_to_printer(self, image):
        from brother_ql.conversion import convert
        from brother_ql.backends.helpers import send
        from brother_ql.raster import BrotherQLRaster
        config = LosTresCazadoresApp.config
        printer = config.get("printer", "printer_id")
        qlr = BrotherQLRaster(config.get("printer", "printer_model"))
        qlr.exception_on_warning = True
        instructions = convert(qlr=qlr,
                               cut=config.getboolean("printer", "printer_cut"),
                               label=config.get("printer", "printer_label_size"),
                               images=[image],
                               threshold=99)

        try:
            status = send(instructions=instructions, printer_identifier=printer, backend_identifier="pyusb",
                          blocking=True)
            if status["outcome"] == "error":
                error = status["printer_state"]["errors"][0]
                translation = error
                if error == 'Media cannot be fed (also when the media end is detected)':
                    translation = "Keine Etiketten!"
                elif error == "End of media (die-cut size only)":
                    translation = "Etiketten aufgebraucht! Bitte nachfüllen."
                self.popup("Fehler", translation)
            print(status)
        except ValueError as e:
            if e.args and "Device not found" in e.args[0]:
                self.popup("Fehler", "Drucker nicht gefunden!\nIst der Drucker eingeschaltet?")
            print(e)

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

    def fill_in_label(self, cut, weight):
        img = Image.open("resources/label/empty_label.png")
        draw = ImageDraw.Draw(img)
        TextPosition(self.animal.title, 70, 2.42, 2.7, False).draw(draw)
        TextPosition(cut.title, 56, 2.38, 1.93, False).draw(draw)
        TextPosition("Verpackt: {}".format(date.today().strftime('%d.%m.%Y')), 36, 20, 1.107, False).draw(draw)
        if self.game_no:
            TextPosition("ZH Wild Nr.: {}".format(self.game_no), 36, 20, 1.409 if weight else 1.24, False).draw(draw)

        if weight:
            TextPosition("Gewicht: {}g".format(weight), 36, 20, 1.24, False).draw(draw)
            TextPosition("Preis: CHF {:.2f}".format(cut.price_per_kg * (weight / 1000)), 36, 1.086, 1.24, True).draw(
                draw)
            TextPosition("(CHF {:.2f}/kg)".format(cut.price_per_kg), 36, 1.086, 1.107, True).draw(draw)

        animal_icon = Image.open(self.animal.image_source)
        img.paste(animal_icon, (int(1109 / 20), int((696 - animal_icon.height) / 2)))
        return img

    def open_game_no_popup(self):
        Factory.GameNoPopup(self.set_game_no).open()

    def set_game_no(self, no):
        self.ids.tif_game_no.text = no


class ClickableBeepLabel(ButtonBehavior, Label, BeepBehavior):

    def __init__(self, **kwargs):
        super(ClickableBeepLabel, self).__init__(**kwargs)


class Cut:

    def __init__(self, title, price_per_kg):
        self.title = title
        self.price_per_kg = price_per_kg


class Animal:

    def __init__(self, animal_json):
        self.title = animal_json['title']
        self.sets = animal_json['sets']
        self.image_source = animal_json['icon_source']
        self.game_no = animal_json['gameNo']
        self.cuts = [Cut(p['title'], p['pricePerKg']) for p in animal_json['cuts']]


class LosTresCazadoresApp(App):
    config = ConfigParser()
    config.read('lostrescazadores.ini')

    sm = ScreenManager(transition=NoTransition())
    animals = []
    scale = None

    def __init__(self):
        super(LosTresCazadoresApp, self).__init__()
        LosTresCazadoresApp.scale = LosTresCazadoresApp.get_scale(
            LosTresCazadoresApp.config.get("usage", "active_scale_module"))

    with open('items.json') as json_file:
        items = json.load(json_file)
        animals.extend([Animal(animal) for animal in items['animals']])

    def switch_to_button(self, btn):
        self.sm.current = btn.text

    def switch_to_main(self):
        self.sm.current = AnimalsScreen.title

    def build(self):
        self.settings_cls = ExtendedSettings
        self.main_widget = AnimalsScreen(self.get_active_animals(self.get_active_game_sets()))
        self.sm.add_widget(self.main_widget)
        self.sm.current = AnimalsScreen.title
        for animal in LosTresCazadoresApp.animals:
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
        btn_ok.bind(on_release=lambda ignore: Clock.schedule_once(self.shutdown, 0.11))
        popup.open()

    def shutdown(self, ignored):
        print("shutdown")
        os.system('systemctl poweroff')

    def get_active_game_sets(self):
        return LosTresCazadoresApp.config.get("usage", "active_game_sets").split(';')

    def get_active_animals(self, active_game_sets):
        return [a for a in LosTresCazadoresApp.animals if any(s in a.sets for s in active_game_sets)]

    def build_config(self, config):
        config.setdefaults('usage', {
            'active_scale_module': "none",
            'active_game_sets': "all;"
        })
        config.setdefaults("printer", {
            "printer_model": "QL-800",
            "printer_id": "",
            "printer_label_size": "62x100",
            "printer_cut": True
        })

    def build_settings(self, settings):
        settings.add_json_panel('Benutzereinstellungen', self.config, filename='settings.json')

    def on_config_change(self, config, section,
                         key, value):
        LosTresCazadoresApp.config.set(section, key, value)
        if key == "active_game_sets":
            self.main_widget.update_animals(self.get_active_animals(value.split(';')))
        elif key == "active_scale_module":
            LosTresCazadoresApp.scale = LosTresCazadoresApp.get_scale(value)

    @staticmethod
    def get_scale(value):
        if value == "Keins":
            return DummyScale()
        elif value == "Manuell":
            return ManualScale()
        elif value == "USB":
            return ManualScale()


def available_game_sets():
    return set((s for animal in LosTresCazadoresApp.animals for s in animal.sets))


def available_printers():
    from brother_ql.backends.helpers import discover
    available_devices = discover(backend_identifier="pyusb")
    return [i["identifier"] for i in available_devices]


if __name__ == '__main__':
    LosTresCazadoresApp().run()
