from kivy.uix.settings import SettingsWithSpinner
class ESettingsPanel(SettingsWithSpinner):
    """
    It is not usually necessary to create subclass of a settings panel. There
    are many built-in types that you can use out of the box
    (SettingsWithSidebar, SettingsWithSpinner etc.).
    You would only want to create a Settings subclass like this if you want to
    change the behavior or appearance of an existing Settings class.
    """
    def on_close(self):
        pass
    def on_config_change(self, config, section, key, value):
        pass
