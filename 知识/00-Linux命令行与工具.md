# 0. Linux 命令行与工具：核心概念清单与自测题库

对应主题页：[0. Linux 命令行与工具](../课程/00-Linux命令行与工具.md)。

## 说明

- 内容依据 [Bash 参考手册](https://www.gnu.org/software/bash/manual/bash.html)、[GNU Coreutils 手册](https://www.gnu.org/software/coreutils/manual/)、[GNU grep 手册](https://www.gnu.org/software/grep/manual/grep.html)、[find(1) 手册页](https://manpages.debian.org/bookworm/findutils/find.1.en.html)整理，每道题标注出处；命令行入门的整体脉络可对照 [Missing Semester 第 1 讲：Shell](https://missing.csail.mit.edu/2026/course-shell/)。
- 每道命令题的"答案"输出，用 `工具/校验题库.py` 在一个全新的空临时目录里实际运行核对，环境为 GNU bash 5.2.21、Ubuntu 24.04、语言环境 `C`。macOS 等使用 BSD 工具的系统，个别选项与输出可能不同。
- 使用方法：先看概念清单，逐条用自己的话解释；再做题库，先预测输出，再对照答案。做错的题进入复习队列。
- 题库共 34 题。题目由编者编写，若与你的教材或课程有出入，以官方手册为准。运行题目时请在一个空的测试目录里，不要在重要目录里试。

## 覆盖范围之外

这份题库检查的是核心概念，不是这门课的全部内容。下面这些内容**没有**覆盖，做完本页题库不代表已经掌握它们，需要另外通过课程本身的作业和实验学习：

- 更复杂的 Shell 编程：数组、`trap` 信号处理、脚本的模块化组织
- 系统服务管理（如 systemd）、日志系统（journalctl）
- 性能诊断工具（`strace`、`perf`、`lsof`）

## 概念清单

学完主题 0 后，下面每一条都应能用一两句话解释并举出例子。括号里是对应的题目。

### 命令与引用

- 命令、选项与参数；shell 按空白切分参数，引号可以把带空格的内容合成一个参数（Q00-01、Q00-30）
- 单引号原样保留，双引号允许变量和命令替换展开（Q00-02）
- 变量的读取与 `${变量}` 写法；给变量赋值时等号两边不能有空格（Q00-03）
- 怎么查帮助：`--help`、`type`（Q00-09）

### 退出状态与命令连接

- 退出状态：0 表示成功，非 0 表示失败；`$?` 取上一条命令的状态（Q00-04）
- `&&`、`||` 按退出状态决定是否执行下一条（Q00-05）

### 文件系统与文件操作

- 绝对路径与相对路径，`.`、`..`、`cd -`（Q00-06）
- 通配符 `*`、`?`、`[...]`；没有匹配时通配符保持原样（Q00-07）
- 隐藏文件与 `ls -a`（Q00-08）
- `cp -r`、`mv`、`rm -r`（Q00-20）

### 重定向与管道

- `>` 覆盖、`>>` 追加（Q00-10）
- 标准输出、标准错误的分别重定向，以及 `2>&1`（Q00-11）
- 管道把前一个命令的输出交给后一个命令（Q00-12）

### 文本处理

- `head`、`tail`、`wc`、`seq`（Q00-13）
- `sort` 默认按字典序，数字要用 `-n`（Q00-14）
- `cut`、`tr`（Q00-15）
- `grep` 的常用选项：`-i`、`-c`、`-v`、`-n`、`-r`、`-l`、`--include`（Q00-16、Q00-17）
- `find` 按名字和类型查找，配合 `-exec` 处理结果（Q00-18、Q00-19）

### 权限与脚本

- 权限位 `rwx` 与数字表示法，`chmod` 的数字与符号写法（Q00-21）
- 直接执行脚本需要执行权限；shebang 指定解释器（Q00-22、Q00-23）
- 脚本参数 `$#`、`$1`、`"$@"`（Q00-28）
- `if` 与 `[ ]` 测试（Q00-29）
- 变量为空或含空格时的风险，以及防范方法（Q00-30、Q00-34）

### 环境与进程

- `PATH` 决定命令去哪里找（Q00-24）
- 环境变量要 `export` 才会传给子进程（Q00-25）
- 命令替换、算术展开、花括号展开（Q00-26、Q00-27）
- 后台任务、`wait`、`kill` 与退出码（Q00-31、Q00-32）
- 启动文件与 `source`（Q00-33）

## 自测题库

### Q00-01 命令的参数怎么切分

- 类型：概念题
- 出处：[Bash 手册 3.5.7 单词拆分](https://www.gnu.org/software/bash/manual/bash.html#Word-Splitting)、[3.1.2 引用](https://www.gnu.org/software/bash/manual/bash.html#Quoting)
- 问题：下面的命令给 `printf` 传了几个参数？打印什么？

```bash
printf '[%s]\n' one two "three four"
```

- 答案：

```text
[one]
[two]
[three four]
```

shell 按空白把命令行切成词。`one`、`two` 各是一个参数，双引号把 `three four` 合成一个参数，所以 `printf` 的格式字符串对每个参数重复一次。

### Q00-02 单引号与双引号

- 类型：易错点
- 出处：[Bash 手册 3.1.2.2 单引号](https://www.gnu.org/software/bash/manual/bash.html#Single-Quotes)、[3.1.2.3 双引号](https://www.gnu.org/software/bash/manual/bash.html#Double-Quotes)
- 问题：下面三行分别打印什么？

```bash
name=Linux
echo "hi $name"
echo 'hi $name'
echo "today is $(echo Monday)"
```

- 答案：

```text
hi Linux
hi $name
today is Monday
```

单引号里的内容原样保留；双引号里 `$变量` 和 `$(命令)` 仍会展开。

### Q00-03 变量的读取与花括号

- 类型：代码题
- 出处：[Bash 手册 3.4 Shell 参数](https://www.gnu.org/software/bash/manual/bash.html#Shell-Parameters)
- 问题：下面打印什么？为什么第三个是空的？

```bash
x=5
echo "[$x] [${x}0] [$x0]"
```

- 答案：

```text
[5] [50] []
```

`$x0` 会被当成一个名叫 `x0` 的变量，它没有定义，展开为空。需要紧跟其他字符时，用 `${x}` 明确变量名的边界。赋值时等号两边不能有空格，`x = 5` 会被当成运行名为 `x` 的命令。

### Q00-04 退出状态

- 类型：概念题
- 出处：[Bash 手册 3.7.5 退出状态](https://www.gnu.org/software/bash/manual/bash.html#Exit-Status)
- 问题：下面三个 `$?` 分别是多少？

```bash
true; echo $?
false; echo $?
ls /nonexistent_dir_xyz 2>/dev/null; echo $?
```

- 答案：

```text
0
1
2
```

命令成功退出状态为 0，失败为非 0；不同命令用不同的非 0 值表示不同的错误，GNU `ls` 找不到文件时返回 2。`$?` 保存的是上一条命令的退出状态。

### Q00-05 `&&` 与 `||`

- 类型：代码题
- 出处：[Bash 手册 3.2.4 命令列表](https://www.gnu.org/software/bash/manual/bash.html#Lists)
- 问题：下面打印什么？

```bash
true && echo A
false && echo B
false || echo C
true || echo D
echo done
```

- 答案：

```text
A
C
done
```

`a && b`：a 成功才执行 b；`a || b`：a 失败才执行 b。

### Q00-06 绝对路径、相对路径与 `cd -`

- 类型：代码题
- 出处：[Bash 手册 4.1 Bourne Shell 内建命令（cd）](https://www.gnu.org/software/bash/manual/bash.html#Bourne-Shell-Builtins)
- 问题：下面每次 `basename "$PWD"` 打印什么？

```bash
mkdir -p a/b
cd a/b
basename "$PWD"
cd ..
basename "$PWD"
cd - >/dev/null
basename "$PWD"
```

- 答案：

```text
b
a
b
```

`cd a/b` 是相对路径；`cd ..` 回到上一级；`cd -` 回到上一次所在的目录。以 `/` 开头的是绝对路径，从根目录算起。

### Q00-07 通配符

- 类型：易错点
- 出处：[Bash 手册 3.5.8 文件名展开](https://www.gnu.org/software/bash/manual/bash.html#Filename-Expansion)
- 问题：下面四行分别打印什么？注意最后一行。

```bash
touch a1.txt a2.txt b1.txt notes.md
echo *.txt
echo a?.txt
echo [ab]1.txt
echo *.jpg
```

- 答案：

```text
a1.txt a2.txt b1.txt
a1.txt a2.txt
a1.txt b1.txt
*.jpg
```

`*` 匹配任意多个字符，`?` 匹配一个字符，`[ab]` 匹配方括号里的任一字符。展开由 shell 完成，命令拿到的是展开后的文件名。没有任何文件匹配时，通配符保持原样，不会变成空。

### Q00-08 隐藏文件

- 类型：代码题
- 出处：[GNU Coreutils：ls 命令](https://www.gnu.org/software/coreutils/manual/html_node/ls-invocation.html)
- 问题：`ls` 与 `ls -a` 的区别是什么？

```bash
touch .hidden visible
ls
echo ---
ls -a
```

- 答案：

```text
visible
---
.
..
.hidden
visible
```

以 `.` 开头的文件是隐藏文件，`ls` 默认不显示，`-a` 显示全部，包括代表当前目录的 `.` 和上一级目录的 `..`。

### Q00-09 怎么查帮助

- 类型：概念题
- 出处：[Bash 手册 4.2 Bash 内建命令（type）](https://www.gnu.org/software/bash/manual/bash.html#Bash-Builtins)
- 问题：遇到不认识的命令，怎么查它的用法？`type -t` 能告诉你什么？

```bash
ls --help | head -1
type -t cd
type -t ls
type -t if
```

- 答案：

```text
Usage: ls [OPTION]... [FILE]...
builtin
file
keyword
```

多数 GNU 命令支持 `--help`，也可以用 `man 命令` 查手册页。`type -t` 说明一个名字是什么：`builtin` 是 shell 内建命令，`file` 是磁盘上的可执行文件，`keyword` 是 shell 关键字。

### Q00-10 覆盖与追加

- 类型：代码题
- 出处：[Bash 手册 3.6.2 重定向输出](https://www.gnu.org/software/bash/manual/bash.html#Redirecting-Output)、[3.6.3 追加重定向输出](https://www.gnu.org/software/bash/manual/bash.html#Appending-Redirected-Output)
- 问题：下面两次 `cat` 分别打印什么？

```bash
echo one > f.txt
echo two > f.txt
cat f.txt
echo three >> f.txt
cat f.txt
```

- 答案：

```text
two
two
three
```

`>` 会先清空文件再写入，所以 `one` 被覆盖；`>>` 追加到末尾。

### Q00-11 标准输出与标准错误

- 类型：代码题
- 出处：[Bash 手册 3.6 重定向](https://www.gnu.org/software/bash/manual/bash.html#Redirections)
- 问题：下面三行分别打印什么？

```bash
ls nonexistent_xyz > out.txt 2> err.txt
echo "out: $(wc -c < out.txt)"
echo "err lines: $(wc -l < err.txt)"
ls nonexistent_xyz > both.txt 2>&1
wc -l < both.txt
```

- 答案：

```text
out: 0
err lines: 1
1
```

程序有两个输出通道：标准输出（编号 1）和标准错误（编号 2）。`>` 只重定向标准输出，`2>` 重定向标准错误；`2>&1` 让标准错误跟随标准输出，一起写进同一个文件。

### Q00-12 管道统计词频

- 类型：代码题
- 出处：[Bash 手册 3.2.3 管道](https://www.gnu.org/software/bash/manual/bash.html#Pipelines)、[Coreutils：uniq 命令](https://www.gnu.org/software/coreutils/manual/html_node/uniq-invocation.html)
- 问题：下面的命令统计了什么？打印什么？

```bash
printf 'b\na\nb\nc\na\nb\n' | sort | uniq -c | sort -rn | awk '{print $2, $1}'
```

- 答案：

```text
b 3
a 2
c 1
```

先 `sort` 让相同的行相邻，`uniq -c` 统计相邻重复的次数，再按次数从大到小排序，最后 `awk` 把两列换个顺序输出。`uniq` 只处理相邻的重复行，所以前面必须先排序。

### Q00-13 `head`、`tail`、`wc`、`seq`

- 类型：代码题
- 出处：[Coreutils：head 命令](https://www.gnu.org/software/coreutils/manual/html_node/head-invocation.html)、[tail 命令](https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html)、[wc 命令](https://www.gnu.org/software/coreutils/manual/html_node/wc-invocation.html)
- 问题：下面打印什么？

```bash
seq 1 10 > n.txt
head -n 3 n.txt
tail -n 2 n.txt
wc -l < n.txt
```

- 答案：

```text
1
2
3
9
10
10
```

`seq 1 10` 生成 1 到 10；`head -n 3` 取前 3 行，`tail -n 2` 取后 2 行，`wc -l` 数行数。

### Q00-14 `sort` 默认按字典序

- 类型：易错点
- 出处：[Coreutils：sort 命令](https://www.gnu.org/software/coreutils/manual/html_node/sort-invocation.html)
- 问题：下面两条命令分别输出什么顺序？

```bash
printf '10\n9\n100\n' | sort
echo ---
printf '10\n9\n100\n' | sort -n
```

- 答案：

```text
10
100
9
---
9
10
100
```

`sort` 默认逐字符比较，`"10"` 在 `"9"` 前面，因为 `"1"` 小于 `"9"`。按数值排序要加 `-n`。

### Q00-15 `cut` 与 `tr`

- 类型：代码题
- 出处：[Coreutils：cut 命令](https://www.gnu.org/software/coreutils/manual/html_node/cut-invocation.html)、[tr 命令](https://www.gnu.org/software/coreutils/manual/html_node/tr-invocation.html)
- 问题：下面打印什么？

```bash
printf 'alice:30\nbob:5\ncarol:100\n' | cut -d: -f2 | sort -n
printf 'alice:30\nbob:5\ncarol:100\n' | sort -t: -k2 -n | tail -1
printf 'Hello' | tr 'a-z' 'A-Z'; echo
```

- 答案：

```text
5
30
100
carol:100
HELLO
```

`cut -d: -f2` 以冒号为分隔符取第 2 列；`sort -t: -k2 -n` 按第 2 列数值排序，`tail -1` 取最大的一行；`tr` 逐字符替换，这里把小写变大写。

### Q00-16 `grep` 的常用选项

- 类型：代码题
- 出处：[GNU grep 手册](https://www.gnu.org/software/grep/manual/grep.html)
- 问题：下面四条命令分别打印什么？

```bash
printf 'Apple\nbanana\napple pie\ncherry\n' > f.txt
grep -i apple f.txt
grep -c a f.txt
grep -v a f.txt
grep -n cherry f.txt
```

- 答案：

```text
Apple
apple pie
2
Apple
cherry
4:cherry
```

`-i` 忽略大小写；`-c` 只输出匹配的行数（含小写 a 的行是 `banana` 与 `apple pie`，共 2 行）；`-v` 反选，输出不含 a 的行；`-n` 在行首显示行号。

### Q00-17 递归搜索

- 类型：代码题
- 出处：[GNU grep 手册](https://www.gnu.org/software/grep/manual/grep.html)
- 问题：下面两条命令分别打印什么？

```bash
mkdir -p src
echo 'TODO: fix' > src/a.py
echo 'done' > src/b.py
echo 'TODO: docs' > src/c.txt
grep -rl TODO src | sort
echo ---
grep -rl TODO --include='*.py' src
```

- 答案：

```text
src/a.py
src/c.txt
---
src/a.py
```

`-r` 递归搜索目录，`-l` 只列出含有匹配的文件名，`--include` 限定只搜索名字匹配的文件。

### Q00-18 `find` 按名字和类型

- 类型：代码题
- 出处：[find(1) 手册页](https://manpages.debian.org/bookworm/findutils/find.1.en.html)
- 问题：下面两条命令分别打印什么？

```bash
mkdir -p d/sub
touch d/a.py d/b.txt d/sub/c.py
find d -name '*.py' | sort
echo ---
find d -type d | sort
```

- 答案：

```text
d/a.py
d/sub/c.py
---
d
d/sub
```

`find 目录 条件` 递归遍历目录。`-name '*.py'` 按文件名匹配（通配符要加引号，避免被 shell 提前展开），`-type d` 只找目录。

### Q00-19 `find` 配合 `-exec` 统计行数

- 类型：代码题
- 出处：[find(1) 手册页](https://manpages.debian.org/bookworm/findutils/find.1.en.html)
- 问题：怎样统计一个目录树里所有 `.py` 文件的总行数？

```bash
mkdir -p d
printf '1\n2\n' > d/a.py
printf '1\n2\n3\n' > d/b.py
find d -name '*.py' -exec cat {} + | wc -l
```

- 答案：

```text
5
```

`-exec 命令 {} +` 把找到的所有文件一次性交给命令，这里 `cat` 把它们连在一起输出，`wc -l` 统计总行数。

### Q00-20 复制、移动与删除目录

- 类型：代码题
- 出处：[Coreutils：cp 命令](https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html)
- 问题：下面打印什么？

```bash
mkdir -p a/x
echo hi > a/x/f
cp -r a b
mv b/x b/y
find b | sort
rm -r a b
ls | wc -l
```

- 答案：

```text
b
b/y
b/y/f
0
```

`cp -r` 递归复制目录；`mv` 既能移动也能改名；`rm -r` 递归删除。删除操作无法撤销，使用 `rm -r` 前先确认路径。

### Q00-21 权限的数字与符号写法

- 类型：代码题
- 出处：[Coreutils：chmod 命令](https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html)、[stat 命令](https://www.gnu.org/software/coreutils/manual/html_node/stat-invocation.html)
- 问题：`chmod 754` 之后文件的权限是什么？再执行 `chmod u-x,g=r,o-r` 后呢？

```bash
touch f
chmod 754 f
stat -c '%a %A' f
chmod u-x,g=r,o-r f
stat -c '%a %A' f
```

- 答案：

```text
754 -rwxr-xr--
640 -rw-r-----
```

权限分为所有者（u）、所属组（g）、其他人（o）三组，每组有读 r=4、写 w=2、执行 x=1。754 就是 7（rwx）、5（r-x）、4（r--）。符号写法 `u-x` 去掉所有者的执行位，`g=r` 把组权限设为只读，`o-r` 去掉其他人的读权限。

### Q00-22 直接执行脚本需要执行权限

- 类型：概念题
- 出处：[Bash 手册 3.7.2 命令查找与执行](https://www.gnu.org/software/bash/manual/bash.html#Command-Search-and-Execution)
- 问题：下面每一步的结果是什么？

```bash
printf '#!/bin/sh\necho hi\n' > s.sh
./s.sh 2>/dev/null; echo "exit=$?"
chmod +x s.sh
./s.sh
sh s.sh
```

- 答案：

```text
exit=126
hi
hi
```

刚创建的文件没有执行权限，直接执行会失败，退出状态是 126（找到了但无法执行）。`chmod +x` 之后可以直接执行；用 `sh s.sh` 把它当作参数交给解释器则不需要执行权限，因为读文件即可。

### Q00-23 shebang 的作用

- 类型：易错点
- 出处：[Bash 手册 3.7.2 命令查找与执行](https://www.gnu.org/software/bash/manual/bash.html#Command-Search-and-Execution)
- 问题：没有 shebang（第一行的 `#!`）的脚本，加了执行权限后能直接运行吗？那还要不要写 shebang？

```bash
printf 'echo no-shebang\n' > t.sh
chmod +x t.sh
./t.sh
```

- 答案：

```text
no-shebang
```

在 bash 里可以运行：手册说明，执行因"文件不是可执行格式"而失败时，shell 会把它当作 shell 脚本来执行。但这依赖运行它的程序有这种回退行为，而且不指明用哪种 shell。写上 shebang（如 `#!/bin/bash`）能明确指定解释器，从其他程序调用时也更可靠，所以仍然建议写。

### Q00-24 `PATH` 决定去哪里找命令

- 类型：易错点
- 出处：[Bash 手册 3.7.2 命令查找与执行](https://www.gnu.org/software/bash/manual/bash.html#Command-Search-and-Execution)
- 问题：下面每一步的结果是什么？

```bash
mkdir bin
printf '#!/bin/sh\necho mytool\n' > bin/mytool
chmod +x bin/mytool
mytool 2>/dev/null; echo "exit=$?"
PATH="$PWD/bin:$PATH"
mytool
```

- 答案：

```text
exit=127
mytool
```

输入不带路径的命令名时，shell 依次在 `PATH` 列出的目录里查找。找不到时退出状态是 127。把目录加到 `PATH` 前面之后就能找到。永久生效需要写进启动文件（见 Q00-33）。

### Q00-25 环境变量与子进程

- 类型：易错点
- 出处：[Bash 手册 3.7.4 环境](https://www.gnu.org/software/bash/manual/bash.html#Environment)
- 问题：下面两次子 shell 打印什么？

```bash
x=1
bash -c 'echo "[$x]"'
export x
bash -c 'echo "[$x]"'
```

- 答案：

```text
[]
[1]
```

普通变量只在当前 shell 里有效；`export` 把变量放进环境，之后启动的子进程才能读到它。

### Q00-26 命令替换与算术展开

- 类型：代码题
- 出处：[Bash 手册 3.5.4 命令替换](https://www.gnu.org/software/bash/manual/bash.html#Command-Substitution)、[3.5.5 算术展开](https://www.gnu.org/software/bash/manual/bash.html#Arithmetic-Expansion)
- 问题：下面三行打印什么？

```bash
echo "files: $(ls | wc -l)"
touch a b c
echo "files: $(ls | wc -l)"
echo $((3 + 4 * 2))
```

- 答案：

```text
files: 0
files: 3
11
```

`$(命令)` 用命令的输出替换自己；`$((表达式))` 做整数算术，乘法优先于加法。

### Q00-27 花括号展开与 `for`

- 类型：代码题
- 出处：[Bash 手册 3.5.1 花括号展开](https://www.gnu.org/software/bash/manual/bash.html#Brace-Expansion)、[3.2.5.1 循环结构](https://www.gnu.org/software/bash/manual/bash.html#Looping-Constructs)
- 问题：下面打印什么？

```bash
for i in {1..3}; do echo "n$i"; done
echo file{A,B}.txt
```

- 答案：

```text
n1
n2
n3
fileA.txt fileB.txt
```

`{1..3}` 展开成 1 2 3，`file{A,B}.txt` 展开成两个词。花括号展开发生在其他展开之前，由 shell 完成，与文件是否存在无关。

### Q00-28 脚本参数

- 类型：代码题
- 出处：[Bash 手册 3.4.2 特殊参数](https://www.gnu.org/software/bash/manual/bash.html#Special-Parameters)
- 问题：运行 `bash args.sh x "y z"`，脚本打印什么？

```bash
cat > args.sh <<'EOF'
echo "count=$#"
echo "first=$1"
for a in "$@"; do echo "arg: $a"; done
EOF
bash args.sh x "y z"
```

- 答案：

```text
count=2
first=x
arg: x
arg: y z
```

`$#` 是参数个数，`$1` 是第一个参数，`"$@"` 把每个参数各自保留为一个词（带空格的参数不会被拆开）。

### Q00-29 `if` 与 `[ ]`

- 类型：代码题
- 出处：[Bash 手册 3.2.5.2 条件结构](https://www.gnu.org/software/bash/manual/bash.html#Conditional-Constructs)、[6.4 Bash 条件表达式](https://www.gnu.org/software/bash/manual/bash.html#Bash-Conditional-Expressions)
- 问题：下面打印什么？

```bash
n=7
if [ "$n" -gt 5 ]; then echo big; else echo small; fi
s=abc
if [ "$s" = "abc" ]; then echo same; fi
[ -f nofile ] && echo exists || echo missing
```

- 答案：

```text
big
same
missing
```

`[ ]` 是测试命令，成功返回 0。数值比较用 `-gt`、`-lt`、`-eq`，字符串比较用 `=`，`-f` 判断是不是普通文件。方括号与内容之间必须有空格。

### Q00-30 含空格的变量必须加引号

- 类型：易错点
- 出处：[Bash 手册 3.5.7 单词拆分](https://www.gnu.org/software/bash/manual/bash.html#Word-Splitting)
- 问题：文件名是 `my file.txt`，下面每一步的结果是什么？

```bash
f="my file.txt"
touch "$f"
ls -1
rm $f 2>&1 | wc -l
rm "$f"
ls -1 | wc -l
```

- 答案：

```text
my file.txt
2
0
```

变量不加引号展开时会按空白被拆成两个词，`rm $f` 变成 `rm my file.txt`，去找名为 `my` 和 `file.txt` 的两个文件，各报一次错，共 2 行。加上双引号 `"$f"` 才是一个整体。使用变量时养成加双引号的习惯。

### Q00-31 后台任务与 `wait`

- 类型：代码题
- 出处：[Bash 手册 3.2.4 命令列表（后台执行）](https://www.gnu.org/software/bash/manual/bash.html#Lists)、[7.1 作业控制基础](https://www.gnu.org/software/bash/manual/bash.html#Job-Control-Basics)
- 问题：下面打印什么？`wait` 起什么作用？

```bash
sleep 1 &
echo "started"
wait
echo "finished"
```

- 答案：

```text
started
finished
```

命令末尾的 `&` 让它在后台运行，shell 不等它结束就继续往下执行；`wait` 等待后台任务全部结束。

### Q00-32 用 `kill` 结束进程

- 类型：概念题
- 出处：[Bash 手册 3.7.6 信号](https://www.gnu.org/software/bash/manual/bash.html#Signals)
- 问题：结束后台进程后，`wait` 得到的退出码是多少？

```bash
sleep 30 &
pid=$!
kill $pid
wait $pid 2>/dev/null
echo "exit=$?"
```

- 答案：

```text
exit=143
```

`$!` 是最近一个后台进程的进程号。`kill` 默认发送 SIGTERM（信号 15）；被信号终止的进程，退出码是 128 加信号编号，所以是 143。

### Q00-33 修改 `~/.bashrc` 之后

- 类型：概念题
- 出处：[Bash 手册 6.2 Bash 启动文件](https://www.gnu.org/software/bash/manual/bash.html#Bash-Startup-Files)
- 问题：在 `~/.bashrc` 里加了一行 `export PATH="$HOME/bin:$PATH"`，为什么当前打开的终端里没有生效？怎么让它立刻生效？
- 答案：

启动文件只在 shell 启动时读取一次。当前终端已经启动了，所以看不到修改；新开一个终端会读取新内容。想立刻生效，可以运行 `source ~/.bashrc`，让当前 shell 重新执行这个文件里的命令。

### Q00-34 变量为空时的 `rm -rf`

- 类型：概念题
- 出处：[Bash 手册 3.5.3 Shell 参数展开](https://www.gnu.org/software/bash/manual/bash.html#Shell-Parameter-Expansion)、[4.3.1 set 内建命令](https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin)
- 问题：脚本里写了 `rm -rf $dir/*`，如果变量 `dir` 没有设置会发生什么？怎么防范？
- 答案：

未设置的变量展开为空，命令就变成 `rm -rf /*`，会试图删除根目录下的所有内容。防范办法：变量加双引号；用 `${dir:?}` 让变量为空时报错退出；在脚本开头写 `set -u`，使用未定义的变量时报错；先用 `echo` 把要执行的命令打印出来，确认无误再真正执行。
