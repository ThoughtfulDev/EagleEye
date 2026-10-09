import csv
import os
from pathlib import Path
import sys
import tempfile
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import utils.config as cfg
import utils.console as console


def filterLink(link):
    filters = cfg.google_filter()
    for f in filters:
        if link and f in link:
            return True
    return False


class ImageRaiderGrabber:
    def __init__(self):
        console.section('ImageRaider Reverse Image Search')
        console.task('Opening Webdriver')
        self.driver = cfg.getWebDriver()
        self.csv_error = False

    def insertImageLinks(self, images):
        self.driver.get("https://www.imageraider.com/")
        inputs = self.driver.find_elements(By.XPATH, '//*[@id="topurllist"]')
        if not inputs:
            console.subfailure("Could not find ImageRaider URL input")
            return
        inp = inputs[0]
        for i in images:
            console.subtask('Inserting {0}'.format(i))
            inp.send_keys(i)
            inp.send_keys(Keys.RETURN)
        console.subtask('Submitting...')
        btns = self.driver.find_elements(By.XPATH, '/html/body/div[4]/div/div/article/div/div[1]/form/span/input')
        if btns:
            btns[0].click()

    def uploadLocalImage(self, img):
        self.driver.get("https://www.imageraider.com/")
        inputs = self.driver.find_elements(By.XPATH, '//*[@id="file"]')
        if not inputs:
            console.subfailure("Could not find ImageRaider file input")
            return
        p_i = os.path.join(os.getcwd(), img)
        inputs[0].send_keys(p_i)
        btns = self.driver.find_elements(By.XPATH, '/html/body/div[4]/div/div/article/div/div[1]/span/form/input[3]')
        if btns:
            btns[0].click()

    def downloadCSV(self):
        time.sleep(5)
        console.task('Waiting for page to finish')
        try:
            while "Loading" in self.driver.page_source:
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(1)
        except Exception:
            console.subfailure('Pagetimeout')
            sys.exit(-1)
        print('')
        console.task('Downloading CSV')
        time.sleep(2)
        try:
            dls = self.driver.find_elements(By.XPATH, '//*[@id="dltop"]')
            if dls:
                dls[0].click()
            else:
                console.failure('No Results...')
                self.csv_error = True
        except Exception:
            console.failure('No Results...')
            self.csv_error = True
        try:
            self.driver.quit()
        except Exception:
            pass

    def processCSV(self):
        if not self.csv_error:
            time.sleep(2)
            p = os.path.join(tempfile.gettempdir(), 'imageraider')
            if not os.path.isdir(p):
                return []
            pathlist = Path(p).glob('**/*')
            links = []
            for path in pathlist:
                if not path.is_file():
                    continue
                path_str = str(path)
                try:
                    with open(path_str, 'r', encoding='utf-8', errors='replace') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            page_url = row.get('Discovered Page URL')
                            if page_url and filterLink(page_url):
                                console.subtask('Added {0}'.format(page_url))
                                links.append(page_url)
                except Exception:
                    continue
            return links
        else:
            return []
