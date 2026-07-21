import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://127.0.0.1"

class LoginTests(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        self.driver.quit()

    def test_short_password_rejected(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.NAME, "password").send_keys("short1")
        self.driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)
        self.assertIn("at least 10 characters", self.driver.page_source)

    def test_common_password_rejected(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.NAME, "password").send_keys("qwertyuiop")
        self.driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)
        self.assertIn("too common", self.driver.page_source)

    def test_valid_password_accepted(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.NAME, "password").send_keys("Xk9mQr2vTzUnique")
        self.driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)
        self.assertIn("Welcome", self.driver.page_source)
        self.assertIn("Xk9mQr2vTzUnique", self.driver.page_source)

    def test_logout_returns_home(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.NAME, "password").send_keys("Xk9mQr2vTzUnique")
        self.driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)
        self.driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)
        self.assertIn("Login", self.driver.page_source)

if __name__ == "__main__":
    unittest.main()