import json
import os
import sys
import tempfile
from selenium import webdriver

with open('./config.json') as json_data:
    cfg = json.load(json_data)


def timeout():
    return int(cfg['DEFAULTS']['SLEEP_DELAY'])


def google_img_pages():
    return int(cfg['DEFAULTS']['GOOGLE_IMG_PAGES'])


def google_filter():
    return cfg['FILTER']

def instaLimit():
    return int(cfg['INSTA_VALIDATION_MAX_IMAGES'])

def getWebDriver():
    if not os.path.isfile(cfg['WEBDRIVER']['PATH']):
        print("{0} does not exist - install a webdriver".format(cfg['WEBDRIVER']['PATH']))
        sys.exit(-2)
    d = cfg['WEBDRIVER']['ENGINE']
    if d.lower() == 'firefox':
        os.environ["webdriver.firefox.driver"] = cfg['WEBDRIVER']['PATH']
        p = os.path.join(tempfile.gettempdir(), 'imageraider')
        if not os.path.isdir(p):
            os.makedirs(p)
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2) # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', p)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
        return webdriver.Firefox(profile)
    else:
        os.environ["webdriver.chrome.driver"] = cfg['WEBDRIVER']['PATH']
        return webdriver.Chrome()
