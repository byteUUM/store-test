"""搜索高级测试 — TC-SEARCH-005/006/007/008"""

import pytest

from config import API, SEARCH_KEYWORDS
from conftest import has_text, has_error_body


SEARCH_WD_302_ENDPOINT = "/?s=search/index/wd/{encoded}.html"


def follow_search(post_form, wd):
    """POST 搜索并跟随重定向到结果页，返回最终响应。"""
    resp = post_form(API["search_post"], data={"wd": wd}, allow_redirects=True)
    return resp


@pytest.mark.p0
def test_tc_search_001_keyword_search(post_form):
    """TC-SEARCH-001 关键词搜索「手机」（现有用例强化）"""
    resp = follow_search(post_form, SEARCH_KEYWORDS["normal"])
    assert resp.status_code == 200
    assert has_text(resp, SEARCH_KEYWORDS["normal"]) or b"goods" in resp.content.lower()


@pytest.mark.p1
def test_tc_search_005_english_keyword(post_form):
    """TC-SEARCH-005 英文关键词搜索"""
    resp = follow_search(post_form, SEARCH_KEYWORDS["english"])
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_search_006_special_regex_chars(post_form):
    """TC-SEARCH-006 正则特殊字符搜索"""
    resp = follow_search(post_form, SEARCH_KEYWORDS["special_regex"])
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_search_007_very_long_keyword(post_form):
    """TC-SEARCH-007 超长关键词（1000字符）"""
    resp = follow_search(post_form, SEARCH_KEYWORDS["very_long"])
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_search_008_redirect_keyword_search(post_form):
    """搜索后重定向的 URL 是否可访问（跟随即可达）"""
    resp = follow_search(post_form, SEARCH_KEYWORDS["normal"])
    assert resp.status_code == 200
    # 搜索结果应包含商品列表
    assert b"goods" in resp.content.lower() or has_text(resp, "商品")
