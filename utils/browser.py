import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.service import Service

ROOT_PATH = Path(__file__).parent.parent
FIREFOX_NAME = 'geckodriver.exe'
FIREFOX_PATH = ROOT_PATH / 'bin' / FIREFOX_NAME


# --headless
def make_browser(*args):
    firefox_options = webdriver.FirefoxOptions()

    if args is not None:
        for arg in args:
            firefox_options.add_argument(arg)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        firefox_options.add_argument('--headless')

    firefox_service = Service(executable_path=FIREFOX_PATH)
    browser = webdriver.Firefox(service=firefox_service, options=firefox_options)
    return browser


if __name__ == '__main__':
    browser = make_browser('--headless')
    browser.get('http://www.google.com.br')
    browser.quit()
