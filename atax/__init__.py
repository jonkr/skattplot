import importlib.resources as pkg_resources
import os

from . import data

class RawRow:
    """Raw input line

    Knows how to get the values from the fixed width columns.
    """

    VALID_TABLE_NUMBERS = range(29, 40 + 1)
    AMOUNT_ROW_TYPE_INDICATOR = "B"
    PERCENTAGE_ROW_TYPE_INDICATOR = "%"
    VALID_TYPE_INDICATORS = (
        AMOUNT_ROW_TYPE_INDICATOR,
        PERCENTAGE_ROW_TYPE_INDICATOR,
    )

    def __init__(self, raw_line):
        assert raw_line[0:2] == "30", "Unexpected line format"
        self._line = raw_line

    @property
    def table_number(self):
        _table_num = int(self._line[3:5])
        assert _table_num in self.VALID_TABLE_NUMBERS
        return _table_num

    @property
    def lower_bound(self):
        return int(self._line[5:12])

    @property
    def upper_bound(self):
        if self._line[12:19] == "       ":  # last line in table
            return float("inf")
        else:
            return int(self._line[12:19])

    @property
    def row_type(self):
        _type = self._line[2:3]
        assert _type in self.VALID_TYPE_INDICATORS
        return _type

    @property
    def tax(self):
        """Either the tax deduction amount or the tax percentage"""
        _tax = int(self._line[19:24])
        if self.row_type == self.PERCENTAGE_ROW_TYPE_INDICATOR:
            assert 0 <= _tax <= 100  # ensure valid percentage
        return _tax


class AmountRow:
    """Represents a row with explicit tax decuction amount"""

    VALID_ROW_TYPE_INDICATOR = "B"

    def __init__(self, raw_row):
        assert raw_row.row_type == self.VALID_ROW_TYPE_INDICATOR
        self.lower_bound = raw_row.lower_bound
        self.upper_bound = raw_row.upper_bound
        self._tax = raw_row.tax

    def get_tax(self, gross_salary):
        return self._tax


class PercentageRow:
    """Represents a row with tax deducation percentage instead of explicit amount"""

    VALID_ROW_TYPE_INDICATOR = "%"

    def __init__(self, raw_row):
        assert raw_row.row_type == self.VALID_ROW_TYPE_INDICATOR
        self.lower_bound = raw_row.lower_bound
        self.upper_bound = raw_row.upper_bound
        self.tax_rate = raw_row.tax

    def get_tax(self, gross_salary):
        return round(float(self.tax_rate) / 100 * gross_salary)


class TableBuilder:

    def __init__(self, table_number):
        self.table_number = table_number
        self.table = []

    def build(self):
        for raw_line in self._raw_lines():
            self._add_line(raw_line)
        return self.table

    def _raw_lines(self):
        for line in pkg_resources.open_text(data, "monthly_tax_2021.txt"):
            yield line

    def _append_line(self, raw_row):
        if raw_row.row_type == RawRow.AMOUNT_ROW_TYPE_INDICATOR:
            self.table.append(AmountRow(raw_row))
        else:
            self.table.append(PercentageRow(raw_row))

    def _add_line(self, raw_line):
        raw_row = RawRow(raw_line)
        if self.table_number == raw_row.table_number:
            self._append_line(raw_row)


class ATax:
    def __init__(self, table_number=30):
        self.table = None
        self.table_number = table_number

    def _build(self):
        if not self.table:
            self.table = TableBuilder(self.table_number).build()
            assert len(self.table) > 0, 'Too few rows parsed'

    def get(self, gross_salary):
        self._build()
        if gross_salary <= 0:
            return 0
        gross_salary = round(gross_salary, 0)
        assert gross_salary >= self.table[0].lower_bound
        assert gross_salary <= self.table[-1].upper_bound
        for row in self.table:
            if row.lower_bound <= gross_salary <= row.upper_bound:
                return row.get_tax(gross_salary)

    @property
    def bounds(self):
        self._build()
        for row in self.table:
            yield row.lower_bound
            if row.upper_bound != float("inf"):
                yield row.upper_bound
            else:
                # Last row in table, tax rate is constant from here on.
                # We fake a reasonable value to get a nice line when plotting.
                yield 2 * row.lower_bound