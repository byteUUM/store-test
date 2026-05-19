"""ShopXO 自动化测试配置 — 对应测试计划 §3"""

import os

BASE_URL = os.getenv("SHOPXO_BASE_URL", "http://49.235.61.184").rstrip("/")

COOKIES = {
    "uuid": os.getenv("SHOPXO_UUID", "ed00ec1f-d45b-859d-29c7-4733fb0054a5"),
    "admin_info": os.getenv("SHOPXO_ADMIN_INFO", "null"),
    "PHPSESSID": os.getenv("SHOPXO_PHPSESSID", "6c48dc9942ecf66e5b3513728801c938"),
}

HEADERS = {
    "User-Agent": "ShopXO-AutoTest/1.0",
    "Accept": "text/html,application/xhtml+xml,application/json",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

PATHS = {
    "home": "/",
    "category": "/?s=category/index.html",
    "search": "/?s=search/index.html",
    "goods": "/?s=goods/index/id/{goods_id}.html",
    "login": "/?s=user/logininfo.html",
    "register": "/?s=user/reginfo.html",
    "forget_pwd": "/?s=user/forgetpwdinfo.html",
    "cart": "/?s=cart/index.html",
    "buy": "/?s=buy/index.html",
    "user_center": "/?s=user/index.html",
    "order": "/index.php?s=order/index.html",
    "logout": "/?s=user/logout.html",
    "agreement_register": "/?s=agreement/index/document/userregister.html",
    "agreement_privacy": "/?s=agreement/index/document/userprivacy.html",
    "article": "/?s=article/index/id/{article_id}.html",
}

API = {
    # Search
    "search_post": "/?s=search/index.html",
    # User auth
    "login_post": "/?s=user/login.html",
    "reg_post": "/?s=user/reg.html",
    "login_verify_send": "/?s=user/loginverifysend.html",
    "reg_verify_send": "/?s=user/regverifysend.html",
    "verify_login": "/?s=user/userverifyentry/type/user_login.html",
    "verify_reg": "/?s=user/userverifyentry/type/user_reg.html",
    # Goods
    "goods_comments": "/?s=goods/comments.html",
    "goods_favor": "/?s=goods/favor.html",
    "goods_spectype": "/?s=goods/spectype.html",
    "goods_specdetail": "/?s=goods/specdetail.html",
    "goods_stock": "/?s=goods/stock.html",
    "goods_cartinfo": "/?s=goods/cartinfo.html",
    # Cart / Buy
    "cart_save": "/?s=cart/save.html",
    "buy_post": "/?s=buy/index.html",
    # UEditor
    "ueditor_upload": "/?s=ueditor/index/path_type/public.html",
}

# Test data — goods
DEFAULT_GOODS_ID = int(os.getenv("SHOPXO_GOODS_ID", "99"))
INVALID_GOODS_ID = int(os.getenv("SHOPXO_INVALID_GOODS_ID", "999999999"))
EDGE_GOODS_IDS = [0, -1]

# Test data — categories
INVALID_CATEGORY_ID = int(os.getenv("SHOPXO_INVALID_CID", "999999"))
EDGE_CATEGORY_IDS = [0, -1]

# Test data — search
SEARCH_KEYWORDS = {
    "normal": "手机",
    "english": "phone",
    "empty": "",
    "xss": "<script>alert(1)</script>",
    "xss_img": "<img src=x onerror=alert(1)>",
    "sql": "1' OR '1'='1",
    "path_traversal": "../../../etc/passwd",
    "null_byte": "\x00null",
    "long": "a" * 300,
    "very_long": "a" * 1000,
    "special_regex": r".*+?^$()[]{}|\\",
}

# Test accounts (set env vars to enable login-dependent tests)
TEST_USERNAME = os.getenv("SHOPXO_TEST_USERNAME", "")
TEST_PASSWORD = os.getenv("SHOPXO_TEST_PASSWORD", "")

REQUEST_TIMEOUT = int(os.getenv("SHOPXO_TIMEOUT", "15"))
