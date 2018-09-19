import itertools
import time
from abc import abstractmethod, ABC
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


def _get_element(driver, name, id, selector):
    if (not name and not id and not selector) or any([a and b for a, b in itertools.permutations([name, id, selector], 2)]):
        raise Exception('Must specify name xor id xor selector')

    if name:
        return driver.find_element_by_name(name)

    elif id:
        return driver.find_element_by_id(id)

    else:
        return driver.find_element_by_css_selector(selector)


class Form:
    def __init__(self, url, headless=False):
        self.url = url

        options = webdriver.ChromeOptions()
        options.headless = headless
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(3)
        self.driver.get(self.url)

    def fill(self, elements):
        for element in elements:
            element._run(self.driver)

    def fill_from_row(self, row, elements):
        elems_to_fill = {element.col: element for element in elements if isinstance(element, InputFormElement)}

        for header, cell in zip(row.spreadsheet.header, row.cells):
            elems_to_fill[header].val = cell

        self.fill(elements)

    def get_text(self, name=None, id=None, selector=None):
        return _get_element(self.driver, name, id, selector).text

    @contextmanager
    def wait_for_element_destroy(self, element, timeout=30):
        old_elem = _get_element(self.driver, element.name, element.id, element.selector)
        yield WebDriverWait(self.driver, timeout).until(staleness_of(old_elem))


class FormElement(ABC):
    def __init__(self, name=None, id=None, selector=None):
        self.name = name
        self.id = id
        self.selector = selector

    def _run(self, driver):
        self.run(_get_element(driver, self.name, self.id, self.selector))

    @abstractmethod
    def run(self, element):
        raise Exception('Not implemented')


class InputFormElement(FormElement, ABC):
    def __init__(self, name=None, id=None, selector=None, val=None, col=None):
        super().__init__(name, id, selector)
        self.val = val
        self.col = col

        if not val and not col:
            raise Exception('Must specify val or col')

    @abstractmethod
    def run(self, element):
        raise Exception('Not implemented')


class TextFormElement(InputFormElement):
    def __init__(self, name=None, id=None, selector=None, val=None, col=None):
        super().__init__(name, id, selector, val, col)

    def run(self, element):
        if not self.val:
            raise Exception('Missing val')

        element.send_keys(self.val)


class SelectFormElement(InputFormElement):
    def __init__(self, name=None, id=None, selector=None, val=None, col=None):
        super().__init__(name, id, selector, val, col)

    def run(self, element):
        if not self.val:
            raise Exception('Missing val')

        Select(element).select_by_visible_text(self.val)


class ButtonFormElement(FormElement):
    def __init__(self, name=None, id=None, selector=None):
        super().__init__(name, id, selector)

    def run(self, element):
        element.click()


class SleepElement(FormElement):
    def __init__(self, seconds):
        super().__init__(name='__sleep__')
        self.seconds = seconds

    def _run(self, driver):
        time.sleep(self.seconds)

    def run(self, element):
        pass
