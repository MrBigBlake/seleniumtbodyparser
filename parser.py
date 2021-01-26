from typing import List, NoReturn
from pyquery import PyQuery


class Tbody:

    __slots__ = ("selector", "element", "rows")

    def __init__(self, selector: str = None, element: PyQuery = None):
        self.selector = selector
        self.element = element
        self.rows = []
        row_elements = self.element.find("tr").items() if self.element else []
        for row_index, row_element in enumerate(row_elements):
            row_selector = self.selector + f"> tr:nth-child({row_index + 1})"
            row = Row(row_selector, row_element)
            self.rows.append(row)

    def __getitem__(self, index):
        if isinstance(index, slice):
            new_tbody = Tbody()
            new_tbody.rows = self.rows[index]
            return new_tbody
        elif isinstance(index, int):
            return self.rows[index]
        else:
            raise TypeError("Tbody indices must be integers")

    def __len__(self):
        return len(self.rows)

    def __iadd__(self, other):
        self.rows.extend(other.rows)
        return self

    def __repr__(self):
        return "\n".join([repr(row) for row in self.rows])

    def __bool__(self):
        if not len(self.rows):
            return False
        # return False if the length of the last row lte 1
        if len(self.rows[-1]) <= 1:
            return False
        return True

    def __contains__(self, item):
        for row in self.rows:
            if item in row:
                return True
        return False

    def get_tbody_with_matched_rows(self, *args, **kwargs):
        """
        get_tbody_with_matched_rows by column index and text and return a Tbody object
        * a pair of restrictions:
            `get_tbody_with_matched_rows(0, "alpha")` or `get_tbody_with_matched_rows({0: "alpha"})`
        * multiple pairs of restrictions:
            `get_tbody_with_matched_rows({0: "alpha", 1: "bravo"})`
        * a pair of restrictions with fuzzy search:
            `get_tbody_with_matched_rows(0, "alpha", fuzzy=True)`
        :param args:
        :return: a Tbody object
        """
        if not args:
            raise TypeError("expected at least one positional argument")
        elif len(args) > 2:
            raise TypeError(f"expected at most 2 positional arguments, got {len(args)}")
        elif len(args) == 1:
            assert isinstance(args[0], dict), f"Invalid argument, {args[0]!r} is not a dict"
            param_dict = args[0]
        else:
            assert isinstance(args[0], int), f"Invalid argument, {args[0]!r} is not a int"
            assert isinstance(args[1], str), f"Invalid argument, {args[1]!r} is not a str"
            param_dict = {args[0]: args[1]}
        fuzzy = kwargs.get("fuzzy")  # fuzzy search or not
        rows = []
        for row in self.rows:
            row_matched = True
            for index, text in param_dict.items():
                cell_matched = row.is_target_cell_text_contains(index, text) if fuzzy \
                    else row.is_target_cell_text_equals(index, text)
                if not cell_matched:
                    row_matched = False
                    break
            if not row_matched:
                continue
            rows.append(row)
        tbody = Tbody()
        tbody.rows = rows
        return tbody

    def get_target_column_text_list(self, index: int) -> List[str]:
        text_list = []
        for row in self.rows:
            try:
                cell_text = row.cells[index].text
                text_list.append(cell_text)
            except IndexError:
                continue
        return text_list

    def remove_invisible_rows(self) -> NoReturn:
        rows = []
        for row in self.rows:
            row_element = row.element
            style = row_element.attr("style")
            if style and ("display" in style or "hidden" in style):
                continue
            rows.append(row)
        self.rows = rows


class Row:

    __slots__ = ("selector", "element", "cells")

    def __init__(self, selector: str = None, element: PyQuery = None):
        self.selector = selector
        self.element = element
        self.cells = []
        cell_elements = list(self.element.find("td").items()) if self.element else []
        cell_elements_th = list(self.element.find("th").items()) if self.element else []
        if not cell_elements and cell_elements_th:
            cell_elements = cell_elements_th
            td = "th"
        else:
            td = "td"
        for cell_index, cell_element in enumerate(cell_elements):
            cell_selector = self.selector + f"> {td}:nth-child({cell_index + 1})"
            cell = Cell(cell_selector, cell_element)
            self.cells.append(cell)

    def __getitem__(self, index):
        if isinstance(index, slice):
            new_row = Row()
            new_row.cells = self.cells[index]
            return new_row
        elif isinstance(index, int):
            return self.cells[index]
        else:
            raise TypeError("Row indices must be integers")

    def __len__(self):
        return len(self.cells)

    def __iadd__(self, other):
        self.cells.extend(other.cells)
        return self

    def __repr__(self):
        return ", ".join([cell.text for cell in self.cells])

    def __contains__(self, item):
        return item in [cell.text for cell in self.cells]

    def is_target_cell_text_equals(self, index: int, text: str) -> bool:
        try:
            cell = self.cells[index]
            if text == cell.text:
                return True
            return False
        except IndexError:
            return False

    def is_target_cell_text_contains(self, index: int, text: str) -> bool:
        try:
            cell = self.cells[index]
            if text in cell:
                return True
            return False
        except IndexError:
            return False


class Cell:
    
    __slots__ = ("selector", "element", "text")

    def __init__(self, selector: str = None, element: PyQuery = None):
        self.selector = selector
        self.element = element
        self.text = self.element.text() if self.element else ""
        if not self.text and self.element:
            input_elements = list(self.element.find("input").items())
            for index, input_element in enumerate(input_elements):
                style = input_element.attr("style")
                # ignore invisible input element
                if style and ("display" in style or "hidden" in style):
                    continue
                self.text = input_element.attr("value")
                self.selector = self.selector + f"> input:nth-child({index + 1})"
                break
        self.text = self.text.strip().replace("\n", "") if self.text else ""

    def __repr__(self):
        return self.text[:20]

    def __len__(self):
        return len(self.text)

    def __contains__(self, item):
        return item in self.text
