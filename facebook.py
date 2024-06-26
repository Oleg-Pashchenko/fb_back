import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from exceptions import *


class Facebook:

    def __init__(self, email: str, password: str):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.chrome = webdriver.Chrome(options=chrome_options)
        self.email = email
        self.password = password

    def login(self):
        self.chrome.get('https://www.facebook.com/')
        self.chrome.find_element(By.ID, 'email').send_keys(self.email)
        self.chrome.find_element(By.ID, 'pass').send_keys(self.password)
        self.chrome.find_element(By.ID, 'loginbutton').click()

    def is_logged_in(self) -> bool:
        try:
            WebDriverWait(self.chrome, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Create a post"]'))
            )
            return True
        except TimeoutException:
            return False

    def is_has_subscription(self) -> bool:
        try:
            WebDriverWait(self.chrome, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                "//span[text()='Joined']")))
            return True
        except Exception as e:
            return False

    def subscribe(self):
        try:
            button = WebDriverWait(self.chrome, 30).until(
                EC.presence_of_element_located((By.XPATH, '//span[text()="Join group"]'))
            )
            button.click()
        except:
            raise FacebookSubscribeError("Произошла ошибка при попытке подписаться на группу!")

    def create_post(self, text: str):
        span = self.chrome.find_element(By.XPATH, "//span[text()='Write something...']")
        span.click()
        time.sleep(1)
        span = self.chrome.find_element(By.XPATH, "//div[@aria-label='Create a public post…']")
        time.sleep(1)
        span.send_keys(text)
        time.sleep(1)
        span.send_keys(Keys.CONTROL, 'v')
        time.sleep(2)
        self.chrome.find_element(By.XPATH, "//div[@aria-label='Post']").click()
        time.sleep(5)

    def execute(self, group_url: str, text: str):
        self.login()

        if not self.is_logged_in():
            self.chrome.quit()
            raise FacebookAuthError("Невозможно зайти в аккаунт!")

        self.chrome.get(group_url)
        time.sleep(10)
        if not self.is_has_subscription():
            self.subscribe()

        if not self.is_has_subscription():
            raise FacebookZeroSubscription("Отсутствует подписка на группу!")

        self.create_post(text)
    def close(self):
        self.chrome.quit()


test_group = 'https://www.facebook.com/groups/201068038703444'
test_email = 'rakedat508@pursip.com'
test_password = 'nila@420'
