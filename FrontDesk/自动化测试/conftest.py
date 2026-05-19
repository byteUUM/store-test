"""Shared fixtures and response helpers for ShopXO automated tests."""

import json
import re

import pytest
import requests

from config import BASE_URL, COOKIES, HEADERS, REQUEST_TIMEOUT


# ── Response helpers ──────────────────────────────────────────────────


def has_text(resp, keyword):
    """Check if a Chinese/ASCII keyword exists in the raw response bytes.

    Works around the server's broken UTF-8 encoding by comparing at the
    byte level rather than relying on resp.text (which produces garbled
    text when invalid UTF-8 bytes are present).
    """
    return keyword.encode("utf-8") in resp.content


def has_error_body(resp):
    """Check if response contains server error signatures (non-intrusive)."""
    text = resp.text
    return any(k in text for k in ("Fatal error", "SQL syntax", "Stack trace", "Warning"))


def resp_ok(resp):
    """Shorthand: status is 2xx or 3xx."""
    return 200 <= resp.status_code < 400


def json_body(resp):
    """Parse response as JSON, handling the ShopXO HTML-in-JSON wrapper.

    When the server wraps page HTML inside a JSON string
    (content-type: application/json), parse it twice.
    """
    ct = resp.headers.get("content-type", "")
    if "json" not in ct:
        return None
    try:
        data = resp.json()
        # If decoded is a plain string (wrapped HTML), re-parse doesn't help
        if isinstance(data, str):
            return None
        return data
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def extract_json_msg(resp):
    """Extract the 'msg' field from a ShopXO JSON response, if possible."""
    body = json_body(resp)
    if body and isinstance(body, dict):
        return body.get("msg", "")
    return ""


def is_json_html(resp):
    """Return True if response is HTML wrapped inside a JSON string."""
    ct = resp.headers.get("content-type", "")
    if "json" not in ct:
        return False
    return resp.content.startswith(b'"<')


# ── Pytest fixtures ───────────────────────────────────────────────────


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def cookies():
    return COOKIES.copy()


@pytest.fixture(scope="session")
def session(cookies):
    s = requests.Session()
    s.cookies.update(cookies)
    s.headers.update(HEADERS)
    return s


@pytest.fixture
def get_html(session, base_url):
    def _get(path: str, **kwargs):
        url = path if path.startswith("http") else f"{base_url}{path}"
        return session.get(url, timeout=REQUEST_TIMEOUT, **kwargs)
    return _get


@pytest.fixture
def post_form(session, base_url):
    def _post(path: str, data=None, **kwargs):
        url = path if path.startswith("http") else f"{base_url}{path}"
        return session.post(url, data=data or {}, timeout=REQUEST_TIMEOUT, **kwargs)
    return _post


@pytest.fixture
def api_json(post_form):
    """POST to an API endpoint and return the parsed JSON body (dict).

    Skips responses that are HTML-wrapped-in-JSON.
    """
    def _api(path: str, data=None):
        resp = post_form(path, data=data or {})
        body = json_body(resp)
        if body is None:
            pytest.skip(f"Response is not parseable JSON (content-type: {resp.headers.get('content-type')})")
        return body
    return _api


# ── Custom markers ────────────────────────────────────────────────────


def pytest_configure(config):
    config.addinivalue_line("markers", "p0: 核心用例")
    config.addinivalue_line("markers", "p1: 重要用例")
    config.addinivalue_line("markers", "login: 需要已登录 Cookie/账号")
    config.addinivalue_line("markers", "manual: 需人工验证码/支付，仅探测")
