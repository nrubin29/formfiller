from abc import abstractmethod

from lib import FormFiller, FormElement


class Spreadsheet:
    def __init__(self, file_name):
        if not file_name.endswith('csv'):
            raise Exception('Only csv files are supported.')

        self.file_name = file_name

        with open(file_name) as file:
            header, *lines = map(str.strip, file.readlines())
            self.header = header.split(',')
            self.lines = map(lambda line: line.split(','), lines)

    def set_cell(self, line_number, column_name, value):
        self.lines[line_number][self.header.index(column_name)] = value

    def save(self):
        with open(self.file_name, 'w') as file:
            file.write(','.join(self.header))
            file.writelines([','.join(line) for line in self.lines])


class FileFormFiller(FormFiller):
    def __init__(self, spreadsheet, elements):
        super().__init__(elements)
        self.spreadsheet = spreadsheet

    def run(self, driver):
        for i, line in enumerate(self.spreadsheet.lines):
            for header, cell in zip(self.spreadsheet.header, line):
                self.elements[header].val = cell

            for element in self.elements.values():
                if isinstance(element, FileFormElement):
                    element._run_file(element, self.spreadsheet, i)

                else:
                    element.run(driver)


class FileFormElement(FormElement):
    def __init__(self, name=None, id=None, selector=None):
        super().__init__(name, id, selector)

    def _run(self, element):
        raise Exception('FileFormElement must be in a FileFormFiller and use _run_file.')

    @abstractmethod
    def _run_file(self, element, spreadsheet, line_number):
        raise Exception('Not implemented')


class UpdateSpreadsheetColumn(FileFormElement):
    def __init__(self, column_name, name=None, id=None, selector=None):
        super().__init__(name, id, selector)
        self.column_name = column_name

    def _run_file(self, element, spreadsheet, line_number):
        spreadsheet.set_cell(line_number, self.column_name, element.text)
