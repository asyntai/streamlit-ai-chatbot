"""Runs chatbot() inside a real Streamlit script with AppTest."""
import os
import textwrap

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

import streamlit_ai_chatbot
from streamlit_ai_chatbot import _supports_page_scripts

PAGE_SCRIPTS = _supports_page_scripts(st)


def _app(body):
    return AppTest.from_string(textwrap.dedent(body), default_timeout=30)


def _html_bodies(at):
    """Bodies of st.html blocks in the rendered app."""
    bodies = []
    for node in at.get('html'):
        proto = getattr(node, 'proto', None)
        bodies.append(getattr(proto, 'body', '') if proto is not None else '')
    return bodies


def _iframes(at):
    return [n for n in at.get('iframe')]


def _widget_rendered(at):
    if PAGE_SCRIPTS:
        return any('asyntai_ab12cd34' in body for body in _html_bodies(at))
    return any('asyntai_ab12cd34' in (getattr(n.proto, 'srcdoc', '') or '') for n in _iframes(at))


def test_valid_id_renders_the_widget():
    at = _app("""
        from streamlit_ai_chatbot import chatbot
        import streamlit as st
        ok = chatbot("asyntai_ab12cd34")
        st.write("ok" if ok else "no")
    """).run()
    assert not at.exception
    assert at.markdown[0].value == 'ok'
    assert _widget_rendered(at)


def test_pasted_snippet_works():
    at = _app("""
        from streamlit_ai_chatbot import chatbot
        chatbot('<script src="x" data-asyntai-id="asyntai_ab12cd34"></script>')
    """).run()
    assert not at.exception
    assert _widget_rendered(at)


def test_bad_id_shows_nothing_and_returns_false():
    at = _app("""
        import warnings
        from streamlit_ai_chatbot import chatbot
        import streamlit as st
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            ok = chatbot("not-an-id")
        st.write(f"{ok}|{len(caught)}")
    """).run()
    assert not at.exception
    assert at.markdown[0].value == 'False|1'
    assert not _widget_rendered(at)
    assert not _html_bodies(at) and not _iframes(at)


def test_bad_script_url_returns_false():
    at = _app("""
        import warnings
        from streamlit_ai_chatbot import chatbot
        import streamlit as st
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            ok = chatbot("asyntai_ab12cd34", script_url="javascript:alert(1)")
        st.write(f"{ok}|{len(caught)}")
    """).run()
    assert at.markdown[0].value == 'False|1'
    assert not _widget_rendered(at)


def test_id_from_environment(monkeypatch):
    monkeypatch.setenv('ASYNTAI_WIDGET_ID', 'asyntai_ab12cd34')
    at = _app("""
        from streamlit_ai_chatbot import chatbot
        chatbot()
    """).run()
    assert not at.exception
    assert _widget_rendered(at)


def test_id_from_secrets(monkeypatch):
    monkeypatch.delenv('ASYNTAI_WIDGET_ID', raising=False)
    at = _app("""
        from streamlit_ai_chatbot import chatbot
        chatbot()
    """)
    at.secrets['ASYNTAI_WIDGET_ID'] = 'asyntai_ab12cd34'
    at.run()
    assert not at.exception
    assert _widget_rendered(at)


def test_no_id_anywhere_returns_false(monkeypatch):
    monkeypatch.delenv('ASYNTAI_WIDGET_ID', raising=False)
    at = _app("""
        import warnings
        from streamlit_ai_chatbot import chatbot
        import streamlit as st
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            st.write(str(chatbot()))
    """).run()
    assert at.markdown[0].value == 'False'


def test_rerun_keeps_working():
    at = _app("""
        from streamlit_ai_chatbot import chatbot
        import streamlit as st
        chatbot("asyntai_ab12cd34")
        st.button("again")
    """).run()
    at.button[0].click().run()
    assert not at.exception
    assert _widget_rendered(at)


def test_version_matches_pyproject():
    root = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(root, 'pyproject.toml'), encoding='utf-8') as fh:
        assert 'version = "%s"' % streamlit_ai_chatbot.__version__ in fh.read()
