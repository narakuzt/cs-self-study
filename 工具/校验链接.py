#!/usr/bin/env python3
"""逐个核对仓库里所有 Markdown 文件的外部链接（只用标准库，需要联网）。

对不同站点用不同的核对方式，因为有些站点对不存在的地址也返回 200：
  - B 站：调用公开接口，检查稿件是否存在，并显示标题与集数
  - 中国大学 MOOC：读取页面标题，占位页视为失效
  - YouTube：用 oEmbed 获取标题
  - 带 #锚点 的链接：检查页面里是否有该 id
  - 其他站点：HTTP 状态码为 2xx（连接失败会重试一次），并显示页面标题

用法：
  python3 工具/校验链接.py            # 检查整个仓库，打印全部结果
  python3 工具/校验链接.py --failed   # 只打印有问题的
有失效链接时退出码为 1。
"""
import argparse
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote, urlparse

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"  # 一些站点（如 gnu.org）会拒绝过于简单的标识


def curl(url, extra=(), timeout=30):
    p = subprocess.run(["curl", "-sk", "-L", "-m", str(timeout), "-A", UA, *extra, url],
                       capture_output=True)
    return p.stdout.decode("utf8", "ignore")


def status(url):
    """返回 HTTP 状态码；连接失败（000）时重试一次。"""
    for _ in range(2):
        p = subprocess.run(["curl", "-sk", "-o", "/dev/null", "-L", "-m", "30", "-A", UA,
                            "-w", "%{http_code}", url], capture_output=True)
        code = p.stdout.decode()
        if code != "000":
            break
    return code


def title(html):
    m = re.search(r'og:title" content="([^"]*)', html) or re.search(r"<title[^>]*>([^<]*)</title>", html)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def check(url):
    host = urlparse(url).netloc
    try:
        if "bilibili.com" in host:
            m = re.search(r"(BV[0-9A-Za-z]{10})", url)
            if not m:
                return "B站", "?", "链接里没有 BV 号"
            j = json.loads(curl("https://api.bilibili.com/x/web-interface/view?bvid=" + m.group(1), timeout=25) or "{}")
            if j.get("code") != 0:
                return "B站", "失效", f"接口返回 {j.get('code')} {j.get('message')}"
            d = j["data"]
            return "B站", "正常", f"{d['title']} | {d['videos']} 集 | {d['owner']['name']}"
        if "youtube.com" in host or "youtu.be" in host:
            j = curl("https://www.youtube.com/oembed?format=json&url=" + quote(url, safe=""), timeout=25)
            try:
                d = json.loads(j)
                return "YouTube", "正常", f"{d['title']} | {d['author_name']}"
            except Exception:
                return "YouTube", "无法核实", "oEmbed 无结果（频道页不支持，或视频已失效）"
        if "icourse163.org" in host:
            t = title(curl(url))
            if not t or t.startswith("中国大学MOOC_优质"):
                return "慕课", "失效", "占位页或无标题"
            return "慕课", "正常", t
        page, _, anchor = url.partition("#")
        c = status(page)
        if not c.startswith("2"):
            return "网页", "失效", f"HTTP {c}"
        html = curl(page)
        if anchor and f'id="{anchor}"' not in html:
            return "网页", "失效", f"页面存在，但没有锚点 #{anchor}"
        return "网页", "正常", title(html)[:80]
    except Exception as e:
        return "?", "出错", str(e)[:80]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--failed", action="store_true", help="只打印有问题的链接")
    a = ap.parse_args()
    urls = set()
    for f in Path(a.root).rglob("*.md"):
        for u in re.findall(r"\]\((https?://[^)\s]+)\)", f.read_text(encoding="utf-8")):
            urls.add(u.rstrip(".,;，。、"))
    urls = sorted(urls)

    def run(u):
        time.sleep(0.05)
        return (u,) + check(u)

    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, urls))
    bad = [r for r in res if r[2] != "正常"]
    for u, kind, st, info in res:
        if a.failed and st == "正常":
            continue
        print(f"[{st}] {kind} {u}\n      {info}")
    print(f"\n共 {len(res)} 个链接，正常 {len(res) - len(bad)}，需要处理 {len(bad)}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
