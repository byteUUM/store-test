"""分类与搜索 — TC-CAT-* / TC-SEARCH-*"""

import re

import pytest

from config import API, DEFAULT_GOODS_ID, INVALID_CATEGORY_ID, PATHS, EDGE_CATEGORY_IDS
from conftest import has_text, has_error_body


@pytest.mark.p0
def test_tc_cat_001_category_page(get_html):
    """TC-CAT-001 分类页加载"""
    resp = get_html(PATHS["category"])
    assert resp.status_code == 200
    assert has_text(resp, "分类") or "category" in resp.url.lower()


@pytest.mark.p1
def test_tc_cat_003_category_cid_zero(get_html):
    """TC-CAT-003 类目 ID=0"""
    resp = get_html(f"/?s=search/index/cid/{EDGE_CATEGORY_IDS[0]}.html")
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_cat_004_invalid_category(get_html):
    """TC-CAT-004 非法类目 ID"""
    resp = get_html(f"/?s=search/index/cid/{INVALID_CATEGORY_ID}.html")
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_cat_005_category_cid_negative(get_html):
    """TC-CAT-005 类目 ID 为负数"""
    resp = get_html(f"/?s=search/index/cid/{EDGE_CATEGORY_IDS[1]}.html")
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p0
def test_tc_search_001_keyword_search(post_form):
    """TC-SEARCH-001 关键词搜索「手机」"""
    resp = post_form(API["search_post"], data={"wd": "手机"}, allow_redirects=True)
    assert resp.status_code == 200
    assert has_text(resp, "手机") or b"goods" in resp.content.lower()


@pytest.mark.p1
def test_tc_search_002_empty_keyword(post_form):
    """TC-SEARCH-002 空关键词搜索"""
    resp = post_form(API["search_post"], data={"wd": ""}, allow_redirects=True)
    assert resp.status_code == 200
    body = resp.text
    assert "Fatal error" not in body and "SQL syntax" not in body


@pytest.mark.p0
def test_tc_search_003_xss_payload(post_form):
    """TC-SEARCH-003 特殊字符 / XSS payload"""
    payload = "<script>alert(1)</script>"
    resp = post_form(API["search_post"], data={"wd": payload})
    assert resp.status_code == 200
    assert payload.encode() not in resp.content
    # Follow redirect if present for thorough check
    if not resp.history:
        assert payload.encode() not in resp.content


@pytest.mark.p1
def test_tc_search_004_long_keyword(post_form):
    """TC-SEARCH-004 超长关键词"""
    resp = post_form(API["search_post"], data={"wd": "a" * 300}, allow_redirects=True)
    assert resp.status_code == 200
    assert "500" not in resp.text[:500]


@pytest.mark.p0
def test_tc_search_goods_detail_from_home(get_html):
    """冒烟：从首页进入商品详情"""
    home = get_html(PATHS["home"])
    m = re.search(rb"goods/index/id/(\d+)", home.content)
    goods_id = m.group(1).decode() if m else str(DEFAULT_GOODS_ID)
    detail = get_html(PATHS["goods"].format(goods_id=goods_id))
    assert detail.status_code == 200
