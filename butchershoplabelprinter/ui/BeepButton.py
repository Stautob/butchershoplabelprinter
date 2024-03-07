from butchershoplabelprinter.BeepBehavior import BeepBehavior


from kivy.uix.button import Button


class BeepButton(Button, BeepBehavior):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)