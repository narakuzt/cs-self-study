#!/usr/bin/env python3
"""间隔复习队列工具（只用标准库）。

队列是学习记录目录里的 `复习队列.md`（模板见 模板/复习队列模板.md）。
卡片可以是知识层题库里的题（如 Q02-01），也可以是自己写的卡片（复习卡片/ 里的 `## 卡 001`）。

间隔：新卡次日复习；每答对一次进入下一档，依次隔 3、7、14、30 天；答对 30 天档后移出队列；答错回到第 1 档。

用法（--dir 默认是本仓库同级的「学习记录」目录）：
  python3 工具/复习.py due                          列出今天到期的卡片
  python3 工具/复习.py quiz                         逐题闭卷抽问，按回答自动更新队列
  python3 工具/复习.py add Q02-01 知识/02-Python基础.md   加入一张卡
  python3 工具/复习.py add-all 知识/02-Python基础.md --limit 5   把题库里还没入队的题加入若干道
  python3 工具/复习.py pass Q02-01 / fail Q02-01     手动记录一次答对或答错
  python3 工具/复习.py status                       查看各档数量
  加 --today YYYY-MM-DD 可以指定"今天"（测试用）。
"""
import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INTERVALS = [1, 3, 7, 14, 30]  # INTERVALS[k-1]：进入第 k 档后，隔多少天复习
HEAD = ("# 复习队列\n\n间隔：次日、3 天、7 天、14 天、30 天。答对进入下一档，答错回到第 1 档。"
        "通过 30 天档后移出队列。\n\n| 卡片 | 所在文件 | 当前档 | 下次复习日期 | 上次结果 |\n|---|---|---|---|---|\n")
ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([1-5])\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([^|]*?)\s*\|\s*$")


class Queue:
    def __init__(self, path):
        self.path = Path(path)
        lines = self.path.read_text(encoding="utf-8").splitlines() if self.path.exists() else []
        idx = next((i for i, l in enumerate(lines) if l.startswith("| 卡片")), None)
        if idx is None:
            self.head, body = HEAD, []
        else:
            self.head = "\n".join(lines[: idx + 2]) + "\n"
            body = lines[idx + 2:]
        self.rows = []
        for l in body:
            m = ROW.match(l)
            if m:
                self.rows.append({"id": m[1], "file": m[2], "level": int(m[3]), "due": m[4], "last": m[5]})

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        out = self.head + "".join(
            f"| {r['id']} | {r['file']} | {r['level']} | {r['due']} | {r['last']} |\n" for r in self.rows)
        self.path.write_text(out, encoding="utf-8")

    def get(self, cid):
        return next((r for r in self.rows if r["id"] == cid), None)


def add(q, cid, file, today):
    if q.get(cid):
        return False
    q.rows.append({"id": cid, "file": file, "level": 1, "due": str(today + timedelta(days=INTERVALS[0])), "last": "新建"})
    return True


def answer(q, cid, ok, today):
    r = q.get(cid)
    if not r:
        sys.exit(f"队列里没有 {cid}")
    if not ok:
        r.update(level=1, due=str(today + timedelta(days=INTERVALS[0])), last=f"{today} 答错")
        return "答错，回到第 1 档"
    if r["level"] == 5:
        q.rows.remove(r)
        return "答对 30 天档，移出队列"
    r["level"] += 1
    r.update(due=str(today + timedelta(days=INTERVALS[r["level"] - 1])), last=f"{today} 答对")
    return f"答对，进入第 {r['level']} 档，下次 {r['due']}"


