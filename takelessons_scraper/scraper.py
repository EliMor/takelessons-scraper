import time
import logging
from contextlib import contextmanager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

@contextmanager
def session(driver_path, headless=True, window_size="1920,1080"):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    
    chrome_options.add_argument(f"--window-size={window_size}")
    driver = webdriver.Chrome(executable_path=driver_path,
        chrome_options=chrome_options)
    try:
        yield driver
    finally:
        driver.quit()


class Scraper:

    def __init__(self, selenium_driver):
        self.driver = selenium_driver

    def login(self, username, password):
        login_url = 'https://takelessons.com/login'
        self.driver.get(login_url)
        self.driver.find_element_by_id("Email").send_keys(username)
        self.driver.find_element_by_id("Password").send_keys(password)
        self.driver.find_element_by_css_selector('button.PillButton.Blue').click()

    def chat_window(self, xpath_pattern):
        self.driver.find_element_by_xpath(xpath_pattern).click()
        content = self.driver.find_element_by_xpath("//div[@class='ChatLogOverlay_Container']")
        raw_text = content.get_attribute('innerHTML')
        self.driver.find_element_by_xpath("//div[@class='ChatLogOverlay_Close']").click()
        return raw_text

    def get_chat_history(self):
        chat_url = 'https://takelessons.com/client/journal'
        self.driver.get(chat_url)
        # trick to get the scroll down to work
        self.driver.find_element_by_tag_name('body').click()
        idx = 1
        xpath_pattern = '/html/body/div[4]/div[1]/div/div/div[2]/div/div[{idx}]/div[2]/div[4]/div'
        while True:
            time.sleep(10)
            try:
                #scoot down to force more to be loaded
                self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
                #grab text
                raw_text = self.chat_window(xpath_pattern.format(idx=idx))
                idx += 1
                # TODO: Return a chat object that parses out the content
                yield raw_text
            except Exception as e:
                logging.warning(e)
                # TODO: cleanly exit the loop
                break

class Chat:
    ...