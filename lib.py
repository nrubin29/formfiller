import itertools
import time
from abc import abstractmethod

from selenium import webdriver
from selenium.webdriver.support.select import Select


class FormBatch:
    def __init__(self, url, form_fillers, headless=False):
        self.url = url
        self.form_fillers = form_fillers

        options = webdriver.ChromeOptions()
        options.headless = headless
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.url)

    def run(self):
        for form_filler in self.form_fillers:
            form_filler.run(self.driver)


class FormFiller:
    def __init__(self, elements):
        self.elements = {elem.identifier: elem for elem in elements}

    def run(self, driver):
        for element in self.elements.values():
            element.run(driver)


class FormElement:
    def __init__(self, name=None, id=None, selector=None):
        self.name = name
        self.id = id
        self.selector = selector

        if (not self.name and not self.id and not self.selector) or any([a and b for a, b in itertools.permutations([self.name, self.id, self.selector], 2)]):
            raise Exception('Must specify name xor id xor selector')

    @property
    def identifier(self):
        return self.name if self.name else self.id if self.id else self.selector

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

    def _run(self, element):
        if not self.val:
            raise Exception('Must specify val')

        element.send_keys(self.val)


class SelectFormElement(FormElement):
    def __init__(self, name=None, id=None, selector=None, val=None):
        super().__init__(name, id, selector)
        self.val = val

    def _run(self, element):
        if not self.val:
            raise Exception('Must specify val')

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
