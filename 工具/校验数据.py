#!/usr/bin/env python3
"""核对各课程页里的星级、学时、周数与每周投入，是否和数据来源一致（只用标准库，需要联网）。

- 星级与学时：对照 csdiy.wiki 的源仓库（PKUFlyingPig/cs-self-learning）里各课程页的原文
- 周数与每周投入：对照 OSSU 的 README

用法：
  python3 工具/校验数据.py
有不一致时退出码为 1。来源更新后，课程页里的数字可能需要同步修改。
"""
import glob
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
CSDIY = "https://raw.githubusercontent.com/PKUFlyingPig/cs-self-learning/master/docs/"
OSSU = "https://raw.githubusercontent.com/ossu/computer-science/master/README.md"

# (课程页编号, 页面里用来定位的关键词, csdiy.wiki 源仓库里的文件路径)
CSDIY_ENTRIES = [
    ("00", "Missing Semester", "编程入门/MIT-Missing-Semester.md"),
    ("02", "CS50P", "编程入门/Python/CS50P.md"),
    ("02", "MIT 6.100L", "编程入门/Python/MIT6.100L.md"),
    ("02", "CS61A（UC", "编程入门/Python/CS61A.md"),
    ("03", "CS106L", "编程入门/cpp/CS106L.md"),
    ("03", "CS106B/X", "编程入门/cpp/CS106B_CS106X.md"),
    ("04", "CS70", "数学进阶/CS70.md"),
    ("04", "MIT 6.042J：Math", "数学进阶/6.042J.md"),
    ("05", "MIT 6.006", "数据结构与算法/6.006.md"),
    ("06", "### 第一步：Nand2Tetris", "体系结构/N2T.md"),
    ("06", "CSAPP / CMU", "计算机系统基础/CSAPP.md"),
    ("06", "UC Berkeley CS61C", "体系结构/CS61C.md"),
    ("06", "ETH Digital", "体系结构/DDCA.md"),
    ("07", "哈尔滨工业大学《操作系统》", "操作系统/HITOS.md"),
    ("07", "MIT 6.1810", "操作系统/MIT6.S081.md"),
    ("07", "南京大学《操作系统》", "操作系统/NJUOS.md"),
    ("07", "UC Berkeley CS162", "操作系统/CS162.md"),
    ("08", "中国科学技术大学《计算机网络", "计算机网络/topdown_ustc.md"),
    ("08", "Kurose & Ross", "计算机网络/topdown.md"),
    ("08", "Stanford CS144", "计算机网络/CS144.md"),
    ("08", "CS168", "计算机网络/CS168.md"),
    ("10", "CMU 15-445", "数据库系统/15445.md"),
    ("10", "UC Berkeley CS186", "数据库系统/CS186.md"),
    ("11", "Stanford CS142", "Web开发/CS142.md"),
    ("11", "MIT Web Development", "Web开发/mitweb.md"),
    ("11", "University of Helsinki", "Web开发/fullstackopen.md"),
    ("12", "UC Berkeley CS61A", "编程入门/Python/CS61A.md"),
    ("13", "Stanford CS110L", "编程入门/Rust/CS110L.md"),
    ("13", "MIT 6.092", "编程入门/Java/MIT 6.092.md"),
    ("13", "Cornell CS3110", "编程入门/Functional/CS3110.md"),
    ("13", "北京大学编译原理实践", "编译原理/PKU-Compilers.md"),
    ("13", "南京大学编译原理", "编译原理/NJU-Compilers.md"),
    ("13", "Stanford CS143", "编译原理/CS143.md"),
    ("14", "MIT 6.5840", "并行与分布式系统/MIT6.824.md"),
    ("14", "SEED Labs", "系统安全/SEEDLabs.md"),
    ("14", "UC Berkeley CS161", "系统安全/CS161.md"),
    ("14", "李宏毅机器学习", "深度学习/LHY.md"),
    ("14", "GAMES101", "计算机图形学/GAMES101.md"),
]

