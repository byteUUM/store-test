"""接口测试 — TC-API-*"""

import requests
import pytest

from config import API, BASE_URL, DEFAULT_GOODS_ID, HEADERS, PATHS, REQUEST_TIMEOUT
from conftest import has_text, has_error_body, json_body


@pytest.mark.p1
def test_tc_api_001_comments_structure(post_form):
    """TC-API-001 评论接口返回结构"""
    resp = post_form(API["goods_comments"], data={"goods_id": DEFAULT_GOODS_ID, "page": 1})
    assert resp.status_code == 200
    body = json_body(resp)
    if body:
        assert any(k in body for k in ("code", "msg", "data"))


@pytest.mark.p0
def test_tc_api_002_missing_goods_id(post_form):
    """TC-API-002 缺少必填参数"""
    resp = post_form(API["goods_comments"], data={})
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p0
def test_tc_api_005_favor_requires_login(post_form):
    """TC-API-005 未登录收藏"""
    resp = post_form(API["goods_favor"], data={"goods_id": DEFAULT_GOODS_ID})
    assert resp.status_code == 200
    body = json_body(resp)
    if body:
        assert body.get("code") != 0 or "登录" in str(body.get("msg", ""))


@pytest.mark.p0
def test_tc_api_006_expired_session():
    """TC-API-006 伪造/过期 session"""
    s = requests.Session()
    s.cookies.set("PHPSESSID", "invalid_session_for_test_000")
    s.headers.update(HEADERS)
    resp = s.get(f"{BASE_URL}{PATHS['cart']}", timeout=REQUEST_TIMEOUT, allow_redirects=True)
    body = resp.text
    assert "SQL syntax" not in body
    assert "mysqli" not in body.lower()
    assert "Fatal error" not in body


@pytest.mark.p1
def test_tc_api_007_comments_invalid_page(post_form):
    """TC-API-007 评论接口非法页码"""
    resp = post_form(API["goods_comments"], data={"goods_id": DEFAULT_GOODS_ID, "page": -1})
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_api_008_comments_empty_page(post_form):
    """TC-API-008 评论接口超大页码"""
    resp = post_form(API["goods_comments"], data={"goods_id": DEFAULT_GOODS_ID, "page": 99999})
    assert resp.status_code == 200
    assert not has_error_body(resp)
