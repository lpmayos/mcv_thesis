from __future__ import print_function  # Only needed for Python 2
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException


class seleniumChromeDriver():

    def __init__(self, chrome_path):
        self.driver = webdriver.Chrome(chrome_path)
        # self.driver.implicitly_wait(10)  # seconds

    def find_element(self, num_times, action, param):
        """
        """
        i = 0
        while i < num_times:
            try:
                element = action(param)
                return element
            except NoSuchElementException:
                self.close_popups()
                i += 1

    def click_element(self, num_times, element):
        """
        """
        i = 0
        while i < num_times:
            try:
                element.click()
                return
            except WebDriverException:
                self.close_popups()
                i += 1

    def get(self, url):
        """
        """
        self.driver.get('https://admin.typeform.com/login/')

    def close_popups(self):
        """
        """
        try:
            self.driver.find_element_by_class_name('close-button').click()
        except NoSuchElementException:
            pass
        try:
            self.driver.find_element_by_class_name('close-button-save-account-popup').click()
        except NoSuchElementException:
            pass

    def send_keys(self, id, text):
        """
        """
        element = self.find_element(1000, self.driver.find_element_by_id, id)
        element.clear()
        element.send_keys(text)

    def click_element_by_css_selector(self, selector):
        """
        """
        element = self.find_element(1000, self.driver.find_element_by_css_selector, selector)
        self.click_element(1000, element)

    def click_element_by_link_text(self, text):
        """
        """
        element = self.find_element(1000, self.driver.find_element_by_link_text, text)
        self.click_element(1000, element)

    def click_element_by_class_name(self, class_name):
        """
        """
        element = self.find_element(1000, self.driver.find_element_by_class_name, class_name)
        self.click_element(1000, element)

    def click_element_by_id(self, id):
        """
        """
        element = self.find_element(1000, self.driver.find_element_by_id, id)
        self.click_element(1000, element)

    def switch_to_frame(self, id):
        """
        """
        element = self.find_element(1000, self.driver.find_element_by_id, id)
        self.driver.switch_to_frame(element)

    def find_element_by_css_selector(self, selector):
        """
        """
        return self.find_element(1000, self.driver.find_element_by_css_selector, selector)
