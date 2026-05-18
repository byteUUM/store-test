"""商品详情 — TC-GOODS-*"""

import pytest

from config import API, DEFAULT_GOODS_ID, INVALID_GOODS_ID, PATHS
from conftest import has_text, has_error_body


@pytest.mark.p0
def test_tc_goods_001_detail_load(get_html):
    """TC-GOODS-001 商品详情加载"""
    resp = get_html(PATHS["goods"].format(goods_id=DEFAULT_GOODS_ID))
    assert resp.status_code == 200
    assert has_text(resp, "商品") or has_text(resp, "价格")


@pytest.mark.p1
def test_tc_goods_008_comments_api(post_form):
    """TC-GOODS-008 评论接口"""
    resp = post_form(API["goods_comments"], data={"goods_id": DEFAULT_GOODS_ID, "page": 1})
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_goods_009_not_exist(get_html):
    """TC-GOODS-009 商品不存在"""
    resp = get_html(PATHS["goods"].format(goods_id=INVALID_GOODS_ID))
    assert resp.status_code == 200
    assert any(has_text(resp, k) for k in ("不存在", "已删除", "无数据", "404"))


@pytest.mark.p0
def test_tc_goods_004_unauth_add_cart_redirect_or_hint(post_form):
    """TC-GOODS-004 / TC-CART-002 未登录加购应拦截"""
    resp = post_form(API["cart_save"], data={"goods_data": "[]"})
    assert resp.status_code == 200
    # 返回 JS 跳转登录页或 JSON 拦截提示
    assert any((
        has_text(resp, "登录"),
        b"logininfo" in resp.content,
        "logininfo" in resp.text,
    ))


@pytest.mark.p1
def test_tc_goods_010_detail_goods_id_zero(get_html):
    """TC-GOODS-010 商品 ID 为 0"""
    resp = get_html(PATHS["goods"].format(goods_id=0))
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_goods_011_detail_goods_id_negative(get_html):
    """TC-GOODS-011 商品 ID 为负数"""
    resp = get_html(PATHS["goods"].format(goods_id=-1))
    assert resp.status_code == 200
    assert not has_error_body(resp)
