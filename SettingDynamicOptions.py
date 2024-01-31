import importlib

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingOptions, SettingSpacer, SettingItem
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget


class SettingDynamicOptions(SettingOptions):
    '''Implementation of an option list that creates the items in the possible
        options list by calling an external method, that should be defined in
        the settings class.'''

    function_string = StringProperty()
    '''The function's name to call each time the list should be updated.
    It should return a list of strings, to be used for the options.
    '''

    def _create_popup(self, instance):
        # Update the 
        mod_name, func_name = self.function_string.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        self.options = func()

        # Call the parent __init__
        super(SettingDynamicOptions, self)._create_popup(instance)


class SettingMultipleOptions(SettingItem):
    options = ListProperty([])
    '''List of all availables options. This must be a list of "string" items.
    Otherwise, it will crash. :)

    :attr:`options` is a :class:`~kivy.properties.ListProperty` and defaults
    to [].
    '''

    popup = ObjectProperty(None, allownone=True)
    '''(internal) Used to store the current popup when it is shown.

    :attr:`popup` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    def on_panel(self, instance, value):
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def _set_option(self, instance):
        tag = "{};".format(instance.text)
        if tag in self.value:
            self.value = self.value.replace(tag, "")
        else:
            self.value += tag
        self.popup.dismiss()

    def _create_popup(self, instance):
        # create the popup
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            content=content, title=self.title, size_hint=(None, None),
            size=(popup_width, '400dp'))
        popup.height = len(self.options) * dp(55) + dp(150)

        # add all the options
        content.add_widget(Widget(size_hint_y=None, height=1))
        uid = str(self.uid)
        for option in self.options:
            state = 'down' if "{};".format(option) in self.value else 'normal'
            btn = ToggleButton(text=option, state=state, group=uid)
            btn.bind(on_release=self._set_option)
            content.add_widget(btn)

        # finally, add a cancel button to return on the previous panel
        content.add_widget(SettingSpacer())
        btn = Button(text='Cancel', size_hint_y=None, height=dp(50))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)

        # and open the popup !
        popup.open()


class SettingMultipleDynamicOptions(SettingMultipleOptions):
    '''Implementation of an option list that creates the items in the possible
        options list by calling an external method, that should be defined in
        the settings class.'''

    function_string = StringProperty()
    '''The function's name to call each time the list should be updated.
    It should return a list of strings, to be used for the options.
    '''

    def _create_popup(self, instance):
        # Update the options
        mod_name, func_name = self.function_string.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        self.options = func()

        # Call the parent __init__
        super(SettingMultipleDynamicOptions, self)._create_popup(instance)
