# 12. Python 进阶：核心概念清单与自测题库

对应主题页：[12. Python 进阶](../课程/12-Python进阶.md)。

## 说明

- 内容依据 [Python 官方文档：functools 模块](https://docs.python.org/zh-cn/3/library/functools.html)、[itertools 模块](https://docs.python.org/zh-cn/3/library/itertools.html)、[contextlib 模块](https://docs.python.org/zh-cn/3/library/contextlib.html)、[dataclasses 模块](https://docs.python.org/zh-cn/3/library/dataclasses.html)、[unittest 模块](https://docs.python.org/zh-cn/3/library/unittest.html)整理，覆盖装饰器、生成器、上下文管理器、常用标准库工具、测试。并发部分（多线程、多进程、GIL）已经在[主题 7](07-操作系统.md)结合操作系统知识讲过，这里不重复，只在概念清单里做一次索引。
- 代码题用 `工具/校验题库.py` 在 Python 3.12.3 上实际运行核对。
- 使用方法：先看概念清单，逐条用自己的话解释；再做题库，先预测输出，再对照答案。做错的题进入复习队列。
- 题库共 18 题。题目由编者编写，若与你的教材（如《流畅的 Python》）有出入，以官方文档为准。

## 概念清单

学完主题 12 后，下面每一条都应能用一两句话解释并举出例子。括号里是对应的题目。

### 装饰器

- 装饰器是一个接收函数、返回新函数的函数，用来在不改动原函数代码的前提下加上额外行为（Q12-01）
- `functools.wraps` 保留被装饰函数的名字等元信息（Q12-02）
- 带参数的装饰器需要多包一层函数（Q12-03）

### 生成器

- 生成器函数用 `yield` 产出值，调用时不立刻执行函数体，而是惰性地一步步执行到下一个 `yield`（Q12-04）
- 生成器比一次性构造整个列表更省内存，适合处理大数据或无穷序列（Q12-05）

### 上下文管理器

- `with` 语句保证进入和离开代码块时分别执行 `__enter__`、`__exit__`，即使中途抛出异常也会执行 `__exit__`（Q12-06、Q12-07）
- `contextlib.contextmanager` 用一个生成器函数就能写出上下文管理器，不需要手写类（Q12-08）
- `contextlib.suppress` 可以安静地忽略指定类型的异常（Q12-09）

### 常用标准库工具

- `functools.partial` 固定一个函数的部分参数，得到一个新函数（Q12-10）
- `functools.reduce` 把一个二元操作依次应用到序列上，"累积"出一个结果（Q12-11）
- `functools.lru_cache` 给函数加缓存（与主题 5 的 Q05-22 相衔接）（Q12-12）
- `itertools.chain` 把多个可迭代对象串联成一个；`itertools.groupby` 对连续相同的键分组（Q12-13、Q12-14）

### 类型标注与数据类

- 类型标注（type hint）只是注解，Python 运行时不会强制检查类型（Q12-15）
- `dataclasses.dataclass` 自动生成 `__init__`、`__eq__` 等方法，减少样板代码（Q12-16）

### 测试

- `unittest` 是标准库自带的测试框架，不需要额外安装（Q12-17）
- 海象运算符 `:=` 能在表达式内部完成赋值（Q12-18）

### 并发（衔接主题 7）

- 多线程、多进程、GIL、竞态条件、锁——这些概念已经在[主题 7](07-操作系统.md)结合操作系统知识详细讲过，这里不重复。

## 自测题库

### Q12-01 装饰器的本质

- 类型：代码题
- 出处：[Python 官方文档：函数定义（装饰器语法）](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#function-definitions)
- 问题：`@decorator` 语法糖展开后是什么样？

```python
def logged(func):
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logged
def add(a, b):
    return a + b

result_with_syntax = add(1, 2)

def add2(a, b):
    return a + b
add2 = logged(add2)
result_manual = add2(1, 2)

print(result_with_syntax, result_manual)
```

- 答案：

```text
调用 add
调用 add2
3 3
```

`@decorator` 放在函数定义上面，等价于"定义完函数后，把这个函数传给 `decorator`，再把返回值重新赋值给原来的名字"，即 `func = decorator(func)`。这里手动写的 `add2 = logged(add2)` 和用 `@logged` 语法糖的效果完全一样，只是语法糖更简洁、意图更明显。

### Q12-02 `functools.wraps` 保留元信息

- 类型：易错点
- 出处：[Python 官方文档：functools.wraps](https://docs.python.org/zh-cn/3/library/functools.html#functools.wraps)
- 问题：不用 `functools.wraps`，装饰后的函数名字会变成什么？

```python
import functools

def without_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def with_wraps(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@without_wraps
def f1():
    pass

@with_wraps
def f2():
    pass

print(f1.__name__, f2.__name__)
```

- 答案：

```text
wrapper f2
```

装饰器返回的其实是内部定义的 `wrapper` 函数，如果不做特殊处理，`f1.__name__` 会变成 `"wrapper"` 而不是 `"f1"`——这在调试、打印日志、自动生成文档时会造成困惑（看起来所有被装饰的函数都叫 `wrapper`）。`functools.wraps(func)` 是一个装饰器，专门用来把原函数 `func` 的 `__name__`、`__doc__` 等元信息复制到 `wrapper` 上，让 `f2.__name__` 正确地显示为 `"f2"`。写装饰器时应该养成加 `@functools.wraps` 的习惯。

### Q12-03 带参数的装饰器

- 类型：代码题
- 出处：装饰器工厂模式（返回装饰器的函数）
- 问题：`@repeat(3)` 这种带参数的装饰器，比不带参数的装饰器多了哪一层？

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def greet():
    return "hi"

print(greet())
```

- 答案：

```text
['hi', 'hi', 'hi']
```

普通装饰器是"函数接收函数，返回函数"（一层）；带参数的装饰器多了一层："`repeat(3)` 先返回一个真正的装饰器（`decorator`），这个装饰器再去装饰 `greet`"。可以这样理解：`@repeat(3)` 这一整行，先执行 `repeat(3)` 得到一个装饰器，再用这个装饰器去装饰下面的函数，等价于 `greet = repeat(3)(greet)`。

### Q12-04 生成器惰性执行

- 类型：代码题
- 出处：[Python 官方文档：yield 表达式](https://docs.python.org/zh-cn/3/reference/expressions.html#yield-expressions)
- 问题：调用一个含 `yield` 的函数，函数体会立刻开始执行吗？

```python
def gen():
    print("start")
    yield 1
    print("middle")
    yield 2

g = gen()
print("生成器已创建，但还没打印 start")
print(next(g))
print(next(g))
```

- 答案：

```text
生成器已创建，但还没打印 start
start
1
middle
2
```

调用 `gen()` 并不会执行函数体里的任何代码，只是创建一个生成器对象。函数体要等第一次调用 `next()` 时才真正从头开始执行，一直跑到第一个 `yield` 处暂停并把值交出来；再次 `next()` 会从暂停的地方继续往下执行，直到遇到下一个 `yield` 或函数结束。这种"用到才算"的惰性求值，和"一次性把所有结果都算出来存进列表"是完全不同的执行方式。

### Q12-05 生成器更省内存

- 类型：代码题
- 出处：[Python 官方文档：生成器表达式](https://docs.python.org/zh-cn/3/reference/expressions.html#generator-expressions)
- 问题：`[x for x in range(100000)]` 和 `(x for x in range(100000))` 占用的内存一样吗？

```python
import sys

as_list = [x for x in range(100000)]
as_generator = (x for x in range(100000))
print(sys.getsizeof(as_list) > sys.getsizeof(as_generator))
```

- 答案：

```text
True
```

列表推导式 `[...]` 会立刻算出所有 10 万个元素并全部存进内存；生成器表达式 `(...)` 只存了"怎么算下一个值"的逻辑，并不会预先把所有值都算出来存着，所以生成器对象本身占用的内存远小于装满数据的列表，且不随元素个数增长而线性增长。处理大文件、无穷序列这类场景时，用生成器可以避免一次性把所有数据都读进内存。

### Q12-06 `with` 保证 `__exit__` 一定执行

- 类型：代码题
- 出处：[Python 官方文档：with 语句](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#the-with-statement)
- 问题：`with` 代码块里如果抛出异常，`__exit__` 还会被调用吗？

```python
class Resource:
    def __enter__(self):
        print("acquire")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("release")
        return False  # 不吞掉异常，让它继续往外传播

try:
    with Resource():
        raise ValueError("出错了")
except ValueError:
    print("caught outside")
```

- 答案：

```text
acquire
release
caught outside
```

`with` 语句保证：进入代码块前调用 `__enter__`，离开代码块时（不管是正常结束还是因为异常提前退出）都会调用 `__exit__`。这里代码块内抛出了异常，`release` 仍然被打印出来，说明 `__exit__` 确实执行了；`__exit__` 返回 `False`（或不返回值）表示"不处理这个异常"，异常会继续往外传播，被外层的 `except` 捕获。这正是[主题 3](03-C与C++基础.md) Q03-28 讲的 RAII 思想在 Python 里的体现：即使出了异常，资源清理代码也不会被跳过。

### Q12-07 `__exit__` 可以吞掉异常

- 类型：易错点
- 出处：[Python 官方文档：object.__exit__](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__exit__)
- 问题：`__exit__` 返回 `True` 会怎样？

```python
class Suppressor:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("忽略了", exc_type.__name__ if exc_type else None)
        return True  # 返回真值会"吞掉"异常

with Suppressor():
    raise ValueError("这个异常会被吞掉")
print("代码能继续往下走")
```

- 答案：

```text
忽略了 ValueError
代码能继续往下走
```

`__exit__` 的返回值有特殊含义：如果返回一个真值（比如 `True`），表示"这个异常我已经处理好了，不要再往外传播"，异常就在这里被吞掉，`with` 语句之后的代码能正常继续执行，不会中断整个程序。这个机制很强大，但也容易被滥用——不小心让 `__exit__` 返回了真值，可能会悄悄吞掉本应该被发现的错误，调试时如果发现异常"凭空消失"，可以往这个方向排查。

### Q12-08 用生成器函数写上下文管理器

- 类型：代码题
- 出处：[Python 官方文档：contextlib.contextmanager](https://docs.python.org/zh-cn/3/library/contextlib.html#contextlib.contextmanager)
- 问题：`@contextmanager` 怎样把一个生成器函数变成上下文管理器？

```python
from contextlib import contextmanager

@contextmanager
def resource():
    print("acquire")
    yield "the-value"
    print("release")

with resource() as v:
    print("using", v)
```

- 答案：

```text
acquire
using the-value
release
```

`yield` 之前的代码相当于 `__enter__`，`yield` 出来的值就是 `as` 后面拿到的对象；`yield` 之后的代码相当于 `__exit__`，在 `with` 代码块结束时执行。这比 Q12-06 那种手写一个带 `__enter__`/`__exit__` 的类要简洁得多，是标准库里"用生成器语法糖代替样板类"的典型例子。

### Q12-09 `contextlib.suppress` 忽略指定异常

- 类型：代码题
- 出处：[Python 官方文档：contextlib.suppress](https://docs.python.org/zh-cn/3/library/contextlib.html#contextlib.suppress)
- 问题：怎样简洁地写"这段代码可能抛出某种异常，抛出就直接忽略，继续往下走"？

```python
from contextlib import suppress

with suppress(ZeroDivisionError):
    1 / 0
print("即使上面出错，这行也会执行")
```

- 答案：

```text
即使上面出错，这行也会执行
```

`suppress(某异常类型)` 是标准库提供的一个上下文管理器，等价于写一个 `try/except 某异常类型: pass`，但更简洁、意图更清楚：一眼就能看出"这里预期可能会抛出这种异常，而且明确决定忽略它"。只应该用来忽略确实不需要处理的异常，滥用可能会掩盖真正的 bug。

### Q12-10 `functools.partial`

- 类型：代码题
- 出处：[Python 官方文档：functools.partial](https://docs.python.org/zh-cn/3/library/functools.html#functools.partial)
- 问题：怎样基于一个通用函数，固定住某些参数，得到一个更专用的函数？

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print(square(5), cube(2))
```

- 答案：

```text
25 8
```

`partial(函数, 固定的参数...)` 返回一个新函数，调用这个新函数时，之前固定的参数会自动补上，只需要传剩下的参数。这里 `square` 就是"指数固定为 2 的 `power`"，`cube` 是"指数固定为 3 的 `power`"，比每次都手写 `lambda base: power(base, 2)` 更直接地表达了意图。

### Q12-11 `functools.reduce`

- 类型：代码题
- 出处：[Python 官方文档：functools.reduce](https://docs.python.org/zh-cn/3/library/functools.html#functools.reduce)
- 问题：`reduce` 怎样把一个列表"累积"成一个值？

```python
from functools import reduce

nums = [1, 2, 3, 4]
total = reduce(lambda acc, x: acc + x, nums, 0)
product = reduce(lambda acc, x: acc * x, nums, 1)
print(total, product)
```

- 答案：

```text
10 24
```

`reduce(函数, 序列, 初始值)` 从初始值开始，把函数依次应用到"当前累积结果"和"序列的下一个元素"上，用新的返回值更新累积结果，直到序列遍历完。求和是把"加法"当作这个二元操作反复应用（0+1=1, 1+2=3, 3+3=6, 6+4=10），求积同理（用乘法、初始值 1）。Python 内置的 `sum()` 本质上就是一种专门为求和优化过的 `reduce`。

### Q12-12 `functools.lru_cache`

- 类型：代码题
- 出处：[Python 官方文档：functools.lru_cache](https://docs.python.org/zh-cn/3/library/functools.html#functools.lru_cache)；与主题 5 的 Q05-22 相衔接
- 问题：怎样知道一个加了缓存的函数，某次调用是真的重新计算了，还是直接用了缓存？

```python
from functools import lru_cache

calls = []

@lru_cache(maxsize=None)
def slow_square(x):
    calls.append(x)
    return x * x

slow_square(3)
slow_square(3)
slow_square(4)
print(calls)
print(slow_square.cache_info().hits, slow_square.cache_info().misses)
```

- 答案：

```text
[3, 4]
1 2
```

`calls` 列表只在函数体真正执行时才会追加，`slow_square(3)` 被调用了两次，但函数体只真正跑了一次（第二次直接命中缓存），所以 `calls` 里 3 只出现一次。`cache_info()` 能查看命中（hits，直接用缓存）和未命中（misses，真正计算并存入缓存）的次数：`slow_square(3)`（首次）和 `slow_square(4)` 各触发一次未命中（共 2 次），`slow_square(3)`（第二次）命中缓存（1 次）。

### Q12-13 `itertools.chain`

- 类型：代码题
- 出处：[Python 官方文档：itertools.chain](https://docs.python.org/zh-cn/3/library/itertools.html#itertools.chain)
- 问题：想依次遍历好几个列表，但不想先把它们拼成一个大列表，怎么办？

```python
from itertools import chain

a = [1, 2]
b = [3, 4]
c = [5]
for x in chain(a, b, c):
    print(x, end=" ")
print()
```

- 答案：

```text
1 2 3 4 5
```

`chain(a, b, c)` 把多个可迭代对象逻辑上串联成一个，遍历时依次取完 `a` 的元素、再取 `b` 的、再取 `c` 的，但并不需要真的先构造一个包含所有元素的新列表（类似 Q12-05 生成器的惰性思路），适合需要遍历多个来源但不关心它们各自边界的场景。

### Q12-14 `itertools.groupby`

- 类型：易错点
- 出处：[Python 官方文档：itertools.groupby](https://docs.python.org/zh-cn/3/library/itertools.html#itertools.groupby)
- 问题：`groupby` 是把整个序列按键分组，还是只把"连续"相同键的分到一组？

```python
from itertools import groupby

data = ["a", "a", "b", "a", "a"]
grouped = [(k, list(g)) for k, g in groupby(data)]
print(grouped)
```

- 答案：

```text
[('a', ['a', 'a']), ('b', ['b']), ('a', ['a', 'a'])]
```

`itertools.groupby` 只把**连续**出现的相同键分到一组，不会像字典那样把所有键相同的元素（不管在序列里离得多远）都聚到一起——这里两段 `'a'` 因为被中间的 `'b'` 隔开，被分成了两个独立的组，而不是合并成一组。使用 `groupby` 之前通常需要先按分组的键排序，否则很容易产生"同一个键出现好几组"这种意料之外的结果。

### Q12-15 类型标注不强制检查

- 类型：代码题
- 出处：[Python 官方文档：typing 模块](https://docs.python.org/zh-cn/3/library/typing.html)（类型提示是可选的、渐进式的，运行时不强制执行）
- 问题：给参数标注 `x: int`，传一个字符串进去会报错吗？

```python
def double(x: int):
    return x + x

print(double("abc"))
print(double(21))
print(double.__annotations__)
```

- 答案：

```text
abcabc
42
{'x': <class 'int'>}
```

Python 的类型标注只是给人（和第三方静态检查工具，如 `mypy`）看的注释，解释器本身在运行时完全不会检查参数是否真的符合标注的类型，也不会因为传了"标注之外"的类型就报错或拒绝调用。这里参数标注是 `int`，但传一个字符串照样能正常运行——只要函数体里的操作（这里是 `+`）对这个类型本身是合法的（字符串支持用 `+` 做拼接），就不会出任何问题。真正会报错的情况只发生在传入的类型根本不支持函数体里用到的操作时（比如给这个函数传一个整数列表，`x + x` 会得到拼接后的列表而不报错，但传一个字典就会因为字典不支持 `+` 而报错）——这类错误永远发生在真正执行不兼容操作的那一行，而不是在传参、或看到类型标注的那一刻。`__annotations__` 能查看一个函数上写了哪些类型标注，供工具使用，这里只标注了参数没标注返回值，所以字典里只有一项。

### Q12-16 `dataclass` 自动生成方法

- 类型：代码题
- 出处：[Python 官方文档：dataclasses](https://docs.python.org/zh-cn/3/library/dataclasses.html)
- 问题：不用 `@dataclass`，要让两个对象"字段相同就判等"，需要自己写什么？用了 `@dataclass` 呢？

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1 == p2)
print(p1)
```

- 答案：

```text
True
Point(x=1, y=2)
```

普通的类默认按对象的内存地址判断是否相等（两个不同实例即使字段完全一样也判 `False`），要按字段内容判等需要自己实现 `__eq__`。`@dataclass` 装饰器会根据类里标注的字段，自动生成 `__init__`（接收这些字段作为参数）、`__eq__`（按字段值比较）、`__repr__`（打印时显示字段内容），大幅减少这类"数据容器"类需要手写的样板代码。

### Q12-17 用 `unittest` 写测试

- 类型：代码题
- 出处：[Python 官方文档：unittest](https://docs.python.org/zh-cn/3/library/unittest.html)
- 问题：标准库自带的测试框架怎么用？

```python
import unittest

def add(a, b):
    return a + b

class TestAdd(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(add(1, 2), 3)

    def test_negative(self):
        self.assertEqual(add(-1, -2), -3)

suite = unittest.TestLoader().loadTestsFromTestCase(TestAdd)
result = unittest.TextTestRunner(verbosity=0).run(suite)
print(result.testsRun, result.wasSuccessful())
```

- 答案：

```text
2 True
```

继承 `unittest.TestCase`，每个以 `test_` 开头的方法就是一条独立的测试用例，`self.assertEqual` 等断言方法检查实际结果是否符合预期，不符合就判这条用例失败。`unittest` 是标准库自带的，不需要额外安装（第三方的 `pytest` 语法更简洁、功能更丰富，但需要单独安装）。测试运行的详细过程信息（"Ran 2 tests..."这类）默认输出到标准错误，不会和 `print` 的内容混在一起。

### Q12-18 海象运算符

- 类型：代码题
- 出处：[Python 官方文档：赋值表达式](https://docs.python.org/zh-cn/3/reference/expressions.html#assignment-expressions)
- 问题：`:=` 能在什么场景下省掉一个额外的变量赋值步骤？

```python
data = [1, 2, 3, 4, 5]
result = [y for x in data if (y := x * 2) > 4]
print(result)
```

- 答案：

```text
[6, 8, 10]
```

`(y := x * 2)` 在判断条件 `> 4` 的同时，把算出来的 `x * 2` 赋值给 `y` 并且这个赋值表达式本身的值就是 `y`；后面的 `for` 输出直接复用这个 `y`，不用再重新计算一遍 `x * 2`。如果没有海象运算符，要么得写两次 `x * 2`（一次判断、一次输出），要么得写成更啰嗦的普通 `for` 循环加 `if` 加 `append`。这个语法在 while 循环读取数据（如 `while (line := f.readline()):`）这类场景里也很常用。
