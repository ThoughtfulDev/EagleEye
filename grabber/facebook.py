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
        profile_img_links = driver.find_elements_by_xpath("//a[@class='_2ial']")
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
            profile_img_links = driver.find_elements_by_xpath("//a[@class='_2ial']")
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

class FBProfileGrabber:
    def __init__(self, profile_links):
        self._pl = profile_links
    
    def grabLinks(self):
        img_urls = []
        console.task('Opening Webdriver')
        driver = cfg.getWebDriver()
        for profile_url in self._pl:
            driver.get(profile_url)

            #first possibility
            profile_img_links = driver.find_elements_by_xpath("/html/body/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[3]/div/div[2]/div[3]/div/div/div/img")
            for e in profile_img_links:
                img_src = e.get_attribute("src")
                img_urls.append(img_src)
            
            #second possivility
            profile_img_links = driver.find_elements_by_xpath("/html/body/div[1]/div[4]/div[1]/div/div/div[1]/div/div/div[1]/div/a/img")
            for e in profile_img_links:
                img_src = e.get_attribute("src")
                img_urls.append(img_src)
            
        driver.close()
        return list(set(img_urls))
                