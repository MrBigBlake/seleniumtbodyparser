seleniumtbodyparser 是一个基于 selenium 的网页 tbody 解析工具

目前支持的 tbody 格式:
- tbody > tr > td
- tbody > tr > th
- tbody > tr > td > input


# 安装
```
pip install seleniumtbodyparser
```
# 使用示例

![image-20200912171452262](https://md-img-hub.oss-cn-shanghai.aliyuncs.com/img/image-20200912171452262.png)

## 基本使用

对如上表格的 tbody 进行解析

```python
from selenium import webdriver
from seleniumtbodyparser import Parser

driver = webdriver.Chrome()
driver.get(r"seleniumtbodyparser\demo.html")

parser = Parser(driver)
tbody = parser.parse(tbody_selector="#tbody")
for row in tbody.rows:
    print(row)
    # for cell in row.cells:
    #     print(cell.text)
```

解析结果如下

```
1, 大米1, 手机, 6666, 2
2, 香蕉2, 手机, 8888, 1
3, Kindle, 电纸书, 999, 1
4, 三体, 纸质书, 99, 1
```



## 根据列索引和文本进行匹配

根据列索引和文本匹配到行, 返回包含这些行的 `tbody` 对象

- **一对限制条件**

```python
mobile_tbody = tbody.get_inner_tbody(2, "手机")
for row in mobile_tbody.rows:
    print(row)
    # for cell in row.cells:
    #     print(cell.text)   
```

匹配到第 3 列文本是 "手机" 的行,  返回包含这些行的 `tbody` 对象, 解析结果如下

```
1, 大米1, 手机, 6666, 2
2, 香蕉2, 手机, 8888, 1
```

- **多对限制条件**

```python
mobile_tbody_2 = tbody.get_inner_tbody({2: "手机", 4: "2"})
for row in mobile_tbody_2.rows:
    print(row)
    # for cell in row.cells:
    # print(cell.text)
```

匹配到第 3 列文本是 "手机" , 第 5 列 是 "2" 的行,  返回包含这些行的 `tbody` 对象, 解析结果如下

```
1, 大米1, 手机, 6666, 2
```

- **模糊匹配**

```python
book_tbody = tbody.get_inner_tbody_fuzzy(2, "书")
for row in book_tbody.rows:
    print(row)
    # for cell in row.cells:
    #     print(cell.text)
```

匹配到第 3 列文本包含 "书" 的行,  返回包含这些行的 `tbody` 对象, 解析结果如下

```
3, Kindle, 电纸书, 999, 1
4, 三体, 纸质书, 99, 1
```

