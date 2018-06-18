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


class GoogleGrabber:
    def __init__(self):
        self.max_pages = cfg.google_img_pages()
        console.section('Google Reverse Image Search')
        console.task('Opening Webdriver')
        self.driver = cfg.getWebDriver()
        self.links = []
        self.predictions = []
    
    def collectLinks(self, img_url):
        console.task('New Image: {0}'.format(img_url.strip()[:90]))  
        driver = self.driver
        driver.get("https://www.google.com/imghp")
        console.subtask('Inserting Image URL')
        elems = driver.find_elements_by_xpath('//*[@id="qbi"]')[0]
        elems.click()
        time.sleep(1)
        input = driver.find_elements_by_xpath('//*[@id="qbui"]')[0]
        input.clear()
        input.send_keys(img_url)
        input.send_keys(Keys.RETURN)
        console.subtask('Searching for Image...')
        time.sleep(cfg.timeout())
        try:
            pred = driver.find_element_by_xpath("/html/body/div[5]/div[3]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/a")
            pred = pred.text
        except NoSuchElementException:
            console.subfailure('No Prediction given sry...')
            pred = None
        self.predictions.append(pred)
    
        link_name=driver.find_elements_by_xpath(".//h3[@class='r']/a")     
        console.subtask("Collecting Links...(Page 1)")
        for link in link_name:
            href = link.get_attribute('href')
            if filterLink(href):
                console.subtask('Added {0}'.format(href))
                self.links.append(href)

        for num in range(2, self.max_pages+1):
            console.subtask("Switching to Page {0}".format(num))
            try:
                page_n = driver.find_element_by_link_text(str(num))
                page_n.click()
                time.sleep(cfg.timeout())
                console.subtask("Collecting Links...(Page {0})".format(num))       
                link_name=driver.find_elements_by_xpath(".//h3[@class='r']/a")
                for link in link_name:
                    href = link.get_attribute('href')
                    if filterLink(href):
                        console.subtask('Added {0}'.format(href))
                        self.links.append(href)
            except NoSuchElementException:
                console.subfailure('No more pages...')
                break    

    def collectLinksLocal(self):
        driver = self.driver
        console.section("Uploading Local Known Images")
        pathlist = Path('./known').glob('**/*.jpg')
        for p in pathlist:
            str_p = str(p)
            driver.get("https://www.google.com/imghp")
            elems = driver.find_elements_by_xpath('//*[@id="qbi"]')[0]
            elems.click()
            time.sleep(1)
            elems = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div/div[2]/form/div[1]/div/a')
            elems.click()
            time.sleep(1)
            console.subtask("Inserting Path")
            input_box = driver.find_element_by_xpath('//*[@id="qbfile"]')
            p_i = os.path.join(os.getcwd(), str_p)
            input_box.send_keys(p_i)
            time.sleep(cfg.timeout() * 2)
            try:
                pred = driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/a")
                pred = pred.text
            except NoSuchElementException:
                console.subfailure('No Prediction given sry...')
                pred = None
            self.predictions.append(pred)
            link_name=driver.find_elements_by_xpath(".//h3[@class='r']/a")     
            console.subtask("Collecting Links...(Page 1)")
            for link in link_name:
                href = link.get_attribute('href')
                if filterLink(href):
                    console.subtask('Added {0}'.format(href))
                    self.links.append(href)
            
            for num in range(2, self.max_pages+1):
                console.subtask("Switching to Page {0}".format(num))
                try:
                    page_n = driver.find_element_by_link_text(str(num))
                    page_n.click()
                    time.sleep(cfg.timeout())
                    console.subtask("Collecting Links...(Page {0})".format(num))       
                    link_name=driver.find_elements_by_xpath(".//h3[@class='r']/a")
                    for link in link_name:
                        href = link.get_attribute('href')
                        if filterLink(href):
                            console.subtask('Added {0}'.format(href))
                            self.links.append(href)
                except NoSuchElementException:
                    console.subfailure('No more pages...')
                    break    

    def finish(self):
        self.driver.close()
        return self.links, self.predictions
