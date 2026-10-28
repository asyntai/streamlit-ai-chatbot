"""Add the Asyntai AI chat assistant to a Streamlit app.

    import streamlit as st
    from streamlit_ai_chatbot import chatbot

    chatbot("asyntai_ab12cd34")

The chat button then shows in the corner of every page of the app.
"""
import inspect
import os
import warnings

from ._snippet import html_block, iframe_document
from ._validate import DEFAULT_SCRIPT_URL, clean_script_url, clean_widget_id

__all__ = ['chatbot', 'DEFAULT_SCRIPT_URL']
__version__ = '1.0.0'

_ENV_NAME = 'ASYNTAI_WIDGET_ID'


def _id_from_settings():
    """The widget ID from Streamlit secrets or the environment, or ''."""
    try:
        import streamlit as st
        value = st.secrets.get(_ENV_NAME, '')
        if value:
            return str(value)
    except Exception:
        # No secrets file. That is normal, so we look at the environment.
        pass
    return os.environ.get(_ENV_NAME, '')


def _supports_page_scripts(st):
    """True when st.html can run JavaScript in the page itself."""
    html = getattr(st, 'html', None)
    if html is None:
        return False
    try:
        return 'unsafe_allow_javascript' in inspect.signature(html).parameters
    except (TypeError, ValueError):
        return False


def chatbot(widget_id=None, *, script_url=None):
    """Show the Asyntai chat button on the page.

    widget_id: the ID from the Install page of your Asyntai dashboard, for
        example "asyntai_ab12cd34". You can also paste the whole snippet.
        When you leave it out, the package reads ASYNTAI_WIDGET_ID from
        st.secrets or from the environment.
    script_url: optional; another https address for the widget script.

    Call it once near the top of the app. Calling it again on a rerun does
    no harm: the widget loads only once per browser tab.

    Returns True when the widget is on the page, False when the ID or the
    address is not valid.
    """
    import streamlit as st

    raw_id = widget_id if widget_id is not None else _id_from_settings()
    clean_id = clean_widget_id(raw_id)
    if not clean_id:
        warnings.warn(
            'streamlit-ai-chatbot: no valid widget ID. Copy it from the '
            'Install page of your Asyntai dashboard, for example '
            '"asyntai_ab12cd34".',
            stacklevel=2,
        )
        return False

    clean_url = clean_script_url(script_url)
    if not clean_url:
        warnings.warn(
            'streamlit-ai-chatbot: script_url must be an https address.',
            stacklevel=2,
        )
        return False

    if _supports_page_scripts(st):
        st.html(html_block(clean_id, clean_url), unsafe_allow_javascript=True)
    else:
        import streamlit.components.v1 as components
        components.html(iframe_document(clean_id, clean_url), height=0)
    return True
