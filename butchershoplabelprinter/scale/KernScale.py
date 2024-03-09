from typing import Callable, Tuple
import serial

from butchershoplabelprinter.scale.Scale import Scale

# Format für stabile Werte für Gewicht/Stückzahl/Prozentangabe
# 1  2  3  4  5  6  7  8  9  10 11 12  13 14 15 16 17 18
# M  S  N1 N2 N3 N4 N5 N6 N7 N8 N9 N10 B  U1 U2 U3 CR LF
#
# Format im Fehlerfall
# 1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
# B  B  B  B  B  B  B  B  B  B  B  E  r  r  o  r  CR LF
#
# M Leerzeichen oder M
# S Leerzeichen oder negatives Vorzeichen (-)
# N1 … N10 10 numerische ASCII-Codes für Gewichtswerte einschließlich Dezi-
# malstelle oder Leerzeichen
# U1 … U3 3 ASCII-Codes für Wägeeinheit Stk. / % / oder Leerzeichen
# B Leerzeichen
# E, o, r ASCII-Code oder “E, o, r”
# CR Carriage Return
# LF (Line Feed)

class KernScale(Scale):

    id : Tuple[str,str] = ("kern", "Kern")
    
    isReal: bool = True

    isTareable: bool = True

    MSG_LENGTH = 18
    ERROR_SLICE = slice(12, 16)
    UNIT_SLICE = slice(13, 15)
    VALUE_SLICE = slice(1, 12)

    def measure(self, callback: Callable[[float], None]) -> None:
        with serial.Serial('/dev/ttyUSB0', 9600) as ser:
            ser.write(b'w')
            ser.flush()
            s = ser.read(KernScale.MSG_LENGTH)
            unit = s[KernScale.UNIT_SLICE].strip()
            error = s[KernScale.ERROR_SLICE]
            value = s[KernScale.VALUE_SLICE].strip()
            if unit != b"g":
                print(f"WARNING: Kern scale unit is not set to g! Unit is: {unit}")
                callback(0.0)
            elif error == b"error":
                raise Exception("Kern Scale Error")
            else:
                try:
                    callback(float(value))
                except:
                    print(f"Kern Scale Error: Unit:{unit}, ERROR:{error}, Value:{value}")
                    callback(0.0)

    def tare(self):
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
            ser.write(b't')
            ser.flush()

