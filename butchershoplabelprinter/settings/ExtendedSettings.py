from kivy.uix.settings import SettingsWithSpinner

from butchershoplabelprinter.settings.SettingDynamicOptions import SettingDynamicOptions, SettingMultipleOptions, SettingMultipleDynamicOptions


class ExtendedSettings(SettingsWithSpinner):

    def __init__(self, *args, **kargs):
        super(ExtendedSettings, self).__init__(*args, **kargs)
        self.register_type('dynamic_options', SettingDynamicOptions)
        self.register_type('multi_options', SettingMultipleOptions)
        self.register_type('multi_dynamic_options', SettingMultipleDynamicOptions)