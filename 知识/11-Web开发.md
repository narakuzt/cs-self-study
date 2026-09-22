# 11. Web 开发：核心概念清单与自测题库

对应主题页：[11. Web 开发](../课程/11-Web开发.md)。

## 说明

- 内容依据 [MDN Web 文档](https://developer.mozilla.org/zh-CN/)、[Node.js 官方文档](https://nodejs.org/docs/latest/api/)整理，覆盖 HTML 结构、CSS 基本规则、JavaScript 语言本身；HTTP 请求响应的细节已经在[主题 8](08-计算机网络.md)讲过，这里不重复。
- JavaScript 代码题用 `工具/校验题库.py` 通过 `node` 实际运行核对（Node.js v24），这是脱离浏览器也能验证 JS 语言行为的方式；HTML 结构用 Python 标准库的 `html.parser` 解析验证；CSS 涉及页面视觉效果（布局、颜色）的部分，脱离浏览器无法自动核对，这类概念以说明为主，不提供可运行代码。
- 使用方法：先看概念清单，逐条用自己的话解释；再做题库，先预测输出，再对照答案。做错的题进入复习队列。
- 题库共 16 题。题目由编者编写，若与你的课程或教材有出入，以 MDN 或语言规范为准。

## 覆盖范围之外

这份题库检查的是核心概念，不是这门课的全部内容。下面这些内容**没有**覆盖，做完本页题库不代表已经掌握它们，需要另外通过课程本身的作业和实验学习：

- CSS 布局系统的具体规则（Flexbox、Grid）
- 前端框架（React、Vue 等）
- 常见 Web 安全漏洞（XSS、CSRF）与防护
- 前端性能优化

## 概念清单

学完主题 11 后，下面每一条都应能用一两句话解释并举出例子。括号里是对应的题目。

### HTML

- HTML 用标签描述内容的结构和语义，不是描述外观（Q11-01）
- 标签可以嵌套，形成一棵树状结构（DOM 树的基础）（Q11-02）

### CSS

- 选择器的特殊性（specificity）决定多条冲突的样式规则哪条生效，ID 选择器比类选择器优先级更高（Q11-03）
- 盒模型：每个元素占的空间由内容、内边距、边框、外边距组成（Q11-04）

### JavaScript：变量与作用域

- `var` 是函数作用域，`let`/`const` 是块作用域（Q11-05）
- 闭包：函数能记住并访问它定义时所在的作用域，即使外层函数已经执行完毕（Q11-06）
- `this` 在普通函数和箭头函数里的绑定规则不同（Q11-07）

### JavaScript：类型与比较

- `==` 会做类型转换再比较，`===` 不转换类型、类型不同直接判不等（Q11-08）
- JSON 是一种基于 JavaScript 对象字面量语法的数据交换格式，`JSON.stringify`/`JSON.parse` 互为逆操作（Q11-09）

### JavaScript：异步

- JavaScript 是单线程的，用事件循环处理异步任务；`setTimeout(fn, 0)` 也要等当前同步代码跑完才执行（Q11-10）
- `Promise`/`async`/`await` 是对"异步操作完成后做什么"的结构化写法（Q11-11、Q11-12）

### JavaScript：常用语法

- 数组的 `map`、`filter`、`reduce` 分别做什么（Q11-13）
- 解构赋值与展开运算符（Q11-14）
- 模板字符串（Q11-15）

### 前后端交互（衔接主题 8）

- 浏览器发起的跨域请求受同源策略限制，服务器需要显式允许（CORS）才能被跨域访问（Q11-16）

## 自测题库

### Q11-01 HTML 描述结构，不描述外观

- 类型：代码题
- 出处：[Python 官方文档：html.parser](https://docs.python.org/zh-cn/3/library/html.parser.html)
- 问题：一段 HTML 里，标签本身能看出多少信息？

```python
from html.parser import HTMLParser

class TagCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)

parser = TagCollector()
parser.feed("<article><h1>标题</h1><p>正文内容</p></article>")
print(parser.tags)
```

- 答案：

```text
['article', 'h1', 'p']
```

`<h1>` 表示"这是一级标题"、`<p>` 表示"这是一个段落"、`<article>` 表示"这是一篇独立的文章内容"——HTML 标签描述的是内容各部分**是什么**（语义结构），不规定它们具体长什么样（字号多大、什么颜色）。外观交给 CSS 负责，这种"结构和外观分离"的设计，使同一份 HTML 换一套 CSS 就能呈现完全不同的视觉效果。

### Q11-02 标签嵌套形成树状结构

- 类型：代码题
- 出处：[Python 官方文档：html.parser](https://docs.python.org/zh-cn/3/library/html.parser.html)
- 问题：HTML 里标签可以嵌套，这种嵌套关系可以怎样表示？

```python
from html.parser import HTMLParser

class DepthTracker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.max_depth = 0

    def handle_starttag(self, tag, attrs):
        self.depth += 1
        self.max_depth = max(self.max_depth, self.depth)

    def handle_endtag(self, tag):
        self.depth -= 1

parser = DepthTracker()
parser.feed("<div><ul><li><span>项</span></li></ul></div>")
print(parser.max_depth)
```

- 答案：

```text
4
```

`<div>` 包着 `<ul>`，`<ul>` 包着 `<li>`，`<li>` 包着 `<span>`，形成 4 层嵌套。浏览器解析 HTML 后，会在内存里建立一棵对应的树（DOM 树），每个标签是树上的一个节点，父子关系对应嵌套关系。JavaScript 操作页面内容，本质上就是在操作这棵树。

### Q11-03 CSS 选择器的特殊性

- 类型：代码题
- 出处：[MDN：CSS 特殊性](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Specificity)
- 问题：一条用 ID 选择器写的规则，和一条用两个类选择器写的规则冲突时，哪条生效？

```python
def specificity(selector):
    ids = selector.count("#")
    classes = selector.count(".")
    return (ids, classes)

a = specificity("#main")
b = specificity(".box.highlight")
print(a, b, a > b)
```

- 答案：

```text
(1, 0) (0, 2) True
```

CSS 的特殊性按"ID 选择器数量、类选择器数量、标签选择器数量"依次比较（这里只演示前两级），ID 选择器的优先级高于任意数量的类选择器组合，即使类选择器数量更多。当多条规则都能匹配同一个元素、又设置了相同的属性时，特殊性更高的规则生效，这是排查"我明明写了样式，怎么不生效"这类问题的关键知识。

### Q11-04 盒模型

- 类型：概念题
- 出处：[MDN：CSS 盒模型](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_box_model/Introduction_to_the_CSS_box_model)
- 问题：一个设置了 `width: 100px` 的元素，它在页面上实际占据的宽度就是 100px 吗？
- 答案：

不一定。CSS 盒模型把每个元素的空间从内到外分成四层：内容（content）、内边距（padding）、边框（border）、外边距（margin）。默认的 `box-sizing: content-box` 下，`width` 只指定内容区域的宽度，实际占据的总宽度是 `width + 左右 padding + 左右 border`（外边距不算在"占据的空间"内，但会影响和相邻元素的间距）。如果设置了 `box-sizing: border-box`，`width` 就包含了 padding 和 border，这也是很多 CSS 重置样式表（reset）里第一件事就是把所有元素设成 `border-box` 的原因——它更符合"我设的宽度就是最终看到的宽度"这种直觉。

### Q11-05 `var` 与 `let` 的作用域

- 类型：易错点
- 出处：[MDN：let](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/let)
- 问题：花括号里用 `var` 和用 `let` 重新赋值同名变量，对外面的变量分别有什么影响？

```js
let a = 10;
{
  let a = 20;
}
console.log(a);

var b = 1;
{
  var b = 2;
}
console.log(b);
```

- 答案：

```text
10
2
```

`let` 是块级作用域：花括号里的 `let a` 是一个全新的、只在这对花括号内有效的变量，不会影响外面的 `a`，所以外面打印的还是 10。`var` 不认花括号这层作用域（只认函数作用域），花括号里的 `var b = 2` 操作的其实是外面同一个 `b`，所以外面打印的是被改过的 2。这个差异是很多 JS 新手困惑的来源，现代代码几乎都用 `let`/`const` 而不是 `var`。

### Q11-06 闭包

- 类型：代码题
- 出处：[MDN：闭包](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Closures)
- 问题：一个函数执行完之后，它内部的局部变量应该已经"消失"了；但下面这样写为什么还能记住状态？

```js
function makeCounter() {
  let count = 0;
  return function () {
    count += 1;
    return count;
  };
}

const counter = makeCounter();
console.log(counter(), counter(), counter());
```

- 答案：

```text
1 2 3
```

`makeCounter` 每次调用都返回一个新的内部函数，这个内部函数"记住"了它被创建时所在的作用域（包含变量 `count`），即使外层的 `makeCounter` 调用已经结束，`count` 也不会被回收，因为内部函数还在引用它——这就是闭包。每次调用 `counter()`，都在操作同一个被"记住"的 `count`，所以计数能持续累加，而不是每次都从 0 开始。

### Q11-07 `this` 在普通函数和箭头函数里不同

- 类型：代码题
- 出处：[MDN：箭头函数](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Functions/Arrow_functions)
- 问题：对象的方法用普通函数和箭头函数分别定义，`this` 指向一样吗？

```js
const obj = {
  value: 42,
  regular: function () {
    return this.value;
  },
};

console.log(obj.regular());
```

- 答案：

```text
42
```

普通函数（`function` 关键字定义）的 `this` 由**调用方式**决定：`obj.regular()` 这样调用时，`this` 指向 `.` 前面的 `obj`，所以能访问到 `obj.value`。箭头函数则不同：它没有自己的 `this`，而是直接使用定义它时外层作用域的 `this`（不随调用方式变化），这是箭头函数常被用在回调函数里的原因之一——不用担心 `this` 意外"变成别的东西"。

### Q11-08 `==` 与 `===`

- 类型：易错点
- 出处：[MDN：相等性判断](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Equality_comparisons_and_sameness)
- 问题：`1 == "1"` 和 `1 === "1"` 结果一样吗？

```js
console.log(1 == "1", 1 === "1");
console.log(null == undefined, null === undefined);
```

- 答案：

```text
true false
true false
```

`==`（宽松相等）在比较之前会先做类型转换，字符串 `"1"` 被转换成数字 `1` 再比较，所以 `1 == "1"` 是 `true`；`null == undefined` 也是一条被规范特别允许的宽松相等。`===`（严格相等）不做任何类型转换，类型不同直接判定为不相等，`1 === "1"` 因为一个是数字一个是字符串，直接是 `false`。`==` 的隐式类型转换规则历史上出过不少反直觉的例子，现代 JS 代码几乎总是推荐使用 `===`，只在明确需要类型转换语义时才用 `==`。

### Q11-09 JSON 与 JavaScript 对象互转

- 类型：代码题
- 出处：[MDN：JSON.stringify](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)、[JSON.parse](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse)
- 问题：把一个对象转成 JSON 字符串，再转回来，还是原来的对象吗？

```js
const obj = { name: "Alice", tags: ["a", "b"], active: true };
const text = JSON.stringify(obj);
const back = JSON.parse(text);
console.log(text);
console.log(back.name, back.tags.length, back.active);
```

- 答案：

```text
{"name":"Alice","tags":["a","b"],"active":true}
Alice 2 true
```

`JSON.stringify` 把 JavaScript 对象变成一段符合 JSON 格式的纯文本，`JSON.parse` 做相反的转换，重建出一个新对象，两个操作互为逆运算。JSON 是几乎所有 Web API 用来传输结构化数据的标准格式：前端发请求把数据 `stringify` 成文本发出去，后端收到后 `parse` 回对象来处理，反过来响应也是同样的过程——这也是[主题 8](08-计算机网络.md) Q08-14 里 `Content-Type: application/json` 的意义所在。

### Q11-10 事件循环：`setTimeout(fn, 0)` 不是立刻执行

- 类型：易错点
- 出处：[MDN：事件循环](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Execution_model)
- 问题：`setTimeout(fn, 0)` 里的延迟时间填 0，`fn` 会在下一行代码之前执行吗？

```js
console.log("1");
setTimeout(() => console.log("3"), 0);
console.log("2");
```

- 答案：

```text
1
2
3
```

JavaScript 是单线程的：同一时刻只能执行一段代码。`setTimeout` 不管延迟填多少，都不会打断当前正在执行的同步代码，而是把回调函数放进一个队列，等**当前所有同步代码都执行完**之后，由"事件循环"负责取出来执行。所以即使延迟是 0，`"3"` 也一定排在同步执行的 `"1"`、`"2"` 之后打印，这是很多"为什么我的回调没有按写的顺序执行"疑惑的根源。

### Q11-11 `Promise` 表示一个异步操作的结果

- 类型：代码题
- 出处：[MDN：Promise](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- 问题：`Promise` 解决了什么问题？

```js
function delay(value) {
  return new Promise((resolve) => {
    setTimeout(() => resolve(value), 0);
  });
}

delay("done").then((v) => console.log(v));
console.log("sync code first");
```

- 答案：

```text
sync code first
done
```

在 `Promise` 之前，异步操作的结果通常通过"回调函数"传递，多层异步操作嵌套容易写成难以阅读的"回调地狱"。`Promise` 把"一个异步操作最终会成功或失败"这件事包装成一个对象，用 `.then(...)` 注册"成功后要做什么"，代码结构更平、更好组合。这里 `delay(...)` 立刻返回一个 `Promise`（不会阻塞），所以同步的 `console.log("sync code first")` 先执行，异步的结果稍后通过 `.then` 处理，这和 Q11-10 的事件循环是同一套机制。

### Q11-12 `async`/`await` 是 `Promise` 的语法糖

- 类型：代码题
- 出处：[MDN：async function](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/async_function)
- 问题：`await` 会让代码"暂停"等待吗？会阻塞整个程序吗？

```js
async function main() {
  console.log("A");
  await Promise.resolve();
  console.log("B");
}

main();
console.log("C");
```

- 答案：

```text
A
C
B
```

`await` 只会"暂停"它所在的这个 `async` 函数往下执行，把控制权交还给外面，并不会阻塞整个 JavaScript 引擎——`main()` 执行到 `await` 那一行时先打印了 `A`，然后暂停，把控制权交还，于是外面的 `console.log("C")` 得以先执行；`await` 等到的结果就绪后，`main` 函数才恢复、继续打印 `B`。`async`/`await` 本质上是让基于 `Promise` 的异步代码写起来更像同步代码，但底层运行机制和 Q11-11 的 `.then` 是一致的。

### Q11-13 数组的 `map`、`filter`、`reduce`

- 类型：代码题
- 出处：[MDN：Array.prototype.map](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array/map)、[filter](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array/filter)、[reduce](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce)
- 问题：这三个数组方法分别做什么？

```js
const nums = [1, 2, 3, 4, 5];
console.log(JSON.stringify(nums.map((x) => x * 2)));
console.log(JSON.stringify(nums.filter((x) => x % 2 === 0)));
console.log(nums.reduce((acc, x) => acc + x, 0));
```

- 答案：

```text
[2,4,6,8,10]
[2,4]
15
```

`map` 把数组每一项按规则变换，得到一个同样长度的新数组（这里每个数乘 2）；`filter` 只保留满足条件的项，长度可能变短（这里只留偶数）；`reduce` 把整个数组"归约"成一个值（这里从初始值 0 开始累加求和）。这三个方法都不修改原数组，而是返回一个新的结果，这种"不改变原数据、返回新结果"的风格是函数式编程常见的写法。

### Q11-14 解构赋值与展开运算符

- 类型：代码题
- 出处：[MDN：解构赋值](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment)、[展开语法](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Spread_syntax)
- 问题：怎样从一个对象里快速取出某个字段（带默认值），怎样把两个数组合并成一个？

```js
const config = { host: "localhost" };
const { host, port = 8080 } = config;
console.log(host, port);

const merged = [...[1, 2], ...[3, 4]];
console.log(JSON.stringify(merged));
```

- 答案：

```text
localhost 8080
[1,2,3,4]
```

解构赋值 `const { host, port = 8080 } = config` 从对象里按字段名取值，字段不存在时用 `= 8080` 指定的默认值兜底（这里 `config` 没有 `port` 字段，所以用了默认值）。展开运算符 `...` 把一个数组"摊开"成它的各个元素，`[...a, ...b]` 就是把两个数组的元素依次放进一个新数组，比手写循环拼接更简洁。

### Q11-15 模板字符串

- 类型：代码题
- 出处：[MDN：模板字符串](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Template_literals)
- 问题：怎样在字符串里直接嵌入变量，而不用一堆 `+` 拼接？

```js
const name = "小明";
const age = 18;
const message = `${name} 今年 ${age} 岁，明年 ${age + 1} 岁`;
console.log(message);
```

- 答案：

```text
小明 今年 18 岁，明年 19 岁
```

反引号（`` ` ``）包起来的是模板字符串，`${表达式}` 里可以直接放任意 JavaScript 表达式，运行时会被替换成表达式的值并拼进字符串里，不需要像传统写法那样用一堆 `+` 号手动拼接字符串和变量。这和主题 2 的 Q02-30（Python 的 f-string）是同一类设计，只是语法不同。

### Q11-16 同源策略与 CORS

- 类型：概念题
- 出处：[MDN：同源策略](https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy)、[MDN：CORS](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Guides/CORS)
- 问题：网页 A 用 JavaScript 向另一个域名的服务器发请求，浏览器会怎样处理？
- 答案：

出于安全考虑，浏览器默认执行"同源策略"：一个网页的 JavaScript 代码，默认只能自由访问和它同源（协议、域名、端口都相同）的资源。如果网页 A 想用 `fetch` 访问一个不同源的服务器 B，浏览器仍然会发出这个请求，但会检查 B 的响应里有没有 `Access-Control-Allow-Origin` 这类响应头，明确表示"允许来自 A 的跨域访问"；如果没有，浏览器会阻止网页上的代码读取到这个响应（即使请求已经真的发到了服务器）。这套机制叫 CORS（跨域资源共享），是防止恶意网页偷偷用你已登录的身份去别的网站执行操作（比如转账）的重要防线，需要服务器端显式配置才能允许跨域访问。
