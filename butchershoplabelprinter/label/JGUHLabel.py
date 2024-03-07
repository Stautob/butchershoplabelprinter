from typing import Optional, Tuple

from datetime import date

from butchershoplabelprinter.label.PrinterLabel import PrinterLabel
from butchershoplabelprinter.dto.Cut import Cut


class JGUHLabel(PrinterLabel):

    id: Tuple[str, str] = ("jguh", "JG Uster Hard")
    
    pixels: Tuple[int, int] = (696, 1109)

    dimension: Tuple[int, int] = (62, 100)
    
    label_uri: str = "resources/label/empty_label_jguh.png"


    def _do_fill_in_label(self, cut: Cut, weight: Optional[float], game_no: Optional[str] = None):

        self._new_text(cut.animal.title, 70, 2.42, 2.7)
        self._new_text(cut.title, 56, 2.38, 1.93)

        self._new_text(f"Verpackt am: {date.today().strftime('%d.%m.%Y')}", 36, 20, 1.24 if game_no else 1.107, bold=True)

        if game_no:
            self._new_text(f"ZH Wild Nr.: {game_no}", 36, 20, 1.107)

        if weight:
            self._new_text(f"Gewicht: {weight}g", 36, 20, 1.409 if game_no else 1.24)
            self._new_text(f"Preis: CHF {cut.price_per_kg * (weight / 1000):.2f}", 36, 1.086, 1.24, align_right=True)
            self._new_text(f"(CHF {cut.price_per_kg:.2f}/kg)", 36, 1.086, 1.107, align_right=True)

        self._new_icon(cut.animal.image_source, 1/20, 1/2)
  
  
    def __init__(self, cut: Cut, weight: Optional[float], game_no: Optional[str] = None):
        super().__init__(cut, weight, game_no)