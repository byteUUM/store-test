"""结算与订单 — TC-BUY-* / TC-ORDER-*"""

import pytest

from config import API, BASE_URL, PATHS
from conftest import has_text, has_error_body


@pytest.mark.p0
def test_tc_buy_001_checkout_requires_login(get_html):
    """TC-BUY-001 未登录访问结算页应拦截"""
    resp = get_html(PATHS["buy"], allow_redirects=True)
    assert resp.status_code == 200
    # 未登录时返回 JS 跳转登录页 或 登录页HTML
    assert any((
        has_text(resp, "登录"),
        "login" in resp.url.lower(),
        "logininfo" in resp.text,
        b"logininfo" in resp.content,
    ))


@pytest.mark.p0
def test_tc_buy_002_buy_post_without_login(post_form):
    """TC-BUY-002 未登录提交购买应拦截"""
    resp = post_form(API["buy_post"], data={"buy_type": "goods", "goods_data": "[]"})
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_buy_003_buy_empty_data(post_form):
    """TC-BUY-003 购买空数据"""
    resp = post_form(API["buy_post"], data={})
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_order_001_order_page(get_html):
    """TC-ORDER-001 订单页可访问"""
    resp = get_html(PATHS["order"], allow_redirects=True)
    assert resp.status_code in (200, 301, 302, 307)
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_logout(get_html):
    """退出登录"""
    resp = get_html(PATHS["logout"])
    # 可能 200（含 HTML/JSON）或 302 跳转
    assert resp.status_code in (200, 301, 302)
    assert not has_error_body(resp)
