import itertools
import time
from abc import abstractmethod

from selenium import webdriver
from selenium.webdriver.support.select import Select


class FormBatch:
    def __init__(self, form_fillers, headless=False):
        self.form_fillers = form_fillers

        options = webdriver.ChromeOptions()
        options.headless = headless
        self.driver = webdriver.Chrome(options=options)

    def run(self):
        for form_filler in self.form_fillers:
            form_filler.run(self.driver)


class FormFiller:
    def __init__(self, url, elements):
        self.url = url
        self.elements = elements

    def run(self, driver):
        if self.url:
            driver.get(self.url)

        for element in self.elements:
            element.run(driver)


class FormElement:
    def __init__(self, name=None, id=None, selector=None):
        self.name = name
        self.id = id
        self.selector = selector

        if (not self.name and not self.id and not self.selector) or any([a and b for a, b in itertools.permutations([self.name, self.id, self.selector], 2)]):
            raise Exception('Must specify name xor id xor selector')

    def run(self, driver):
        if self.name:
            self._run(driver.find_element_by_name(self.name))

        elif self.id:
            self._run(driver.find_element_by_id(self.id))

        else:
            self._run(driver.find_element_by_css_selector(self.selector))

    @abstractmethod
    def _run(self, element):
        raise Exception('Not implemented')


class TextFormElement(FormElement):
    def __init__(self, name=None, id=None, selector=None, val=None):
        super().__init__(name, id, selector)
        self.val = val

        if not self.val:
            raise Exception('Must specify val')

    def _run(self, element):
        element.send_keys(self.val)


class SelectFormElement(FormElement):
    def __init__(self, name=None, id=None, selector=None, val=None):
        super().__init__(name, id, selector)
        self.val = val

        if not self.val:
            raise Exception('Must specify val')

    def _run(self, element):
        Select(element).select_by_visible_text(self.val)


class ButtonFormElement(FormElement):
    def __init__(self, name=None, id=None, selector=None):
        super().__init__(name, id, selector)

    def _run(self, element):
        element.click()


class SleepElement(FormElement):
    def __init__(self, seconds):
        super().__init__(name='__sleep__')
        self.seconds = seconds

    def run(self, driver):
        time.sleep(self.seconds)

    def _run(self, element):
        pass
