class Row:
    def __init__(self, i, line, spreadsheet):
        self.i = i
        self.line = line
        self.spreadsheet = spreadsheet

    def set(self, column, value):
        self.line[self.spreadsheet.header.index(column)] = value

    def to_csv(self):
        return ','.join(self.line)


class Spreadsheet:
    def __init__(self, file_name):
        if not file_name.endswith('csv'):
            raise Exception('Only csv files are supported.')

        self.file_name = file_name

        with open(file_name) as file:
            header, *lines = map(str.strip, file.readlines())
            self.header = header.split(',')
            self.rows = list(map(lambda en: (lambda i, line: Row(i, line.split(','), self))(*en), enumerate(lines)))

    def save(self):
        with open(self.file_name, 'w') as file:
            file.write(','.join(self.header))
            file.writelines([row.to_csv() for row in self.rows])
