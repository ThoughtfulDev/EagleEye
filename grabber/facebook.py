import time
import os
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import utils.config as cfg
import utils.console as console


class FBGrabber:
    def __init__(self, name):
        f_name = name.replace(' ', '%20')
        self.url = "https://facebook.com/public/?query={0}".format(f_name)
        self.profile_list = []
        self.profile_img = []

    def grabData(self):
        console.task('Opening Webdriver')
        driver = cfg.getWebDriver()
        try:
            driver.get(self.url)
            self.profile_list = []
            self.profile_img = []

            console.task("Please agree to facebook's stuff in the browser")
            time.sleep(10)

            # get all profile image links
            profile_img_links = driver.find_elements(By.XPATH, "//a[@class='_2ial']")
            console.subtask('Collecting Image URLs...(Page 1)')

            if len(profile_img_links) <= 0:
                console.subfailure('No FB Links found')
            else:
                for e in profile_img_links:
                    href = e.get_attribute("href")
                    try:
                        image = e.find_element(By.TAG_NAME, "img")
                        img_src = image.get_attribute("src")
                        self.profile_list.append(href)
                        self.profile_img.append(img_src)
                    except NoSuchElementException:
                        continue

            pages = driver.find_elements(By.XPATH, "//a")
            pages_links = []
            for e in pages:
                try:
                    link = e.get_attribute('href')
                    if link and "&page" in link:
                        pages_links.append(link)
                except Exception:
                    continue
            pages_links = list(set(pages_links))

            for page in pages_links:
                driver.get(page)
                profile_img_links = driver.find_elements(By.XPATH, "//a[@class='_2ial']")
                page_num = page[-1:]
                console.subtask('Collecting Images URLs...(Page {0})'.format(page_num))
                for e in profile_img_links:
                    href = e.get_attribute("href")
                    try:
                        image = e.find_element(By.TAG_NAME, "img")
                        img_src = image.get_attribute("src")
                        self.profile_list.append(href)
                        self.profile_img.append(img_src)
                    except NoSuchElementException:
                        continue
                time.sleep(1)
        finally:
            try:
                driver.quit()
            except Exception:
                pass

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
        try:
            for profile_url in self._pl:
                driver.get(profile_url)
                candidate_xpaths = [
                    "/html/body/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[3]/div/div[2]/div[3]/div/div/div/img",
                    "/html/body/div[1]/div[1]/div[3]/div[1]/div/div/div[1]/div/div/div[1]/div/div/div/a/div/img",
                    "//img[contains(@class, 'profile') or contains(@class, 'avatar')]"
                ]
                for xpath in candidate_xpaths:
                    profile_img_links = driver.find_elements(By.XPATH, xpath)
                    for e in profile_img_links:
                        img_src = e.get_attribute("src")
                        if img_src:
                            img_urls.append(img_src)
        finally:
            try:
                driver.quit()
            except Exception:
                pass
        return list(set(img_urls))