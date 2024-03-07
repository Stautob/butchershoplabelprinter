from typing import Callable, Tuple
import serial

from butchershoplabelprinter.scale.Scale import Scale

# Format für stabile Werte für Gewicht/Stückzahl/Prozentangabe
# 1 2 3  4  5  6  7  8  9  10 11 12  13 14 15 16 17 18
# M S N1 N2 N3 N4 N5 N6 N7 N8 N9 N10 B  U1 U2 U3 CR LF
#
# Format im Fehlerfall
# 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
# B B B B B B B B B B  B  E  r  r  o  r  CR LF
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

    ERROR_BYTES = b"           Error\r\n"

    def measure(self, callback: Callable[[float], None]) -> None:
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
            ser.write(b'w')
            ser.flush()
            s = ser.read(18)
            if not s[12:16] == b"error":
                try:
                    print("Unit", s[13:15])
                    callback(float(s[2:12].strip()))
                except:
                    print("Error: " + str(s) + " , " + str(s[2:12]))
            else:
                raise Exception("Waage Error")

    def tare(self):
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
            ser.write(b't')
            ser.flush()

