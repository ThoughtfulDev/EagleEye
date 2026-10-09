import time
import os
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import utils.config as cfg
import utils.console as console


def filterLink(link):
    filters = cfg.google_filter()
    for f in filters:
        if link is not None and f in link:
            return True
    return False


class GoogleGrabber:
    PHOTO_XPATH = '//*[@id="sbtc"]/div/div[3]/div[2]/span'
    PHOTO_UPLOAD_XPATH = '//*[@id="dRSWfb"]/div/a'
    PRED_XPATH = "/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[1]/div/div[2]/a"
    PRED_LINKS = "//*[@class='g']"

    def __init__(self):
        self.max_pages = cfg.google_img_pages()
        console.section('Google Reverse Image Search')
        console.task('Opening Webdriver')
        self.driver = cfg.getWebDriver()
        self.links = []
        self.predictions = []

    def _clickConsent(self):
        try:
            buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Accept') or contains(., 'agree') or contains(., 'Agree')]")
            if buttons:
                buttons[0].click()
                time.sleep(1)
        except Exception:
            pass

    def _findCameraBtn(self):
        selectors = [
            "//*[@aria-label='Search by image' or @title='Search by image']",
            "//div[@role='button' and (contains(@aria-label, 'image') or contains(@aria-label, 'Image'))]",
            "//div[contains(@class, 'nDcEnd')]",
            self.PHOTO_XPATH
        ]
        for sel in selectors:
            try:
                elems = self.driver.find_elements(By.XPATH, sel)
                if elems:
                    return elems[0]
            except Exception:
                continue
        return None

    def _findFileInput(self):
        selectors = [
            "//input[@type='file']",
            "//input[@name='encoded_image']",
            "//*[@id='awyMjb']"
        ]
        for sel in selectors:
            try:
                elems = self.driver.find_elements(By.XPATH, sel)
                if elems:
                    return elems[0]
            except Exception:
                continue
        return None

    def _findUrlInput(self):
        selectors = [
            "//input[@placeholder='Paste image link' or @aria-label='Paste image link']",
            "//input[contains(@class, 'cB9M7')]",
            "//*[@id='Ycyxxc']"
        ]
        for sel in selectors:
            try:
                elems = self.driver.find_elements(By.XPATH, sel)
                if elems:
                    return elems[0]
            except Exception:
                continue
        return None

    def getLinks(self):
        try:
            link_name = self.driver.find_elements(By.TAG_NAME, 'a')
            links = []
            for l in link_name:
                try:
                    link = l.get_attribute('href')
                except Exception:
                    continue
                if link is not None:
                    if filterLink(link):
                        if ("https://www.google.com/imgres?imgurl" not in link) and ("translate" not in link) and ("cdninstagram" not in link):
                            links.append(link)
            links = list(set(links))
            for link in links:
                if "url?" in link:
                    try:
                        self.driver.execute_script('''window.open("''' + link + '''","_blank");''')
                        time.sleep(2)
                        if len(self.driver.window_handles) > 1:
                            self.driver.switch_to.window(self.driver.window_handles[1])
                            time.sleep(1)
                            url = self.driver.current_url
                            self.driver.close()
                            time.sleep(1)
                            self.driver.switch_to.window(self.driver.window_handles[0])
                            time.sleep(1)
                            self.links.append(url)
                            console.subtask("Added {}".format(url))
                    except Exception:
                        pass
                else:
                    console.subtask("Skipping {}".format(link))
                    self.links.append(link)
        except Exception:
            pass

    def collectLinks(self, img_url):
        console.task('New Image: {0}'.format(img_url.strip()[:90]))
        driver = self.driver
        driver.get("https://www.google.com/imghp?hl=en")
        console.subtask('Inserting Image URL')
        console.task("Please agree to google's stuff in the browser")
        time.sleep(10)
        self._clickConsent()

        cam = self._findCameraBtn()
        if cam:
            try:
                cam.click()
                time.sleep(2)
            except Exception:
                console.subfailure('Could not click camera button')
                return
        else:
            console.subfailure('Camera button not found on Google Images')
            return

        url_input = self._findUrlInput()
        if url_input:
            try:
                url_input.clear()
                url_input.send_keys(img_url)
                url_input.send_keys(Keys.RETURN)
                console.subtask('Searching for Image...')
                time.sleep(cfg.timeout() * 2)
            except Exception:
                console.subfailure('Failed to submit Image URL')
                return
        else:
            console.subfailure('Image URL input box not found on Google Images')
            return

        pred_error = False
        try:
            pred = driver.find_element(By.XPATH, self.PRED_XPATH)
        except NoSuchElementException:
            console.subfailure('No Prediction given sry...')
            pred = None
            pred_error = True
        except BrokenPipeError:
            try:
                pred = driver.find_element(By.XPATH, self.PRED_XPATH)
            except NoSuchElementException:
                console.subfailure('Broken pipe Error. This is not a Problem...moving on!')
                console.subfailure('No Prediction given sry...')
                pred = None
                pred_error = True

        if not pred_error and pred is not None:
            pred = pred.text
            self.predictions.append(pred)

        console.subtask("Collecting Links...(Page 1)")
        self.getLinks()

        for num in range(2, self.max_pages + 1):
            console.subtask("Switching to Page {0}".format(num))
            try:
                page_n = driver.find_element(By.LINK_TEXT, str(num))
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
            driver.get("https://www.google.com/imghp?hl=en")
            console.task("Please agree to google's stuff in the browser")
            time.sleep(10)
            self._clickConsent()

            cam = self._findCameraBtn()
            if cam:
                try:
                    cam.click()
                    time.sleep(2)
                except Exception:
                    console.subfailure('Could not click camera button')
                    continue
            else:
                console.subfailure('Camera button not found on Google Images')
                continue

            file_input = self._findFileInput()
            if not file_input:
                try:
                    upload_tab = driver.find_element(By.XPATH, self.PHOTO_UPLOAD_XPATH)
                    upload_tab.click()
                    time.sleep(1)
                    file_input = self._findFileInput()
                except Exception:
                    pass

            if file_input:
                console.subtask("Inserting Path")
                p_i = os.path.abspath(str_p)
                try:
                    file_input.send_keys(p_i)
                    time.sleep(cfg.timeout() * 2)
                except Exception as ex:
                    console.subfailure('Failed to upload image file: {}'.format(ex))
                    continue
            else:
                console.subfailure('Image upload input not found on Google Images')
                continue

            pred_error = False
            try:
                pred = driver.find_element(By.XPATH, self.PRED_XPATH)
            except NoSuchElementException:
                console.subfailure('No Prediction given sry...')
                pred = None
                pred_error = True
            except BrokenPipeError:
                try:
                    pred = driver.find_element(By.XPATH, self.PRED_XPATH)
                except NoSuchElementException:
                    console.subfailure('Broken pipe Error. This is not a Problem...moving on!')
                    console.subfailure('No Prediction given sry...')
                    pred = None
                    pred_error = True

            if not pred_error and pred is not None:
                pred = pred.text
                self.predictions.append(pred)

            console.subtask("Collecting Links...(Page 1)")
            self.getLinks()

            for num in range(2, self.max_pages + 1):
                console.subtask("Switching to Page {0}".format(num))
                try:
                    page_n = driver.find_element(By.LINK_TEXT, str(num))
                    page_n.click()
                    time.sleep(cfg.timeout())
                    console.subtask("Collecting Links...(Page {0})".format(num))
                    self.getLinks()
                except NoSuchElementException:
                    console.subfailure('No more pages...')
                    break

    def finish(self):
        try:
            self.driver.close()
        except Exception:
            pass
        return self.links, self.predictions
