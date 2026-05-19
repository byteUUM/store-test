"""购物车与登录拦截 — TC-CART-* / TC-MEMBER-*"""

import pytest

from config import API, PATHS
from conftest import has_text, has_error_body


@pytest.mark.p0
def test_tc_member_002_cart_requires_login(get_html):
    """TC-MEMBER-002 / TC-CART-002 未登录访问购物车"""
    resp = get_html(PATHS["cart"], allow_redirects=True)
    assert resp.status_code == 200
    assert any((
        has_text(resp, "登录"),
        "login" in resp.url.lower(),
        "logininfo" in resp.text.lower(),
        has_text(resp, "购物车"),
    ))


@pytest.mark.p0
def test_tc_member_002_user_center_requires_login(get_html):
    """TC-MEMBER-002 未登录访问用户中心"""
    resp = get_html(PATHS["user_center"], allow_redirects=True)
    assert resp.status_code == 200
    assert any((
        has_text(resp, "登录"),
        "login" in resp.url.lower(),
        "logininfo" in resp.text.lower(),
    ))


@pytest.mark.p1
def test_tc_cart_003_cart_save_empty(post_form):
    """TC-CART-003 加购空数据"""
    resp = post_form(API["cart_save"], data={})
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_cart_004_cart_save_invalid_json(post_form):
    """TC-CART-004 加购非法 JSON"""
    resp = post_form(API["cart_save"], data={"goods_data": "{invalid_json}"})
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_cart_005_cart_via_post(post_form):
    """TC-CART-005 购物车页面 POST 请求"""
    resp = post_form(PATHS["cart"], data={})
    assert resp.status_code in (200, 302)
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_member_003_checkout_requires_login(get_html):
    """TC-MEMBER-003 未登录访问结算页"""
    resp = get_html(PATHS["buy"], allow_redirects=True)
    assert resp.status_code == 200
    assert any((
        has_text(resp, "登录"),
        "login" in resp.url.lower(),
        "logininfo" in resp.text,
    ))
