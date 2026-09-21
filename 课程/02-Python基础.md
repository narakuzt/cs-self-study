# 2. Python 基础

| 项目 | 内容 |
|---|---|
| 先修要求 | 无（csdiy.wiki 与 OSSU 的入门课均无先修；OSSU 要求高中代数） |
| 语言 | Python 3 |
| 规模参考 | csdiy.wiki：CS50P 30-40 小时；OSSU：Intro CS（即 MIT 6.100L）14 周，每周 6-10 小时 |

## 为什么学

第一门语言，承担两个任务：学会把想法写成程序，并为后面的「数据结构与算法」提供实现语言。

## 课程与资源

> 说明：星级、学时、先修要求来自 csdiy.wiki 或 OSSU 的原文；"主力、进阶、备选"的划分、学习顺序是编者建议。

### 主力：《Python 编程：从入门到实践》第 3 版

- [配套资源网站](https://ehmatthes.github.io/pcc_3e/)：含代码与习题指引。前半本讲基础，后半本是完整项目（数量与内容以书的目录为准）。
- 选择依据：编者选定。csdiy.wiki 与 OSSU 未收录，无课程数据。

### 配套课程（三选一，与书同步）

| 课程 | csdiy.wiki 数据 | 备注 |
|---|---|---|
| [CS50P（哈佛）](https://cs50.harvard.edu/python/2022/) | 2 星，30-40 小时，先修无；[B 站视频](https://www.bilibili.com/video/BV1z5411X7wX) | 共 10 周（第 0-9 周）：函数与变量、条件、循环、异常、库、单元测试、文件读写、正则、面向对象、杂项；有每周习题与期末项目；可用 `check50` 自动检查 |
| MIT 6.100L | 2 星，50 小时以上，先修无；[课程网站](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/pages/material-by-lecture/) | csdiy.wiki：总体难度平滑，适合小白循序渐进；26 节课 |
| CS61A（UC Berkeley） | 3 星，50 小时，先修无；[课程网站](https://cs61a.org) | csdiy.wiki 提醒：完全没有编程基础直接上手需要学习能力和自律；为避免挫折，可以先选 CS10 或 CS50 |

OSSU 选的入门课就是上表的 MIT 6.100L（《Introduction to Computer Science and Programming using Python》），14 周，每周 6-10 小时，先修高中代数。OSSU 目前把它标为"审查中"：设计上面向零基础，但如果觉得难跟，可以先做 OSSU 列出的更基础的编程入门课再回来。csdiy.wiki 给该课的学时是 50 小时以上，与 OSSU 的周数估算相差较大。

## 学习顺序（编者建议）

1. 主力书前半与所选配套课程同步（以 CS50P 为例：前 4 周）：书讲原理，课程出题练手。
2. 书里"动手试一试"必做，不跳过。
3. 学完基础后做书后半的项目，或自选一个小的命令行工具作综合练习。
4. 进程、线程、GIL 这类系统概念放到 [7. 操作系统](07-操作系统.md) 之后学。

## 过关标准

- [ ] CS50P：通过全部问题集（`check50`），并提交期末项目
- [ ] 书后半的项目完成其中一个
- [ ] 自检：不看资料，用循环与字典统计一段文本的词频并排序输出
- [ ] 自检：用 `try/except` 处理文件不存在和格式错误

## 来源与核实

- 课程数据引自 csdiy.wiki 与 OSSU README 原文（均 MIT 许可证）；CS50P 周主题取自其官网。
- 2026-09-22 逐项核对：本页链接均已打开；B 站链接通过 B 站公开接口核对标题与集数，YouTube 链接通过 oEmbed 核对标题，慕课链接通过页面标题核对课程名。
