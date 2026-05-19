"""文章与协议 — TC-ARTICLE-*"""

import pytest

from config import PATHS
from conftest import has_text, has_error_body


@pytest.mark.p1
def test_tc_article_002_user_agreement(get_html):
    """TC-ARTICLE-002 用户注册协议"""
    resp = get_html(PATHS["agreement_register"])
    assert resp.status_code == 200
    assert has_text(resp, "协议") or has_text(resp, "注册")


@pytest.mark.p1
def test_tc_article_003_privacy(get_html):
    """TC-ARTICLE-003 隐私协议"""
    resp = get_html(PATHS["agreement_privacy"])
    assert resp.status_code == 200
    assert has_text(resp, "隐私") or has_text(resp, "协议")


@pytest.mark.p1
def test_tc_article_004_invalid_article(get_html):
    """TC-ARTICLE-004 不存在文章"""
    resp = get_html(PATHS["article"].format(article_id=999999))
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_article_005_article_id_zero(get_html):
    """TC-ARTICLE-005 文章 ID = 0"""
    resp = get_html(PATHS["article"].format(article_id=0))
    assert resp.status_code == 200
    assert not has_error_body(resp)
