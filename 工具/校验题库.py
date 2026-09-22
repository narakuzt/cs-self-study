#!/usr/bin/env python3
"""校验知识层题库里代码题的答案。

每道题是一个 "### Q…" 小节。小节里第一个 ```python、```bash、```c、```cpp 或 ```js 代码块会被运行：
  - python：直接运行
  - bash：在一个全新的空临时目录里运行，语言环境固定为 C；Git 的全局配置被屏蔽，
    提交者信息固定为测试用户，因此 Git 命令的输出不受你本机配置影响
  - c / cpp：用 gcc -std=c11 / g++ -std=c++17（带 -Wall -Wextra）编译后运行
  - js：用 node 运行
其标准输出必须与「答案」之后第一个 ```text 代码块完全一致（忽略行尾空白）。
没有代码块的题（纯概念题）会被跳过。

用法：
  python3 工具/校验题库.py 知识/02-Python基础.md
  python3 工具/校验题库.py 知识/*.md
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def sections(text):
    parts = re.split(r"(?m)^### (?=Q)", text)
    return parts[1:]


def norm(s):
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def check_file(path):
    text = Path(path).read_text(encoding="utf-8")
    ok = bad = skipped = 0
    for sec in sections(text):
        title = sec.splitlines()[0]
        code = re.search(r"```(python|bash|cpp|c|js)\n(.*?)```", sec, re.S)
        ans = re.search(r"- 答案：\s*```text\n(.*?)```", sec, re.S)
        if not code or not ans:
            skipped += 1
            continue
        lang, src = code.group(1), code.group(2)
        workdir = tempfile.mkdtemp()
        try:
            env = {**os.environ, "LC_ALL": "C", "LANG": "C",
                   "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1", "GIT_PAGER": "cat",
                   "GIT_EDITOR": "true", "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "t@example.com",
                   "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "t@example.com"}
            if lang == "python":
                script = Path(workdir) / "q.py"
                script.write_text(src, encoding="utf-8")
                cmd = [sys.executable, str(script)]
            elif lang == "bash":
                cmd = ["bash", "-c", src]
            elif lang == "js":
                script = Path(workdir) / "q.js"
                script.write_text(src, encoding="utf-8")
                cmd = ["node", str(script)]
            else:
                ext, compiler, std = ("c", "gcc", "-std=c11") if lang == "c" else ("cpp", "g++", "-std=c++17")
                source = Path(workdir) / f"q.{ext}"
                source.write_text(src, encoding="utf-8")
                comp = subprocess.run([compiler, std, "-Wall", "-Wextra", "-o", str(Path(workdir) / "q"),
                                       str(source), "-lm"], capture_output=True, text=True, timeout=60)
                if comp.returncode != 0:
                    print(f"✗ {title}：编译失败\n{comp.stderr.strip()[:400]}")
                    bad += 1
                    continue
                cmd = [str(Path(workdir) / "q")]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=workdir, env=env)
        except subprocess.TimeoutExpired:
            print(f"✗ {title}：运行超时")
            bad += 1
            continue
        finally:
            shutil.rmtree(workdir, ignore_errors=True)
        got, want = norm(r.stdout), norm(ans.group(1))
        if r.returncode == 0 and got == want:
            ok += 1
        else:
            bad += 1
            print(f"✗ {title}")
            print("  期望：", want.replace("\n", " ⏎ "))
            print("  实际：", got.replace("\n", " ⏎ "), r.stderr.strip()[:200])
    def first(cmd):
        try:
            return subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines()[0]
        except Exception:
            return "未安装"
    print(f"{path}: 通过 {ok}，失败 {bad}，跳过（无代码）{skipped}")
    print(f"  环境：Python {sys.version.split()[0]}；{first(['bash', '--version'])}；{first(['git', '--version'])}；{first(['gcc', '--version'])}；{first(['g++', '--version'])}；node {first(['node', '--version'])}")
    return bad


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(1 if sum(check_file(p) for p in sys.argv[1:]) else 0)
