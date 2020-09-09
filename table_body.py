from pyquery import PyQuery


class Tbody:
    def __init__(self, selector, outer_html):
        self.selector = selector
        self.outer_html = outer_html
        self.rows = []
        self.init_tbody()

    def init_tbody(self):
        rows = []
        if self.selector:
            tbody_element = PyQuery(self.outer_html)
            row_elements = tbody_element.find("tr").items()
            for row_index, row_element in enumerate(row_elements):
                row_selector = self.selector + f"> tr:nth-child({row_index + 1})"
                row = Row(row_element, row_selector)
                rows.append(row)
        self.rows = rows

    @property
    def length(self):
        return len(self.rows)

    @property
    def is_empty(self):
        return self.length == 0

    @property
    def has_no_data(self):
        if self.is_empty:
            return True
        if self.rows[-1].length <= 1:
            return True
        return False

    def get_inner_tbody(self, *args):
        """
        :param args:
        :return:
        """
        assert 0 < len(args) <= 2
        if len(args) == 1:
            assert isinstance(args[0], dict)
            tbody = self._get_inner_tbody_multiple(args[0])
        else:
            assert isinstance(args[0], int)
            assert isinstance(args[1], str)
            tbody = self._get_inner_tbody_single(args[1], args[0])
        return tbody

    def get_inner_tbody_fuzzy(self, *args):
        """
        :param args:
        :return:
        """
        assert 0 < len(args) <= 2
        if len(args) == 1:
            assert isinstance(args[0], dict)
            tbody = self._get_inner_tbody_multiple(args[0], fuzzy=True)
        else:
            assert isinstance(args[0], int)
            assert isinstance(args[1], str)
            tbody = self._get_inner_tbody_single(args[1], args[0], fuzzy=True)
        return tbody

    def _get_inner_tbody_single(self, cell_text, cell_index, fuzzy=False):
        """
        :param cell_text:
        :param cell_index:
        :param fuzzy:
        :return:
        """
        rows = []
        for row in self.rows:
            flag = row.target_cell_text_contains(cell_index, cell_text) \
                if fuzzy else row.target_cell_text_equals(cell_index, cell_text)
            if flag:
                rows.append(row)
        tbody = Tbody(selector="", outer_html="")
        tbody.rows = rows
        return tbody

    def _get_inner_tbody_multiple(self, cells: dict, fuzzy=False):
        """
        :param cells: {0: "xxx", 1: "xxx"}
        :param fuzzy: 是否模糊匹配
        :return:
        """
        rows = []
        for row in self.rows:
            flag1 = True
            for cell_index, cell_text in cells.items():
                flag2 = row.target_cell_text_contains(cell_index, cell_text) \
                    if fuzzy else row.target_cell_text_equals(cell_index, cell_text)
                if not flag2:
                    flag1 = False
                    break
            if flag1:
                rows.append(row)
        tbody = Tbody(selector="", outer_html="")
        tbody.rows = rows
        return tbody

    def get_target_col_cell_texts(self, col_index: int) -> list:
        """
        获取某一列所有单元格的值
        :param col_index: 第几列, 从0开始
        :return:
        """
        cell_texts = []
        for row in self.rows:
            if row.length >= col_index + 1:
                cell_text = row.cells[col_index].text
                cell_texts.append(cell_text)
        return cell_texts

    def remove_invisible_rows(self):
        """
        移除不可见的行
        :return:
        """
        for row in self.rows:
            row_element = row.row_element
            style = row_element.attr("style")
            if not style:
                continue
            if "display" in style or "hidden" in style:
                self.rows.remove(row)


class Row:
    def __init__(self, row_element, row_selector):
        self.row_element = row_element
        self.selector = row_selector
        self.cells = []
        self.init_row()

    def init_row(self):
        cells = []
        cell_elements = list(self.row_element.find("td").items())
        cell_elements_th = list(self.row_element.find("th").items())
        # 有的表单第一行是 tr > th, 这里做一个兼容
        if not cell_elements and cell_elements_th:
            cell_elements = cell_elements_th
            td = "th"
        else:
            td = "td"
        for cell_index, cell_element in enumerate(cell_elements):
            cell_selector = self.selector + f"> {td}:nth-child({cell_index + 1})"
            cell = Cell(cell_element, cell_selector)
            cells.append(cell)
        self.cells = cells

    def _target_cell_text_equals(self, index, text):
        """
        :param index:
        :param text:
        :return:
        """
        if self.length >= index + 1:
            cell = self.cells[index]
            if text == cell.text:
                return True
        return False

    def _target_cell_text_contains(self, index, text):
        """
        :param index:
        :param text:
        :return:
        """
        if self.length >= index + 1:
            cell = self.cells[index]
            if text in cell.text:
                return True
        return False

    @property
    def length(self):
        return len(self.cells)

    @property
    def is_empty(self):
        return self.length == 0

    def __str__(self):
        return ", ".join([cell.text for cell in self.cells])


class Cell:
    def __init__(self, cell_element, cell_selector):
        self.cell_element = cell_element
        self.selector = cell_selector
        self.text = ""
        self.init_cell()

    def init_cell(self):
        text = self.cell_element.text()
        # 适配 td > input
        if not text:
            input_element = self.cell_element.find("input")
            if input_element:
                text = input_element.attr("value")
                self.selector = self.selector + "> input:nth-child(1)"
        self.text = text.strip().replace("\n", "") if text else ""

    def __str__(self):
        return self.text
