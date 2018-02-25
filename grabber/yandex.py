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



class YandexGrabber:
    def __init__(self):
        console.section('Yandex Reverse Image Search')
        console.task('Opening Webdriver')
        self.driver = cfg.getWebDriver()
        self.links = []
    
    def collectLinks(self, img_url):
        l_unreal = []
        console.task('New Image: {0}'.format(img_url.strip()[:90]))  
        driver = self.driver
        driver.get("https://www.yandex.com/images/")
        console.subtask('Inserting Image URL')
        elems = driver.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div[2]/form/div[1]/span/span/table/tbody/tr/td[2]/div/button')[0]
        elems.click()
        input = driver.find_elements_by_xpath('/html/body/div[3]/div/div[1]/div/form[2]/span/span/input')[0]
        input.clear()
        input.send_keys(img_url)
        input.send_keys(Keys.RETURN)
        console.subtask('Searching for Image...')
        time.sleep(cfg.timeout())
        link_name=driver.find_elements_by_xpath('/html/body/div[6]/div[1]/div[1]/div[3]/ul/li/div/a[2]')     
        console.subtask("Collecting Links...")
        for link in link_name:
            href = link.get_attribute('href')
            l_unreal.append(href)
        
        console.subtask("Getting real links from Yandex ShortURLs")
        l_real = []
        for l_u in l_unreal:
            driver.get(l_u)
            if(filterLink(driver.current_url)):
                l_real.append(driver.current_url)
                console.subtask('Added verified {0}'.format(driver.current_url.strip()[:90]))
        self.links = l_real

    def finish(self):
        self.driver.close()
        return self.links
