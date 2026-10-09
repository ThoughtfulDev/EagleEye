import json
import os
import sys
import shutil
import tempfile
from selenium import webdriver

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')
with open(CONFIG_PATH, 'r', encoding='utf-8') as json_data:
    cfg = json.load(json_data)


def timeout():
    return int(cfg['DEFAULTS']['SLEEP_DELAY'])


def google_img_pages():
    return int(cfg['DEFAULTS']['GOOGLE_IMG_PAGES'])


def google_filter():
    return cfg['FILTER']


def instaLimit():
    return int(cfg['INSTA_VALIDATION_MAX_IMAGES'])


def jitters():
    return int(cfg['JITTERS'])


def getWebDriver():
    engine = cfg.get('WEBDRIVER', {}).get('ENGINE', 'firefox').lower()
    driver_path = cfg.get('WEBDRIVER', {}).get('PATH', '')

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Check if configured path exists directly or relative to repo root
    if driver_path:
        if not os.path.isabs(driver_path):
            resolved = os.path.join(base_dir, driver_path)
            if os.path.isfile(resolved):
                driver_path = resolved

    # Fallback auto-discovery if configured driver path does not exist
    if not driver_path or not os.path.isfile(driver_path):
        candidate_names = []
        if engine == 'chrome':
            candidate_names = ['chromedriver.exe', 'chromedriver']
        else:
            candidate_names = ['geckodriver.exe', 'geckodriver']

        found = False
        for name in candidate_names:
            local_cand = os.path.join(base_dir, name)
            if os.path.isfile(local_cand):
                driver_path = local_cand
                found = True
                break
            which_cand = shutil.which(name)
            if which_cand:
                driver_path = which_cand
                found = True
                break

        if not found:
            # Check other driver if primary is not found
            alt_names = ['chromedriver.exe', 'chromedriver'] if engine == 'firefox' else ['geckodriver.exe', 'geckodriver']
            for name in alt_names:
                local_cand = os.path.join(base_dir, name)
                if os.path.isfile(local_cand):
                    driver_path = local_cand
                    engine = 'chrome' if 'chrome' in name else 'firefox'
                    found = True
                    break
                which_cand = shutil.which(name)
                if which_cand:
                    driver_path = which_cand
                    engine = 'chrome' if 'chrome' in name else 'firefox'
                    found = True
                    break

        if not found and (not driver_path or not os.path.isfile(driver_path)):
            print("{0} does not exist - install a webdriver".format(driver_path or engine))
            sys.exit(-2)

    if engine == 'firefox':
        os.environ["webdriver.firefox.driver"] = driver_path
        p = os.path.join(tempfile.gettempdir(), 'imageraider')
        if not os.path.isdir(p):
            os.makedirs(p)
        try:
            from selenium.webdriver.firefox.service import Service as FirefoxService
            service = FirefoxService(driver_path)
            profile = webdriver.FirefoxProfile()
            profile.set_preference('browser.download.folderList', 2)
            profile.set_preference('browser.download.manager.showWhenStarting', False)
            profile.set_preference('browser.download.dir', p)
            profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
            profile.set_preference("browser.link.open_newwindow", 3)
            profile.set_preference("browser.link.open_newwindow.restriction", 2)
            return webdriver.Firefox(service=service, firefox_profile=profile)
        except Exception:
            try:
                from selenium.webdriver.firefox.service import Service as FirefoxService
                return webdriver.Firefox(service=FirefoxService(driver_path))
            except Exception:
                return webdriver.Firefox(executable_path=driver_path)
    else:
        from selenium.webdriver.chrome.service import Service
        service = Service(driver_path)
        return webdriver.Chrome(service=service)
