import time
import os
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import utils.config as cfg
import utils.console as console

class FBGrabber:
    def __init__(self, name):
        f_name = name.replace(' ', '%20')
        self.url = "https://facebook.com/public/?query={0}".format(f_name)
    
    def grabData(self):
        console.task('Opening Webdriver')
        driver = cfg.getWebDriver()
        driver.get(self.url)
        self.profile_list = []
        self.profile_img = []

        #get all profile image links
        profile_img_links = driver.find_elements_by_xpath("//a[@class='_2ial _8o _8s lfloat _ohe']")
        console.subtask('Collecting Image URLs...(Page 1)')

        for e in profile_img_links:
            href = e.get_attribute("href")
            image = e.find_element_by_tag_name("img")
            img_src = image.get_attribute("src")
            self.profile_list.append(href)
            self.profile_img.append(img_src)
        
        pages = driver.find_elements_by_xpath("//a")
        pages_links = []
        for e in pages:
            link = e.get_attribute('href')
            if "&page" in link:
                pages_links.append(link)
        pages_links = list(set(pages_links))

        for page in pages_links:
            driver.get(page)
            profile_img_links = driver.find_elements_by_xpath("//a[@class='_2ial _8o _8s lfloat _ohe']")
            page_num = page[-1:]
            console.subtask('Collecting Images URLs...(Page {0})'.format(page_num))
            for e in profile_img_links:
                href = e.get_attribute("href")
                image = e.find_element_by_tag_name("img")
                img_src = image.get_attribute("src")
                self.profile_list.append(href)
                self.profile_img.append(img_src)
            time.sleep(1)
        driver.close()

    def getProfileLinks(self):
        return self.profile_list

    def getProfileImages(self):
        return self.profile_img