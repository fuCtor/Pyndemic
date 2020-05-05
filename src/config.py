# coding: utf-8
import os
from configparser import ConfigParser
import i18n

ROOT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
SETTINGS_DEFAULT_LOCATION = os.path.join(ROOT_DIR, 'settings.cfg')

_CACHED_SETTINGS = None
i18n.load_path.append(os.path.join(ROOT_DIR, 'data', 'i18n'))
i18n.set('filename_format', '{locale}.{format}')

i18n.set('locale', 'ru')
i18n.set('fallback', 'en')

def get_settings(settings_location=None, *, refresh=False):
    global _CACHED_SETTINGS

    if refresh or _CACHED_SETTINGS is None:
        refresh_settings(settings_location)

    app_config = _CACHED_SETTINGS
    return app_config


def refresh_settings(settings_location=None):
    global _CACHED_SETTINGS

    if settings_location is None:
        settings_location = SETTINGS_DEFAULT_LOCATION

    app_config = ConfigParser()
    app_config.read(settings_location)

    _CACHED_SETTINGS = app_config

