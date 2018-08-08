from abc import abstractmethod

from selenium.webdriver.support.select import Select


class FormElement:
    def __init__(self, name=None, id=None):
        self.name = name
        self.id = id

        if (not self.name and not self.id) or (self.name and self.id):
            raise Exception('Must specify name xor id')

    def run(self, driver):
        if self.name:
            self._run(driver.find_element_by_name(self.name))

        else:
            self._run(driver.find_element_by_id(self.id))

    @abstractmethod
    def _run(self, element):
        raise Exception('Not implemented')


class TextFormElement(FormElement):
    def __init__(self, name=None, id=None, val=None):
        super().__init__(name, id)
        self.val = val

        if not self.val:
            raise Exception('Must specify val')

    def _run(self, element):
        element.send_keys(self.val)


class SelectFormElement(FormElement):
    def __init__(self, name=None, id=None, val=None):
        super().__init__(name, id)
        self.val = val

        if not self.val:
            raise Exception('Must specify val')

    def _run(self, element):
        Select(element).select_by_visible_text(self.val)


class ButtonFormElement(FormElement):
    def __init__(self, name=None, id=None):
        super().__init__(name, id),

    def _run(self, element):
        element.click()