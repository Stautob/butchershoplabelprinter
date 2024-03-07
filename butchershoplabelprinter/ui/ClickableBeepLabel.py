from butchershoplabelprinter.BeepBehavior import BeepBehavior


from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.properties import AliasProperty, StringProperty


class ClickableBeepLabel(ButtonBehavior, Label, BeepBehavior):
    _hint_text = StringProperty('')
    _text = StringProperty('')

    def _get_hint_text(self):
        return self._hint_text

    def _set_hint_text(self, value):
        if isinstance(value, bytes):
            value = value.decode('utf8')
        self._hint_text = value
        self._label.text = value

    hint_text = AliasProperty(_get_hint_text, _set_hint_text, bind=('_hint_text', ))


    def _set_text(self, text):
        self._text = text
        self.color = [0.25, 0.25, 0.25, 1] if text else [0, 0, 0, 1]
        self._label.text = text if text else self._hint_text


    def _get_text(self):
        return self._text

    text = AliasProperty(_get_text, _set_text,  bind=('_text', '_hint_text' ))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)