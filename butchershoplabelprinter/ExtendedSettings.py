from kivy.uix.settings import SettingsWithSpinner

import butchershoplabelprinter.SettingDynamicOptions


class ExtendedSettings(SettingsWithSpinner):

    def __init__(self, *args, **kargs):
        super(ExtendedSettings, self).__init__(*args, **kargs)
        self.register_type('dynamic_options', SettingDynamicOptions.SettingDynamicOptions)
        self.register_type('multi_options', SettingDynamicOptions.SettingMultipleOptions)
        self.register_type('multi_dynamic_options', SettingDynamicOptions.SettingMultipleDynamicOptions)