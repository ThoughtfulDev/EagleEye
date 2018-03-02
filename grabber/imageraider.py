from selenium.webdriver.common.keys import Keys
import utils.config as cfg
import utils.console as console
from pathlib import Path
import os
import time
import sys
import tempfile
import csv

def filterLink(link):
    filters = cfg.google_filter()
    for f in filters:
        if f in link:
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
        input = self.driver.find_elements_by_xpath('//*[@id="topurllist"]')[0]
        for i in images:
            console.subtask('Inserting {0}'.format(i))
            input.send_keys(i)
            input.send_keys(Keys.RETURN)
        console.subtask('Submitting...')
        btn = self.driver.find_elements_by_xpath('/html/body/div[3]/div/div/article/div/div[1]/form/span/input')[0]
        btn.click()
    
    def uploadLocalImage(self, img):
        self.driver.get("https://www.imageraider.com/")
        input = self.driver.find_elements_by_xpath('//*[@id="file"]')[0]
        p_i = os.path.join(os.getcwd(), img)
        input.send_keys(p_i)
        btn = self.driver.find_elements_by_xpath('/html/body/div[3]/div/div/article/div/div[1]/span/form/input[3]')[0]
        btn.click()
    
    def downloadCSV(self):
        time.sleep(5)
        console.task('Waiting for page to finish')
        try:
            while "Loading" in self.driver.page_source:
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(1)
        except:
            console.subfailure('Pagetimeout')
            sys.exit(-1)
        print('')
        console.task('Downloading CSV')
        time.sleep(2)
        try:
            dl = self.driver.find_elements_by_xpath('//*[@id="dltop"]')[0]
            dl.click()
        except:
            console.failure('No Results...')
            self.csv_error = True
        self.driver.close()
    
    def processCSV(self):
        if not self.csv_error:
            time.sleep(2)
            p = os.path.join(tempfile.gettempdir(), 'imageraider')
            pathlist = Path(p).glob('**/*')
            links = []
            for path in pathlist:
                path = str(path)
                with open(path, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if filterLink(row['Discovered Page URL']):
                            console.subtask('Added {0}'.format(row['Discovered Page URL']))
                            links.append(row['Discovered Page URL'])
            return links
        else:
            return []


