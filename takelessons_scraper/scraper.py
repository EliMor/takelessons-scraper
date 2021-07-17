import time
import json
import requests

import pendulum

from datetime import datetime
from collections import defaultdict
from contextlib import contextmanager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

import selenium_tools 

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
    def __init__(selenium_driver_path=None, user_agent=None):
        self.selenium_driver_path = selenium_driver_path
        self.user_agent = user_agent
        if not bool(user_agent):
            self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'

    def get_login_cookies(self, username, password) -> str:
        login_url = 'https://takelessons.com/login'
        with session(self.selenium_driver_path) as tl_session:
            tl_session.get(login_url)
            tl_session.find_element_by_id("Email").send_keys(username)
            tl_session.find_element_by_id("Password").send_keys(password)
            tl_session.find_element_by_css_selector('button.PillButton.Blue').click()
            cookies = tl_session.get_cookies()
        return selenium_tools.convert_cookies_to_str(cookies)

    def get_chat_history(self, date, cookies):
        chat_ajax_url = f'https://takelessons.com/client/journal/ajaxEvents?end_date={date}'
        headers = {'Cookie':cookies, 'Referer':'https://takelessons.com/client/journal', 
            'Accept':'application/json', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent': self.user_agent}
        response = requests.get(chat_ajax_url, headers=headers)
        if response.status_code == 200:
            chat = Chat(json.loads(response.content))
            return chat

class Chat:
    
    def __init__(chat_json):
        self.raw_chat = chat_json
        self.processed_chat_log = self.process_chat_log(chat_json)
        self.teacher = self.processed_chat_log['teacher']
        self.day = self.processed_chat_log['day']
        self.next_day = self.processed_chat_log['next_day']
        self.teacher_chat = self.processed_chat_log['teacher_chat']
        self.student_chat = self.processed_chat_log['student_chat']

    @staticmethod
    def process_chat_log(chat_json):
        log = chat_json['params'] # Why is this called params??
        events, next_event = log['events'], log['nextEndDate']
        moderator_chat = defaultdict() # teacher : chat
        participant_chat = defaultdict() # student : chat
        day = None
        for l in events:
            date = pendulum.parse(l['date'])
            if day 
                if day < date:
                    day = date
            else:
                day = date

            type_speaker = l['type'].lower()
            if type_speaker == 'moderator':
                moderator_chat[name].append((date, body))
            elif type_speaker == 'participant':
                participant_chat[name].append((date, body))

        return {'teacher':moderator_chat.keys(),
            'day': f'{day.year}-{day.month}-{day.day}',
            'teacher_chat': moderator_chat,
            'student_chat': participant_chat,
            'next_day': next_event}
