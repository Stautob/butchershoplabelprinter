import serial
from kivy.factory import Factory

class KernScale:

    def __init__(self):
        super(KernScale, self).__init__()

    def measure(self, callback):
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
            ser.write(b'w')
            ser.flush()
            s = ser.read(18)
            error_string = s[12:16]
            print(s)
            if not error_string == b"error":
                callback(float(s[2:12].strip()))
            else:
                raise Exception("Waage Error")

    def tare(self):
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
            ser.write(b't')
            ser.flush()

