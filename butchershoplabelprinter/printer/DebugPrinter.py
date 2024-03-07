from typing import Tuple
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


from butchershoplabelprinter.ui.BeepButton import BeepButton

from butchershoplabelprinter.label.PrinterLabel import PrinterLabel
from butchershoplabelprinter.printer.Printer import Printer

class DebugPrinter(Printer):

    id: Tuple[str, str] = ("debug", "Debug Printer")

    temp_img_uri = "resources/temp/filled_label.png"

    def print_label(self, label: PrinterLabel) -> Tuple[int, str]:

        image = label.image

        image.save(DebugPrinter.temp_img_uri)

        button = BeepButton(text="OK", font_size="24sp", size_hint=(0.3, 0.3), padding=(20, 20), pos_hint={'center_x': 0.5})
        content = BoxLayout(orientation="vertical")
        content.add_widget(Image(source=DebugPrinter.temp_img_uri, nocache=True))
        content.add_widget(button)
        popup = Popup(title="Label", title_align="center", title_size="30sp", content=content, size_hint=(0.7, 0.5))
        button.bind(on_release=popup.dismiss)
        popup.open()

    # def __init__(self):
        
