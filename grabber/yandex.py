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
        elems = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div[1]/div[2]/form/div[1]/span/span[2]')[0]
        elems.click()
        input = driver.find_elements_by_xpath('//*[@id="uniq151721871321712645"]')[0]
        
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
        for l in l_real:
            self.links.append(l)
    
    def collectLinksLocal(self):
        l_unreal = []
        console.task('Uploading Local Images')  
        driver = self.driver
        driver.get("https://www.yandex.com/images/")
        pathlist = Path('./known').glob('**/*.jpg')
        for p in pathlist:
            str_p = str(p)
            console.subtask('Inserting Image URL')
            elems = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div[1]/div[2]/form/div[1]/span/span[2]')[0]
            elems.click()
            input = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div[4]/div/div[1]/div/form[1]/input')[0]
            input.clear()
            p_i = os.path.join(os.getcwd(), str_p)
            input.send_keys(p_i)
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
        for l in l_real:
            self.links.append(l)

    def finish(self):
        self.driver.close()
        return self.links
