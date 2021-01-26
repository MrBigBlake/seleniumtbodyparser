"""
selenium web table body parser based on pyquery
"""
from pyquery import PyQuery
from selenium.webdriver.remote.webdriver import WebDriver
from .parser import Tbody

__version__ = "1.0.1"
__date__ = "2021-01-26"
__author__ = "MrBigB"

# Copyright (c) 2021 MrBigB
# Licensed under the MIT licence:
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

__all__ = ["parse"]


def parse(tbody_selector: str,
          driver: WebDriver = None,
          page_source: str = None) -> Tbody:
    """
    parse tbody and return a Tbody object
    :param tbody_selector: css selector of target tbody element
    :param driver: selenium web driver object
    :param page_source: parse tbody directly from page_source when page_source is given
    :return: a Tbody object
    """
    if not (driver or page_source):
        raise TypeError("expected at least one of these two arguments: 'driver', 'page_source'")
    if page_source:
        tbody_outer_html = PyQuery(page_source).find(tbody_selector).outer_html()
    else:
        tbody_outer_html = driver.find_element_by_css_selector(tbody_selector).get_attribute("outerHTML")
    tbody_element = PyQuery(tbody_outer_html)
    tbody = Tbody(tbody_selector, tbody_element)
    return tbody
