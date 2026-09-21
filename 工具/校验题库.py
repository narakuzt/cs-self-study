#!/usr/bin/env python3
"""校验知识层题库里代码题的答案。

每道题是一个 "### Q…" 小节。小节里第一个 ```python 代码块会被运行，
其标准输出必须与「答案」之后第一个 ```text 代码块完全一致（忽略行尾空白）。
没有代码块的题（纯概念题）会被跳过。

用法：
  python3 工具/校验题库.py 知识/02-Python基础.md
  python3 工具/校验题库.py 知识/*.md
"""
import re
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
        code = re.search(r"```python\n(.*?)```", sec, re.S)
        ans = re.search(r"- 答案：\s*```text\n(.*?)```", sec, re.S)
        if not code or not ans:
            skipped += 1
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write(code.group(1))
            name = f.name
        try:
            r = subprocess.run([sys.executable, name], capture_output=True, text=True, timeout=15)
        except subprocess.TimeoutExpired:
            print(f"✗ {title}：运行超时")
            bad += 1
            continue
        finally:
            Path(name).unlink(missing_ok=True)
        got, want = norm(r.stdout), norm(ans.group(1))
        if r.returncode == 0 and got == want:
            ok += 1
        else:
            bad += 1
            print(f"✗ {title}")
            print("  期望：", want.replace("\n", " ⏎ "))
            print("  实际：", got.replace("\n", " ⏎ "), r.stderr.strip()[:200])
    print(f"{path}: 通过 {ok}，失败 {bad}，跳过（无代码）{skipped}，Python {sys.version.split()[0]}")
    return bad


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(1 if sum(check_file(p) for p in sys.argv[1:]) else 0)
