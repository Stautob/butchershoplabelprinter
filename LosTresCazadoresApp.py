import kivy
from kivy.app import App
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


class MainScreen(Screen):
    title = "main"

    def __init__(self):
        super(MainScreen, self).__init__(name=MainScreen.title)

    # kivy.resources.resource_add_path("resources/images")

    def check_status(self, btn):
        print('button state is: {state}'.format(state=btn.state))
        print('text input text is: {txt}'.format(txt=self.txt_inpt))

    def open_settings(self):
        print("This would open the settings")


class SettingsScreen(Screen):
    title = "settings"

    def __init__(self):
        super(SettingsScreen, self).__init__(name=SettingsScreen.title)


class AnimalScreen(Screen):

    def __init__(self, title, products):
        super(AnimalScreen, self).__init__(name=title)
        self.title = StringProperty(title)
        self.products = ListProperty(products)

    def get_title(self):
        return self.title


class RoeScreen(AnimalScreen):

    def __init__(self):
        super(RoeScreen, self).__init__("Reh", {"Schnitzel", "Filet"})


class LosTresCazadoresApp(App):
    sm = ScreenManager()

    def switchToMain(self):
        self.sm.current = MainScreen.title

    def switchToSettings(self):
        self.sm.current = SettingsScreen.title

    def build(self):
        self.sm.add_widget(MainScreen())
        self.sm.current= MainScreen.title
        self.sm.add_widget(RoeScreen())
        return self.sm


if __name__ == '__main__':
    LosTresCazadoresApp().run()