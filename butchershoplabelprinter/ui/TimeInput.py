from kivy.uix.textinput import TextInput


class TimeInput(TextInput):

    def do_backspace(self, from_undo: bool = False, mode: str = "bkspc"):
        if len(self.text) == 0:
            return
        if len(self.text) > 0 and self.text[-1] == ":":
            super().do_backspace(from_undo, mode)
        if len(self.text) <=2 and int(self.text) > 24 \
            or len(self.text) == 5 and int(self.text[3:-1]) > 59:
            self.background_color = [1, 0, 0, 1]
        else:
            self.background_color = [1, 1, 1, 1]
        super().do_backspace(from_undo, mode)
        

    def insert_text(self, substring: str, from_undo: bool = False):
        if not substring.isdigit or len(self.text) >= 5:
            return

        if len(self.text) == 1 and int(self.text + substring) > 23:
            self.background_color = [1, 0, 0, 1]
        elif len(self.text) >= 2 and int(self.text[0:2]) > 23:
            self.background_color = [1, 0, 0, 1]
        elif len(self.text) == 4 and int(self.text[3] + substring) > 59:
            self.background_color = [1, 0, 0, 1]
        else:
            self.background_color = [1, 1, 1, 1]
        return super().insert_text(
            substring if len(self.text) != 2 else ":" + substring, from_undo=from_undo
        )

    def validate_time(self) -> bool:
        return (
            len(self.text) == 5
            and int(self.text[0:2]) <= 23
            and int(self.text[3:5]) <= 59
        )
