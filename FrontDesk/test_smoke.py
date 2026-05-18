"""冒烟流程 SMOKE-001/002：游客浏览"""

import re

import pytest

from config import API, PATHS


@pytest.mark.p0
def test_smoke_001_guest_browse(get_html, post_form):
    """SMOKE-001: 首页 -> 分类 -> 搜索 -> 商品详情"""
    home = get_html(PATHS["home"])
    assert home.status_code == 200

    cat = get_html(PATHS["category"])
    assert cat.status_code == 200

    search = post_form(API["search_post"], data={"wd": "手机"}, allow_redirects=True)
    assert search.status_code == 200

    m = re.search(rb"goods/index/id/(\d+)", home.content)
    goods_id = m.group(1).decode() if m else "99"
    detail = get_html(PATHS["goods"].format(goods_id=goods_id))
    assert detail.status_code == 200


@pytest.mark.p0
def test_smoke_002_register_page_accessible(get_html):
    """SMOKE-002: 注册页可访问"""
    resp = get_html(PATHS["register"])
    assert resp.status_code == 200


@pytest.mark.p0
def test_smoke_003_login_page_accessible(get_html):
    """SMOKE-003: 登录页可访问"""
    resp = get_html(PATHS["login"])
    assert resp.status_code == 200


@pytest.mark.p0
def test_smoke_004_agreement_pages_accessible(get_html):
    """SMOKE-004: 协议页可访问"""
    r1 = get_html(PATHS["agreement_register"])
    r2 = get_html(PATHS["agreement_privacy"])
    assert r1.status_code == 200
    assert r2.status_code == 200
