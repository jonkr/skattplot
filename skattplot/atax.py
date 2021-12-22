import re


class TableRow:

    def __init__(self, raw_line):
        row_type_indicator = raw_line[2:3]
        assert row_type_indicator in ('B', '%')
        assert raw_line[0:2] == '30', 'Unexpected line format'

        self.tax_number = int(raw_line[3:5])
        assert self.tax_number in range(29, 40 + 1)

        self.lower_bound = int(raw_line[5:12])

        if raw_line[12:19] == '       ':
            self.upper_bound = float('inf')
        else:
            self.upper_bound = int(raw_line[12:19])

        self._type = row_type_indicator
        if self._type == 'B':
            self._tax = int(raw_line[19:24])
        elif self._type == '%':
            self._tax_rate = int(raw_line[19:24])

    @classmethod
    def include_row(cls, raw_line, table_number):
        tax_number = int(raw_line[3:5])
        assert tax_number in range(29, 40 + 1)
        return tax_number == table_number

    def get_tax(self, gross_salary):
        assert isinstance(gross_salary, int)
        if self._type == '%':
            return round(float(self._tax_rate)/100 * gross_salary)
        else:
            return self._tax



class ATax:

    VALID_TABLE_NUMBERS = range(29, 40 +1)
    DEFAULT_TABLE_NUMBER = 30

    RAW_DATA_FILE = './skattplot/data/monthly_tax_2021.txt'

    def __init__(self, table_number=DEFAULT_TABLE_NUMBER):
        self.table = self._read_tax_table(table_number)

    def _read_tax_table(self, table_number):
        table = []
        with open(self.RAW_DATA_FILE) as raw_lines:
            for raw_line in raw_lines:
                if TableRow.include_row(raw_line, table_number):
                    table.append(TableRow(raw_line))
        return table

    def get(self, gross_salary):
        if gross_salary == 0:
            return 0
        gross_salary = round(gross_salary, 0)
        assert gross_salary >= self.table[0].lower_bound
        assert gross_salary <= self.table[-1].upper_bound
        for row in self.table:
            if row.lower_bound <= gross_salary <= row.upper_bound:
                return row.get_tax(gross_salary)
