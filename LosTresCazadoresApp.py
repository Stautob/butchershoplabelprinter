from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MainWidget(BoxLayout):

    def check_status(self, btn):
        print('button state is: {state}'.format(state=btn.state))
        print('text input text is: {txt}'.format(txt=self.txt_inpt))


class LosTresCazadoresApp(App):

    def build(self):
        return MainWidget()


if __name__ == '__main__':
    LosTresCazadoresApp().run()