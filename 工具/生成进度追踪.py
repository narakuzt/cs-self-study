#!/usr/bin/env python3
"""按各课程页「过关标准」的编号（如 2.1）生成进度追踪清单。

用法：
  python3 工具/生成进度追踪.py > 我的进度追踪.md
  python3 工具/生成进度追踪.py --keep 我的进度追踪.md > 新的.md   # 保留已勾选的状态

课程页里的条目是固定编号的，进度只记录在你自己的文件里，更新课程仓库时不会冲突。
"""
import argparse, glob, os, re, sys

GROUPS = [(0, 3, "语言基础"), (4, 8, "CS 核心地基"), (9, 11, "工程与工具"),
          (12, 14, "进阶与拓展"), (15, 15, "收尾")]

def group_of(n):
    for lo, hi, name in GROUPS:
        if lo <= n <= hi:
            return name
    return "其他"

def load_ticks(path):
    ticks = set()
    if path and os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            m = re.match(r"- \[[xX]\] \*\*(\d+\.\d+)\*\*", line)
            if m:
                ticks.add(m.group(1))
    return ticks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", help="已有的进度文件，保留其中已勾选的条目")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), ".."), help="课程仓库根目录")
    a = ap.parse_args()
    ticks = load_ticks(a.keep)
    out = ["# 进度追踪", "", "由 `工具/生成进度追踪.py` 按各主题页「过关标准」的编号生成。通过一条就把 `[ ]` 改成 `[x]`。", ""]
    last = None
    for f in sorted(glob.glob(os.path.join(a.root, "课程", "*.md"))):
        text = open(f, encoding="utf-8").read()
        title = re.match(r"# (.+)", text).group(1)
        n = int(re.match(r"(\d+)", title).group(1))
        m = re.search(r"## 过关标准\n\n(.*?)(?=\n## |\Z)", text, re.S)
        items = re.findall(r"- \*\*(\d+\.\d+)\*\* (.+)", m.group(1)) if m else []
        g = group_of(n)
        if g != last:
            out += [f"## {g}", ""]
            last = g
        out += [f"### {title}", ""]
        for i, t in items:
            t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)  # 条目里的链接化为纯文字，避免相对路径失效
            out.append(f"- [{'x' if i in ticks else ' '}] **{i}** {t}")
        out.append("")
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