def card_text(cid, file, roots):
    """返回卡片所在小节的文本（忽略代码块里的 # 行）。"""
    for root in roots:
        p = Path(root) / file
        if not p.exists():
            continue
        lines = p.read_text(encoding="utf-8").splitlines()
        in_code, start, level = False, None, 0
        for i, l in enumerate(lines):
            if l.startswith("```"):
                in_code = not in_code
                continue
            m = re.match(r"^(#{2,4}) (.+)$", l)
            if in_code or not m:
                continue
            if start is None:
                if m[2].split()[0] == cid or m[2].startswith(cid + " "):
                    start, level = i, len(m[1])
            elif len(m[1]) <= level:
                return "\n".join(lines[start:i])
        if start is not None:
            return "\n".join(lines[start:])
    return None


def split_qa(text):
    m = re.search(r"(?m)^- 答案", text)
    return (text[: m.start()], text[m.start():]) if m else (text, "（这张卡没有写答案）")


def main():
    ap = argparse.ArgumentParser(description="间隔复习队列工具")
    ap.add_argument("cmd", choices=["due", "quiz", "add", "add-all", "pass", "fail", "status"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--dir", default=str(REPO.parent / "学习记录"), help="学习记录目录")
    ap.add_argument("--today", help="指定今天的日期，格式 YYYY-MM-DD")
    ap.add_argument("--limit", type=int, default=5, help="add-all 一次加入的最大数量")
    a = ap.parse_args()
    today = date.fromisoformat(a.today) if a.today else date.today()
    q = Queue(Path(a.dir) / "复习队列.md")
    roots = [REPO, Path(a.dir)]

    if a.cmd == "status":
        print(f"队列共 {len(q.rows)} 张，今天到期 {sum(r['due'] <= str(today) for r in q.rows)} 张")
        for k in range(1, 6):
            print(f"  第 {k} 档：{sum(r['level'] == k for r in q.rows)} 张")
    elif a.cmd == "due":
        due = sorted((r for r in q.rows if r["due"] <= str(today)), key=lambda r: (r["due"], r["id"]))
        print(f"{today} 到期 {len(due)} 张")
        for r in due:
            print(f"  {r['id']}  第 {r['level']} 档  应复习于 {r['due']}  {r['file']}")
    elif a.cmd == "add":
        if len(a.args) != 2:
            sys.exit("用法：add 卡片ID 所在文件")
        cid, file = a.args
        if not card_text(cid, file, roots):
            sys.exit(f"在 {file} 里找不到 {cid}")
        print("已加入" if add(q, cid, file, today) else "已在队列中")
        q.save()
    elif a.cmd == "add-all":
        if len(a.args) != 1:
            sys.exit("用法：add-all 题库文件")
        p = Path(a.args[0]).resolve()
        file = str(p.relative_to(REPO)) if REPO in p.parents else a.args[0]
        ids = re.findall(r"(?m)^### (Q\d+-\d+)", p.read_text(encoding="utf-8"))
        n = 0
        for cid in ids:
            if n >= a.limit:
                break
            n += add(q, cid, file, today)
        q.save()
        print(f"加入 {n} 张，队列共 {len(q.rows)} 张")
    elif a.cmd in ("pass", "fail"):
        if len(a.args) != 1:
            sys.exit(f"用法：{a.cmd} 卡片ID")
        print(answer(q, a.args[0], a.cmd == "pass", today))
        q.save()
    elif a.cmd == "quiz":
        due = sorted((r for r in q.rows if r["due"] <= str(today)), key=lambda r: (r["due"], r["id"]))
        if not due:
            print(f"{today} 没有到期的卡片")
            return
        for n, r in enumerate(due, 1):
            text = card_text(r["id"], r["file"], roots)
            print(f"\n===== {n}/{len(due)}  {r['id']}（第 {r['level']} 档）=====")
            if not text:
                print(f"找不到卡片内容：{r['file']}")
                continue
            ques, ans = split_qa(text)
            print(ques)
            try:
                input("先在心里或纸上作答，按回车看答案……")
                print(ans)
                ok = input("答对了吗？(y/n) ").strip().lower().startswith("y")
            except EOFError:
                break
            print(answer(q, r["id"], ok, today))
            q.save()


if __name__ == "__main__":
    main()
