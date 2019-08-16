import time
import os
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import utils.config as cfg
import utils.console as console



def filterLink(link):
    filters = cfg.google_filter()
    for f in filters:
        if link != None and f in link:
            return True
    return False


class GoogleGrabber:

    PHOTO_XPATH = "/html/body/div[1]/div[4]/div[2]/form/div[2]/div/div[1]/div/div[2]/div/span"
    PHOTO_UPLOAD_XPATH = "/html/body/div[1]/div[4]/div[2]/div/div[2]/form/div[1]/div/a"
    PRED_XPATH = "/html/body/div[6]/div[3]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/a"

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
        elems = driver.find_elements_by_xpath(self.PHOTO_XPATH)[0]
        elems.click()
        time.sleep(1)
        input = driver.find_elements_by_xpath('//*[@id="qbui"]')[0]
        input.clear()
        input.send_keys(img_url)
        input.send_keys(Keys.RETURN)
        console.subtask('Searching for Image...')
        time.sleep(cfg.timeout() * 2)
        pred_error = False
        try:
            pred = driver.find_element_by_xpath(self.PRED_XPATH)
        except NoSuchElementException:
            console.subfailure('No Prediction given sry...')
            pred = None
            pred_error = True
        except BrokenPipeError:
            #just try again...
            try:
                pred = driver.find_element_by_xpath(self.PRED_XPATH)
            except NoSuchElementException:
                console.subfailure('Broken pipe Error. This is not a Problem...moving on!')
                console.subfailure('No Prediction given sry...')
                pred = None
                pred_error = True
                
        if not pred_error:
            pred = pred.text       
        self.predictions.append(pred)
    
        try:
            
            link_name=driver.find_elements_by_xpath("//*[@class='iUh30']")
            #link_name=driver.find_elements_by_xpath(".//h3[@class='r']/a")
        except BrokenPipeError:
            link_name=driver.find_elements_by_xpath("//*[@class='iUh30']")
            #link_name=driver.find_elements_by_xpath(".//h3[@class='r']/a")
        console.subtask("Collecting Links...(Page 1)")
        if len(link_name) <= 0: 
            console.subfailure('No Links found')
        else:
            for link in link_name:
                #href = link.get_attribute('href')
                if link != None:
                    href = link.text
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
                try:  
                    link_name=driver.find_elements_by_xpath("//*[@class='iUh30']")
                except BrokenPipeError:
                    link_name=driver.find_elements_by_xpath("//*[@class='iUh30']")
                for link in link_name:
                    href = link.text
                    if filterLink(href):
                        console.subtask('Added {0}'.format(href))
                        self.links.append(href)
            except NoSuchElementException:
                console.subfailure('No more pages...')
                break    

    def collectLinksLocal(self):
        driver = self.driver
        console.section("Uploading Local Known Images")
        pa_g = Path('./known')
        pathlist = []
        for ext in ['.jpg', '.JPG', '.png', '.PNG', '.jpeg', '.JPEG', '.bmp', '.BMP']:
            tmp_pl = pa_g.glob('**/*{}'.format(ext))
            for t in tmp_pl:
                pathlist.append(t)
        for p in pathlist:
            str_p = str(p)
            driver.get("https://www.google.com/imghp")
            elems = driver.find_elements_by_xpath(self.PHOTO_XPATH)[0]
            elems.click()
            time.sleep(1)
            elems = driver.find_element_by_xpath(self.PHOTO_UPLOAD_XPATH)
            
            elems.click()
            time.sleep(1)
            console.subtask("Inserting Path")
            input_box = driver.find_element_by_xpath('//*[@id="qbfile"]')
            p_i = os.path.join(os.getcwd(), str_p)
            input_box.send_keys(p_i)
            time.sleep(cfg.timeout() * 2)
            pred_error = False
            try:
                pred = driver.find_element_by_xpath(self.PRED_XPATH)
            except NoSuchElementException:
                console.subfailure('No Prediction given sry...')
                pred = None
                pred_error = True
            except BrokenPipeError:
                #just try again...
                try:
                    pred = driver.find_element_by_xpath(self.PRED_XPATH)
                except NoSuchElementException:
                    console.subfailure('Broken pipe Error. This is not a Problem...moving on!')
                    console.subfailure('No Prediction given sry...')
                    pred = None
                    pred_error = True
                
            if not pred_error:
                pred = pred.text       
            self.predictions.append(pred)
            try:
                link_name=driver.find_elements_by_xpath("//*[@class='iUh30']")
            except BrokenPipeError:
                link_name=driver.find_elements_by_xpath("//*[@class='iUh30']")
            console.subtask("Collecting Links...(Page 1)")
            if len(link_name) <= 0: 
                console.subfailure('No Links found')
            else:
                for link in link_name:
                    if link != None:
                        href = link.text
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
                    try:   
                        link_name=driver.find_elements_by_xpath("//*[@class='iUh30']")
                    except BrokenPipeError:
                        link_name=driver.find_elements_by_xpath("//*[@class='iUh30']")
                    for link in link_name:
                        href = link.text
                        if filterLink(href):
                            console.subtask('Added {0}'.format(href))
                            self.links.append(href)
                except NoSuchElementException:
                    console.subfailure('No more pages...')
                    break    

    def finish(self):
        self.driver.close()
        return self.links, self.predictions
