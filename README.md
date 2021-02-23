seleniumtbodyparser is a tool to parse web table body based on pyquery

# Supported tbody formats
- tbody > tr > td
- tbody > tr > th
- tbody > tr > td > input


# Install
```
pip install seleniumtbodyparser
```
# Usage
```python
from selenium import webdriver
from seleniumtbodyparser import parse


driver = webdriver.Chrome()
driver.get(r"C:\seleniumtbodyparser\demo.html")
tbody_1 = parse(tbody_selector="#tbody_1", driver=driver)
print(tbody_1)
```