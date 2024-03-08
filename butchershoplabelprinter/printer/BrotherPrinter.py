from typing import Tuple
from kivy.app import App

from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

from brother_ql.backends.pyusb import BrotherQLBackendPyUSB
from butchershoplabelprinter.label.PrinterLabel import PrinterLabel
from butchershoplabelprinter.printer.Printer import Printer

class BrotherPrinter(Printer):

    id: Tuple[str, str] = ("brother", "Brother Printer")

    # TODO convert from using argument parser calls to api calls
    def print_label(self, label: PrinterLabel) -> Tuple[int, str]:

        instructions = convert(qlr=self.qlr, cut=self.do_cut, threshold=99, images=[label.image], 
                               label=f"{label.dimension[0]}x{label.dimension[1]}")

        try:
            status = send(instructions=instructions, printer_identifier=self.printer_id, backend_identifier="pyusb", blocking=True)
            if status["outcome"] == "error":
                error = status["printer_state"]["errors"][0]
                if error == 'Media cannot be fed (also when the media end is detected)':
                    return (False, "Keine Etiketten!")
                elif error == "End of media (die-cut size only)":
                    return (False, "Etiketten aufgebraucht! Bitte nachfüllen.")
            return ( True, "Printed")
        except ValueError as e:
            if e.args and "Device not found" in e.args[0]:
                return (False, "Drucker nicht gefunden!\nIst der Drucker eingeschaltet?")
            print("BrotherPrinter:", e)
            return (False, str(e))

    def __init__(self):
        self.config = App.get_running_app().config
        available_printers = BrotherPrinter.available_printers()
        if not available_printers:
            raise Exception("No compatible printer found.")
        
        self.printer_id = available_printers[0]
        self.do_cut = self.config.getboolean("printer", "printer_cut")
        qlr = BrotherQLRaster(self.config.get("f", "printer_model"))
        qlr.exception_on_warning = True

        # self.printer = BrotherQLBackendPyUSB(self.printer_id)

    @staticmethod
    def available_printers():
        from brother_ql.backends.helpers import discover
        available_devices = discover(backend_identifier="pyusb")
        return [i["identifier"] for i in available_devices]