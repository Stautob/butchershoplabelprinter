from typing import List, Tuple

from butchershoplabelprinter.label.PrinterLabel import PrinterLabel


class Printer:

    id: Tuple[str, str] = (None, None)

    def print_label(self, label: PrinterLabel) -> Tuple[bool, str]:
        pass

    @staticmethod
    def available_printers() -> List[str]:
        return [s.id[0] for s in Printer.__subclasses__()]
