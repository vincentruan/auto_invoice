from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service

from invoice_selector import config

prefs = {
    "download.default_directory": config.get_location(),
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

chrome_option = Options()
chrome_option.add_experimental_option('prefs', prefs)


class DriverSingleton:
    _instance = None
    _driver: WebDriver = None
    _wait:WebDriverWait = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DriverSingleton, cls).__new__(cls)
            try:
                if config.get_chrome_driver_mode() == 'manual':
                    service = Service(executable_path=config.get_chrome_driver_path())
                    cls._driver = webdriver.Chrome(service=service, options=chrome_option)
                else:
                    cls._driver = webdriver.Chrome(options=chrome_option)
                cls._wait = WebDriverWait(cls._driver, 30)  # 可以调整等待时间
            except Exception as e:
                # 如果auto模式失败，自动切换为manual
                if config.get_chrome_driver_mode() == 'auto':
                    try:
                        service = Service(executable_path=config.get_chrome_driver_path())
                        cls._driver = webdriver.Chrome(service=service, options=chrome_option)
                        cls._wait = WebDriverWait(cls._driver, 30)
                    except Exception as e2:
                        raise RuntimeError(f"Chrome启动失败，已尝试auto/manual两种方式，错误信息: {e2}")
                else:
                    raise RuntimeError(f"Chrome启动失败，错误信息: {e}")
        return cls._instance

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            cls()
        return cls._driver

    @classmethod
    def get_wait(cls):
        if cls._wait is None:
            cls()
        return cls._wait

    @classmethod
    def init(cls):
        if cls._driver is None or cls._wait is None:
            cls()
        return cls._driver, cls._wait
