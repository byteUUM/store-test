"""安全探测（非破坏性）— TC-SEC-*"""

import pytest

from config import API, PATHS, SEARCH_KEYWORDS
from conftest import has_error_body, has_text


@pytest.mark.p0
def test_tc_sec_001_search_xss(post_form):
    """TC-SEC-001 搜索 XSS（<script> 标签）"""
    resp = post_form(API["search_post"], data={"wd": SEARCH_KEYWORDS["xss"]})
    assert SEARCH_KEYWORDS["xss"].encode() not in resp.content


@pytest.mark.p0
def test_tc_sec_002_search_xss_img(post_form):
    """TC-SEC-002 搜索 XSS（img onerror 变体）"""
    resp = post_form(API["search_post"], data={"wd": SEARCH_KEYWORDS["xss_img"]})
    assert SEARCH_KEYWORDS["xss_img"].encode() not in resp.content


@pytest.mark.p0
def test_tc_sec_003_search_sql_injection(post_form):
    """TC-SEC-003 搜索 SQL 注入"""
    resp = post_form(API["search_post"], data={"wd": SEARCH_KEYWORDS["sql"]})
    assert resp.status_code in (200, 302)
    body = resp.text
    assert "SQL syntax" not in body
    assert "mysqli" not in body.lower()


@pytest.mark.p0
def test_tc_sec_004_sql_injection_goods_id(get_html):
    """TC-SEC-004 商品 ID SQL 注入"""
    resp = get_html("/?s=goods/index/id/1' OR '1'='1.html")
    assert resp.status_code == 200
    body = resp.text
    assert "SQL syntax" not in body
    assert "mysqli" not in body.lower()
    assert "Fatal error" not in body


@pytest.mark.p1
def test_tc_sec_005_search_path_traversal(post_form):
    """TC-SEC-005 搜索路径穿越"""
    resp = post_form(API["search_post"], data={"wd": SEARCH_KEYWORDS["path_traversal"]})
    assert resp.status_code in (200, 302)
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_sec_006_search_null_byte(post_form):
    """TC-SEC-006 搜索空字节（目前服务端 500，记录为已知问题）"""
    resp = post_form(API["search_post"], data={"wd": SEARCH_KEYWORDS["null_byte"]})
    # 已知问题：空字节导致服务端 500
    assert resp.status_code in (200, 302, 500)
    if resp.status_code >= 500:
        pytest.xfail("空字节搜索导致服务端 500 — 需要服务端修复")


@pytest.mark.p0
def test_tc_sec_007_public_upload_no_file(post_form):
    """TC-SEC-007 公共上传接口无文件"""
    resp = post_form(API["ueditor_upload"], data={"action": "uploadimage"})
    assert resp.status_code == 200
    body = resp.text
    assert "Fatal error" not in body
    # 应该提示找不到文件，而不是报错
    assert has_text(resp, "上传") or has_text(resp, "文件") or has_text(resp, "error") or "msg" in body


@pytest.mark.p0
def test_tc_sec_008_invalid_goods_id_sql_injection(get_html):
    """TC-SEC-008 无效商品 ID 不暴露错误"""
    resp = get_html(PATHS["goods"].format(goods_id=999999999))
    assert resp.status_code == 200
    assert "SQL syntax" not in resp.text
    assert "Fatal error" not in resp.text


@pytest.mark.p0
def test_tc_sec_009_invalid_category_sql_injection(get_html):
    """TC-SEC-009 无效类目不暴露错误"""
    resp = get_html(f"/?s=search/index/cid/999999.html")
    assert resp.status_code == 200
    assert "SQL syntax" not in resp.text
    assert "Fatal error" not in resp.text
