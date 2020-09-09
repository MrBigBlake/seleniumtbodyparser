from .table_body import Tbody


def parse_tbody(driver, tbody_selector):
    """
    解析表单
    :param driver: 浏览器驱动
    :param tbody_selector: table_body 的css选择器
    :return: 返回一个Tbody对象
    """
    outer_html = driver.find_element_by_css_selector(tbody_selector).attr("outHTML")
    tbody = Tbody(tbody_selector, outer_html)
    return tbody
