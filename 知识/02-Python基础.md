# 2. Python 基础：核心概念清单与自测题库

对应主题页：[2. Python 基础](../课程/02-Python基础.md)。

## 说明

- 内容依据 [Python 官方教程（简体中文）](https://docs.python.org/zh-cn/3/tutorial/index.html) 与官方参考文档整理，每道题标注出处章节。
- 每道代码题的"答案"输出，用 `工具/校验题库.py` 在 Python 3.12.3 上实际运行核对；官方文档链接指向文档的当前版本。
- 使用方法：先看概念清单，逐条用自己的话解释；再做题库，先预测输出，再对照答案。做错的题进入复习队列。
- 题库共 34 题。题目由编者编写，若与你的课程或教材有出入，以官方文档为准。

## 概念清单

学完主题 2 后，下面每一条都应能用一两句话解释并举出例子。括号里是对应的题目。

### 变量与对象

- 变量是绑定到对象的名字，赋值不会复制对象（Q02-01）
- `==` 比较值，`is` 比较是否同一个对象（Q02-02）
- 可变对象（list、dict、set）与不可变对象（int、str、tuple）的区别（Q02-03、Q02-08）
- 浅拷贝只复制最外层，内部的可变对象仍是同一个（Q02-11）

### 数值、字符串与布尔

- 整数没有大小上限（Q02-34）；`/`、`//`、`%` 的区别，负数整除向下取整（Q02-05）
- 浮点数是二进制近似，不能直接用 `==` 比较（Q02-06）
- 字符串不可变，可切片；常用方法 `split`、`strip`、`join`（Q02-03、Q02-04、Q02-31）
- f-string 与格式说明符（Q02-30）
- 哪些值在条件判断里为假（Q02-07）

### 容器

- list 的 `append` 与 `extend`、`sort` 与 `sorted`（Q02-09、Q02-10）
- tuple 不可变，但可以包含可变对象（Q02-08）
- dict 的取值方式与键的要求（Q02-12、Q02-13）
- set 用于去重与成员判断（Q02-14）
- 推导式（Q02-15）

### 控制流

- `range` 的三个参数与取值区间（Q02-16）
- 循环的 `else` 子句、`break` 与 `continue`（Q02-17、Q02-18）

### 函数

- 没有 `return` 的函数返回 `None`（Q02-20）
- 位置参数、默认值、`*args`、`**kwargs`（Q02-21）
- 默认参数只在定义时求值一次，可变默认值会累积（Q02-19）
- 局部变量、全局变量与 `global`（Q02-22）

### 异常

- `try`、`except`、`else`、`finally` 的执行顺序（Q02-23）
- 常见异常类型：`ValueError`、`IndexError`、`KeyError`、`AttributeError`（Q02-24）

### 文件与模块

- 用 `with` 读写文件并显式指定编码（Q02-25）
- `import` 与 `from ... import ...` 的区别（Q02-33）
- `if __name__ == "__main__":` 的作用（Q02-26）

### 类

- 类属性与实例属性（Q02-27）
- 继承与 `super()`（Q02-28）
- `__str__` 与 `__repr__`（Q02-29）

## 自测题库

### Q02-01 赋值不复制对象

- 类型：易错点
- 出处：[教程 3.1.3 列表](https://docs.python.org/zh-cn/3/tutorial/introduction.html#lists)
- 问题：下面的代码打印什么？为什么？

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```

- 答案：

```text
[1, 2, 3, 4]
```

赋值不复制数据，`a` 与 `b` 是同一个列表对象的两个名字，通过任何一个名字修改，另一个都能看到。

### Q02-02 `==` 与 `is`

- 类型：概念题
- 出处：[参考手册 3.1 对象、值与类型](https://docs.python.org/zh-cn/3/reference/datamodel.html#objects-values-and-types)
- 问题：下面的代码打印什么？

```python
a = [1, 2]
b = [1, 2]
c = a
print(a == b, a is b, a is c)
```

- 答案：

```text
True False True
```

`==` 比较两个对象的值是否相等；`is` 比较它们是不是同一个对象。`a` 与 `b` 值相等但是两个对象，`c` 与 `a` 是同一个对象。

### Q02-03 字符串不可变

- 类型：概念题
- 出处：[教程 3.1.2 文本](https://docs.python.org/zh-cn/3/tutorial/introduction.html#text)
- 问题：能不能用 `s[0] = "H"` 把 `"hello"` 改成 `"Hello"`？如果不能，怎么得到 `"Hello"`？

```python
s = "hello"
try:
    s[0] = "H"
except TypeError as e:
    print("TypeError:", e)
s2 = "H" + s[1:]
print(s2)
```

- 答案：

```text
TypeError: 'str' object does not support item assignment
Hello
```

字符串不可变，不能原地修改某个字符，只能构造一个新字符串。

### Q02-04 字符串切片

- 类型：代码题
- 出处：[教程 3.1.2 文本](https://docs.python.org/zh-cn/3/tutorial/introduction.html#text)
- 问题：下面打印什么？

```python
s = "Python"
print(s[1:4], s[-2:], s[::-1])
```

- 答案：

```text
yth on nohtyP
```

切片 `s[a:b]` 取下标 a 到 b-1；负数下标从末尾数起；步长为 -1 表示倒序。

### Q02-05 除法与取整

- 类型：代码题
- 出处：[教程 3.1.1 数字](https://docs.python.org/zh-cn/3/tutorial/introduction.html#numbers)
- 问题：下面打印什么？特别注意最后一个。

```python
print(7 / 2, 7 // 2, 7 % 2, -7 // 2)
```

- 答案：

```text
3.5 3 1 -4
```

`/` 是真除法，结果是浮点数；`//` 是向下取整的整除，`-7 // 2` 是 -3.5 向下取整得 -4；`%` 是余数。

### Q02-06 浮点数比较

- 类型：易错点
- 出处：[教程 15 浮点算术：问题和限制](https://docs.python.org/zh-cn/3/tutorial/floatingpoint.html)
- 问题：`0.1 + 0.2 == 0.3` 是什么？为什么？怎么比较更可靠？

```python
print(0.1 + 0.2 == 0.3)
print(round(0.1 + 0.2, 2) == 0.3)
```

- 答案：

```text
False
True
```

十进制小数在二进制里通常无法精确表示，加法后有极小误差。比较浮点数时不要直接用 `==`，可以先 `round`，或使用 `math.isclose`。

### Q02-07 条件判断里的假值

- 类型：概念题
- 出处：[标准库：真值检测](https://docs.python.org/zh-cn/3/library/stdtypes.html#truth-value-testing)
- 问题：下面每个值转成布尔值是什么？

```python
print(bool([]), bool(""), bool("0"), bool(0), bool(None), bool([0]))
```

- 答案：

```text
False False True False False True
```

空容器、空字符串、数字 0 和 `None` 为假；`"0"`（非空字符串）与 `[0]`（非空列表）为真。

### Q02-08 元组不可变，但内部可以是可变对象

- 类型：易错点
- 出处：[教程 5.3 元组和序列](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#tuples-and-sequences)
- 问题：下面打印什么？

```python
t = (1, [2, 3])
t[1].append(4)
print(t)
try:
    t[0] = 9
except TypeError as e:
    print("TypeError:", e)
```

- 答案：

```text
(1, [2, 3, 4])
TypeError: 'tuple' object does not support item assignment
```

元组不能重新绑定元素，但元素本身若是可变对象（这里是列表），它的内容仍然可以改变。

### Q02-09 `append` 与 `extend`

- 类型：代码题
- 出处：[教程 5.1 列表详解](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#more-on-lists)
- 问题：下面两段分别打印什么？

```python
a = [1]
a.append([2, 3])
print(a)
b = [1]
b.extend([2, 3])
print(b)
```

- 答案：

```text
[1, [2, 3]]
[1, 2, 3]
```

`append` 把参数当作一个元素加到末尾；`extend` 把参数里的每个元素逐个加进去。

### Q02-10 `sorted` 与 `list.sort`

- 类型：易错点
- 出处：[教程 5.1 列表详解](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#more-on-lists)
- 问题：下面打印什么？

```python
a = [3, 1, 2]
print(sorted(a), a)
print(a.sort(), a)
```

- 答案：

```text
[1, 2, 3] [3, 1, 2]
None [1, 2, 3]
```

`sorted(a)` 返回新列表，不改变 `a`；`a.sort()` 原地排序，返回 `None`。常见错误是写成 `a = a.sort()`，结果 `a` 变成 `None`。

### Q02-11 浅拷贝

- 类型：易错点
- 出处：[教程 5.1 列表详解](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#more-on-lists)、[copy 模块](https://docs.python.org/zh-cn/3/library/copy.html)
- 问题：下面打印什么？

```python
a = [[1], [2]]
b = a.copy()
b[0].append(9)
print(a)
```

- 答案：

```text
[[1, 9], [2]]
```

`copy()` 是浅拷贝，只复制最外层列表，里面的子列表仍是同一个对象。需要完全独立时用 `copy.deepcopy`。

### Q02-12 字典取值

- 类型：代码题
- 出处：[教程 5.5 字典](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#dictionaries)
- 问题：`d["b"]` 与 `d.get("b")` 在键不存在时有什么区别？

```python
d = {"a": 1}
print(d.get("b"), d.get("b", 0))
try:
    d["b"]
except KeyError as e:
    print("KeyError:", e)
```

- 答案：

```text
None 0
KeyError: 'b'
```

用 `[]` 取不存在的键会抛出 `KeyError`；`get` 返回 `None` 或你指定的默认值。

### Q02-13 字典的键必须可哈希

- 类型：概念题
- 出处：[教程 5.5 字典](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#dictionaries)
- 问题：列表能不能作字典的键？元组呢？

```python
try:
    d = {[1, 2]: "x"}
except TypeError as e:
    print("TypeError:", e)
d = {(1, 2): "x"}
print(d[(1, 2)])
```

- 答案：

```text
TypeError: unhashable type: 'list'
x
```

键必须是可哈希的（一般是不可变对象）。列表可变，不能作键；只含不可变元素的元组可以。

### Q02-14 集合去重

- 类型：代码题
- 出处：[教程 5.4 集合](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#sets)
- 问题：下面打印什么？

```python
print(sorted(set([3, 1, 3, 2, 1])))
print(len({1, 2, 2, 3}))
```

- 答案：

```text
[1, 2, 3]
3
```

集合里的元素唯一且无序，常用于去重和成员判断。

### Q02-15 列表推导式与字典推导式

- 类型：代码题
- 出处：[教程 5.1.3 列表推导式](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#list-comprehensions)
- 问题：下面打印什么？

```python
print([x * x for x in range(5) if x % 2 == 0])
print({c: len(c) for c in ["a", "bb"]})
```

- 答案：

```text
[0, 4, 16]
{'a': 1, 'bb': 2}
```

推导式的形式是 `[表达式 for 变量 in 可迭代对象 if 条件]`，条件可省略。

### Q02-16 `range` 的区间

- 类型：代码题
- 出处：[教程 4.3 range() 函数](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#the-range-function)
- 问题：下面打印什么？

```python
print(list(range(5)), list(range(2, 10, 3)), list(range(3, 0, -1)))
```

- 答案：

```text
[0, 1, 2, 3, 4] [2, 5, 8] [3, 2, 1]
```

`range(start, stop, step)` 包含 start，不包含 stop。

### Q02-17 循环的 `else` 子句

- 类型：易错点
- 出处：[教程 4.4 break 和 continue 语句](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#break-and-continue-statements)
- 问题：下面会打印什么？

```python
for i in range(3):
    if i == 5:
        break
else:
    print("没有 break")
for i in range(3):
    if i == 1:
        break
else:
    print("不会打印")
print("结束")
```

- 答案：

```text
没有 break
结束
```

循环的 `else` 只在循环正常结束（没有被 `break` 打断）时执行。

### Q02-18 `while` 与 `continue`

- 类型：代码题
- 出处：[教程 4.4 break 和 continue 语句](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#break-and-continue-statements)
- 问题：下面打印什么？

```python
i = 0
total = 0
while i < 6:
    i += 1
    if i % 2 == 0:
        continue
    total += i
print(total)
```

- 答案：

```text
9
```

`continue` 跳过本轮剩余代码进入下一轮，所以只有奇数 1、3、5 被累加。

### Q02-19 默认参数只求值一次

- 类型：易错点
- 出处：[教程 4.9.1 默认值参数](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#default-argument-values)
- 问题：下面打印什么？第二个函数为什么不会出问题？

```python
def add(item, box=[]):
    box.append(item)
    return box

print(add(1))
print(add(2))

def add2(item, box=None):
    if box is None:
        box = []
    box.append(item)
    return box

print(add2(1))
print(add2(2))
```

- 答案：

```text
[1]
[1, 2]
[1]
[2]
```

默认值在函数定义时只计算一次，可变默认值（如列表）会在多次调用之间累积。惯用写法是用 `None` 作默认值，在函数体里创建新对象。

### Q02-20 没有 `return` 的函数

- 类型：概念题
- 出处：[教程 4.8 定义函数](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions)
- 问题：下面打印什么？

```python
def f():
    pass

print(f())
```

- 答案：

```text
None
```

没有 `return` 语句的函数返回 `None`。

### Q02-21 参数的几种形式

- 类型：代码题
- 出处：[教程 4.9.2 关键字参数](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#keyword-arguments)、[4.9.4 任意实参列表](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#arbitrary-argument-lists)
- 问题：下面打印什么？

```python
def f(a, b=2, *args, **kw):
    return a, b, args, kw

print(f(1))
print(f(1, 3, 4, 5, x=6))
```

- 答案：

```text
(1, 2, (), {})
(1, 3, (4, 5), {'x': 6})
```

`*args` 收集多余的位置参数为元组，`**kw` 收集多余的关键字参数为字典。

### Q02-22 局部变量与 `global`

- 类型：易错点
- 出处：[教程 9.2 Python 作用域和命名空间](https://docs.python.org/zh-cn/3/tutorial/classes.html#python-scopes-and-namespaces)
- 问题：下面每一步打印什么？

```python
x = 10

def show():
    x = 5
    return x

print(show(), x)

count = 0

def inc():
    global count
    count += 1

inc()
print(count)

def bad():
    count += 1

try:
    bad()
except UnboundLocalError as e:
    print("UnboundLocalError:", e)
```

- 答案：

```text
5 10
1
UnboundLocalError: cannot access local variable 'count' where it is not associated with a value
```

函数里对名字赋值，默认创建局部变量，不影响全局的同名变量。要修改全局变量需要 `global` 声明；没声明就对它做 `+=`，Python 把它当局部变量，在赋值前读取就会报错。报错信息文字随 Python 版本可能略有不同。

### Q02-23 `try`、`except`、`else`、`finally`

- 类型：代码题
- 出处：[教程 8.3 异常的处理](https://docs.python.org/zh-cn/3/tutorial/errors.html#handling-exceptions)、[8.7 定义清理操作](https://docs.python.org/zh-cn/3/tutorial/errors.html#defining-clean-up-actions)
- 问题：`t(2)` 与 `t(0)` 分别打印什么？

```python
def t(x):
    try:
        r = 10 / x
    except ZeroDivisionError:
        print("除零")
    else:
        print("成功", r)
    finally:
        print("清理")

t(2)
t(0)
```

- 答案：

```text
成功 5.0
清理
除零
清理
```

没有异常时执行 `else`；发生异常且被捕获时执行对应的 `except`；无论如何最后都会执行 `finally`。

### Q02-24 常见异常类型

- 类型：概念题
- 出处：[教程 8.3 异常的处理](https://docs.python.org/zh-cn/3/tutorial/errors.html#handling-exceptions)
- 问题：下面四个表达式各抛出什么类型的异常？

```python
for code in ['int("abc")', '[1][3]', '{}["k"]', 'None.x']:
    try:
        eval(code)
    except Exception as e:
        print(type(e).__name__)
```

- 答案：

```text
ValueError
IndexError
KeyError
AttributeError
```

值不合法用 `ValueError`，下标越界 `IndexError`，字典缺键 `KeyError`，对象没有该属性 `AttributeError`。

### Q02-25 用 `with` 读写文件

- 类型：代码题
- 出处：[教程 7.2 读写文件](https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#reading-and-writing-files)
- 问题：为什么推荐 `with open(...)`？为什么要写 `encoding="utf-8"`？下面打印什么？

```python
import os, tempfile
p = os.path.join(tempfile.mkdtemp(), "t.txt")
with open(p, "w", encoding="utf-8") as f:
    f.write("你好\n第二行\n")
with open(p, encoding="utf-8") as f:
    for line in f:
        print(line.rstrip())
print(f.closed)
```

- 答案：

```text
你好
第二行
True
```

`with` 在代码块结束时自动关闭文件，即使中途出错也会关闭。不指定编码时使用系统默认编码，不同平台可能不同，读写中文文件时容易出现乱码，所以建议显式指定。

### Q02-26 `__name__ == "__main__"`

- 类型：概念题
- 出处：[教程 6.1.1 以脚本方式执行模块](https://docs.python.org/zh-cn/3/tutorial/modules.html#executing-modules-as-scripts)
- 问题：直接运行一个脚本时，`__name__` 是什么？被别的文件 `import` 时呢？

```python
print(__name__)
```

- 答案：

```text
__main__
```

直接运行时 `__name__` 是 `"__main__"`；被导入时是模块名。所以 `if __name__ == "__main__":` 下的代码只在直接运行时执行，被导入时不执行。

### Q02-27 类属性与实例属性

- 类型：易错点
- 出处：[教程 9.3.5 类和实例变量](https://docs.python.org/zh-cn/3/tutorial/classes.html#class-and-instance-variables)
- 问题：下面打印什么？

```python
class Dog:
    count = 0

    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name}：汪"

d1, d2 = Dog("小黑"), Dog("小白")
print(d1.speak())
d1.count = 5
print(Dog.count, d1.count, d2.count)
```

- 答案：

```text
小黑：汪
0 5 0
```

`d1.count = 5` 在实例 `d1` 上创建了自己的属性，不改变类属性 `Dog.count`，也不影响 `d2`。

### Q02-28 继承与 `super()`

- 类型：代码题
- 出处：[教程 9.5 继承](https://docs.python.org/zh-cn/3/tutorial/classes.html#inheritance)
- 问题：下面打印什么？

```python
class A:
    def hi(self):
        return "A"

class B(A):
    def hi(self):
        return super().hi() + "B"

print(B().hi(), isinstance(B(), A))
```

- 答案：

```text
AB True
```

子类可以重写父类方法，用 `super()` 调用父类的实现；子类的实例也是父类的实例。

### Q02-29 `__str__` 与 `__repr__`

- 类型：概念题
- 出处：[参考手册：object.__repr__](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__repr__)、[object.__str__](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__str__)
- 问题：下面打印什么？

```python
class P:
    def __repr__(self):
        return "P()"

    def __str__(self):
        return "一个 P"

print(P())
print([P()])
```

- 答案：

```text
一个 P
[P()]
```

`print` 单个对象用 `__str__`（给人看的）；对象放在容器里显示时用 `__repr__`（偏调试、尽量无歧义）。

### Q02-30 f-string

- 类型：代码题
- 出处：[教程 7.1.1 格式化字符串字面值](https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#formatted-string-literals)
- 问题：下面打印什么？

```python
name, age, pi = "小明", 18, 3.14159
print(f"{name}今年{age}岁，明年{age + 1}岁")
print(f"{pi:.2f}")
```

- 答案：

```text
小明今年18岁，明年19岁
3.14
```

花括号里可以放任意表达式；冒号后是格式说明符，`.2f` 表示保留两位小数。

### Q02-31 常用字符串方法

- 类型：代码题
- 出处：[标准库：字符串方法](https://docs.python.org/zh-cn/3/library/stdtypes.html#string-methods)
- 问题：下面打印什么？

```python
print("a,b,,c".split(","))
print("  x ".strip())
print("-".join(["a", "b", "c"]))
```

- 答案：

```text
['a', 'b', '', 'c']
x
a-b-c
```

`split` 按分隔符切开（连续分隔符之间产生空串）；`strip` 去掉两端空白；`join` 用分隔符把字符串序列连起来。

### Q02-32 可变对象的元素修改与遍历

- 类型：易错点
- 出处：[教程 4.2 for 语句](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#for-statements)
- 问题：下面打印什么？为什么列表 `nums` 没有全部变成 0？

```python
nums = [1, 2, 3]
for n in nums:
    n = 0
print(nums)
for i in range(len(nums)):
    nums[i] = 0
print(nums)
```

- 答案：

```text
[1, 2, 3]
[0, 0, 0]
```

循环变量 `n` 只是绑定到列表元素的一个名字，给 `n` 重新赋值不会改变列表本身；要修改列表元素，需要通过下标赋值。

### Q02-33 `import` 的两种写法

- 类型：概念题
- 出处：[教程 6.1 模块详解](https://docs.python.org/zh-cn/3/tutorial/modules.html#more-on-modules)
- 问题：`import math` 与 `from math import sqrt` 的区别是什么？

```python
import math
from math import sqrt
print(math.sqrt(16), sqrt(16))
```

- 答案：

```text
4.0 4.0
```

`import math` 把模块名放入当前命名空间，用 `math.sqrt` 访问；`from math import sqrt` 把 `sqrt` 这个名字直接放入当前命名空间，可以直接写 `sqrt`。

### Q02-34 整数没有大小上限

- 类型：概念题
- 出处：[教程 3.1.1 数字](https://docs.python.org/zh-cn/3/tutorial/introduction.html#numbers)
- 问题：`2 ** 100` 会溢出吗？

```python
print(2 ** 100)
print(type(2 ** 100).__name__)
```

- 答案：

```text
1267650600228229401496703205376
int
```

Python 的整数是任意精度的，不会像 C 语言的固定宽度整数那样溢出，只受内存限制。
