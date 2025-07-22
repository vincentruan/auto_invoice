import yaml
import os

setting = None

def parse_setting():
    global setting
    if setting is None:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            setting = yaml.safe_load(file)
    return setting


def get_location():
    return parse_setting().get('location')


def get_out_date():
    return parse_setting().get('out_date')


def get_base_url():
    return parse_setting().get('base_url')


def get_max_count():
    return parse_setting()['max_count']


def get_chrome_driver_mode():
    return parse_setting().get('chrome_driver_mode', 'auto')


def get_chrome_driver_path():
    return parse_setting().get('google_chrome_driver_path', './webdriver/chromedriver')
