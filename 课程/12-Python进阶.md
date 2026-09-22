# 12. Python 进阶

| 项目 | 内容 |
|---|---|
| 先修要求 | [2. Python 基础](02-Python基础.md)、[5. 数据结构与算法](05-数据结构与算法.md)；并发部分需 [7. 操作系统](07-操作系统.md)（均为编者建议） |
| 语言 | Python 3 |
| 规模参考 | csdiy.wiki：CS61A 约 50 小时；书籍无数据 |

## 默认路径

按下面几步走，其余资源是可选的（编者建议）。

1. 按序读《流畅的 Python》，配合官方中文文档与 pytest。
2. 学完 7 后回头学并发部分。
3. CS61A 是挑战项目；完成「过关标准」。

## 为什么学

基础阶段学的是"能写"；进阶阶段学的是"写得好、看得懂别人的、知道为什么这样设计"。装饰器、生成器、上下文管理器、类型标注、并发，都是读真实项目代码的必备。

## 课程与资源

> 说明：星级、学时、先修要求来自 csdiy.wiki 或 OSSU 的原文；"主力、进阶、备选"的划分、学习顺序是编者建议。

### 主力：书籍

- 《流畅的 Python》（Fluent Python，书）：数据模型、函数、面向对象、并发。
- 《Effective Python》（书）：具体写法建议，按条读。
- 选择依据：编者选定的参考书单；csdiy.wiki 与 OSSU 未收录，无数据。

### 官方文档

- [Python 官方文档（简体中文）](https://docs.python.org/zh-cn/3/)、[PEP 8 代码风格](https://peps.python.org/pep-0008/)、[pytest 文档](https://docs.pytest.org/)。

### 进阶课程

| 课程 | csdiy.wiki 数据 |
|---|---|
| [UC Berkeley CS61A](https://cs61a.org) | 3 星，50 小时，先修无；Python、Scheme、SQL；共 4 个 Project（2026 秋具体为 Hog、Typing Software、Ants vs SomeBees、Animator，历年会调整）；讲抽象、函数式编程、数据抽象、面向对象；csdiy.wiki 页标题为 Structure and Interpretation of Computer Programs（csdiy.wiki 提到的"用 Python 实现 Scheme 解释器"是往年的 Project 内容，已随课程更新不再是当前内容）；teachyourselfcs 推荐 SICP（书）配合 Brian Harvey 讲的 CS61A 视频 |

## 学习顺序（编者建议）

1. 数据模型（特殊方法）、函数作为对象、装饰器与闭包。
2. 迭代器、生成器、上下文管理器，做[知识层](../知识/12-Python进阶.md)的自测题库。
3. 类型标注与测试（pytest）。
4. 并发：线程、进程、`asyncio`，回到 [7. 操作系统](07-操作系统.md) 对照理解。
5. 挑战：CS61A 的项目。

## 过关标准

- **12.1** 自检：手写一个带参数的装饰器，并说明闭包如何保存状态
- **12.2** 自检：用生成器处理大文件，内存占用保持恒定
- **12.3** 自检：给项目写 20 条以上 `pytest` 用例，含参数化与夹具
- **12.4** （进阶）完成 CS61A 的全部官方 Project（2026 秋共 4 个，具体题目会随学期调整，以当时官网为准）
- **12.5** 闭卷做完[知识层](../知识/12-Python进阶.md)的 18 道自测题，做错的加入复习队列，一周后复测

## 来源与核实

- CS61A 数据引自 csdiy.wiki 原文（MIT 许可证）；Project 数量与名称取自 2026 秋官网当前页面（随学期会变化）。
- 2026-09-22 逐项核对：本页链接均已打开；B 站链接通过 B 站公开接口核对标题与集数，YouTube 链接通过 oEmbed 核对标题，慕课链接通过页面标题核对课程名。