# (OSSU README 里的关键词, 课程页编号, 页面里应出现的文字)
OSSU_ENTRIES = [
    ("Introduction to Computer Science and Programming using Python", "02", "14 周，每周 6-10 小时"),
    ("Missing Semester", "00", "2 周，每周 12 小时"),
    ("Build a Modern Computer from First Principles: From Nand", "06", "6 周、每周 7-13 小时"),
    ("Nand to Tetris Part II](https://www.coursera.org/learn/nand2tetris2) |", "06", "6 周、每周 12-18 小时"),
    ("Operating Systems: Three Easy Pieces", "07", "10-12 周，每周 6-10 小时"),
    ("Computer Networking: a Top-Down", "08", "8 周，每周 4-12 小时"),
    ("Mathematics for Computer Science", "04", "13 周，每周 5 小时"),
    ("Calculus 1A", "04", "13 周（每周 6-10 小时）"),
    ("Calculus 1C", "04", "6 周（每周 5-10 小时）"),
    ("Algorithms: Design and Analysis, Part 1", "05", "各 8 周，每周 4-8 小时"),
    ("Databases: Relational Databases and SQL", "10", "各 2 周，每周 10 小时"),
    ("Machine Learning](https://www.deeplearning.ai", "14", "11 周，每周 9 小时"),
    ("Cybersecurity Fundamentals", "14", "8 周，每周 10-12 小时"),
    ("Fullstack Open", "11", "12 周，每周 15 小时"),
]


def fetch(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read().decode("utf-8")


def page_text(num):
    f = glob.glob(str(ROOT / "课程" / f"{num}-*.md"))[0]
    return Path(f).read_text(encoding="utf-8").split("\n")


def check_csdiy():
    bad = 0
    for num, kw, path in CSDIY_ENTRIES:
        src = fetch(CSDIY + quote(path))
        stars = re.search(r"课程难度[:：\*]*\s*(🌟+)", src) or re.search(r"(🌟+)", src)
        n = len(stars.group(1)) if stars else None
        h = re.search(r"预计学时[:：\*]*\s*([^\n]+)", src)
        hours = re.sub(r"[（(].*", "", h.group(1)).strip() if h else ""
        nums = re.findall(r"\d+", hours)
        lines = page_text(num)
        idx = [i for i, l in enumerate(lines) if kw in l]
        win = " ".join(" ".join(lines[i:i + 8]) for i in idx)
        ok = bool(idx) and n is not None and f"{n} 星" in win and all(x in win for x in nums)
        if not ok:
            bad += 1
            print(f"✗ 第 {num} 页「{kw}」：来源 {n} 星，学时「{hours}」，页面{'未找到该课程' if not idx else '与之不符'}")
    print(f"csdiy.wiki：核对 {len(CSDIY_ENTRIES)} 门课，不一致 {bad}")
    return bad


def check_ossu():
    rows = fetch(OSSU).split("\n")
    bad = 0
    for kw, num, expect in OSSU_ENTRIES:
        row = next((l for l in rows if kw in l and "|" in l), "")
        d = re.search(r"(\d+(?:-\d+)?) weeks?", row)
        e = re.search(r"(\d+(?:[-–]\d+)?) hours?/week", row)
        page = "\n".join(page_text(num))
        ok = bool(d and e and d.group(1) in expect and e.group(1).replace("–", "-") in expect and expect in page)
        if not ok:
            bad += 1
            print(f"✗ 第 {num} 页「{kw[:30]}」：来源 {d.group(1) if d else '?'} 周 / {e.group(1) if e else '?'} 小时每周，页面应含「{expect}」")
    print(f"OSSU：核对 {len(OSSU_ENTRIES)} 项，不一致 {bad}")
    return bad


if __name__ == "__main__":
    sys.exit(1 if check_csdiy() + check_ossu() else 0)
