import itertools
import time
from abc import abstractmethod, ABC
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.support.select import Select


class Form:
    def __init__(self, url, headless=False):
        self.url = url

        options = webdriver.ChromeOptions()
        options.headless = headless
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(3)
        self.driver.get(self.url)

    def select(self, name=None, id=None, selector=None, nth_child=None, **kwargs):
        if (not name and not id and not selector) or any(
                [a and b for a, b in itertools.permutations([name, id, selector], 2)]):
            raise Exception('Must specify name xor id xor selector')

        if name:
            elems = self.driver.find_elements_by_name(name)

        elif id:
            elems = self.driver.find_elements_by_id(id)

        else:
            elems = self.driver.find_elements_by_css_selector(selector)

        elem = elems[0 if nth_child is None else nth_child]

        if elem.tag_name == 'input':
            if elem.get_attribute('type') == 'submit' or elem.get_attribute('type') == 'button':
                return ButtonFormElement(elem)

            else:
                return TextFormElement(elem **kwargs)

        elif elem.tag_name == 'button' or elem.tag_name == 'a':
            return ButtonFormElement(elem)

        elif elem.tag_name == 'textarea':
            return TextFormElement(elem, **kwargs)

        elif elem.tag_name == 'select':
            return SelectFormElement(elem, **kwargs)

        else:
            return FormElement(elem)

    def fill(self, elements):
        for element in elements:
            element.run(self.driver)

    def fill_from_row(self, row, elements):
        elems_to_fill = {element.col: element for element in elements if isinstance(element, InputFormElement)}

        for header, cell in zip(row.spreadsheet.header, row.cells):
            elems_to_fill[header].val = cell

        self.fill(elements)

    @contextmanager
    def frame(self, id):
        self.driver.switch_to.frame(self.driver.find_element_by_id(id))
        yield
        self.driver.switch_to.default_content()


class FormElement(ABC):
    def __init__(self, element):
        self.element = element

    @property
    def text(self):
        return self.element.text

    def attribute(self, name):
        return self.element.get_attribute(name)

    @abstractmethod
    def run(self):
        pass


class InputFormElement(FormElement, ABC):
    def __init__(self, element, val=None, col=None):
        super().__init__(element)
        self.val = val
        self.col = col

        if not val and not col:
            raise Exception('Must specify val or col')

    @abstractmethod
    def run(self):
        pass


class TextFormElement(InputFormElement):
    def __init__(self, element, val=None, col=None):
        super().__init__(element, val, col)

    def run(self):
        if not self.val:
            raise Exception('Missing val')

        self.element.send_keys(self.val)


class SelectFormElement(InputFormElement):
    def __init__(self, element, val=None, col=None):
        super().__init__(element, val, col)

    def run(self):
        if not self.val:
            raise Exception('Missing val')

        Select(self.element).select_by_visible_text(self.val)


class ButtonFormElement(FormElement):
    def __init__(self, element):
        super().__init__(element)

    def run(self):
        self.element.click()


class SleepElement(FormElement):
    def __init__(self, seconds):
        super().__init__(None)
        self.seconds = seconds

    def run(self):
        time.sleep(self.seconds)
