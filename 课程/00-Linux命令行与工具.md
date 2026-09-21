# 0. Linux 命令行与工具

| 项目 | 内容 |
|---|---|
| 先修要求 | 无 |
| 语言 | Shell（Bash） |
| 规模参考 | csdiy.wiki：Missing Semester 约 10 小时；OSSU：2 周，每周 12 小时 |

## 默认路径

按下面几步走，其余资源是可选的（编者建议）。

1. 读《快乐的 Linux 命令行》，边读边在真实终端里敲。
2. 上完主题 1 与主题 2 的入门部分后，学 Missing Semester（csdiy.wiki 约 10 小时）。
3. 对照「过关标准」自测。命令行的艺术、鸟哥、菜鸟教程是可选的速查。

## 为什么学

后面所有主题的实验都在终端里做：编译、调试、看进程、抓包、跑数据库。csdiy.wiki 把它放在"必学工具"里：熟练使用命令行会极大地提高灵活性和生产力。

## 课程与资源

> 说明：星级、学时、先修要求来自 csdiy.wiki 或 OSSU 的原文；"主力、进阶、备选"的划分、学习顺序是编者建议。

### 中文入门：《快乐的 Linux 命令行》

- [The Linux Command Line（作者网站，免费）](https://linuxcommand.org/tlcl.php)；中文版书名《快乐的 Linux 命令行》。
- 选择依据：编者选定；csdiy.wiki 与 OSSU 未收录，无难度学时数据。

### 中文补充

- [命令行的艺术（中文）](https://github.com/jlevy/the-art-of-command-line/blob/master/README-zh.md)：csdiy.wiki 推荐，GitHub 十万星的经典教程，不长，建议反复通读。
- [《鸟哥的 Linux 私房菜》](https://linux.vbird.org/)：工具书，以 CentOS 为主，Ubuntu 用户把 `yum` 换成 `apt`。
- [菜鸟教程 Linux 命令大全](https://www.runoob.com/linux/linux-command-manual.html)：速查。

### 系统课程：The Missing Semester of Your CS Education（MIT）

| 项目 | csdiy.wiki 数据 | OSSU 数据 |
|---|---|---|
| 先修要求 | 无 | 无 |
| 难度 / 时长 | 2 星，10 小时 | 2 周，每周 12 小时 |
| 作业 | 随堂小练习，见课程网站 | — |

- [课程网站](https://missing.csail.mit.edu/)；视频在 YouTube（[IAP 2026 播放列表](https://www.youtube.com/playlist?list=PLyzOVJj3bHQunmnnTXrNbZnBaCA-ieK4L)），YouTube 通常提供自动翻译字幕（该播放列表的字幕情况未核实）。
- 2026 版共 9 讲：Shell、命令行环境、开发环境、调试与性能分析、版本控制与 Git、打包与发布、Agentic Coding、Beyond the Code、代码质量。
- csdiy.wiki 提醒：课程里会不时提到与开发流程相关的术语，建议至少学完计算机导论级别的课程再学。

## 学习顺序（编者建议）

1. 先读《快乐的 Linux 命令行》，边读边在真实终端敲。
2. 完成 [1. 计算机整体直觉](01-计算机整体直觉.md) 与 [2. Python 基础](02-Python基础.md) 的入门部分后，再上 Missing Semester。
3. 遇到不会的命令，先 `man 命令`，再查速查手册。

## 过关标准

- **0.1** 完成 Missing Semester 各讲的随堂练习
- **0.2** 自检：用 `find`、`grep`、管道组合，找出目录树中所有含指定字符串的文件并统计行数
- **0.3** 自检：写一个 Bash 脚本，接收目录参数，输出体积最大的 5 个文件，并处理参数缺失
- **0.4** 自检：解释 `chmod 754`；说明脚本要能被执行需要哪两个条件（执行权限与 shebang）

## 来源与核实

- 课程数据引自 csdiy.wiki 与 OSSU README 原文（均 MIT 许可证）。
- 2026-09-22 逐项核对：本页链接均已打开；B 站链接通过 B 站公开接口核对标题与集数，YouTube 链接通过 oEmbed 核对标题，慕课链接通过页面标题核对课程名。
