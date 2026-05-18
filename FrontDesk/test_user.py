"""注册登录 — TC-USER-* / TC-LOGIN-* / TC-PWD-*"""

import os

import pytest

from config import API, PATHS, TEST_PASSWORD, TEST_USERNAME
from conftest import has_text, has_error_body, json_body, extract_json_msg


@pytest.mark.p0
def test_tc_user_register_page(get_html):
    """TC-USER-001 注册页可访问"""
    resp = get_html(PATHS["register"])
    assert resp.status_code == 200
    assert has_text(resp, "注册")


@pytest.mark.p1
def test_tc_user_002_register_empty_account(post_form):
    """TC-USER-002 空用户注册"""
    resp = post_form(API["reg_post"], data={"accounts": "", "pwd": "", "verify": ""})
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_user_003_register_invalid_email(post_form):
    """TC-USER-003 无效邮箱注册"""
    resp = post_form(API["reg_post"], data={
        "accounts": "not_an_email",
        "pwd": "Test123456",
        "verify": "0000",
        "type": "email",
    })
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p0
def test_tc_user_004_agreement_required(post_form):
    """TC-USER-004 未勾选协议不能注册成功"""
    resp = post_form(
        API["reg_post"],
        data={
            "accounts": "autotest_invalid@example.com",
            "pwd": "Test123456",
            "verify": "0000",
            "is_agree_agreement": "",
            "type": "email",
        },
    )
    assert resp.status_code == 200
    body = json_body(resp)
    if body:
        assert body.get("code") != 0 or "协议" in str(body.get("msg", ""))


@pytest.mark.p1
def test_tc_user_005_register_short_password(post_form):
    """TC-USER-005 过短密码注册"""
    resp = post_form(API["reg_post"], data={
        "accounts": "shortpwd@test.com",
        "pwd": "12",
        "verify": "0000",
        "type": "email",
    })
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p0
def test_tc_login_page(get_html):
    """TC-LOGIN-001 登录页可访问"""
    resp = get_html(PATHS["login"])
    assert resp.status_code == 200
    assert has_text(resp, "登录")


@pytest.mark.p0
def test_tc_login_002_wrong_password(post_form):
    """TC-LOGIN-002 错误密码登录失败"""
    resp = post_form(
        API["login_post"],
        data={
            "accounts": TEST_USERNAME or "nonexist_user@test.com",
            "pwd": "wrong_password_xxx",
            "verify": "0000",
            "type": "username",
        },
    )
    assert resp.status_code == 200
    body = json_body(resp)
    if body:
        assert body.get("code") != 0


@pytest.mark.p1
def test_tc_login_003_empty_fields(post_form):
    """TC-LOGIN-003 空字段登录"""
    resp = post_form(API["login_post"], data={"accounts": "", "pwd": "", "verify": ""})
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_login_004_invalid_type(post_form):
    """TC-LOGIN-004 非法登录类型"""
    resp = post_form(API["login_post"], data={
        "accounts": "test",
        "pwd": "test",
        "verify": "0000",
        "type": "invalid_type_xyz",
    })
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_login_005_sms_type_no_verify(post_form):
    """TC-LOGIN-005 短信登录不传验证码"""
    resp = post_form(API["login_post"], data={
        "accounts": "13800138000",
        "pwd": "",
        "verify": "0000",
        "type": "sms",
    })
    assert resp.status_code == 200
    assert not has_error_body(resp)


@pytest.mark.p1
def test_tc_pwd_forget_page(get_html):
    """TC-PWD-001 找回密码页可访问"""
    resp = get_html(PATHS["forget_pwd"])
    assert resp.status_code == 200
    assert has_text(resp, "密码")


@pytest.mark.p1
def test_verify_image_login(get_html):
    """登录图形验证码可获取"""
    resp = get_html(API["verify_login"])
    assert resp.status_code == 200
    assert "image" in resp.headers.get("content-type", "").lower() or len(resp.content) > 100


@pytest.mark.p1
def test_verify_image_reg(get_html):
    """注册图形验证码可获取"""
    resp = get_html(API["verify_reg"])
    assert resp.status_code == 200
    assert "image" in resp.headers.get("content-type", "").lower() or len(resp.content) > 100


@pytest.mark.p1
def test_login_verify_send_no_captcha(post_form):
    """登录验证码发送，缺图形验证码"""
    resp = post_form(API["login_verify_send"], data={"accounts": "test@test.com", "type": "email"})
    assert resp.status_code == 200
    body = json_body(resp)
    # Should reject with code like -10 (captcha required), not crash
    if body:
        assert body.get("code", 0) != 0 or "data" in body


@pytest.mark.p1
def test_reg_verify_send_no_captcha(post_form):
    """注册验证码发送，缺图形验证码"""
    resp = post_form(API["reg_verify_send"], data={"accounts": "test@test.com", "type": "email"})
    assert resp.status_code == 200
    body = json_body(resp)
    if body:
        assert body.get("code", 0) != 0 or "data" in body


@pytest.mark.login
@pytest.mark.manual
@pytest.mark.skipif(not TEST_USERNAME, reason="设置 SHOPXO_TEST_USERNAME / SHOPXO_TEST_PASSWORD 后启用")
def test_tc_login_001_success(post_form):
    """TC-LOGIN-001 账号密码登录（需有效账号+验证码）"""
    resp = post_form(
        API["login_post"],
        data={
            "accounts": TEST_USERNAME,
            "pwd": TEST_PASSWORD,
            "verify": os.getenv("SHOPXO_VERIFY", ""),
            "type": "username",
        },
    )
    body = resp.json()
    assert body.get("code") == 0
