"""首页与导航 — 对应用例 TC-HOME-*"""

import re

import pytest

from config import BASE_URL, PATHS
from conftest import has_text


@pytest.mark.p0
def test_tc_home_001_homepage_loads(get_html):
    """TC-HOME-001 首页正常加载"""
    resp = get_html(PATHS["home"])
    assert resp.status_code == 200
    assert has_text(resp, "电商平台") or b"ShopXO" in resp.content
    assert has_text(resp, "首页") or "index" in resp.url.lower()


@pytest.mark.p1
def test_tc_home_003_nav_links_present(get_html):
    """TC-HOME-003 导航入口存在"""
    resp = get_html(PATHS["home"])
    assert has_text(resp, "分类"), "缺少分类导航"
    assert has_text(resp, "购物车") or has_text(resp, "我的"), "缺少购物车/用户入口"


@pytest.mark.p0
def test_tc_home_005_goods_link_pattern(get_html):
    """TC-HOME-005 推荐商品含商品详情链接"""
    resp = get_html(PATHS["home"])
    assert re.search(rb"goods.{0,10}id.{0,10}\d+", resp.content) or has_text(resp, "商品")


@pytest.mark.p1
def test_tc_home_006_no_obvious_404_assets(get_html):
    """TC-HOME-006 核心静态资源无明显 404（抽样）"""
    resp = get_html(PATHS["home"])
    urls = re.findall(rb'(?:href|src)=["\']([^"\']+\.(?:css|js))["\']', resp.content)[:5]
    for u in urls:
        u = u.decode()
        if u.startswith("//"):
            u = "http:" + u
        elif u.startswith("/"):
            u = BASE_URL + u
        elif not u.startswith("http"):
            continue
        r = get_html(u)
        assert r.status_code < 400, f"资源不可访问: {u}"
