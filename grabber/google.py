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
    
    PHOTO_XPATH = "/html/body/div/div[3]/div[2]/form/div[2]/div[1]/div[1]/div/div[3]/div[2]/span"
    PHOTO_UPLOAD_XPATH = "/html/body/div[1]/div[3]/div[2]/div/div[2]/form/div[1]/div/a"
    PRED_XPATH = "/html/body/div[6]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/a"
    #PRED_LINKS = "//*[@class='iUh30']"
    PRED_LINKS = "//*[@class='g']"

    def __init__(self):
        self.max_pages = cfg.google_img_pages()
        console.section('Google Reverse Image Search')
        console.task('Opening Webdriver')
        self.driver = cfg.getWebDriver()
        self.links = []
        self.predictions = []

    def getLinks(self):
        try:
            link_name = self.driver.find_elements_by_tag_name('a')
            links = []
            for l in link_name:
                link = l.get_attribute('href')
                if not link == None:
                    if filterLink(link):
                        if (not "https://www.google.com/imgres?imgurl" in link) or (not "translate" in link) or (not "cdninstagram" in link):
                            links.append(link)
            links = list(set(links))
            #print(len(links))
            #print(links)
            for link in links:
                if "url?" in link:
                    self.driver.execute_script('''window.open("''' + link + '''","_blank");''')
                    time.sleep(2)
                    #switch to tab
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    time.sleep(1)
                    url = self.driver.current_url
                    self.driver.close()
                    time.sleep(1)
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    time.sleep(1)
                    self.links.append(url)
                    console.subtask("Added {}".format(url))
                else:
                    console.subtask("Skipping {}".format(link))
                    self.links.append(link)
        except:
            pass

    def collectLinks(self, img_url):
        console.task('New Image: {0}'.format(img_url.strip()[:90]))  
        driver = self.driver
        driver.get("https://www.google.com/imghp")
        console.subtask('Inserting Image URL')
        elems = driver.find_elements_by_xpath(self.PHOTO_XPATH)[0]
        elems.click()
        time.sleep(1)
        input = driver.find_elements_by_xpath('//*[@id="Ycyxxc"]')[0]
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

        console.subtask("Collecting Links...(Page 1)")
        self.getLinks()
            
            
        for num in range(2, self.max_pages+1):
            console.subtask("Switching to Page {0}".format(num))
            try:
                page_n = driver.find_element_by_link_text(str(num))
                page_n.click()
                time.sleep(cfg.timeout())
                console.subtask("Collecting Links...(Page {0})".format(num))
                self.getLinks()
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
            input_box = driver.find_element_by_xpath('//*[@id="awyMjb"]')
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
            console.subtask("Collecting Links...(Page 1)")
            self.getLinks()
            
            
            for num in range(2, self.max_pages+1):
                console.subtask("Switching to Page {0}".format(num))
                try:
                    page_n = driver.find_element_by_link_text(str(num))
                    page_n.click()
                    time.sleep(cfg.timeout())
                    console.subtask("Collecting Links...(Page {0})".format(num))
                    self.getLinks()
                except NoSuchElementException:
                    console.subfailure('No more pages...')
                    break
            

    def finish(self):
        self.driver.close()
        return self.links, self.predictions
