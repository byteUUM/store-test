"""注册页快速检查 — 可 python register.py 单独执行"""

import sys

import requests

from config import BASE_URL, COOKIES, HEADERS, PATHS, REQUEST_TIMEOUT


def main():
    url = f"{BASE_URL}{PATHS['register']}"
    resp = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    print(f"GET {url} -> {resp.status_code}")
    if resp.status_code != 200 or "注册" not in resp.text:
        print("FAIL: 注册页异常")
        sys.exit(1)
    print("OK: 注册页正常")
    sys.exit(0)


if __name__ == "__main__":
    main()
