from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

from butchershoplabelprinter.dto.Cut import Cut

class PrinterLabel:

    id: Tuple[str, str] = (None, None)

    pixels: Tuple[int, int] = (696, 1109)

    dimension: Tuple[int, int] = (62, 100)

    label_uri: str = "resources/label/empty_label.png"

    font_uri: str = "resources/label/font.otf"

    # TODO fetch those dynamically via brother_ql.devicedependent.label_sizes
    
    def _new_text(self, text: str, font_size: int, x_part: float, y_part: float, align_right: bool = False, bold: bool = False):
        img_font = ImageFont.truetype(font=self.font_uri, size=font_size)
        width = self.draw.textbbox((0, 0), text=text, font=img_font)[2] if align_right else 0
        self.draw.text((self.pixels[1] / x_part - width, self.pixels[0] / y_part), text, stroke_width=1 if bold else 0, fill="black", font=img_font)

    def _new_icon(self, source: str, x_part: float, y_part: float):
        with Image.open(source) as icon:
            self.image.paste(icon, (int(self.pixels[1] * x_part), int((self.pixels[0] - icon.height) * y_part)))

   
    def _do_fill_in_label(self, cut: Cut, weight: Optional[float], game_no: Optional[str] = None):
        pass

    def __init__(self, cut: Cut, weight: Optional[float], game_no: Optional[str] = None):
        self.image = Image.open(self.label_uri)
        self.draw = ImageDraw.Draw(self.image)
        self._do_fill_in_label(cut, weight, game_no)


    @staticmethod
    def available_labels() -> List[str]:
        return [s.id[0] for s in PrinterLabel.__subclasses__()]