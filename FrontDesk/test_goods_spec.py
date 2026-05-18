"""商品规格与库存接口 — TC-GOODS-002/003/006/007"""

import pytest

from config import API, DEFAULT_GOODS_ID
from conftest import has_error_body, extract_json_msg


@pytest.mark.p1
def test_tc_goods_002_spec_type_api(post_form):
    """TC-GOODS-002 商品规格类型接口"""
    resp = post_form(API["goods_spectype"], data={"goods_id": DEFAULT_GOODS_ID})
    assert resp.status_code == 200
    assert not has_error_body(resp)
    msg = extract_json_msg(resp)
    # Should either return data or give valid error (but not crash)
    if msg:
        assert "商品id有误" in msg or "id" in msg or msg == ""


@pytest.mark.p1
def test_tc_goods_003_spec_detail_api(post_form):
    """TC-GOODS-003 商品规格详情接口"""
    resp = post_form(API["goods_specdetail"], data={"goods_id": DEFAULT_GOODS_ID})
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_goods_006_stock_api(post_form):
    """TC-GOODS-006 商品库存接口"""
    resp = post_form(API["goods_stock"], data={"goods_id": DEFAULT_GOODS_ID})
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_goods_007_cart_info_api(post_form):
    """TC-GOODS-007 商品加购弹窗信息接口"""
    resp = post_form(API["goods_cartinfo"], data={"goods_id": DEFAULT_GOODS_ID})
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_goods_spec_missing_goods_id(post_form):
    """规格接口缺商品 ID"""
    for ep in [API["goods_spectype"], API["goods_specdetail"], API["goods_stock"]]:
        resp = post_form(ep, data={})
        assert resp.status_code == 200
        assert not has_error_body(resp), f"{ep} missing goods_id caused error"
