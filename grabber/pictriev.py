import time
import os
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import utils.config as cfg
import utils.console as console



def filterLink(link):
    filters = cfg.google_filter()
    for f in filters:
        if f in link:
            return True
    return False



class PictrievGrabber:
    def __init__(self):
        console.section('Picture Age and Gender Detection')
        console.task('Opening Webdriver')
        self.driver = cfg.getWebDriver()
        self.ages = []
        self.males = []
        self.females = []

    def mean(self, arr):
        sum = 0
        for a in arr:
            sum += a
        if sum == 0:
            return 0
        if len(arr) == 0:
            return 0
        return sum/len(arr)


    def collectAges(self, img_url):
        console.task('New Image: {0}'.format(img_url.strip()[:90]))  
        driver = self.driver
        driver.get("http://www.pictriev.com/?lang=en")
        console.subtask('Inserting Image URL')
        input = driver.find_elements_by_xpath('//*[@id="urltext"]')[0]
        input.clear()
        input.send_keys(img_url)
        btn = driver.find_elements_by_xpath('//*[@id="submit-url"]')[0]
        btn.click()
        console.subtask('Searching for Image...')
        time.sleep(cfg.timeout() * 3)
        try:
            age = driver.find_elements_by_css_selector('#age-gauge > svg:nth-child(1) > text:nth-child(6) > tspan:nth-child(1)')[0].text
            if int(age) > 0:
                self.ages.append(int(age))
        except:
            pass

    def finish(self):
        self.driver.close()
        return int(self.mean(self.ages))
